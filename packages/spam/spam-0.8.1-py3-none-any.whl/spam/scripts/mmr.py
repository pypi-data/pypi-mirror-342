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

import numpy
import spam.deformation
import spam.DIC
import spam.helpers
import tifffile

numpy.seterr(all="ignore")


def multiModalRegistrationParser(parser):
    import numpy
    import spam.DIC

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
        "-im1min",
        type=float,
        default=None,
        dest="IM1_MIN",
        help="Minimum of im1 for greylevel scaling. Default = im1.min()",
    )

    parser.add_argument(
        "-im1max",
        type=float,
        default=None,
        dest="IM1_MAX",
        help="Maximum of im1 for greylevel scaling. Default = im1.max()",
    )

    parser.add_argument(
        "-im2min",
        type=float,
        default=None,
        dest="IM2_MIN",
        help="Minimum of im2 for greylevel scaling. Default = im2.min()",
    )

    parser.add_argument(
        "-im2max",
        type=float,
        default=None,
        dest="IM2_MAX",
        help="Maximum of im2 for greylevel scaling. Default = im2.max()",
    )

    parser.add_argument(
        "-im1th",
        "--im1-threshold",
        type=int,
        default=0,
        dest="IM1_THRESHOLD",
        help="Greylevel threshold for image 1. Below this threshold, peaks in the histogram are ignored.",
    )

    parser.add_argument(
        "-im2th",
        "--im2-threshold",
        type=int,
        default=0,
        dest="IM2_THRESHOLD",
        help="Greylevel threshold for image 2. Below this threshold, peaks in the histogram are ignored.",
    )

    parser.add_argument(
        "-bin",
        "--bin-levels",
        type=int,
        default=1,
        dest="NBINS",
        help="Number of binning levels to apply to the data (if given 3, the binning levels used will be 4 2 1).\
              The -phase option is necessary and should define this many phases (i.e., 3 different numbers in this example)",
    )

    parser.add_argument(
        "-ph",
        "--phases",
        nargs="+",
        type=int,
        default=[2],
        dest="PHASES",
        help="Number of phases?",
    )

    parser.add_argument(
        "-jhb",
        "--joint-histogram-bins",
        # nargs=1,
        type=int,
        default=128,
        dest="JOINT_HISTO_BINS",
        help="The number of greylevel bins for both images in the joint histogram",
    )

    parser.add_argument(
        "-dst",
        "--dist-between-max",
        type=int,
        default=None,
        dest="DIST_BETWEEN_MAX",
        help="Minimal distance between two maxima in the histogram",
    )

    parser.add_argument(
        "-fdi",
        "--fit-distance",
        type=float,
        default=None,
        dest="FIT_DISTANCE",
        help="Distance considered around a peak for the Gaussian ellipsoid fitting",
    )

    parser.add_argument(
        "-voc",
        "--voxel-coverage",
        type=float,
        default=1.0,
        dest="VOXEL_COVERAGE",
        help="Percentage (between 0 and 1) of voxel coverage of the phases in the joint histogram",
    )

    parser.add_argument(
        "-int",
        "--interactive",
        action="store_true",
        dest="INTERACTIVE",
        help="Present live-updating plots to the user",
    )

    parser.add_argument(
        "-gra",
        "--graphs",
        action="store_true",
        dest="GRAPHS",
        help="Save graphs to file",
    )

    parser.add_argument(
        "-ssl",
        "--show-slice-axis",
        type=int,
        default=0,
        dest="SHOW_SLICE_AXIS",
        help="Axis of the cut used for the plots",
    )

    parser.add_argument(
        "-dp",
        "--min-delta-phi",
        type=float,
        default=0.0005,
        dest="MIN_PHI_CHANGE",
        help="Subpixel min change in Phi to stop iterations. Default = 0.001",
    )

    parser.add_argument(
        "-it",
        "--max-iterations",
        type=int,
        default=50,
        dest="MAX_ITERATIONS",
        help="Max number of iterations to optimise Phi. Default = 50",
    )

    # parser.add_argument('-tmp',
    #                     '--writeTemporaryFiles',
    #                     action="store_true",
    #                     dest='DATA',
    #                     help='Save temporary files (joint histogram) to \"dat\" file')

    # parser.add_argument('-loadprev',
    # '--load-previous-iteration',
    # action="store_true",
    # dest='LOADPREV',
    # help='Load output pickle files from previous iterations (2* coarser binning)')

    parser.add_argument(
        "-mar",
        "--margin",
        type=float,
        default=0.1,
        dest="MARGIN",
        help="Margin of both images. Default = 0.1, which means 0.1 * image size from both sides",
    )

    parser.add_argument(
        "-cro",
        "--crop",
        type=float,
        default=0.1,
        dest="CROP",
        help="Initial crop of both images. Default = 0.1, which means 0.1 * image size from both sides",
    )

    # parser.add_argument('-pif',
    # default=None,
    # type=argparse.FileType('rb'),
    # dest='FGUESS_PICKLE',
    # help="Pickle file name for initial guess. Should be in position 0 in the array and labeled as 'F' as for registration.")

    # Remove next two arguments for F input, and replace with displacement and rotation inputs on command line
    parser.add_argument(
        "-pf",
        "--phiFile",
        dest="PHIFILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to TSV file containing a single Phi guess (not a field) that deforms im1 onto im2. Default = None",
    )

    # parser.add_argument('-Ffb',
    # '--Ffile-bin-ratio',
    # type=int,
    # default=1,
    # dest='PHIFILE_BIN_RATIO',
    # help="Ratio of binning level between loaded Phi file and current calculation.\
    #        If the input Phi file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    # parser.add_argument('-tra',
    # '--translation',
    # nargs=3,
    # type=float,
    # default=None,
    # dest='TRA',
    # help="Z, Y, X initial displacements to apply at the bin 1 scale")

    # parser.add_argument('-rot',
    # '--rotation',
    # nargs=3,
    # type=float,
    # default=None,
    # dest='ROT',
    # help="Z, Y, X components of rotation vector to apply at the bin 1 scale")

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

    args = parser.parse_args()

    # The number of bin levels must be the same as the number of phases
    if args.NBINS != len(args.PHASES):
        print("\toptionsParser.multiModalRegistrationParser(): Number of bin levels and number of phases not the same, exiting")
        exit()

    # For back compatibility, generate list of bins
    args.BINS = []
    for i in range(args.NBINS)[::-1]:
        args.BINS.append(2**i)

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

    # Get initial guesses
    if args.PHIFILE is not None:
        import spam.helpers

        args.FGUESS = spam.helpers.readCorrelationTSV(args.PHIFILE.name, readConvergence=False, readOnlyDisplacements=False)["PhiField"][0]
    else:
        args.FGUESS = numpy.eye(4)

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0]

    return args


def script():
    # Parse arguments with external helper function
    parser = argparse.ArgumentParser(
        description="spam-mmr "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script performs Multi-Modal Registration (i.e., alignment) between two 3D greyscale images"
        + " of the same sample acquired with different modalities. The two 3D images should have the same size"
        + " in pixels and be roughly aligned, or have a good initial guess. "
        + "For an initial guess by eye you can use the TSV output from the first step of spam-mmr-graphical. "
        + "The output of this function is a TSV with the deformation to apply to the first image. "
        + "In the iterations the *second* input is numerically deformed, and (updated) gradients are computed on this second image.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    args = multiModalRegistrationParser(parser)

    numpy.set_printoptions(precision=3, suppress=True)

    """
    2017-10-05 Emmanuel Ando' and Edward Roubin

    Multimodal -- e.g., x-ray and neutron registration

    Reminder: Gaussian fitting parameters a <-> x2
                                            b <-> xy
                                            c <-> y2
    """

    spam.helpers.displaySettings(args, "spam-mmr")
    
    GRAPHS = args.GRAPHS
    INTERACTIVE = args.INTERACTIVE
    SHOW_SLICE_AXIS = args.SHOW_SLICE_AXIS

    # BINS_NPHASES = [(8, 2), (4, 5), (2, 5)]
    # BINS_NPHASES = [(4,5),(2,4)]
    # BINS_NPHASES = [(2, 5)]

    # if  is None:
    distanceMaxima = args.DIST_BETWEEN_MAX
    # else:
    # distanceMaxima = args.DIST_BETWEEN_MAX

    print("Loading data...")
    im1Initial = tifffile.imread(args.im1.name).astype("<f4")
    im2Initial = tifffile.imread(args.im2.name).astype("<f4")
    print("\tim1 size: {}".format(im1Initial.shape))
    print("\tim2 size: {}".format(im2Initial.shape))

    # crop: the part of the image we consider
    cropRatio = args.CROP
    crop = (
        slice(int(cropRatio * im1Initial.shape[0]), int((1 - cropRatio) * im1Initial.shape[0])),
        slice(int(cropRatio * im1Initial.shape[1]), int((1 - cropRatio) * im1Initial.shape[1])),
        slice(int(cropRatio * im1Initial.shape[2]), int((1 - cropRatio) * im1Initial.shape[2])),
    )

    print("Rescale f and g...")
    print("\tInitial greyvalues")
    print("\t\tf: {} {}".format(im1Initial[crop].min(), im1Initial[crop].max()))
    print("\t\tg: {} {}".format(im2Initial[crop].min(), im2Initial[crop].max()))

    # min max
    if args.IM1_MIN is None:
        im1Min = im1Initial[crop].min()
    else:
        im1Min = args.IM1_MIN

    if args.IM1_MAX is None:
        im1Max = im1Initial[crop].max()
    else:
        im1Max = args.IM1_MAX

    if args.IM2_MIN is None:
        im2Min = im2Initial[crop].min()
    else:
        im2Min = args.IM2_MIN

    if args.IM2_MAX is None:
        im2Max = im2Initial[crop].max()
    else:
        im2Max = args.IM2_MAX

    # # paper
    # im1Min = 7000.0
    # im1Max = 42000.0
    # im2Min = 5000.0
    # im2Max = 65535.0

    # 16bits min max
    # im1Min = 0.0
    # im1Max = 65535.0
    # im2Min = 0.0
    # im2Max = 65535.0

    # This makes sure that the images are rescaled into JOINT_HISTO_BINS greyvalues
    im1greyScaled = float(args.JOINT_HISTO_BINS) * (im1Initial - im1Min) / float(im1Max - im1Min)
    im2greyScaled = float(args.JOINT_HISTO_BINS) * (im2Initial - im2Min) / float(im2Max - im2Min)

    # Convert to 8 bit
    im1greyScaled = im1greyScaled.astype("<u1")
    im2greyScaled = im2greyScaled.astype("<u1")

    # import matplotlib.pyplot as plt
    # plt.hist( im1Initial.ravel() )
    # plt.show()
    # plt.hist( im2Initial.ravel() )
    # plt.show()

    rootPath = args.OUT_DIR

    print("List of binning levels and number of phases considered:")

    # try to detect initial bin level from file name
    try:
        initialBinLevel = int(args.im1.name.split("bin")[-1].split(".")[0])
    except:
        initialBinLevel = 1

    bins = numpy.array(args.BINS) * initialBinLevel
    for i, (bin, nPhases) in enumerate(zip(bins, args.PHASES)):
        print("\tBinning Level: {}, Number of Phases: {}".format(bin, nPhases))
    print("")

    # Loop over the scales
    for i, (bin, nPhases) in enumerate(zip(bins, args.PHASES)):
        str = "# Binning Level: {}, Number of Phases: {} #".format(bin, nPhases)
        print("#" * len(str))
        print(str)
        print("#" * len(str))
        print("")

        print("STEP 1: Scale images")
        factor = initialBinLevel / float(bin)
        if factor == 1:
            im1 = im1greyScaled
            im2 = im2greyScaled
        elif factor < 1:
            print("\tScaling images to binning = {} (zoom factor {})".format(bin, factor))
            im1 = spam.DIC.binning(im1greyScaled, bin)
            im2 = spam.DIC.binning(im2greyScaled, bin)
        else:
            print("binning less than one is mad, go away")
            exit()

        print("\tim1 size: {}".format(im1.shape))
        print("\tim2 size: {}".format(im2.shape))
        print("")

        # load and rescale images
        numpy.array(im1.shape) / 2

        # crop: the part of the image we consider
        cropRatio = args.CROP
        crop = (
            slice(int(cropRatio * im1.shape[0]), int((1 - cropRatio) * im1.shape[0])),
            slice(int(cropRatio * im1.shape[1]), int((1 - cropRatio) * im1.shape[1])),
            slice(int(cropRatio * im1.shape[2]), int((1 - cropRatio) * im1.shape[2])),
        )

        # margin: border needed to feed the transformed image
        margin = int(args.MARGIN * min(im1.shape))
        cropWithMargin = (
            slice(
                int(cropRatio * im1.shape[0] + margin),
                int((1 - cropRatio) * im1.shape[0] - margin),
            ),
            slice(
                int(cropRatio * im1.shape[1] + margin),
                int((1 - cropRatio) * im1.shape[1] - margin),
            ),
            slice(
                int(cropRatio * im1.shape[2] + margin),
                int((1 - cropRatio) * im1.shape[2] - margin),
            ),
        )

        print("STEP 2: Applying initial guess to g for the joint histogram")
        # case first scale: either take input initial guess or pickle file from previous registration
        if i == 0:
            PhiGuess = args.FGUESS
            PhiGuess[0:3, 3] = factor * PhiGuess[0:3, 3]

        # case other scales
        else:
            PhiGuess = registration["Phi"]
            PhiGuess[0:3, 3] = 2.0 * PhiGuess[0:3, 3]

        # gaussian parameters
        tmp = spam.deformation.decomposePhi(PhiGuess)
        print("\tInitial guess translations: {:.4f}, {:.4f}, {:.4f}".format(*tmp["t"]))
        print("\tInitial guess rotations   : {:.4f}, {:.4f}, {:.4f}".format(*tmp["r"]))
        print("\tInitial guess zoom        : {:.4f}, {:.4f}, {:.4f}".format(*tmp["z"]))

        # This is image 2 and Phi points from im1 to im2 doe inv is justified
        # im2Tmp = spam.DIC.applyPhi(im2.copy(), Phi=PhiGuess, Fpoint=imCentre)
        im2def = spam.DIC.applyPhi(im2.copy(), Phi=numpy.linalg.inv(PhiGuess))
        print("")

        print("STEP 3: Get gaussian parameters")
        # try:
        #     gaussianParameters, jointHistogram = pickle.load(open("{}/GaussianMixture_gaussianParameters-bin{}.p".format(rootPath, bin), "r"))
        # except:
        gaussianParameters, jointHistogram = spam.DIC.gaussianMixtureParameters(
            im1[cropWithMargin],
            im2def[cropWithMargin],
            BINS=args.JOINT_HISTO_BINS,
            NPHASES=nPhases,
            im1threshold=args.IM1_THRESHOLD,
            im2threshold=args.IM2_THRESHOLD,
            distanceMaxima=distanceMaxima,
            excludeBorder=False,
            fitDistance=args.FIT_DISTANCE,
            GRAPHS=GRAPHS,
            INTERACTIVE=INTERACTIVE,
            sliceAxis=SHOW_SLICE_AXIS,
            rootPath=rootPath,
            suffix="bin{}".format(bin),
        )
        # tifffile.imwrite("{}/GaussianMixture_jointHistogram-bin{}.tif".format(rootPath, bin), jointHistogram.astype('<f4'))
        # pickle.dump([gaussianParameters, jointHistogram], open("{}/GaussianMixture_gaussianParameters-bin{}.p".format(rootPath, bin), "w"))
        print("")

        # gaussianParameters = numpy.delete(gaussianParameters, 2, axis=0)

        print("STEP 4: Create phase repartition")
        voxelCoverage = args.VOXEL_COVERAGE
        phaseDiagram, actualVoxelCoverage = spam.DIC.phaseDiagram(
            gaussianParameters,
            jointHistogram,
            voxelCoverage,
            # sigmaMax=10,
            BINS=args.JOINT_HISTO_BINS,
            GRAPHS=GRAPHS,
            INTERACTIVE=INTERACTIVE,
            rootPath=rootPath,
            suffix="bin{}".format(bin),
        )
        # tifffile.imwrite("{}/GaussianMixture_phaseDiagram-{:.2f}p-bin{}.tif".format(rootPath, actualVoxelCoverage, bin), phaseDiagram.astype('<u1'))
        print("")

        # registration
        print("STEP 5: Registration")
        registration = spam.DIC.multimodalRegistration(
            im1[crop],
            im2[crop],
            phaseDiagram,
            gaussianParameters,
            maxIterations=args.MAX_ITERATIONS,
            PhiInit=PhiGuess.copy(),  # 2020-05-26: EA OS AT this should NOT be inv
            BINS=args.JOINT_HISTO_BINS,
            deltaPhiMin=args.MIN_PHI_CHANGE,
            verbose=True,
            margin=margin,
            GRAPHS=GRAPHS,
            INTERACTIVE=INTERACTIVE,
            sliceAxis=SHOW_SLICE_AXIS,
            rootPath=rootPath,
            suffix="bin{}".format(bin),
        )

        # Prepare to write TSV
        registration["error"] = registration["logLikelyhood"]
        spam.helpers.writeRegistrationTSV(
            "{}/{}-{}-PhiMMR-bin{}.tsv".format(rootPath, args.im1.name[0:-4], args.im2.name[0:-4], bin),
            (numpy.array(im1.shape) - 1) / 2.0,
            registration,
        )

        # apply registration to image
        # im2Reg = spam.DIC.applyTransformationOperator(im2, Phi=registration['Phi'], Fpoint=imCentre)
        # Actually, reload im2Initial, so that the origial grelevels are finally deformed:
        # im1reg = spam.DIC.applyPhi(im1Initial, Phi=registration["Phi"])

        # print("Final registration")
        # print("\tTranslations: {:.4f}, {:.4f}, {:.4f}".format(*registration['transformation']['t']))
        # print("\tRotations   : {:.4f}, {:.4f}, {:.4f}".format(*registration['transformation']['r']))
        # print("\tZoom        : {:.4f}, {:.4f}, {:.4f}".format(*registration['transformation']['z']))

        # save files
        # tifffile.imwrite("{}_registered-bin{}.tif".format(args.im1.name[0:-4], bin), im1reg)
        # tifffile.imwrite("{}/xn_residual-bin{}.tif".format(rootPath, bin),   registration['residualField'])
        # tifffile.imwrite("{}/xn_phases-bin{}.tif".format(rootPath, bin),     registration['phaseField'])

        # tifffile.imwrite("{}/GaussianMixture_checkerBoardH-bin{}.tif".format(rootPath, bin), spam.DIC.checkerBoard(im1reg[im1reg.shape[0]//2],       im2[im2.shape[0]//2], n=7, ))
        # tifffile.imwrite("{}/GaussianMixture_checkerBoardV-bin{}.tif".format(rootPath, bin), spam.DIC.checkerBoard(im1reg[:, :, im1reg.shape[2]//2], im2[:, :, im2.shape[2]//2], n=7, ))

        print("\n")
