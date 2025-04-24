# Copyright (C) 2020 SPAM Contributors
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This script manipulates different Phi fields:

Single Phi values:
  - spam-ereg
  - spam-reg
  - spam-mmr
  - spam-mmr-graphical

Gridded Phi values:
  - spam-pixelSearch
  - spam-pixelSearchPropagate
  - spam-ldic

Phis defined at labels centres:
  - spam-pixelSearch
  - spam-pixelSearchPropagate
  - spam-ddic


This script allows you to:
  - apply a registration (single Phi) to a series of points:
    - defined on a grid with NS
    - or as centres-of-mass of labelled images

  - apply an existing Phi-field to a new basis:
    - spam-ldic result onto grid with finer NS
    - spam-ldic onto centres-of-mass of labels
    - spam-ddic result onto grid

  - merge fields on different grids

  - subtract kinematics field on the same basis


Outputs are:
  - TSV files
  - (optional) VTK files for visualisation
  - (optional) TIF files in the case of gridded data
"""

import argparse
import os

import spam.deformation
import spam.DIC
import spam.helpers
import spam.label

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import multiprocessing  # noqa: E402

import numpy  # noqa: E402
import tifffile  # noqa: E402

try:
    multiprocessing.set_start_method("fork")
except RuntimeError:
    pass


numpy.seterr(all="ignore")

tol = 1e-6


def passPhiFieldParser(parser):
    parser.add_argument(
        "-F",
        "--apply-F",
        type=str,
        default="all",
        dest="APPLY_F",
        help='Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "all" is default',
    )

    parser.add_argument(
        "-pf",
        "-phiFile",
        dest="PHIFILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to TSV file containing initial Phi guess, can be single-point registration or multiple point correlation. Default = None",
    )

    help = [
        "Ratio of binning level between loaded Phi file and current calculation.",
        "If the input Phi file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2.",
        "Default = 1.",
    ]
    parser.add_argument("-pfb", "--phiFile-bin-ratio", type=float, default=1.0, dest="PHIFILE_BIN_RATIO", help="\n".join(help))

    parser.add_argument(
        "-np",
        "--number-of-processes",
        default=None,
        type=int,
        dest="PROCESSES",
        help="Number of parallel processes to use. Default = multiprocessing.cpu_count()",
    )

    # parser.add_argument('-pfd',
    # '--phiFile-direct',
    # action="store_true",
    # default=1,
    # dest='PHIFILE_DIRECT',
    # help="Trust the Phi file completely? This option ignores and overrides -pfni and requires same nodes in same positions. Default = False")

    parser.add_argument(
        "-lab1",
        "--labelledFile1",
        dest="LAB1",
        nargs="+",
        default=[],
        type=argparse.FileType("r"),
        help="Path to tiff file containing a labelled image 1 that defines zones to correlate. Disactivates -hws and -ns options",
    )

    # Default: node spacing equal in all three directions
    parser.add_argument(
        "-ns",
        "--node-spacing",
        nargs=1,
        type=int,
        default=None,
        dest="NS",
        help="Node spacing in pixels (assumed equal in all 3 directions -- see -ns3 for different setting). Default = 10px",
    )

    parser.add_argument(
        "-ns3",
        "--node-spacing-3",
        nargs=3,
        type=int,
        default=None,
        dest="NS",
        help="Node spacing in pixels (different in 3 directions). Default = 10, 10, 10px",
    )

    parser.add_argument(
        "-im1",
        "--image1",
        dest="im1",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tiff file containing refence image, just to know the image size for the node spacing",
    )

    parser.add_argument(
        "-im1shape",
        "--image1-shape",
        nargs=3,
        type=int,
        default=None,
        dest="im1shape",
        help="Size of im1 in pixels Z Y X",
    )

    parser.add_argument(
        "-regs",
        "--registrationSubtract",
        dest="REGISTRATION_SUBTRACT_FILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to registration TSV file to subtract from file passed with -pf. Default = None",
    )

    parser.add_argument(
        "-regsF",
        "--registrationSubtract-apply-F",
        type=str,
        default="rigid",
        dest="REGISTRATION_SUBTRACT_APPLY_F",
        help='Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "rigid" is default',
    )

    parser.add_argument(
        "-regsb",
        "--registrationSubtract-bin-ratio",
        type=int,
        default=1,
        dest="REGISTRATION_SUBTRACT_BIN_RATIO",
        help="Ratio of binning level between second loaded Phi file and this registration. Default = 1",
    )

    parser.add_argument(
        "-pf2",
        "--phiFile2",
        dest="PHIFILE2",
        nargs="+",
        default=[],
        type=argparse.FileType("r"),
        help="Path to second spam-ddic TSV file(s). Default = None",
    )

    help = [
        "Ratio of binning level between loaded Phi file and current calculation.",
        "If the input Phi file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2.",
        "Default = 1.",
    ]
    parser.add_argument(
        "-pf2b",
        "--phiFile2-bin-ratio",
        type=int,
        default=1,
        dest="PHIFILE2_BIN_RATIO",
        help="Ratio of binning level between second loaded Phi file and current calculation.\
              If the input Phi file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1",
    )

    parser.add_argument(
        "-mpl",
        "--merge-prefer-label",
        action="store_true",
        dest="MERGE_PREFER_LABEL",
        help="When merging grid and discrete correlation results, automatically prefer points inside labels? Default = False",
    )

    parser.add_argument(
        "-nr",
        "--neighbourhood-radius-px",
        type=float,
        default=None,
        dest="NEIGHBOUR_RADIUS",
        help="Radius (in pixels) inside which to select neighbours for field interpolation. Excludes -nn option",
    )

    parser.add_argument(
        "-nn",
        "--number-of-neighbours",
        type=int,
        default=None,
        dest="NUMBER_OF_NEIGHBOURS",
        help="Number of neighbours for field interpolation. Default = None (radius mode is default)",
    )

    parser.add_argument(
        "-cps",
        "--check-point-surrounded",
        action="store_true",
        dest="CHECK_POINT_SURROUNDED",
        help="When interpolating, insist that a point is surrounded by neighbours? Default = False",
    )

    parser.add_argument(
        "-rst",
        "--return-status-threshold",
        type=int,
        default=-4,
        dest="RETURN_STATUS_THRESHOLD",
        help="Lowest return status value to preserve in input PhiField. Default = -4",
    )

    parser.add_argument(
        "-od",
        "--out-dir",
        type=str,
        default=None,
        dest="OUT_DIR",
        help="Output directory, default is the dirname of im1 file",
    )

    parser.add_argument(
        "-pre",
        "--prefix",
        type=str,
        default=None,
        dest="PREFIX",
        help="Prefix for output files (without extension). Default is basename of im1 and im2 files",
    )

    parser.add_argument(
        "-vtk",
        "--VTKout",
        action="store_true",
        dest="VTK",
        help="Activate VTK output format. Default = False",
    )

    parser.add_argument(
        "-tif",
        "-tiff",
        "--TIFFout",
        "--TIFout",
        action="store_true",
        dest="TIFF",
        help="Activate TIFFoutput format. Default = False",
    )

    args = parser.parse_args()

    if args.PHIFILE is None:
        print("This function definitely needs a TSV Phi file input")
        exit()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.PHIFILE.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.PHIFILE.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.PHIFILE.name))[0] + "-passed"
    else:
        args.PREFIX += "-passed"

    if len(args.PHIFILE2) > 0:
        print("\n\nMerge mode")
        args.PREFIX += "-merged"
        print()

    else:
        if args.REGISTRATION_SUBTRACT_FILE is not None:
            print("\n\nRegistration subtract mode, disactivating ")

        elif len(args.LAB1) == 1:
            # We have a labelled image and so no nodeSpacing or halfWindowSize
            print("\n\nI have been passed a labelled image and so I am disactivating:")
            print("\t- node spacing")
            args.NS = None
            args.im1 = None
            args.im1shape = None
            # Output file name prefix
            args.PREFIX += "-labelled"
            print()

        else:
            print("\n\nNo labelled image so I'm in grid mode")
            # We are in grid, with a nodeSpacing and halfWindowSize
            # Catch interdependent node spacing and correlation window sizes
            if args.NS is None:
                print("...actually no node spacing either so, output basis not defined!")
                exit()
            else:
                # Catch 3D options
                if len(args.NS) == 1:
                    args.PREFIX += f"-ns{args.NS[0]}"
                    args.NS = [args.NS[0], args.NS[0], args.NS[0]]
                else:
                    # 3 NSs are passed
                    args.PREFIX += f"-ns{args.NS[0]}-{args.NS[1]}-{args.NS[2]}"

                if args.im1 is None and args.im1shape is None:
                    print("In grid mode, I need to know the image size, please pass either -im1 or -im1shape")
                    exit()
            # We need some way to define the image size for output
            if args.im1 is not None:
                print("Getting im1 dimensions by looking in the file (this ignores -im1shape)")
                tiff = tifffile.TiffFile(args.im1.name)
                args.im1shape = tiff.series[0].shape
            elif args.im1shape is not None:
                print("Trusting -im1shape dimensions as passed")
            else:
                print("You asked for a node spacing, but I don't know the size of the image you want me to define the grid on! Pass -im1 im.tif or -im1shape Z Y X")
                exit()

        if args.APPLY_F not in [
            "all",
            "rigid",
            "no",
        ]:
            print("-F should be 'all' 'rigid' or 'no'")
            exit()

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-passPhiField "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script facilitates the passing of Phi fields onto different bases:\n"
        + "  * discrete base defined by -lab1\n"
        + "  * grid base defined by -ns and -im1\n"
        + "The following operations are supported:\n"
        + "\treg OR grid OR discrete -> grid OR discrete\n"
        + "And also merging:\n"
        + "\tgrid AND discrete -> grid\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = passPhiFieldParser(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-passPhiField")

    ###############################################################
    # ### Step 1 (mandatory) read input Phi File
    ###############################################################
    PhiFromFile = spam.helpers.readCorrelationTSV(args.PHIFILE.name, fieldBinRatio=args.PHIFILE_BIN_RATIO)
    if PhiFromFile is None:
        print(f"\tFailed to read your TSV file passed with -pf {args.PHIFILE.name}")
        exit()

    # 2022-01-19 Finally implementing -regs, putting it on top
    if args.REGISTRATION_SUBTRACT_FILE is not None:
        print("Registation Subtract Mode")
        print(f"I am going to compute the **displacements** of the registration {args.REGISTRATION_SUBTRACT_FILE.name} Phi")
        print(f"applied to the points in {args.PHIFILE.name}, then subtract and return them")

        RegFromFile = spam.helpers.readCorrelationTSV(
            args.REGISTRATION_SUBTRACT_FILE.name,
            fieldBinRatio=args.REGISTRATION_SUBTRACT_BIN_RATIO,
        )
        assert RegFromFile["PhiField"].shape[0] == 1, "I need a TSV file with only one Phi in it (i.e., a registration)!"
        args.PREFIX += "-regs"

        PhiToSubtract = RegFromFile["PhiField"][0].copy()

        if args.REGISTRATION_SUBTRACT_APPLY_F == "no":
            print("\tI'm applying only the displacement in the registration")
            args.PREFIX += "-disp"
            PhiToSubtract[0:3, 0:3] = numpy.eye(3)

        elif args.REGISTRATION_SUBTRACT_APPLY_F == "rigid":
            print("\tI'm applying only the rigid part of the registration")
            args.PREFIX += "-rigid"
            PhiToSubtract = spam.deformation.computeRigidPhi(PhiToSubtract)

        elif args.REGISTRATION_SUBTRACT_APPLY_F == "all":
            print("\tI'm applying all the registration")
            args.PREFIX += "-all"
        else:
            print("Unknown -regsF mode, it must be 'all', 'rigid' or 'no'")
            exit()

        # Now apply PhiToSubtract to the nodes of the PhiField passed with -pf
        registrationPhiField = spam.DIC.applyRegistrationToPoints(
            PhiToSubtract,
            RegFromFile["fieldCoords"][0],
            PhiFromFile["fieldCoords"],
            applyF="no",  # This just avoids copying in Phi into the output registrationPhiField, not related to applying it.
            nProcesses=args.PROCESSES,
            verbose=True,
        )

        # Define variable for writing
        args.LAB1 = None
        outputNodesDim = PhiFromFile["fieldDims"]
        outputNumberOfNodes = PhiFromFile["fieldCoords"].shape[0]
        outputPhiField = PhiFromFile["PhiField"].copy()
        outputPhiField[:, 0:3, -1] -= registrationPhiField[:, 0:3, -1]
        outputNodePositions = PhiFromFile["fieldCoords"]
        args.NS = numpy.array(
            [
                numpy.unique(outputNodePositions[:, i])[1] - numpy.unique(outputNodePositions[:, i])[0]
                if len(numpy.unique(outputNodePositions[:, i])) > 1
                else numpy.unique(outputNodePositions[:, i])[0]
                for i in range(3)
            ]
        )

        if "pixelSearchCC" in PhiFromFile.keys():
            pixelSearchCC = PhiFromFile["pixelSearchCC"]
        else:
            pixelSearchCC = numpy.zeros(PhiFromFile["fieldCoords"].shape[0])

        if "returnStatus" in PhiFromFile.keys():
            returnStatus = PhiFromFile["returnStatus"]
        else:
            returnStatus = numpy.zeros(PhiFromFile["fieldCoords"].shape[0])

        if "error" in PhiFromFile.keys():
            error = PhiFromFile["error"]
        else:
            error = numpy.zeros(PhiFromFile["fieldCoords"].shape[0])

        if "deltaPhiNorm" in PhiFromFile.keys():
            deltaPhiNorm = PhiFromFile["deltaPhiNorm"]
        else:
            deltaPhiNorm = numpy.zeros(PhiFromFile["fieldCoords"].shape[0])

        if "iterations" in PhiFromFile.keys():
            iterations = PhiFromFile["iterations"]
        else:
            iterations = numpy.zeros(PhiFromFile["fieldCoords"].shape[0])

    elif len(args.PHIFILE2) > 0:
        print(f"\n\nspam-passPhiField: I see {len(args.PHIFILE2)} -pf2 file{'s' if len(args.PHIFILE2) > 1 else ''}, so will merge grid + discrete -> grid.")

        # check that -pf file is a grid
        assert PhiFromFile["numberOfLabels"] == 0, "in merge mode, -pf1 should be a grid file from spam-ldic or grid pixelSearch"

        assert len(args.LAB1) == len(args.PHIFILE2), f"in merge mode, the number of -pf2 files ({len(args.PHIFILE2)}) needs to be the same as -lab1 files ({len(args.LAB1)})"

        # If more than one DDIC, output lists, otherwise flat variables
        if len(args.PHIFILE2) > 1:
            discrete = []
            labelledImage = []
            for ddicFile in args.PHIFILE2:
                discrete.append(spam.helpers.readCorrelationTSV(ddicFile.name))
                # check that each -pf2 file is a ddic
                assert discrete[-1]["numberOfLabels"] > 0, f"in merge mode, all -pf2 files should be spam-ddic or discrete pixelSearch files, {ddicFile.name} is not."
            for lab1 in args.LAB1:
                labelledImage.append(tifffile.imread(lab1.name))
        else:
            discrete = spam.helpers.readCorrelationTSV(args.PHIFILE2[0].name)
            assert discrete["numberOfLabels"] > 0, f"in merge mode, all -pf2 files should be spam-ddic or discrete pixelSearch files, {args.PHIFILE2[0].name} is not."
            labelledImage = tifffile.imread(args.LAB1[0].name)

        print("\n\nspam-passPhiField: Starting merging...")
        merged = spam.DIC.mergeRegularGridAndDiscrete(
            regularGrid=PhiFromFile,
            discrete=discrete,
            labelledImage=labelledImage,
            binningLabelled=args.PHIFILE2_BIN_RATIO,
            alwaysLabel=args.MERGE_PREFER_LABEL,
        )
        # merge
        print("\n\ndone. Now saving (without 'mergeSource' field :( )...")

        outputNumberOfNodes = PhiFromFile["fieldCoords"].shape[0]
        outputNodePositions = PhiFromFile["fieldCoords"]
        outputNodesDim = PhiFromFile["fieldDims"]
        outputPhiField = merged["PhiField"]
        pixelSearchCC = merged["pixelSearchCC"]
        returnStatus = merged["returnStatus"]
        error = merged["error"]
        deltaPhiNorm = merged["deltaPhiNorm"]
        iterations = merged["iterations"]

        # Although we do have a lab1, or even more than one, the output is a grid, so override this work the writing part
        args.LAB1 = None

    else:
        ###############################################################
        # ### Not in merging mode!
        ###############################################################
        # ## Little reorganisation of lab1
        # we're not in merge mode, so args.LAB1 should either be a single file or None
        if len(args.LAB1) == 1:
            args.LAB1 = args.LAB1[0]
        elif len(args.LAB1) == 0:
            args.LAB1 = None
        else:
            print("spam-passPhiField: Passing mulitple -LAB1 is not supported outside merge mode, and you didn't pass any -pf2")

        ###############################################################
        # ### Step 0 define OUTPUT node positions -- either grid or labels:
        ###############################################################
        if args.LAB1 is not None:
            lab1 = tifffile.imread(args.LAB1.name).astype(spam.label.labelType)
            boundingBoxes = spam.label.boundingBoxes(lab1)
            outputNodePositions = spam.label.centresOfMass(lab1, boundingBoxes=boundingBoxes)
            outputNumberOfNodes = outputNodePositions.shape[0]

        # ## Otherwise we are in node spacing and half-window size mode
        else:
            outputNodePositions, outputNodesDim = spam.DIC.makeGrid(args.im1shape, args.NS)
            # start setting up
            outputNumberOfNodes = outputNodePositions.shape[0]

        # If the read Phi-file has only one line -- it's a single point registration!
        # We can either apply it to a grid or to labels
        if PhiFromFile["fieldCoords"].shape[0] == 1:
            PhiInit = PhiFromFile["PhiField"][0]
            print(f"\tI read a registration from a file in binning {args.PHIFILE_BIN_RATIO}")

            # In the special case of a registration, initialise output variables:
            pixelSearchCC = numpy.zeros((outputNumberOfNodes), dtype=float)
            error = numpy.zeros((outputNumberOfNodes), dtype=float)
            returnStatus = numpy.ones((outputNumberOfNodes), dtype=int)
            deltaPhiNorm = numpy.ones((outputNumberOfNodes), dtype=int)
            iterations = numpy.ones((outputNumberOfNodes), dtype=int)

            decomposedPhiInit = spam.deformation.decomposePhi(PhiInit)
            print("\tTranslations (px)")
            print("\t\t", decomposedPhiInit["t"])
            print("\tRotations (deg)")
            print("\t\t", decomposedPhiInit["r"])
            print("\tZoom")
            print("\t\t", decomposedPhiInit["z"])
            del decomposedPhiInit

            outputPhiField = spam.DIC.applyRegistrationToPoints(
                PhiInit,
                PhiFromFile["fieldCoords"][0],
                outputNodePositions,
                applyF=args.APPLY_F,
                nProcesses=args.PROCESSES,
                verbose=False,
            )

        ###############################################################
        # ### Input Phi file is a Phi FIELD
        ###############################################################
        else:
            outputPhiField = numpy.zeros((outputNumberOfNodes, 4, 4))

            # Interpolate these?
            pixelSearchCC = numpy.zeros((outputNumberOfNodes), dtype=float)
            error = numpy.zeros((outputNumberOfNodes), dtype=float)
            returnStatus = numpy.ones((outputNumberOfNodes), dtype=int)
            deltaPhiNorm = numpy.ones((outputNumberOfNodes), dtype=int)
            iterations = numpy.ones((outputNumberOfNodes), dtype=int)

            # We don't trust this completely, re-interpolate it onto the grid
            # Read the coordinates and values of the input F field
            inputNodePositions = PhiFromFile["fieldCoords"]
            inputPhiField = PhiFromFile["PhiField"]

            goodPointsMask = numpy.where(PhiFromFile["returnStatus"] >= args.RETURN_STATUS_THRESHOLD)[0]

            goodInputNodePositions = inputNodePositions[goodPointsMask]
            goodInputPhiField = inputPhiField[goodPointsMask]

            # Check neighbour inputs, either args.NEIGHBOUR_RADIUS or args.NUMBER_OF_NEIGHBOURS should be set.
            if args.NEIGHBOUR_RADIUS is not None and args.NUMBER_OF_NEIGHBOURS is not None:
                print("Both number of neighbours and neighbour radius are set, I'm taking the radius and ignoring the number of neighbours")
                args.NUMBER_OF_NEIGHBOURS = None
            # Neither are set... compute a reasonable default
            if args.NEIGHBOUR_RADIUS is None and args.NUMBER_OF_NEIGHBOURS is None:
                if args.LAB1 is None:
                    args.NEIGHBOUR_RADIUS = 2 * int(numpy.mean(args.NS) // 1)
                    print(f"Neither number of neighbours nor neighbour distance set, using default distance of 2*mean(NS) = {args.NEIGHBOUR_RADIUS}")
                else:
                    # Come up with a good default radius size
                    args.NEIGHBOUR_RADIUS = 5 * numpy.mean(spam.label.equivalentRadii(lab1, boundingBoxes=boundingBoxes)[1:])
                    print(f"Neither number of neighbours nor neighbour distance set, using default distance of 5*mean particle radius = {args.NEIGHBOUR_RADIUS}")
                # else:
                # TODO: Last case with DDIC in and DDIC out could be with NNEIGHBOURS

            outputPhiField = spam.DIC.interpolatePhiField(
                goodInputNodePositions,
                goodInputPhiField,
                outputNodePositions,
                nNeighbours=args.NUMBER_OF_NEIGHBOURS,
                neighbourRadius=args.NEIGHBOUR_RADIUS,
                interpolateF=args.APPLY_F,
                checkPointSurrounded=args.CHECK_POINT_SURROUNDED,
                nProcesses=args.PROCESSES,
                verbose=True,
            )

            # - apply a registration (single Phi) to a series of points:
            # - defined on a grid with NS
            # - or as centres-of-mass of labelled images

        # - apply an existing Phi-field to a new basis:
        # - spam-ldic result onto grid with finer NS
        # - spam-ldic onto centres-of-mass of labels
        # - spam-ddic result onto grid

        # - merge fields on different grids

        # - subtract kinematics field on the same basis

    # Outputs are:
    # - TSV files
    # - (optional) VTK files for visualisation
    # - (optional) TIF files in the case of gridded data
    if args.LAB1 is not None:
        TSVheader = "Label\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
    else:
        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
    outMatrix = numpy.array(
        [
            numpy.array(range(outputNumberOfNodes)),
            outputNodePositions[:, 0],
            outputNodePositions[:, 1],
            outputNodePositions[:, 2],
            outputPhiField[:, 0, 0],
            outputPhiField[:, 0, 1],
            outputPhiField[:, 0, 2],
            outputPhiField[:, 0, 3],
            outputPhiField[:, 1, 0],
            outputPhiField[:, 1, 1],
            outputPhiField[:, 1, 2],
            outputPhiField[:, 1, 3],
            outputPhiField[:, 2, 0],
            outputPhiField[:, 2, 1],
            outputPhiField[:, 2, 2],
            outputPhiField[:, 2, 3],
            pixelSearchCC,
            returnStatus,
            error,
            deltaPhiNorm,
            iterations,
        ]
    ).T

    numpy.savetxt(
        args.OUT_DIR + "/" + args.PREFIX + ".tsv",
        outMatrix,
        fmt="%.7f",
        delimiter="\t",
        newline="\n",
        comments="",
        header=TSVheader,
    )

    if args.TIFF:
        if args.LAB1 is None:
            if outputNodesDim[0] != 1:
                tifffile.imwrite(
                    args.OUT_DIR + "/" + args.PREFIX + "-Zdisp.tif",
                    outputPhiField[:, 0, -1].astype("<f4").reshape(outputNodesDim),
                )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-Ydisp.tif",
                outputPhiField[:, 1, -1].astype("<f4").reshape(outputNodesDim),
            )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-Xdisp.tif",
                outputPhiField[:, 2, -1].astype("<f4").reshape(outputNodesDim),
            )
            # tifffile.imwrite(args.OUT_DIR+"/"+args.PREFIX+"-CC.tif",                     pixelSearchCC.astype('<f4').reshape(nodesDim))
            # tifffile.imwrite(args.OUT_DIR+"/"+args.PREFIX+"-returnStatus.tif",           returnStatus.astype('<f4').reshape(nodesDim))
        else:
            # Think about relabelling grains here automatically?
            print("Not (yet) ready to save TIFFs in discrete output mode")

    # Collect data into VTK output
    if args.VTK and args.LAB1 is None:
        cellData = {}
        displacements = outputPhiField[:, 0:3, -1].reshape((outputNodesDim[0], outputNodesDim[1], outputNodesDim[2], 3))

        # Overwrite nans and infs with 0, rubbish I know
        displacements[numpy.logical_not(numpy.isfinite(displacements))] = 0
        cellData["displacements"] = displacements
        cellData["returnStatus"] = returnStatus.reshape((outputNodesDim[0], outputNodesDim[1], outputNodesDim[2]))

        # cellData['pixelSearchCC'] = pixelSearchCC.reshape(outputNodesDim)

        # This is perfect in the case where NS = 2xHWS, these cells will all be in the right place
        #   In the case of overlapping of under use of data, it should be approximately correct
        # If you insist on overlapping, then perhaps it's better to save each point as a cube glyph
        #   and actually *have* overlapping
        # HACK assume HWS is half node spacing
        args.HWS = numpy.array(args.NS) / 2
        spam.helpers.writeStructuredVTK(
            origin=outputNodePositions[0] - args.HWS,
            aspectRatio=args.NS,
            cellData=cellData,
            fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
        )

    elif args.VTK and args.LAB1 is not None:
        print("Labelled VTK output starting...", end="")
        # Redundant output for VTK visualisation
        magDisp = numpy.zeros(outputNumberOfNodes)
        for node in range(outputNumberOfNodes):
            magDisp[node] = numpy.linalg.norm(outputPhiField[node][0:3, -1])

        VTKglyphDict = {
            "displacements": outputPhiField[:, 0:3, -1],
            "mag(displacements)": magDisp,
            # 'pixelSearchCC': pixelSearchCC
        }

        spam.helpers.writeGlyphsVTK(
            outputNodePositions,
            VTKglyphDict,
            fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
        )
        print("done")
