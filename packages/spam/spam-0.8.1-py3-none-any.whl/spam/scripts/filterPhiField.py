# This python facilitates eye-alignment with a graphical QT interface
# for Discrete Digital Image Correlation using SPAM functions
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
This script manipulates a Phi field:

Gridded Phi values:
  - spam-pixelSearch
  - spam-pixelSearchPropagate
  - spam-ldic

Phis defined at labels centres:
  - spam-pixelSearch
  - spam-pixelSearchPropagate
  - spam-ddic


This script allows you to:
  - correct bad points inside a PhiField based on RS, or CC
  - correct incoherent points inside a PhiField based on LQC
  - apply a median filter to the PhiField

Outputs are:
  - TSV files
  - (optional) VTK files for visualisation
  - (optional) TIF files in the case of gridded data
"""

import argparse
import os

import scipy.ndimage
import scipy.spatial
import spam.deformation
import spam.DIC
import spam.helpers
import spam.label

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import multiprocessing  # noqa: E402

import numpy  # noqa: E402

try:
    multiprocessing.set_start_method("fork")
except RuntimeError:
    pass

import tifffile  # noqa: E402

numpy.seterr(all="ignore")

tol = 1e-6


def filterPhiField(parser):
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

    parser.add_argument(
        "-nomask",
        "--nomask",
        action="store_false",
        dest="MASK",
        help="Don't mask correlation points in background according to return status (i.e., include RS=-5 or less)",
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
        "-srs",
        "--select-return-status",
        action="store_true",
        dest="SRS",
        help="Select bad points for correction based on Return Status? This will use -srst as a threshold",
    )

    parser.add_argument(
        "-srst",
        "--select-return-status-threshold",
        type=int,
        default=1,
        dest="SRST",
        help="Return Status Threshold for selecting bad points. Default = 1 or less",
    )

    parser.add_argument(
        "-scc",
        "--select-cc",
        action="store_true",
        dest="SCC",
        help="Select bad points for correction based on Pixel Search CC? This will use -scct as a threshold",
    )

    parser.add_argument(
        "-scct",
        "--select-cc-threshold",
        type=float,
        default=0.99,
        dest="SCCT",
        help="Pixel Search CC for selecting bad points. Default = 0.99 or less",
    )

    parser.add_argument(
        "-slqc",
        "--select-local-quadratic-coherency",
        action="store_true",
        dest="SLQC",
        help="Select bad points for correction based on local quadratic coherency? Threshold = 0.1 or more",
    )

    parser.add_argument(
        "-cint",
        "--correct-by-interpolation",
        action="store_true",
        dest="CINT",
        help="Correct with a local interpolation with weights equal to the inverse of the distance? -mode applies",
    )

    parser.add_argument(
        "-F",
        "-filterF",
        type=str,
        default="all",
        dest="FILTER_F",
        help="What do you want to interpolate/filter? Options: 'all': the full Phi, 'rigid': Rigid body motion, 'no': Only displacements (faster). Default = 'all'.",
    )

    parser.add_argument(
        "-clqf",
        "--correct-by-local-quadratic-fit",
        action="store_true",
        dest="CLQF",
        help="Correct by a local quadratic fit? Only for displacements",
    )

    # parser.add_argument('-dpt',
    # '--delta-phi-norm-threshold',
    # type=float,
    # default=0.001,
    # dest='DELTA_PHI_NORM_THRESHOLD',
    # help="Delta Phi norm threshold BELOW which to consider the point good. Only for a point with return status = 1 . Default = 0.001")

    parser.add_argument(
        "-fm",
        "--filter-median",
        action="store_true",
        dest="FILTER_MEDIAN",
        help="Activates an overall median filter on the input Phi Field. -mode 'all' or 'disp' can be applied",
    )

    parser.add_argument(
        "-fmr",
        "--filter-median-radius",
        type=int,
        default=1,
        dest="FILTER_MEDIAN_RADIUS",
        help="Radius (in pixels) of median filter. Default = 1",
    )

    parser.add_argument(
        "-od",
        "--out-dir",
        type=str,
        default=None,
        dest="OUT_DIR",
        help="Output directory, default is the dirname of input file",
    )

    parser.add_argument(
        "-pre",
        "--prefix",
        type=str,
        default=None,
        dest="PREFIX",
        help="Prefix for output files (without extension). Default is basename of input file",
    )

    parser.add_argument(
        "-tif",
        "-tiff",
        action="store_true",
        dest="TIFF",
        help="Activate TIFF output format. Default = False",
    )

    parser.add_argument(
        "-notsv",
        "-noTSV",
        action="store_false",
        dest="TSV",
        help="Disactivate TSV output format?",
    )

    parser.add_argument(
        "-vtk",
        "--VTKout",
        action="store_true",
        dest="VTK",
        help="Activate VTK output format. Default = False",
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

    if (args.SRS + args.SCC + args.SLQC + args.CINT + args.CLQF) > 1 and args.FILTER_MEDIAN:
        print("WARNING: you can't ask for an overall median filter and a correction")
        exit()

    if args.FILTER_F not in ["all", "rigid", "no"]:
        print("-F option must be either 'all', 'rigid' or 'no'")
        exit()

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.PHIFILE.name))[0] + "-filtered"
    else:
        args.PREFIX += "-filtered"

    if args.CLQF:
        args.PREFIX += "-LQC"

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-filterPhiField " + spam.helpers.optionsParser.GLPv3descriptionHeader + "This script process Phi fields by\n" + "correcting bad or incoherent points or filtering",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = filterPhiField(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-filterPhiField")

    ###############################################################
    # ### Step 1 (mandatory) read input Phi File
    ###############################################################
    PhiFromFile = spam.helpers.readCorrelationTSV(args.PHIFILE.name, readConvergence=True, readPixelSearchCC=True, readError=True)
    if PhiFromFile is None:
        print(f"\tFailed to read your TSV file passed with -pf {args.PHIFILE.name}")
        exit()

    # If the read Phi-file has only one line -- it's a single point registration!
    # We can either apply it to a grid or to labels
    if PhiFromFile["fieldCoords"].shape[0] == 1:
        print(f"\tYour TSV passed with -pf {args.PHIFILE.name} is single line file (a registration). A field is required")
        exit()

    # Check if it is a discrete or gridded field
    grid = True
    discrete = False
    if PhiFromFile["numberOfLabels"] != 0:
        discrete = True
        grid = False

    ###############################################################
    # ### Input Phi file is a Phi FIELD
    ###############################################################
    inputNodesDim = PhiFromFile["fieldDims"]
    inputNodePositions = PhiFromFile["fieldCoords"]
    inputPhiField = PhiFromFile["PhiField"]
    inputDisplacements = PhiFromFile["PhiField"][:, 0:3, -1]
    inputReturnStatus = PhiFromFile["returnStatus"]
    inputPixelSearchCC = PhiFromFile["pixelSearchCC"]
    inputDeltaPhiNorm = PhiFromFile["deltaPhiNorm"]
    inputIterations = PhiFromFile["iterations"]
    inputError = PhiFromFile["error"]
    # ### Empty arrays for masking points
    inputGood = numpy.zeros(inputNodePositions.shape[0], dtype=bool)
    inputBad = numpy.zeros(inputNodePositions.shape[0], dtype=bool)
    inputIgnore = numpy.zeros(inputNodePositions.shape[0], dtype=bool)

    # output arrays
    outputPhiField = numpy.zeros((inputNodePositions.shape[0], 4, 4))
    outputReturnStatus = numpy.ones((inputNodePositions.shape[0]), dtype=float)
    outputDeltaPhiNorm = numpy.ones((inputNodePositions.shape[0]), dtype=float) * 100
    outputIterations = numpy.zeros((inputNodePositions.shape[0]), dtype=float)
    outputError = numpy.ones((inputNodePositions.shape[0]), dtype=float) * 100
    outputPixelSearchCC = numpy.zeros((inputNodePositions.shape[0]), dtype=float)
    # Check neighbour inputs, either args.NEIGHBOUR_RADIUS or args.NUMBER_OF_NEIGHBOURS should be set.
    if args.NEIGHBOUR_RADIUS is not None and args.NUMBER_OF_NEIGHBOURS is not None:
        print("Both number of neighbours and neighbour radius are set, I'm taking the radius and ignoring the number of neighbours")
        args.NUMBER_OF_NEIGHBOURS = None

    if args.NEIGHBOUR_RADIUS is None and args.NUMBER_OF_NEIGHBOURS is None:
        if grid:
            # Gridded input field
            nodeSpacing = numpy.array(
                [
                    numpy.unique(inputNodePositions[:, i])[1] - numpy.unique(inputNodePositions[:, i])[0]
                    if len(numpy.unique(inputNodePositions[:, i])) > 1
                    else numpy.unique(inputNodePositions[:, i])[0]
                    for i in range(3)
                ]
            )
            args.NEIGHBOUR_RADIUS = 4 * int(numpy.mean(nodeSpacing))
            print(f"Neither number of neighbours nor neighbour distance set, using default distance of 4*mean(nodeSpacing) = {args.NEIGHBOUR_RADIUS}")
        else:
            # Discrete input field
            args.NUMBER_OF_NEIGHBOURS = 27
            print("Neither number of neighbours nor neighbour distance set, using default 27 neighbours")

    ###############################################################
    # ### Define IGNORE points:
    ###############################################################
    if args.MASK:
        inputIgnore = inputReturnStatus < -4

    ###############################################################
    # ### Apply threshold to select good and bad points
    ###############################################################
    if args.SRS:
        print(f"\n\nSelecting bad points as Return Status <= {args.SRST}")
        inputGood = numpy.logical_and(inputReturnStatus > args.SRST, ~inputIgnore)
        inputBad = numpy.logical_and(inputReturnStatus <= args.SRST, ~inputIgnore)
        if args.SLQC:
            print("\tYou passed -slqc but you can only have one selection at a time")
        if args.SCC:
            print("\tYou passed -scc but you can only have one selection at a time")

    elif args.SCC:
        print(f"\n\nSelecting bad points with Pixel Search CC <= {args.SCCT}")
        inputGood = numpy.logical_and(inputPixelSearchCC > args.SCCT, ~inputIgnore)
        inputBad = numpy.logical_and(inputPixelSearchCC <= args.SCCT, ~inputIgnore)
        if args.SLQC:
            print("\tYou passed -slqc but you can only have one selection at a time")

    elif args.SLQC:
        print("\n\nCalculate coherency")
        LQC = spam.DIC.estimateLocalQuadraticCoherency(
            inputNodePositions[~inputIgnore],
            inputDisplacements[~inputIgnore],
            neighbourRadius=args.NEIGHBOUR_RADIUS,
            nNeighbours=args.NUMBER_OF_NEIGHBOURS,
            nProcesses=args.PROCESSES,
            verbose=True,
        )
        # print(LQC.shape)
        # print(inputGood[~inputIgnore].shape)
        inputGood[~inputIgnore] = LQC < 0.1
        inputBad[~inputIgnore] = LQC >= 0.1

    ###############################################################
    # ### Copy over the values for good AND ignore to output
    ###############################################################
    gandi = numpy.logical_or(inputGood, inputIgnore)

    outputPhiField[gandi] = inputPhiField[gandi]
    outputReturnStatus[gandi] = inputReturnStatus[gandi]
    outputDeltaPhiNorm[gandi] = inputDeltaPhiNorm[gandi]
    outputIterations[gandi] = inputIterations[gandi]
    outputError[gandi] = inputError[gandi]
    outputPixelSearchCC[gandi] = inputPixelSearchCC[gandi]

    if (args.CINT + args.CLQF) > 0 and numpy.sum(inputBad) == 0:
        print("No points to correct, exiting")
        exit()

    else:
        print(f"\n\nCorrecting {numpy.sum(inputBad)} points ({100*numpy.sum(inputBad)/numpy.sum(inputGood):03.1f}%)")

    ###############################################################
    # ### Correct those bad points
    ###############################################################
    if args.CINT:
        print(f"\n\nCorrection based on local interpolation (filterF = {args.FILTER_F})")
        PhiFieldCorrected = spam.DIC.interpolatePhiField(
            inputNodePositions[inputGood],
            inputPhiField[inputGood],
            inputNodePositions[inputBad],
            nNeighbours=args.NUMBER_OF_NEIGHBOURS,
            neighbourRadius=args.NEIGHBOUR_RADIUS,
            interpolateF=args.FILTER_F,
            nProcesses=args.PROCESSES,
            verbose=True,
        )
        outputPhiField[inputBad] = PhiFieldCorrected
        outputReturnStatus[inputBad] = 1
        if args.CLQF:
            print("\tYou asked to correct with local QC fitting with -clqf, but only one correction mode is supported")

    elif args.CLQF:
        if args.FILTER_F != "no":
            print("WARNING: non-displacement quadratic coherency correction not implemented, only doing displacements, and returning F=eye(3)\n")

        print("\n\nCorrection based on local quadratic coherency")
        dispLQC = spam.DIC.estimateDisplacementFromQuadraticFit(
            inputNodePositions[inputGood],
            inputDisplacements[inputGood],
            inputNodePositions[inputBad],
            neighbourRadius=args.NEIGHBOUR_RADIUS,
            nNeighbours=args.NUMBER_OF_NEIGHBOURS,
            nProcesses=args.PROCESSES,
            verbose=True,
        )
        # pass the displacements
        outputPhiField[inputBad, 0:3, 0:3] = numpy.eye(3)
        outputPhiField[inputBad, 0:3, -1] = dispLQC
        outputReturnStatus[inputBad] = 1

    if args.FILTER_MEDIAN:
        if discrete:
            print("Median filter for discrete mode not implemented... does it even make sense?")
        else:
            # Filter ALL POINTS
            # if asked, apply a median filter of a specific size in the Phi field
            print("\nApplying median filter...")
            filterPointsRadius = int(args.FILTER_MEDIAN_RADIUS)

            if args.MASK:
                inputPhiField[inputIgnore] = numpy.nan

            if args.FILTER_F == "rigid":
                print("Rigid mode not well defined for overall median filtering, exiting")
                exit()

            if args.FILTER_F == "all":
                # Filter F components
                print("Filtering F components...")
                print("\t1/9")
                outputPhiField[:, 0, 0] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 0, 0].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t2/9")
                outputPhiField[:, 1, 0] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 1, 0].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t3/9")
                outputPhiField[:, 2, 0] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 2, 0].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t4/9")
                outputPhiField[:, 0, 1] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 0, 1].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t5/9")
                outputPhiField[:, 1, 1] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 1, 1].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t6/9")
                outputPhiField[:, 2, 1] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 2, 1].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t7/9")
                outputPhiField[:, 0, 2] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 0, 2].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t8/9")
                outputPhiField[:, 1, 2] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 1, 2].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()
                print("\t9/9")
                outputPhiField[:, 2, 2] = scipy.ndimage.generic_filter(
                    inputPhiField[:, 2, 2].reshape(inputNodesDim),
                    numpy.nanmedian,
                    size=(2 * filterPointsRadius + 1),
                ).ravel()

            if args.FILTER_F == "no":
                for n in range(inputNodePositions.shape[0]):
                    outputPhiField[n] = numpy.eye(4)

            print("Filtering displacements...")
            print("\t1/3")
            outputPhiField[:, 0, -1] = scipy.ndimage.generic_filter(
                inputPhiField[:, 0, -1].reshape(inputNodesDim),
                numpy.nanmedian,
                size=(2 * filterPointsRadius + 1),
            ).ravel()
            print("\t2/3")
            outputPhiField[:, 1, -1] = scipy.ndimage.generic_filter(
                inputPhiField[:, 1, -1].reshape(inputNodesDim),
                numpy.nanmedian,
                size=(2 * filterPointsRadius + 1),
            ).ravel()
            print("\t3/3")
            outputPhiField[:, 2, -1] = scipy.ndimage.generic_filter(
                inputPhiField[:, 2, -1].reshape(inputNodesDim),
                numpy.nanmedian,
                size=(2 * filterPointsRadius + 1),
            ).ravel()

            if args.MASK:
                outputPhiField[inputIgnore] = numpy.nan

    # Outputs are:
    # - TSV files
    # - (optional) VTK files for visualisation
    # - (optional) TIF files in the case of gridded data
    if args.TSV:
        if discrete:
            TSVheader = "Label\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
        else:
            TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
        outMatrix = numpy.array(
            [
                numpy.arange(inputNodePositions.shape[0]),
                inputNodePositions[:, 0],
                inputNodePositions[:, 1],
                inputNodePositions[:, 2],
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
                outputPixelSearchCC,
                outputReturnStatus,
                outputError,
                outputDeltaPhiNorm,
                outputIterations,
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
        if grid:
            if inputNodesDim[0] != 1:
                tifffile.imwrite(
                    args.OUT_DIR + "/" + args.PREFIX + "-Zdisp.tif",
                    outputPhiField[:, 0, -1].astype("<f4").reshape(inputNodesDim),
                )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-Ydisp.tif",
                outputPhiField[:, 1, -1].astype("<f4").reshape(inputNodesDim),
            )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-Xdisp.tif",
                outputPhiField[:, 2, -1].astype("<f4").reshape(inputNodesDim),
            )
            # tifffile.imwrite(args.OUT_DIR+"/"+args.PREFIX+"-CC.tif",                     pixelSearchCC.astype('<f4').reshape(nodesDim))
            # tifffile.imwrite(args.OUT_DIR+"/"+args.PREFIX+"-returnStatus.tif",           returnStatus.astype('<f4').reshape(nodesDim))
        else:
            # Think about relabelling grains here automatically?
            pass

    # Collect data into VTK output
    if args.VTK:
        if grid:
            cellData = {}
            cellData["displacements"] = outputPhiField[:, :-1, 3].reshape((inputNodesDim[0], inputNodesDim[1], inputNodesDim[2], 3))

            # Overwrite nans and infs with 0, rubbish I know
            cellData["displacements"][numpy.logical_not(numpy.isfinite(cellData["displacements"]))] = 0

            # This is perfect in the case where NS = 2xHWS, these cells will all be in the right place
            #   In the case of overlapping of under use of data, it should be approximately correct
            # If you insist on overlapping, then perhaps it's better to save each point as a cube glyph
            #   and actually *have* overlapping
            # HACK assume HWS is half node spacing
            nodeSpacing = numpy.array(
                [
                    numpy.unique(inputNodePositions[:, i])[1] - numpy.unique(inputNodePositions[:, i])[0]
                    if len(numpy.unique(inputNodePositions[:, i])) > 1
                    else numpy.unique(inputNodePositions[:, i])[0]
                    for i in range(3)
                ]
            )
            HWS = nodeSpacing / 2
            spam.helpers.writeStructuredVTK(
                origin=inputNodePositions[0] - HWS,
                aspectRatio=nodeSpacing,
                cellData=cellData,
                fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
            )

        else:
            disp = outputPhiField[:, 0:3, -1]
            disp[numpy.logical_not(numpy.isfinite(disp))] = 0

            magDisp = numpy.linalg.norm(disp, axis=1)

            VTKglyphDict = {
                "displacements": outputPhiField[:, 0:3, -1],
                "mag(displacements)": magDisp,
            }

            spam.helpers.writeGlyphsVTK(
                inputNodePositions,
                VTKglyphDict,
                fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
            )
