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

import argparse
import os
import resource ##########

import spam.deformation
import spam.DIC
import spam.helpers

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import multiprocessing  # noqa: E402

import numpy  # noqa: E402
import tifffile  # noqa: E402

numpy.seterr(all="ignore")


def ldicParser(parser):
    parser.add_argument(
        "inFiles",
        nargs="+",
        type=argparse.FileType("r"),
        help="A space-separated list of two or more 3D greyscale tiff files to correlate, in order",
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
        "-mf1",
        "--maskFile1",
        dest="MASK1",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tiff file containing the mask of image 1 -- masks zones not to correlate, which should be == 0",
    )

    # parser.add_argument('-mf2',
    #                     '--maskFile2',
    #                     dest='MASK2',
    #                     default=None,
    #                     type=argparse.FileType('r'),
    #                     help="Path to tiff file containing the mask of image 2 -- masks correlation windows")

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
        "-F",
        "--apply-F",
        type=str,
        default="all",
        dest="APPLY_F",
        help='Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "all" is default',
    )

    parser.add_argument(
        "-rig",
        "--rigid",
        action="store_true",
        dest="RIGID",
        help="Only do a rigid correlation (i.e., displacements and rotations)?",
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
        "-m",
        "-mar",
        "-margin",
        nargs=1,
        type=int,
        default=[3],
        dest="MARGIN",
        help="Margin in pixels for the correlation of each local subvolume. Default = 3 px",
    )

    parser.add_argument(
        "-m3",
        "-mar3",
        "-margin3",
        nargs=3,
        type=int,
        default=None,
        dest="MARGIN",
        help="Margin in pixels for the correlation of each local subvolume. Default = 3 px",
    )

    parser.add_argument(
        "-it",
        "--max-iterations",
        type=int,
        default=50,
        dest="MAX_ITERATIONS",
        help="Maximum iterations for local correlation. Default = 50",
    )

    parser.add_argument(
        "-dp",
        "--min-delta-phi",
        type=float,
        default=0.001,
        dest="MIN_DELTA_PHI",
        help="Minimum change in Phi for local convergence. Default = 0.001",
    )

    parser.add_argument(
        "-o",
        "--interpolation-order",
        type=int,
        default=1,
        dest="INTERPOLATION_ORDER",
        help="Image interpolation order for local correlation. Default = 1, i.e., linear interpolation",
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
        "-ug",
        "--update-gradient",
        action="store_true",
        dest="UPDATE_GRADIENT",
        help="Update gradient in local correlation? More computation time but sometimes more robust and possibly fewer iterations.",
    )

    # parser.add_argument('-sef',
    # '--series-Ffile',
    # action="store_true",
    # dest='SERIES_PHIFILE',
    # help='During a total analysis, activate use of previous Ffield for next correlation')

    parser.add_argument(
        "-sei",
        "--series-incremental",
        action="store_true",
        dest="SERIES_INCREMENTAL",
        help="Perform incremental correlations between images",
    )

    parser.add_argument(
        "-skp",
        "--skip",
        action="store_true",
        default=False,
        dest="SKIP_NODES",
        help="Read the return status of the Phi file run ldic only for the non-converged nodes. Default = False",
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
        "-vtk",
        "--VTKout",
        action="store_true",
        dest="VTK",
        help="Activate VTK output format. Default = False",
    )

    parser.add_argument(
        "-notsv",
        "--noTSV",
        action="store_false",
        dest="TSV",
        help="Disactivate TSV output format. Default = True",
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

    # # 2018-03-24 check for 2D without loading images
    # # try:
    # # except BaseException:
    # #     print("DICregularGrid: Input TIFF files need to be writeable in order to guess their dimensionality")
    # #     exit()
    # # 2019-03-21 EA: better check for dimensions, doesn't depend on writability of files
    # tiff = tifffile.TiffFile(args.inFiles[0].name)
    # # imagejSingleSlice = True
    # # if tiff.imagej_metadata is not None:
    # #     if 'slices' in tiff.imagej_metadata:
    # #         if tiff.imagej_metadata['slices'] > 1:
    # #             imagejSingleSlice = False
    #
    # # 2019-04-05 EA: 2D image detection approved by Christophe Golke, update for shape 2019-08-29
    # if len(tiff.pages) == 1 and len(tiff.series[0].shape) == 2:
    #     twoD = True
    # else:
    #     twoD = False
    # tiff.close()
    twoD = spam.helpers.isTwoDtiff(args.inFiles[0].name)

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFiles[0].name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.inFiles[0].name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

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
        print("spam-ldic: HWS must be defined.")
        exit()

    # Catch 3D options
    if args.NS is not None:
        if len(args.NS) == 1:
            args.NS = [args.NS[0], args.NS[0], args.NS[0]]

    if len(args.HWS) == 1:
        args.HWS = [args.HWS[0], args.HWS[0], args.HWS[0]]

    if len(args.MARGIN) == 1:
        args.MARGIN = [args.MARGIN[0], args.MARGIN[0], args.MARGIN[0]]

    if type(args.MAX_ITERATIONS) == list:
        args.MAX_ITERATIONS = args.MAX_ITERATIONS[0]

    # Catch and overwrite 2D options
    if twoD:
        if args.NS is not None:
            args.NS[0] = 1
        args.HWS[0] = 0
        args.MARGIN[0] = 0

    # Behaviour undefined for series run and im1 mask since im1 will change, complain and continue
    if args.MASK1 is not None and args.SERIES_INCREMENTAL:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: You set an im1 mask and an incremental      ###")
        print("###  series correlation, meaning that im1 will change...  ###")
        print("#############################################################")
        print("#############################################################")

    # Make sure at least one output format has been asked for
    # if args.VTK + args.TSV + args.TIFF== 0:
    # print("#############################################################")
    # print("#############################################################")
    # print("###  WARNING: No output type of VTK, TSV and TIFFoptions  ###")
    # print("###  Are you sure this is right?!                         ###")
    # print("#############################################################")
    # print("#############################################################")

    # if args.SERIES_PHIFILE:
    # args.TSV = True

    # Nor prefix here because LDIC can still do an image series and needs to update the name
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
        description="spam-ldic "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script performs Local Digital Image Correlation script between a series of at least two 3D greyscale images"
        + "with independent measurement points spread on a regular grid (with -ns spacing in pixels between points). "
        + "Around each point a cubic subvolume of +-hws (Half-window size) is extracted and correlated"
        + "\nSee for more details: https://ttk.gricad-pages.univ-grenoble-alpes.fr/spam/tutorial-02b-DIC-practice.html",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = ldicParser(parser)

    if len(args.inFiles) < 2:
        print("\nldic: Did not receive enough input images... you need (at least) two to tango...")
        exit()

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-ldic")

    # Load reference image
    if args.LAZYLOAD:
        try:
            im1 = tifffile.memmap(args.inFiles[0].name)
        except:
            print("\nldic: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im1 = tifffile.imread(args.inFiles[0].name)

    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        im1 = im1[numpy.newaxis, ...]
    if im1.shape[0] == 1:
        twoD = True
    else:
        twoD = False

    if args.MASK1:
        print('We have a mask')
        if args.LAZYLOAD:
            try:
                im1mask = tifffile.memmap(args.MASK1.name) != 0
            except:
                print("\nldic: Problem with tifffile.memmap. Boolean arrays are not supported, try saving your mask in a 8-bit format. Exiting.")
                exit()
        else:
            im1mask = tifffile.imread(args.MASK1.name) != 0 # !=0 to be removed?

        if len(im1mask.shape) == 2:
            print('Problem with `len(im1mask.shape) == 2')
            im1mask = im1mask[numpy.newaxis, ...]
    else:
        im1mask = None

    # ### Interpolation settings
    if args.INTERPOLATION_ORDER == 1:
        pass
    else:
        pass
    # Override interpolator for python in 2D
    if twoD:
        pass

    margin = [-args.MARGIN[0], args.MARGIN[0], -args.MARGIN[1], args.MARGIN[1], -args.MARGIN[2], args.MARGIN[2]]

    # Loop over input images
    for im2number in range(1, len(args.inFiles)):
        # Variables to track last correlation in order to ask MPI workers to hang up
        if im2number == len(args.inFiles) - 1:
            pass
        else:
            pass

        # decide on number, in input files list, of the reference image
        if args.SERIES_INCREMENTAL:
            im1number = im2number - 1
        else:
            im1number = 0

        # Output file name prefix
        if args.PREFIX is None or len(args.inFiles) > 2:
            args.PREFIX = os.path.splitext(os.path.basename(args.inFiles[im1number].name))[0] + "-" + os.path.splitext(os.path.basename(args.inFiles[im2number].name))[0]

        # ## If not first correlation and we're interested in loading previous Ffile:
        # if not firstCorrelation and args.SERIES_PHIFILE:
        # args.PHIFILE = previousPhiFile

        print("\nCorrelating:", args.PREFIX)

        # Load deformed image
        if args.LAZYLOAD:
            try:
                im2 = tifffile.memmap(args.inFiles[im2number].name)
            except:
                print("\nldic: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
                exit()
        else:
            im2 = tifffile.imread(args.inFiles[im2number].name)

        if len(im2.shape) == 2:
            im2 = im2[numpy.newaxis, ...]

        assert im1.shape == im2.shape, "\nim1 and im2 must have the same size! Exiting."
        if args.MASK1:
            assert im1.shape == im1mask.shape, "\nim1 and im1mask must have the same size! Exiting."

        # Three cases to handle:
        #   1. phi file is reg   -> define nodes and apply reg
        #   2. phi file is field -> take everything and check NS if passed
        #   3. no phi file       -> define nodes
        if args.PHIFILE is not None:
            PhiFromFile = spam.helpers.readCorrelationTSV(args.PHIFILE.name, fieldBinRatio=args.PHIFILE_BIN_RATIO, readError=True)
            if PhiFromFile is None:
                print(f"\tFailed to read your TSV file passed with -pf {args.PHIFILE.name}")
                exit()

            # If the read Phi-file has only one line -- it's a single point registration!
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

                # Create nodes
                if args.NS is None:
                    print(f"spam-ldic: You passed a registration file {args.PHIFILE.name}, I need -ns to be defined")
                    exit()
                nodePositions, nodesDim = spam.DIC.makeGrid(im1.shape, args.NS)
                numberOfNodes = nodePositions.shape[0]

                PhiField = spam.DIC.applyRegistrationToPoints(PhiInit.copy(), PhiFromFile["fieldCoords"][0], nodePositions, applyF=args.APPLY_F, nProcesses=args.PROCESSES, verbose=False)

                error = numpy.zeros(numberOfNodes)
                iterations = numpy.zeros(numberOfNodes)
                returnStatus = numpy.zeros(numberOfNodes)
                deltaPhiNorm = numpy.zeros(numberOfNodes)

            else:  # we have a Phi field and not a registration
                nodePositions = PhiFromFile["fieldCoords"]
                numberOfNodes = nodePositions.shape[0]
                nodesDim = PhiFromFile["fieldDims"]
                nodeSpacingFile = numpy.array(
                    [
                        numpy.unique(nodePositions[:, i])[1] - numpy.unique(nodePositions[:, i])[0] if len(numpy.unique(nodePositions[:, i])) > 1 else numpy.unique(nodePositions[:, i])[0]
                        for i in range(3)
                    ]
                )
                PhiField = PhiFromFile["PhiField"]

                # GP: Adding skip nodes option, so we can run ldic only on the diverged nodes
                if args.SKIP_NODES:
                    error = PhiFromFile["error"]
                    iterations = PhiFromFile["iterations"]
                    returnStatus = PhiFromFile["returnStatus"]
                    deltaPhiNorm = PhiFromFile["deltaPhiNorm"]
                else:
                    error = numpy.zeros(numberOfNodes)
                    iterations = numpy.zeros(numberOfNodes)
                    returnStatus = numpy.zeros(numberOfNodes)
                    deltaPhiNorm = numpy.zeros(numberOfNodes)

                # In case NS is also defined, complain, but if it's the same as the loaded data, continue
                if args.NS is not None:
                    # compare them
                    if not numpy.allclose(numpy.array(args.NS), nodeSpacingFile, atol=0.0):
                        print(f"spam-ldic: you passed a -ns={args.NS} which contradicts the node spacing in your Phi Field TSV of {nodeSpacingFile}")
                        print("\thint 1: if you pass a Phi Field TSV you don't need to also define the node spacing")
                        print(f"\thint 2: if you want to use your Phi Field TSV {args.PHIFILE.name} on a finer node spacing, pass it with spam-passPhiField")
                        exit()
                    else:
                        print("spam-ldic: passing -ns with a Phi Field TSV is not needed")

                # If it's compatible, update args.NS
                args.NS = nodeSpacingFile

        else:  # No Phi file at all
            if args.NS is None:
                print("spam-ldic: I don't have a phi file or -ns defined, so don't know how to define grid...")
                exit()
            nodePositions, nodesDim = spam.DIC.makeGrid(im1.shape, args.NS)
            numberOfNodes = nodePositions.shape[0]

            PhiField = numpy.zeros((numberOfNodes, 4, 4))
            for node in range(numberOfNodes):
                PhiField[node] = numpy.eye(4)

            error = numpy.zeros(numberOfNodes)
            iterations = numpy.zeros(numberOfNodes)
            returnStatus = numpy.zeros(numberOfNodes)
            deltaPhiNorm = numpy.zeros(numberOfNodes)

        # GP: Adding the skip function
        if args.SKIP_NODES:
            nodesToCorrelate = (returnStatus == -3) | (returnStatus == -2) | (returnStatus == -1) | (returnStatus == 1)
            nodesToSkip = numpy.logical_not(nodesToCorrelate)
        else:
            nodesToCorrelate = None
            nodesToSkip = None

        # print(PhiField)
        PhiFieldOut, returnStatusOut, errorOut, iterationsOut, deltaPhiNormOut = spam.DIC.ldic(
            im1,
            im2,
            nodePositions,
            args.HWS,
            im1mask=im1mask,
            PhiField=PhiField.copy(),
            margin=margin,
            skipNodesMask=nodesToSkip,
            maskCoverage=args.MASK_COVERAGE,
            greyThreshold=[args.GREY_LOW_THRESH, args.GREY_HIGH_THRESH],
            applyF=args.APPLY_F,
            maxIterations=args.MAX_ITERATIONS,
            deltaPhiMin=args.MIN_DELTA_PHI,
            PhiRigid=args.RIGID,
            updateGradient=args.UPDATE_GRADIENT,
            interpolationOrder=args.INTERPOLATION_ORDER,
            processes=args.PROCESSES,
        )

        # Merge in skipped results
        if args.SKIP_NODES:
            PhiFieldOut[nodesToSkip] = PhiField[nodesToSkip]
            returnStatusOut[nodesToSkip] = returnStatus[nodesToSkip]
            errorOut[nodesToSkip] = error[nodesToSkip]
            iterationsOut[nodesToSkip] = iterations[nodesToSkip]
            deltaPhiNormOut[nodesToSkip] = deltaPhiNorm[nodesToSkip]

        # print(PhiFieldOut[returnStatus==2])
        # print(numpy.unique(returnStatus, return_counts=1))

        print("\n")

        # # Finished! Get ready for output.

        if args.TSV:
            # Make one big array for writing:
            #   First the node number,
            #   3 node positions,
            #   F[0:3,0:2]
            #   Pixel-search CC
            #   SubPixError, SubPixIterations, SubPixelReturnStatus
            TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\terror\titerations\treturnStatus\tdeltaPhiNorm"
            outMatrix = numpy.array(
                [
                    numpy.array(range(nodePositions.shape[0])),
                    nodePositions[:, 0],
                    nodePositions[:, 1],
                    nodePositions[:, 2],
                    PhiFieldOut[:, 0, 0],
                    PhiFieldOut[:, 0, 1],
                    PhiFieldOut[:, 0, 2],
                    PhiFieldOut[:, 0, 3],
                    PhiFieldOut[:, 1, 0],
                    PhiFieldOut[:, 1, 1],
                    PhiFieldOut[:, 1, 2],
                    PhiFieldOut[:, 1, 3],
                    PhiFieldOut[:, 2, 0],
                    PhiFieldOut[:, 2, 1],
                    PhiFieldOut[:, 2, 2],
                    PhiFieldOut[:, 2, 3],
                    errorOut,
                    iterationsOut,
                    returnStatusOut,
                    deltaPhiNormOut,
                ]
            ).T

            numpy.savetxt(args.OUT_DIR + "/" + args.PREFIX + "-ldic.tsv", outMatrix, fmt="%.7f", delimiter="\t", newline="\n", comments="", header=TSVheader)
            # # Hold onto that name if we need to reload
            # if args.SERIES_PHIFILE: previousPhiFile = args.OUT_DIR+"/"+args.PREFIX+".tsv"

        if args.TIFF:
            if nodesDim[0] != 1:
                tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-Zdisp.tif", PhiFieldOut[:, 0, -1].astype("<f4").reshape(nodesDim))
            tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-Ydisp.tif", PhiFieldOut[:, 1, -1].astype("<f4").reshape(nodesDim))
            tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-Xdisp.tif", PhiFieldOut[:, 2, -1].astype("<f4").reshape(nodesDim))
            tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-error.tif", errorOut.astype("<f4").reshape(nodesDim))
            tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-iterations.tif", iterationsOut.astype("<f4").reshape(nodesDim))
            tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-returnStatus.tif", returnStatusOut.astype("<f4").reshape(nodesDim))
            tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-ldic-deltaPhiNorm.tif", deltaPhiNormOut.astype("<f4").reshape(nodesDim))

        # Collect data into VTK output
        if args.VTK:
            cellData = {}
            cellData["displacements"] = PhiFieldOut[:, :-1, 3].reshape((nodesDim[0], nodesDim[1], nodesDim[2], 3))
            cellData["error"] = errorOut.reshape(nodesDim)
            cellData["iterations"] = iterationsOut.reshape(nodesDim)
            cellData["returnStatus"] = returnStatusOut.reshape(nodesDim)
            cellData["deltaPhiNorm"] = deltaPhiNormOut.reshape(nodesDim)

            cellData["error"][numpy.logical_not(numpy.isfinite(cellData["error"]))] = 0
            cellData["iterations"][numpy.logical_not(numpy.isfinite(cellData["iterations"]))] = 0
            cellData["returnStatus"][numpy.logical_not(numpy.isfinite(cellData["returnStatus"]))] = 0
            cellData["deltaPhiNorm"][numpy.logical_not(numpy.isfinite(cellData["deltaPhiNorm"]))] = 0

            # Overwrite nans and infs with 0, rubbish I know
            cellData["displacements"][numpy.logical_not(numpy.isfinite(cellData["displacements"]))] = 0

            # This is perfect in the case where NS = 2xHWS, these cells will all be in the right place
            #   In the case of overlapping of under use of data, it should be approximately correct
            # If you insist on overlapping, then perhaps it's better to save each point as a cube glyph
            #   and actually *have* overlapping
            spam.helpers.writeStructuredVTK(origin=nodePositions[0] - args.HWS, aspectRatio=args.NS, cellData=cellData, fileName=args.OUT_DIR + "/" + args.PREFIX + "-ldic.vtk")

        if args.SERIES_INCREMENTAL:
            # If in incremental mode, current deformed image is next reference image
            im1 = im2.copy()

    # usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # print(f"Memory usage at the end of the script: {usage / 1024} MB")
    if args.LAZYLOAD:
        if args.MASK1:
            del(im1mask) 
        del(im1, im2)
