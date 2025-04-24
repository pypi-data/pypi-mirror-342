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
This script performs a point-by-point "pixel search" which computes a correlation coefficient
of an imagette extracted in im1 to a brute-force search in a given search range in z, y, x in image 2.

Imagettes in im1 can either be defined with a nodeSpacing and a halfWindowSize or a labelled image.
"""


import argparse
import os

import numpy
import progressbar
import spam.DIC
import spam.helpers
import spam.mesh
import tifffile
from scipy.spatial import KDTree

os.environ["OPENBLAS_NUM_THREADS"] = "1"
numpy.seterr(all="ignore")


def pixelSearchPropagateParser(parser):
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
        "-sp",
        "--starting-point-and-displacement",
        nargs=6,
        type=int,
        default=[-1, -1, -1, 0, 0, 0],
        dest="START_POINT_DISP",
        help="Z Y X of first point for the propagation, Z Y X displacement of that point, required",
    )

    parser.add_argument(
        "-gp",
        "--guiding-points-file",
        dest="GUIDING_POINTS_FILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to file containing the guiding points",
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
        "-ld",
        "--label-dilate",
        type=int,
        default=1,
        dest="LABEL_DILATE",
        help="Only if -lab1 is defined: Number of times to dilate labels. Default = 1",
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
        "-sr",
        "--search-range",
        nargs=6,
        type=int,
        default=[-3, 3, -3, 3, -3, 3],
        dest="SEARCH_RANGE",
        help="Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pixel search. Default = +-3px",
    )

    # Default: window size equal in all three directions
    parser.add_argument(
        "-hws",
        "--half-window-size",
        nargs=1,
        type=int,
        default=[5],
        dest="HWS",
        help="Half correlation window size (in pixels), measured each side of the node pixel (assumed equal in all 3 directions -- see -hws3 for different setting).\
              Default = 5 px",
    )

    # Possible: window size different in all three directions
    parser.add_argument(
        "-hws3",
        "--half-window-size-3",
        nargs=3,
        type=int,
        default=None,
        dest="HWS",
        help="Half correlation window size (in pixels), measured each side of the node pixel (different in 3 directions). Default = 10, 10, 10px",
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
        "-nr",
        "--neighbourhood-radius",
        type=float,
        default=None,
        dest="RADIUS",
        help="Radius (in pixels) inside which to select neighbours. Default = mean(hws)+mean(sr)",
    )

    parser.add_argument(
        "-gwd",
        "--gaussian-weighting-distance",
        type=float,
        default=None,
        dest="DIST",
        help="Distance (in pixels) over which the neighbour's distance is weighted. Default = sum(hws)+sum(sr)",
    )

    parser.add_argument(
        "-cct",
        "--CC-threshold",
        type=float,
        default=0.9,
        dest="CC_MIN",
        help="Pixel search correlation coefficient threshold BELOW which the point is considered badly correlated. Default = 0.9",
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

    # 2019-04-05 EA: 2D image detection approved by Christophe Golke, update for shape 2019-08-29
    # tiff = tifffile.TiffFile(args.im1.name)
    # if len(tiff.pages) == 1 and len(tiff.series[0].shape) == 2:
    #    twoD = True
    # else:
    #    twoD = False
    # tiff.close()

    if args.GUIDING_POINTS_FILE is None:
        # You really need a start point...
        if args.START_POINT_DISP[0:3] == [-1, -1, -1]:
            print("You need to input a starting point from which to propagate!\n(even if displacement is zero)")
            exit()

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

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0] + "-pixelSearchPropagate"
    else:
        args.PREFIX += "-pixelSearchPropagate"

    # Fill radius and dist if not given
    if args.RADIUS is None:
        args.RADIUS = numpy.mean(args.HWS) + (args.SEARCH_RANGE[1] + args.SEARCH_RANGE[3] + args.SEARCH_RANGE[5]) / 3.0

    if args.DIST is None:
        args.DIST = numpy.sum(args.HWS) + numpy.sum(args.SEARCH_RANGE[1] + args.SEARCH_RANGE[3] + args.SEARCH_RANGE[5])

    # There are 3 modes:
    # - points-to-correlate defined by input "guiding points", which should be points with good texture
    # - points-to-correlate defined by labelled image
    # - points-to-correlate defined by regular grid
    if args.GUIDING_POINTS_FILE is not None:
        print("I have been passed a guiding points file, so I am disactivating:")
        print("\t- node spacing")
        print("\t- label file")
        args.NS = None
        args.LAB1 = None
        # Catch 3D options
        if len(args.HWS) == 1:
            args.HWS = [args.HWS[0]] * 3

    elif args.LAB1 is not None:
        # We have a labelled image and so no nodeSpacing or halfWindowSize
        print("I have been passed a labelled image and so I am disactivating:")
        print("\t- node spacing")
        print("\t- half-window size")
        args.HWS = None
        args.NS = None
        args.MASK1 = None
        args.MASK_COVERAGE = 0

    else:
        print("Regular grid mode")
        # We are in grid, with a nodeSpacing and halfWindowSize
        # Catch interdependent node spacing and correlation window sizes
        if args.NS is None:
            print("\nUsing default node spacing: "),
            if args.HWS is None:
                print("2x default half window size"),
                args.HWS = [10]
                print("({}) which is".format(args.HWS[0])),
                args.NS = [args.HWS[0] * 2]
            else:
                print("2x user-set half window size"),
                if len(args.HWS) == 1:
                    print("({}) which is".format(args.HWS[0])),
                    args.NS = [int(args.HWS[0] * 2)]
                elif len(args.HWS) == 3:
                    print("({} -- selecting smallest) which is".format(args.HWS)),
                    args.NS = [int(min(args.HWS) * 2)]
            print(args.NS)

        # Catch 3D options
        if len(args.NS) == 1:
            args.NS = [args.NS[0], args.NS[0], args.NS[0]]

        if len(args.HWS) == 1:
            args.HWS = [args.HWS[0], args.HWS[0], args.HWS[0]]

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-pixelSearchPropagate "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script performs a pixel search from im1 to im2 propagating the motion from the top guiding point\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = pixelSearchPropagateParser(parser)

    spam.helpers.displaySettings(args, "spam-pixelSearchPropagate")
    
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
    pixelSearchCCmin = args.CC_MIN
    weightingDistance = args.DIST

    startPoint = numpy.array(args.START_POINT_DISP[0:3])
    startPointDisplacement = numpy.array(args.START_POINT_DISP[3:6])

    # Load reference image
    if args.LAZYLOAD:
        try:
            im1 = tifffile.memmap(args.im1.name)
        except:
            print("\pixelSeachPropagate: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im1 = tifffile.imread(args.im1.name)

    # Detect unpadded 2D image first:
    # if len(im1.shape) == 2: im1 = im1[numpy.newaxis, ...]
    # if im1.shape[0] == 1:   twoD = True
    # else:                   twoD = False

    # Load deformed image
    if args.LAZYLOAD:
        try:
            im2 = tifffile.memmap(args.im2.name)
        except:
            print("\pixelSeachPropagate: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im2 = tifffile.imread(args.im2.name)
    # if len(im2.shape) == 2: im2 = im2[numpy.newaxis, ...]

    if args.MASK1:
        if args.LAZYLOAD:
            try:
                im1mask = tifffile.memmap(args.MASK1.name)!= 0
            except:
                print("\pixelSeachPropagate: Problem with tifffile.memmap. Most probably your mask1 is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
                exit()
        else:
            im1mask = tifffile.imread(args.MASK1.name)!= 0
        # if len(im1mask.shape) == 2:
        #    im1mask = im1mask[numpy.newaxis, ...]
    else:
        im1mask = None

    if args.MASK2:
        if args.LAZYLOAD:
            try:
                im2mask = tifffile.memmap(args.MASK2.name)!= 0
            except:
                print("\pixelSeachPropagate: Problem with tifffile.memmap. Most probably your mask2 is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
                exit()
        else:
            im2mask = tifffile.imread(args.MASK2.name)!= 0
        # if len(im2mask.shape) == 2:
        #    im2mask = im2mask[numpy.newaxis, ...]
    else:
        im2mask = None

    # There are 3 modes:
    # - points-to-correlate defined by input "guiding points", which should be points with good texture
    # - points-to-correlate defined by labelled image
    # - points-to-correlate defined by regular grid

    # Detect guiding points mode
    if args.GUIDING_POINTS_FILE is not None:
        gp = numpy.genfromtxt(args.gp.name)

    # ...or label mode
    elif args.LAB1 is not None:
        if args.LAZYLOAD:
            try:
                lab1 = tifffile.memmap(args.LAB1.name).astype(spam.label.labelType)
            except:
                print("\pixelSeachPropagate: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
                exit()
        else:
            lab1 = tifffile.imread(args.LAB1.name).astype(spam.label.labelType)
        boundingBoxes = spam.label.boundingBoxes(lab1)
        centresOfMass = spam.label.centresOfMass(lab1, boundingBoxes=boundingBoxes)
        im1mask = None
        im2mask = None
        gp = centresOfMass.copy()
        gp[0] = startPoint

    else:
        gp, nodesDim = spam.DIC.makeGrid(im1.shape, args.NS)
        gp = numpy.vstack([startPoint, gp])

    print("\n\tRanking points")
    guidingPoints, rowNumbers = spam.mesh.rankPoints(gp, neighbourRadius=args.RADIUS)
    numberOfPoints = guidingPoints.shape[0]

    # Initialise arrays
    PhiField = numpy.zeros((numberOfPoints, 4, 4))
    for point in range(numberOfPoints):
        PhiField[point] = numpy.eye(4)

    PhiField[0, 0:3, -1] += startPointDisplacement

    pixelSearchCC = numpy.zeros((numberOfPoints), dtype=float)
    # Returns compatible with register()
    error = numpy.zeros((numberOfPoints), dtype=float)
    returnStatus = numpy.zeros((numberOfPoints), dtype=int)
    deltaPhiNorm = numpy.ones((numberOfPoints), dtype=int)
    iterations = numpy.zeros((numberOfPoints), dtype=int)

    print("\n\tStarting sequential Pixel Search")
    widgets = [
        progressbar.FormatLabel(""),
        " ",
        progressbar.Bar(),
        " ",
        progressbar.AdaptiveETA(),
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfPoints)
    pbar.start()

    # Step 1: simple PS for first point
    if args.LAB1 is not None:
        imagetteReturnsTop = spam.label.getImagettesLabelled(
            lab1,
            lab1[startPoint[0], startPoint[1], startPoint[2]],
            PhiField[0].copy(),
            im1,
            im2,
            searchRange.copy(),
            boundingBoxes,
            centresOfMass,
            margin=args.LABEL_DILATE,
            labelDilate=args.LABEL_DILATE,
            applyF="no",
            volumeThreshold=3**3,
        )
        imagetteReturnsTop["imagette2mask"] = None
    else:
        imagetteReturnsTop = spam.DIC.getImagettes(
            im1,
            guidingPoints[0],
            args.HWS,
            PhiField[0].copy(),
            im2,
            searchRange.copy(),
            im1mask=im1mask,
            im2mask=im2mask,
            minMaskCoverage=args.MASK_COVERAGE,
            greyThreshold=[args.GREY_LOW_THRESH, args.GREY_HIGH_THRESH],
            applyF="no",
        )

    # If getImagettes was successful (size check and mask coverage check)
    if imagetteReturnsTop["returnStatus"] == 1:
        PSreturnsTop = spam.DIC.pixelSearch._pixelSearch(
            imagetteReturnsTop["imagette1"],
            imagetteReturnsTop["imagette2"],
            imagette1mask=imagetteReturnsTop["imagette1mask"],
            imagette2mask=imagetteReturnsTop["imagette2mask"],
            returnError=True,
        )

        PhiField[0, 0:3, -1] = PSreturnsTop[0] + imagetteReturnsTop["pixelSearchOffset"]
        pixelSearchCC[0] = PSreturnsTop[1]
        error[0] = PSreturnsTop[2]
    # Failed to extract imagettes or something
    else:
        print("Failed to extract correlation window for starting point, exiting")
        exit()
    if pixelSearchCC[0] < args.CC_MIN:
        print("CC obtained for starting point is less than threshold, not continuing")
        exit()

    # Step 2: Loop sequentially over the guiding points list
    # 2.1: create the tree of the coordinates to find easily neighbours
    treeCoord = KDTree(guidingPoints)
    for point in range(1, numberOfPoints):
        indices = []
        radius = args.RADIUS
        # 2.2: Extract good neighbours
        #      double the radius until it finds at least 1 point in the vicinity
        while len(indices) < 1:
            indices = numpy.array(treeCoord.query_ball_point(guidingPoints[point], radius))
            # Discard current point and points with low CC from indices
            indices = numpy.delete(
                indices,
                numpy.where(numpy.logical_or(indices == point, pixelSearchCC[indices] < pixelSearchCCmin))[0],
            )
            radius *= 2

        # 2.3: Estimate initial displacement
        #      by a gaussian weighting of extracted good neighbours
        distances = numpy.linalg.norm(guidingPoints[point] - guidingPoints[indices], axis=1)
        weights = numpy.exp(-(distances**2) / weightingDistance**2)
        initialDisplacement = numpy.sum(PhiField[indices, 0:3, -1] * weights[:, numpy.newaxis], axis=0) / weights.sum()

        # 2.4: Call PS around the estimated position
        PhiField[point, 0:3, -1] = initialDisplacement

        if args.LAB1 is not None:
            imagetteReturns = spam.label.getImagettesLabelled(
                lab1,
                rowNumbers[point],
                PhiField[0].copy(),
                im1,
                im2,
                searchRange.copy(),
                boundingBoxes,
                centresOfMass,
                margin=args.LABEL_DILATE,
                labelDilate=args.LABEL_DILATE,
                applyF="no",
                volumeThreshold=3**3,
            )
            imagetteReturns["imagette2mask"] = None

        else:
            imagetteReturns = spam.DIC.getImagettes(
                im1,
                guidingPoints[point],
                args.HWS,
                PhiField[point].copy(),
                im2,
                searchRange.copy(),
                im1mask=im1mask,
                im2mask=im2mask,
                minMaskCoverage=args.MASK_COVERAGE,
                greyThreshold=[args.GREY_LOW_THRESH, args.GREY_HIGH_THRESH],
                applyF="no",
            )

        if imagetteReturns["returnStatus"] == 1:
            PSreturns = spam.DIC.pixelSearch._pixelSearch(
                imagetteReturns["imagette1"],
                imagetteReturns["imagette2"],
                imagette1mask=imagetteReturns["imagette1mask"],
                imagette2mask=imagetteReturns["imagette2mask"],
                returnError=True,
            )

            PhiField[point, 0:3, -1] = PSreturns[0] + imagetteReturns["pixelSearchOffset"]
            pixelSearchCC[point] = PSreturns[1]
            error[point] = PSreturns[2]
            returnStatus[point] = imagetteReturns["returnStatus"]

            widgets[0] = progressbar.FormatLabel("  CC={:0>7.5f} ".format(PSreturns[1]))
            pbar.update(point)
        else:
            PhiField[point, 0:3, -1] = [numpy.nan] * 3
            error[point] = numpy.inf
            returnStatus[point] = imagetteReturns["returnStatus"]

    # Detect regular grid mode
    # if args.GUIDING_POINTS_FILE is None:
    if args.GUIDING_POINTS_FILE is None and args.LAB1 is None:
        rowNumbers = rowNumbers[1:]

    guidingPoints = guidingPoints[rowNumbers]
    PhiField = PhiField[rowNumbers]
    error = error[rowNumbers]
    returnStatus = returnStatus[rowNumbers]
    pixelSearchCC = pixelSearchCC[rowNumbers]
    deltaPhiNorm = deltaPhiNorm[rowNumbers]
    iterations = iterations[rowNumbers]

    if args.GUIDING_POINTS_FILE is None and args.LAB1 is None:
        if args.TIFF:
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

    if args.TSV:
        # Make one big array for writing:
        #   First the node number,
        #   3 node positions,
        #   F[0:3,0:3]
        #   Pixel-search CC
        outMatrix = numpy.array(
            [
                numpy.array(range(guidingPoints.shape[0])),
                guidingPoints[:, 0],
                guidingPoints[:, 1],
                guidingPoints[:, 2],
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
        if args.LAB1 is None:
            TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"

        else:  # Lab mode, need to pad one 0 row to the matrix
            TSVheader = "Label\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
            outMatrix[0, :] = 0

        numpy.savetxt(
            args.OUT_DIR + "/" + args.PREFIX + ".tsv",
            outMatrix,
            fmt="%.7f",
            delimiter="\t",
            newline="\n",
            comments="",
            header=TSVheader,
        )

    # Collect data into VTK output
    if args.VTK:
        if args.GUIDING_POINTS_FILE is None and args.LAB1 is None:
            cellData = {}
            cellData["displacements"] = PhiField[:, :-1, 3].reshape((nodesDim[0], nodesDim[1], nodesDim[2], 3))
            cellData["pixelSearchCC"] = pixelSearchCC.reshape(nodesDim)

            # Overwrite nans and infs with 0, rubbish I know
            cellData["displacements"][numpy.logical_not(numpy.isfinite(cellData["displacements"]))] = 0

            # This is perfect in the case where NS = 2xHWS, these cells will all be in the right place
            #   In the case of overlapping of under use of data, it should be approximately correct
            # If you insist on overlapping, then perhaps it's better to save each point as a cube glyph
            #   and actually *have* overlapping
            spam.helpers.writeStructuredVTK(
                origin=guidingPoints[0] - args.HWS,
                aspectRatio=args.NS,
                cellData=cellData,
                fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
            )

        else:
            # boring nans overwriting
            disp = PhiField[:, 0:3, -1]
            disp[numpy.logical_not(numpy.isfinite(disp))] = 0

            magDisp = numpy.linalg.norm(disp, axis=1)

            VTKglyphDict = {
                "displacements": disp,
                "mag(displacements)": magDisp,
                "pixelSearchCC": pixelSearchCC,
            }

            spam.helpers.writeGlyphsVTK(
                guidingPoints,
                VTKglyphDict,
                fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk",
            )
