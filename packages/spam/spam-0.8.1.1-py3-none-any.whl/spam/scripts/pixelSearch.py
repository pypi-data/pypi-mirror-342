"""
Library of SPAM image correlation functions.
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import multiprocessing
import os

import numpy
import spam.DIC
import spam.helpers
import tifffile


def pixelSearchParser(parser):
    parser.add_argument(
        "im1",
        metavar="im1",
        type=argparse.FileType("r"),
        help="Greyscale image of reference state for correlation",
    )

    parser.add_argument(
        "im2",
        metavar="im2",
        type=argparse.FileType("r"),
        help="Greyscale image of deformed state for correlation",
    )

    parser.add_argument(
        "-lab1",
        "--labelledFile1",
        dest="LAB1",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tiff file containing a labelled image 1 that defines zones to correlate. Disactivates -hws and -ns options",
    )

    parser.add_argument(
        "-np",
        "--number-of-processes",
        default=None,
        type=int,
        dest="PROCESSES",
        help="Number of parallel processes to use. Default = multiprocessing.cpu_count()",
    )

    parser.add_argument(
        "-ld",
        "--label-dilate",
        type=int,
        default=1,
        dest="LABEL_DILATE",
        help="Only if -lab1 is defined: Number of times to dilate labels. Default = 1",
    )

    parser.add_argument(
        "-lvt",
        "--label-volume-threshold",
        type=numpy.uint,
        default=100,
        dest="LABEL_VOLUME_THRESHOLD",
        help="Volume threshold below which labels are ignored. Default = 100",
    )

    parser.add_argument(
        "-mf1",
        "--maskFile1",
        dest="MASK1",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tiff file containing the mask of image 1 -- masks zones not to correlate, which should be == 0",
    )

    parser.add_argument(
        "-mf2",
        "--maskFile2",
        dest="MASK2",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tiff file containing the mask of image 2 -- masks zones not to correlate, which should be == 0",
    )

    parser.add_argument(
        "-mc",
        "--mask-coverage",
        type=float,
        default=0.5,
        dest="MASK_COVERAGE",
        help="In case a mask is defined, tolerance for a subvolume's pixels to be masked before it is skipped with RS=-5. Default = 0.5",
    )

    parser.add_argument(
        "-pf",
        "-phiFile",
        dest="PHIFILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to TSV file containing the deformation function field (required)",
    )

    help = [
        "Ratio of binning level between loaded Phi file and current calculation.",
        "If the input Phi file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2.",
        "Default = 1.",
    ]
    parser.add_argument("-pfb", "--phiFile-bin-ratio", type=float, default=1.0, dest="PHIFILE_BIN_RATIO", help="\n".join(help))

    parser.add_argument(
        "-F",
        "--apply-F",
        type=str,
        default="all",
        dest="APPLY_F",
        help='Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "all" is default',
    )

    # parser.add_argument('-regs',
    # '--subtract-registration',
    # action="store_true",
    # dest='REGSUB',
    # help='Subtract rigid part of input registration from output displacements? Only works if you load a registration TSV. Default = False')

    parser.add_argument(
        "-sr",
        "--search-range",
        nargs=6,
        type=int,
        default=[-3, 3, -3, 3, -3, 3],
        dest="SEARCH_RANGE",
        help="Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px",
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

    # Possible: node spacing different in all three directions
    parser.add_argument(
        "-ns3",
        "--node-spacing-3",
        nargs=3,
        type=int,
        default=None,
        dest="NS",
        help="Node spacing in pixels (different in 3 directions). Default = 10, 10, 10px",
    )

    # Default: window size equal in all three directions
    parser.add_argument(
        "-hws",
        "--half-window-size",
        nargs=1,
        type=int,
        default=None,
        dest="HWS",
        help="Half correlation window size, measured each side of the node pixel (assumed equal in all 3 directions -- see -hws3 for different setting). Default = 10 px",
    )

    # Possible: node spacing different in all three directions
    parser.add_argument(
        "-hws3",
        "--half-window-size-3",
        nargs=3,
        type=int,
        default=None,
        dest="HWS",
        help="Half correlation window size, measured each side of the node pixel (different in 3 directions). Default = 10, 10, 10px",
    )

    parser.add_argument(
        "-glt",
        "--grey-low-threshold",
        type=float,
        default=-numpy.inf,
        dest="GREY_LOW_THRESH",
        help="Grey threshold on mean of reference imagette BELOW which the correlation is not performed. Default = -infinity",
    )

    parser.add_argument(
        "-ght",
        "--grey-high-threshold",
        type=float,
        default=numpy.inf,
        dest="GREY_HIGH_THRESH",
        help="Grey threshold on mean of reference imagette ABOVE which the correlation is not performed. Default = infinity",
    )

    parser.add_argument(
        "-od",
        "--out-dir",
        type=str,
        default=None,
        dest="OUT_DIR",
        help="Output directory, default is the dirname of gmsh file",
    )

    parser.add_argument(
        "-pre",
        "--prefix",
        type=str,
        default=None,
        dest="PREFIX",
        help="Prefix for output files (without extension). Default is basename of mesh file",
    )

    # parser.add_argument('-def',
    # '--save-deformed-image1',
    # action="store_true",
    # default=False,
    # dest='DEF',
    # help="Activate the saving of a deformed image 1 (as <im1>-reg-def.tif)")

    parser.add_argument(
        "-vtk",
        "--VTKout",
        action="store_true",
        dest="VTK",
        help="Activate VTK output format. Default = False",
    )

    parser.add_argument(
        "-notsv",
        "--noTSVout",
        action="store_false",
        dest="TSV",
        help="Disactivate TSV output format. Default = False",
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
    
    parser.add_argument(
        "-lazy",
        "--lazy-load",
        action="store_true",
        dest="LAZYLOAD",
        help="Load your images using tifffile.memmap for lazy loading. Default = False",
    )

    args = parser.parse_args()

    # # 2019-04-05 EA: 2D image detection approved by Christophe Golke, update for shape 2019-08-29
    # tiff = tifffile.TiffFile(args.im1.name)
    # if len(tiff.pages) == 1 and len(tiff.series[0].shape) == 2:
    #     twoD = True
    # else:
    #     twoD = False
    # tiff.close()
    twoD = spam.helpers.isTwoDtiff(args.im1.name)

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.im1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.im1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    if args.LAB1 is not None:
        # We have a labelled image and so no nodeSpacing or halfWindowSize
        print("I have been passed a labelled image and so I am disactivating node spacing and half-window size and mask and setting mask coverage to 0")
        args.HWS = None
        args.NS = None
        args.MASK1 = None
        args.MASK_COVERAGE = 0
        # Catch and overwrite 2D options
        if twoD:
            args.SEARCH_RANGE[0] = 0
            args.SEARCH_RANGE[1] = 0
    else:
        # We are in grid, with a nodeSpacing and halfWindowSize
        # Catch interdependent node spacing and correlation window sizes
        # if args.NS is None:
        # print("\nUsing default node spacing: "),
        # if args.HWS is None:
        # print("2x default half window size"),
        # args.HWS = [10]
        # print("({}) which is".format(args.HWS[0])),
        # args.NS = [args.HWS[0] * 2]
        # else:
        # print("2x user-set half window size"),
        # if len(args.HWS) == 1:
        # print("({}) which is".format(args.HWS[0])),
        # args.NS = [int(args.HWS[0] * 2)]
        # elif len(args.HWS) == 3:
        # print("({} -- selecting smallest) which is".format(args.HWS)),
        # args.NS = [int(min(args.HWS) * 2)]
        # print(args.NS)

        if args.HWS is None:
            print("spam-pixelSearch: in grid mode (without -lab1) HWS must be defined.")
            exit()

        # Catch 3D options
        if args.NS is not None:
            if len(args.NS) == 1:
                args.NS = [args.NS[0], args.NS[0], args.NS[0]]

        if len(args.HWS) == 1:
            args.HWS = [args.HWS[0], args.HWS[0], args.HWS[0]]

        # Catch and overwrite 2D options
        if twoD:
            if args.NS is not None:
                args.NS[0] = 1
            args.HWS[0] = 0
            args.SEARCH_RANGE[0] = 0
            args.SEARCH_RANGE[1] = 0

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0] + "-pixelSearch"
    else:
        args.PREFIX += "-pixelSearch"

    if args.APPLY_F not in [
        "all",
        "rigid",
        "no",
    ]:
        print("-F should be 'all' 'rigid' or 'no'")
        exit()

    if (args.SEARCH_RANGE[0] > args.SEARCH_RANGE[1]) or (args.SEARCH_RANGE[2] > args.SEARCH_RANGE[3]) or (args.SEARCH_RANGE[4] > args.SEARCH_RANGE[5]):
        print("spam-pixelSearch: One of the search range lower limits is higher than the upper limit!")
        print(f"\tz: low: {args.SEARCH_RANGE[0]} high: {args.SEARCH_RANGE[1]}")
        print(f"\ty: low: {args.SEARCH_RANGE[2]} high: {args.SEARCH_RANGE[3]}")
        print(f"\tx: low: {args.SEARCH_RANGE[4]} high: {args.SEARCH_RANGE[5]}")
        exit()

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-pixelSearch " + spam.helpers.optionsParser.GLPv3descriptionHeader + "This script performs a pixel search from im1 to im2\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = pixelSearchParser(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-pixelSearch")

    # Fill in search range
    searchRange = numpy.array(
        [
            args.SEARCH_RANGE[0],
            args.SEARCH_RANGE[1],
            args.SEARCH_RANGE[2],
            args.SEARCH_RANGE[3],
            args.SEARCH_RANGE[4],
            args.SEARCH_RANGE[5],
        ]
    )

    # Load reference image
    if args.LAZYLOAD:
        try:
            im1 = tifffile.memmap(args.im1.name)
        except:
            print("\npixelSearch: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im1 = tifffile.imread(args.im1.name)

    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        im1 = im1[numpy.newaxis, ...]
    if im1.shape[0] == 1:
        twoD = True
    else:
        twoD = False

    # Load deformed image
    if args.LAZYLOAD:
        try:
            im2 = tifffile.memmap(args.im2.name)
        except:
            print("\npixelSearch: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im2 = tifffile.imread(args.im2.name)

    if len(im2.shape) == 2:
        im2 = im2[numpy.newaxis, ...]

    # First switch between Lab and Grid pixelSearch

    if args.LAB1 is not None:
        # Load deformed image
        if args.LAZYLOAD:
            try:
                lab1 = tifffile.memmap(args.LAB1.name).astype(spam.label.labelType)
            except:
                print("\npixelSearch: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
                exit()
        else:
            lab1 = tifffile.imread(args.LAB1.name).astype(spam.label.labelType)
        
        boundingBoxes = spam.label.boundingBoxes(lab1)
        nodePositions = spam.label.centresOfMass(lab1, boundingBoxes=boundingBoxes)
        numberOfNodes = nodePositions.shape[0]
        im1mask = None
        im2mask = None
        if twoD:
            lab1 = lab1[numpy.newaxis, ...]

    # Otherwise we are in node spacing and half-window size mode
    else:

        if args.MASK1 is not None:
            if args.LAZYLOAD:
                try:
                    im1mask = tifffile.memmap(args.MASK1.name) != 0
                except:
                    print("\npixelSearch: Problem with tifffile.memmap. Boolean arrays are not supported, try saving your mask1 in a 8-bit format. Exiting.")
                    exit()
            else:
                im1mask = tifffile.imread(args.MASK1.name) != 0 # !=0 to be removed?

            if len(im1mask.shape) == 2:
                im1mask = im1mask[numpy.newaxis, ...]
        else:
            im1mask = None

        if args.MASK2 is not None:
            if args.LAZYLOAD:
                try:
                    im2mask = tifffile.memmap(args.MASK2.name) != 0
                except:
                    print("\npixelSearch: Problem with tifffile.memmap. Boolean arrays are not supported, try saving your mask2 in a 8-bit format. Exiting.")
                    exit()
            else:
                im2mask = tifffile.imread(args.MASK2.name) != 0 # !=0 to be removed?

            if len(im2mask.shape) == 2:
                im2mask = im2mask[numpy.newaxis, ...]
        else:
            im2mask = None

    # Three cases to handle:
    #   1. phi file is reg   -> define nodes and apply reg
    #   2. phi file is field -> take everything and check NS if passed
    #   3. no phi file       -> define nodes
    if args.PHIFILE is not None:
        PhiFromFile = spam.helpers.readCorrelationTSV(args.PHIFILE.name, fieldBinRatio=args.PHIFILE_BIN_RATIO)
        if PhiFromFile is None:
            print(f"\tFailed to read your TSV file passed with -pf {args.PHIFILE.name}")
            exit()

        # Case #1: If the read Phi-file has only one line -- it's a single point registration!
        if PhiFromFile["fieldCoords"].shape[0] == 1:
            PhiInit = PhiFromFile["PhiField"][0]
            print(f"\tI read a registration from a file in binning {args.PHIFILE_BIN_RATIO}")

            decomposedPhiInit = spam.deformation.decomposePhi(PhiInit)
            print("\tTranslations (px)")
            print("\t\t", decomposedPhiInit["t"])
            print("\tRotations (deg)")
            print("\t\t", decomposedPhiInit["r"])
            print("\tZoom")
            print("\t\t", decomposedPhiInit["z"])
            del decomposedPhiInit

            if args.LAB1 is None:
                # Create nodes if in regular mode, in label mode these are already defined
                if args.NS is None:
                    print(f"spam-pixelSearch: You passed a registration file {args.PHIFILE.name}, I need -ns to be defined")
                    exit()
                nodePositions, nodesDim = spam.DIC.makeGrid(im1.shape, args.NS)
                numberOfNodes = nodePositions.shape[0]

            PhiField = spam.DIC.applyRegistrationToPoints(
                PhiInit,
                PhiFromFile["fieldCoords"][0],
                nodePositions,
                applyF=args.APPLY_F,
                nProcesses=args.PROCESSES,
                verbose=False,
            )

        else:
            # Case #2: The read Phi-file contains multiple lines it's an F field!
            nodePositionsFile = PhiFromFile["fieldCoords"]
            numberOfNodes = nodePositionsFile.shape[0]
            nodeSpacingFile = numpy.array(
                [
                    numpy.unique(nodePositionsFile[:, i])[1] - numpy.unique(nodePositionsFile[:, i])[0] if len(numpy.unique(nodePositionsFile[:, i])) > 1 else numpy.unique(nodePositionsFile[:, i])[0]
                    for i in range(3)
                ]
            )
            PhiField = PhiFromFile["PhiField"]
            nodesDim = PhiFromFile["fieldDims"]

            # different checks to be done for lab and grid:
            if args.LAB1 is None:
                # In case NS is also defined, complain, but if it's the same as the loaded data, continue
                if args.NS is not None:
                    # compare them
                    if not numpy.allclose(numpy.array(args.NS), nodeSpacingFile, atol=0.0):
                        print(f"spam-pixelSearch: you passed a -ns={args.NS} which contradicts the node spacing in your Phi Field TSV of {nodeSpacingFile}")
                        print("\thint 1: if you pass a Phi Field TSV you don't need to also define the node spacing")
                        print(f"\thint 2: if you want to use your Phi Field TSV {args.PHIFILE.name} on a finer node spacing, pass it with spam-passPhiField")
                        exit()
                    else:
                        print("spam-pixelSearch: passing -ns with a Phi Field TSV is not needed")
                else:
                    # args.NS is None
                    args.NS = nodeSpacingFile
                nodePositions = nodePositionsFile
            else:
                # Lab phi-field consistency check
                if not numpy.allclose(nodePositionsFile, nodePositions, atol=1.0):
                    print(f"spam-pixelSearch: Input PhiField positions from {args.PHIFILE.name} are not within 1px of the centre of mass of the labels from {args.LAB1}, this seems dangerous.")
                    print("\tplease consider using spam-passPhiField to apply your PhiField to a new labelled image")
                    exit()
    else:  # Case #3: No Phi file
        if args.LAB1 is None:
            if args.NS is None:
                print("spam-pixelSearch: You're in regular grid mode, but no -ns is set and no Phi Field TSV has been passed, exiting.")
                exit()
            nodePositions, nodesDim = spam.DIC.makeGrid(im1.shape, args.NS)
            numberOfNodes = nodePositions.shape[0]

        PhiField = numpy.zeros((numberOfNodes, 4, 4))
        for node in range(numberOfNodes):
            PhiField[node] = numpy.eye(4)

    # Call the respective function
    if args.LAB1 is not None:
        # Discrete version of PS
        dictOut = spam.DIC.pixelSearchDiscrete(
            lab1,
            im1,
            im2,
            searchRange,
            PhiField=PhiField,
            boundingBoxes=boundingBoxes,
            centresOfMass=nodePositions,
            applyF=args.APPLY_F,
            labelDilate=args.LABEL_DILATE,
            volThreshold=args.LABEL_VOLUME_THRESHOLD,
            numProc=args.PROCESSES,
        )
        PhiField = dictOut["PhiField"]
        pixelSearchCC = dictOut["pixelSearchCC"]
        error = dictOut["error"]
        returnStatus = dictOut["returnStatus"]
        # deltaPhiNorm -- do we need this?
        iterations = dictOut["iterations"]
        deltaPhiNorm = numpy.ones(numberOfNodes)
    else:
        # Local version of PS
        PhiField, pixelSearchCC, error, returnStatus, deltaPhiNorm, iterations = spam.DIC.pixelSearchLocal(
            im1,
            im2,
            args.HWS,
            searchRange,
            nodePositions,
            PhiField,
            # numberOfNodes,
            # twoD,
            im1mask,
            im2mask,
            args.APPLY_F,
            args.MASK_COVERAGE,
            args.GREY_LOW_THRESH,
            args.GREY_HIGH_THRESH,
            args.PROCESSES,
        )

    print("\n")

    if args.TSV:
        # Make one big array for writing:
        #   First the node number,
        #   3 node positions,
        #   F[0:3,0:2]
        #   Pixel-search CC
        if args.LAB1 is not None:
            TSVheader = "Label\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
        else:
            TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
        outMatrix = numpy.array(
            [
                numpy.array(range(nodePositions.shape[0])),
                nodePositions[:, 0],
                nodePositions[:, 1],
                nodePositions[:, 2],
                PhiField[:, 0, 0],
                PhiField[:, 0, 1],
                PhiField[:, 0, 2],
                PhiField[:, 0, 3],
                PhiField[:, 1, 0],
                PhiField[:, 1, 1],
                PhiField[:, 1, 2],
                PhiField[:, 1, 3],
                PhiField[:, 2, 0],
                PhiField[:, 2, 1],
                PhiField[:, 2, 2],
                PhiField[:, 2, 3],
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
            if nodesDim[0] != 1:
                tifffile.imwrite(
                    args.OUT_DIR + "/" + args.PREFIX + "-Zdisp.tif",
                    PhiField[:, 0, -1].astype("<f4").reshape(nodesDim),
                )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-Ydisp.tif",
                PhiField[:, 1, -1].astype("<f4").reshape(nodesDim),
            )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-Xdisp.tif",
                PhiField[:, 2, -1].astype("<f4").reshape(nodesDim),
            )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-CC.tif",
                pixelSearchCC.astype("<f4").reshape(nodesDim),
            )
            tifffile.imwrite(
                args.OUT_DIR + "/" + args.PREFIX + "-returnStatus.tif",
                returnStatus.astype("<f4").reshape(nodesDim),
            )
        else:
            # Think about relabelling grains here automatically?
            pass

    # Collect data into VTK output
    if args.VTK and args.LAB1 is None:
        cellData = {}
        cellData["displacements"] = PhiField[:, :-1, 3].reshape((nodesDim[0], nodesDim[1], nodesDim[2], 3))
        cellData["pixelSearchCC"] = pixelSearchCC.reshape(nodesDim)

        # Overwrite nans and infs with 0, rubbish I know
        cellData["displacements"][numpy.logical_not(numpy.isfinite(cellData["displacements"]))] = 0
        # if args.REGSUB:
        # cellData['displacements-regsub'][numpy.logical_not(numpy.isfinite(cellData['displacements-regsub']))] = 0

        # This is perfect in the case where NS = 2xHWS, these cells will all be in the right place
        #   In the case of overlapping of under use of data, it should be approximately correct
        # If you insist on overlapping, then perhaps it's better to save each point as a cube glyph
        #   and actually *have* overlapping
        spam.helpers.writeStructuredVTK(
            origin=nodePositions[0] - args.HWS,
            aspectRatio=args.NS,
            cellData=cellData,
            fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
        )

    elif args.VTK and args.LAB1 is not None:
        # Redundant output for VTK visualisation
        magDisp = numpy.zeros(numberOfNodes)
        for node in range(numberOfNodes):
            magDisp[node] = numpy.linalg.norm(PhiField[node][0:3, -1])

        VTKglyphDict = {
            "displacements": PhiField[:, 0:3, -1],
            "mag(displacements)": magDisp,
            "pixelSearchCC": pixelSearchCC,
        }

        spam.helpers.writeGlyphsVTK(nodePositions, VTKglyphDict, fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk")
