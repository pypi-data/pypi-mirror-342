# This python script performs Discrete Digital Image Correlation using SPAM functions
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
import multiprocessing
import os

import numpy
import spam.deformation
import spam.DIC
import spam.helpers
import spam.label
import tifffile

numpy.seterr(all="ignore")
os.environ["OPENBLAS_NUM_THREADS"] = "1"


def ddicParser(parser):
    parser.add_argument(
        "im1",
        metavar="im1",
        type=argparse.FileType("r"),
        help="Greyscale image of reference state for correlation",
    )

    parser.add_argument(
        "lab1",
        metavar="lab1",
        type=argparse.FileType("r"),
        help="Labelled image of reference state for correlation",
    )

    parser.add_argument(
        "im2",
        metavar="im2",
        type=argparse.FileType("r"),
        help="Greyscale image of deformed state for correlation",
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
        help="Number of times to dilate labels. Default = 1",
    )

    # parser.add_argument('-ldmax',
    # '--label-dilate-maximum',
    # type=int,
    # default=None,
    # dest='LABEL_DILATE_MAX',
    # help="Maximum dilation for label if they don't converge with -ld setting. Default = same as -ld setting")

    parser.add_argument(
        "-vt",
        "--volume-threshold",
        type=numpy.uint,
        default=100,
        dest="VOLUME_THRESHOLD",
        help="Volume threshold below which labels are ignored. Default = 100",
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
        "-F",
        "--apply-F",
        type=str,
        default="rigid",
        dest="APPLY_F",
        help='Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "rigid" is default',
    )

    parser.add_argument(
        "-m",
        "-mar",
        "-margin",
        type=int,
        default=5,
        dest="MARGIN",
        help="Margin in pixels for the correlation of each local subvolume. Default = 5 px",
    )

    parser.add_argument(
        "-it",
        "--max-iterations",
        type=numpy.uint,
        default=50,
        dest="MAX_ITERATIONS",
        help="Maximum iterations for label correlation. Default = 50",
    )

    parser.add_argument(
        "-dp",
        "--min-delta-phi",
        type=float,
        default=0.001,
        dest="MIN_PHI_CHANGE",
        help="Minimum change in Phi to consider label correlation as converged. Default = 0.001",
    )

    parser.add_argument(
        "-o",
        "--interpolation-order",
        type=numpy.uint,
        default=1,
        dest="INTERPOLATION_ORDER",
        help="Interpolation order for label correlation. Default = 1",
    )

    parser.add_argument(
        "-nr",
        "--non-rigid",
        action="store_false",
        dest="CORRELATE_RIGID",
        help="Activate non-rigid registration for each label",
    )

    parser.add_argument(
        "-ug",
        "--update-gradient",
        action="store_true",
        dest="UPDATE_GRADIENT",
        help="Update gradient in label registration? More computation time but more robust and possibly fewer iterations.",
    )

    # parser.add_argument('-lcms',
    # '--label-correlate-multiscale',
    # action="store_true",
    # dest='LABEL_CORRELATE_MULTISCALE',
    # help='Activate multiscale correlation for the label? If you set this, please indicate -lcmsb')

    parser.add_argument(
        "-msb",
        "--multiscale-binning",
        type=numpy.uint,
        default=1,
        dest="MULTISCALE_BINNING",
        help="Binning level for multiscale label correlation. Default = 1",
    )

    parser.add_argument(
        "-dmo",
        "--dont-mask-others",
        action="store_false",
        dest="MASK_OTHERS",
        help="Prevent masking other labels when dilating?",
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
        "-skp",
        "--skip",
        action="store_true",
        default=False,
        dest="SKIP_PARTICLES",
        help="Read the return status of the Phi file run ddic only for the non-converged grains. Default = False",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        dest="DEBUG",
        help="Extremely verbose mode with graphs and text output. Only use for a few particles. Do not use with mpirun",
    )

    parser.add_argument(
        "-lazy",
        "--lazy-load",
        action="store_true",
        dest="LAZYLOAD",
        help="Load your images using tifffile.memmap for lazy loading. Default = False",
    )

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.lab1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0]

    # Set label dilate max as label dilate if it is none
    # if args.LABEL_DILATE_MAX is None:
    # args.LABEL_DILATE_MAX = args.LABEL_DILATE

    # if args.LABEL_DILATE_MAX < args.LABEL_DILATE:
    # print("spam-ddic: Warning \"label dilate max\" is less than \"label dilate\" setting them equal")
    # args.LABEL_DILATE_MAX = args.LABEL_DILATE

    if args.DEBUG:
        print("spam-ddic: DEBUG mode activated, forcing number of processes to 1")
        args.PROCESSES = 1

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-ddic "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script performs Discrete Digital Image Correlation script between two 3D greyscale images"
        + " (reference and deformed configurations) and requires the input of a labelled image for the reference configuration"
        + "\nSee for more details: https://ttk.gricad-pages.univ-grenoble-alpes.fr/spam/tutorial-04-discreteDIC.html",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = ddicParser(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-ddic")
    
    print("\nspam-ddic: Loading Data...", end="")
    
    # Load images 
    if args.LAZYLOAD:
        try:
            im1 = tifffile.memmap(args.im1.name)
            lab1 = tifffile.memmap(args.lab1.name).astype(spam.label.labelType)
            im2 = tifffile.memmap(args.im2.name)
        except:
            print("\nddic: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im1 = tifffile.imread(args.im1.name)
        lab1 = tifffile.imread(args.lab1.name).astype(spam.label.labelType)
        im2 = tifffile.imread(args.im2.name)

    # im1 = tifffile.imread(args.im1.name)
    # lab1 = tifffile.imread(args.lab1.name).astype(spam.label.labelType)
    # im2 = tifffile.imread(args.im2.name)
    print("done.")
    twoD = False
    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        im1 = im1[numpy.newaxis, ...]
        twoD = True
    if len(lab1.shape) == 2:
        lab1 = lab1[numpy.newaxis, ...]
        twoD = True
    if len(im2.shape) == 2:
        im2 = im2[numpy.newaxis, ...]
        twoD = True

    assert im1.shape == im2.shape, "\nim1 and im2 must have the same size! Exiting."
    assert im1.shape == lab1.shape, "\nim1 and lab1 must have the same size! Exiting."

    ###############################################################
    # Analyse labelled volume in state 01 in order to get bounding
    # boxes and centres of mass for correlation
    ###############################################################
    numberOfLabels = (lab1.max() + 1).astype("u4")

    print("spam-ddic: Number of labels = {}\n".format(numberOfLabels - 1))

    print("spam-ddic: Calculating Bounding Boxes and Centres of Mass of all labels.")
    boundingBoxes = spam.label.boundingBoxes(lab1)
    centresOfMass = spam.label.centresOfMass(lab1, boundingBoxes=boundingBoxes)
    print("\n")

    ###############################################################
    # Set up kinematics array
    ###############################################################

    PhiField = numpy.zeros((numberOfLabels, 4, 4), dtype="<f4")
    # Initialise field of Fs with the identity matrix
    for label in range(numberOfLabels):
        PhiField[label] = numpy.eye(4)
    # define empty rigid displacements for registration:
    # if args.REGSUB: rigidDisp = numpy.zeros((numberOfLabels, 3))

    # Option 2 - load previous DVC
    #################################
    if args.PHIFILE is not None:
        PhiFromFile = spam.helpers.readCorrelationTSV(
            args.PHIFILE.name,
            fieldBinRatio=args.PHIFILE_BIN_RATIO,
            readConvergence=True,
            readError=True,
            readLabelDilate=True,
            readPixelSearchCC=True,
        )

        # If the read Phi-file has only one line -- it's a single point registration!
        if PhiFromFile["fieldCoords"].shape[0] == 1:
            PhiInit = PhiFromFile["PhiField"][0]
            print("\tI read a registration from a file in binning {}".format(args.PHIFILE_BIN_RATIO))

            decomposedPhiInit = spam.deformation.decomposePhi(PhiInit)
            print("\tTranslations (px)")
            print("\t\t", decomposedPhiInit["t"])
            print("\tRotations (deg)")
            print("\t\t", decomposedPhiInit["r"])
            print("\tZoom")
            print("\t\t", decomposedPhiInit["z"])

            PhiField = spam.DIC.applyRegistrationToPoints(
                PhiInit.copy(),
                PhiFromFile["fieldCoords"][0],
                centresOfMass,
                applyF=args.APPLY_F,
                nProcesses=args.PROCESSES,
                verbose=False,
            )

        # If the read Phi-file contains multiple lines it's an F field!
        else:
            # print("spam-ddic: Assuming loaded PhiFile is coherent with the current run (i.e., labels are the same).")
            PhiField = PhiFromFile["PhiField"]
            # Also check that the node positions are approx the same as from the labelled image above:
            if not numpy.allclose(PhiFromFile["fieldCoords"], centresOfMass, atol=0.1, equal_nan=True): # set equal_nan=True to deal with missing labels
                print(PhiFromFile["fieldCoords"])
                print(centresOfMass)
                print(f"spam-ddic: Input PhiField positions from {args.PHIFILE.name} are not within 1px of the centre of mass of the labels from {args.lab1.name}, this seems dangerous.")
                print("\tplease consider using spam-passPhiField to apply your PhiField to a new labelled image")
                exit()

    # Add labels to a queue -- mostly useful for MPI
    # q = queue.Queue()
    labelsToCorrelate = numpy.arange(0, numberOfLabels)

    if args.SKIP_PARTICLES:
        labelsToCorrelate = numpy.delete(labelsToCorrelate, numpy.where(PhiFromFile["returnStatus"] == 2)[0])
        labelsToCorrelate = numpy.delete(labelsToCorrelate, 0)
    else:
        labelsToCorrelate = numpy.delete(labelsToCorrelate, 0)

    # Run the function
    _PhiField, _returnStatus, _error, _iterations, _deltaPhiNorm, _labelDilateList, _PSCC = spam.DIC.ddic(
        im1,
        im2,
        lab1,
        labelsToCorrelate,
        PhiField,
        boundingBoxes,
        centresOfMass,
        processes=args.PROCESSES,
        labelDilate=args.LABEL_DILATE,
        margin=args.MARGIN,
        maskOthers=args.MASK_OTHERS,
        volThreshold=args.VOLUME_THRESHOLD,
        multiScaleBin=args.MULTISCALE_BINNING,
        updateGrad=args.UPDATE_GRADIENT,
        correlateRigid=args.CORRELATE_RIGID,
        maxIter=args.MAX_ITERATIONS,
        deltaPhiMin=args.MIN_PHI_CHANGE,
        interpolationOrder=args.INTERPOLATION_ORDER,
        debug=args.DEBUG,
        twoD=twoD,
    )

    if args.SKIP_PARTICLES:
        # Read the previous result for all grains
        returnStatus = PhiFromFile["returnStatus"]
        iterations = PhiFromFile["iterations"]
        deltaPhiNorm = PhiFromFile["deltaPhiNorm"]
        labelDilateList = PhiFromFile["LabelDilate"]
        error = PhiFromFile["error"]
        PSCC = PhiFromFile["pixelSearchCC"]

        # Overwrite old results by the newly processed particles
        for lab in labelsToCorrelate:
            PhiField[lab] = _PhiField[lab]
            returnStatus[lab] = _returnStatus[lab]
            iterations[lab] = _error[lab]
            deltaPhiNorm[lab] = _iterations[lab]
            labelDilateList[lab] = _deltaPhiNorm[lab]
            error[lab] = _labelDilateList[lab]
            PSCC[lab] = _PSCC[lab]

    else:
        # we're not in skip mode, just pass through the results of the correlation aboce
        PhiField = _PhiField
        returnStatus = _returnStatus
        error = _error
        iterations = _iterations
        deltaPhiNorm = _deltaPhiNorm
        labelDilateList = _labelDilateList
        PSCC = _PSCC

    # Redundant output for VTK visualisation
    magDisp = numpy.zeros(numberOfLabels)
    for label in range(numberOfLabels):
        magDisp[label] = numpy.linalg.norm(PhiField[label][0:3, -1])

    # Finished! Get ready for output.
    # if args.REGSUB:
    # print("\n\tFinished correlations. Subtracting rigid-body motion from displacements of each particle")
    # PhiFieldMinusRigid = PhiField.copy()
    # magDispRegsub = numpy.zeros(numberOfLabels)
    # for label in range(numberOfLabels):
    # PhiFieldMinusRigid[label][0:3,-1] -= rigidDisp[label]
    # magDispRegsub[label] = numpy.linalg.norm(PhiFieldMinusRigid[label][0:3,-1])

    outMatrix = numpy.array(
        [
            numpy.array(range(numberOfLabels)),
            centresOfMass[:, 0],
            centresOfMass[:, 1],
            centresOfMass[:, 2],
            PhiField[:, 0, 3],
            PhiField[:, 1, 3],
            PhiField[:, 2, 3],
            PhiField[:, 0, 0],
            PhiField[:, 0, 1],
            PhiField[:, 0, 2],
            PhiField[:, 1, 0],
            PhiField[:, 1, 1],
            PhiField[:, 1, 2],
            PhiField[:, 2, 0],
            PhiField[:, 2, 1],
            PhiField[:, 2, 2],
            PSCC,
            error,
            iterations,
            returnStatus,
            deltaPhiNorm,
            labelDilateList,
        ]
    ).T

    numpy.savetxt(
        args.OUT_DIR + "/" + args.PREFIX + "-ddic.tsv",
        outMatrix,
        fmt="%.7f",
        delimiter="\t",
        newline="\n",
        comments="",
        header="Label\tZpos\tYpos\tXpos\t" + "Zdisp\tYdisp\tXdisp\t" + "Fzz\tFzy\tFzx\t" + "Fyz\tFyy\tFyx\t" + "Fxz\tFxy\tFxx\t" + "PSCC\terror\titerations\treturnStatus\tdeltaPhiNorm\tLabelDilate",
    )

    # Prepare VTK outputs with no nans
    dispField = PhiField[:, 0:3, -1]
    dispFieldNoNans = dispField.copy()
    dispFieldNoNans[numpy.isnan(dispFieldNoNans)] = 0.0
    magDispNoNans = magDisp.copy()
    magDispNoNans[numpy.isnan(magDispNoNans)] = 0.0
    centresOfMassNoNans = centresOfMass.copy()
    centresOfMassNoNans[numpy.isnan(centresOfMassNoNans)] = 0.0

    VTKglyphDict = {
        "displacements": dispFieldNoNans,
        "mag(displacements)": magDispNoNans,
        "returnStatus": returnStatus,
    }

    # if regsub add a line to VTK output and also save separate TSV file
    # if args.REGSUB:
    # VTKglyphDict['displacements-regsub'] = PhiFieldMinusRigid[:, 0:3, -1]
    # VTKglyphDict['mag(displacements-regsub)'] = magDispRegsub

    # outMatrix = numpy.array([numpy.array(range(numberOfLabels)),
    # centresOfMass[:, 0], centresOfMass[:, 1], centresOfMass[:, 2],
    # PhiFieldMinusRigid[:, 0, 3], PhiFieldMinusRigid[:, 1, 3], PhiFieldMinusRigid[:, 2, 3],
    # PhiFieldMinusRigid[:, 0, 0], PhiFieldMinusRigid[:, 0, 1], PhiFieldMinusRigid[:, 0, 2],
    # PhiFieldMinusRigid[:, 1, 0], PhiFieldMinusRigid[:, 1, 1], PhiFieldMinusRigid[:, 1, 2],
    # PhiFieldMinusRigid[:, 2, 0], PhiFieldMinusRigid[:, 2, 1], PhiFieldMinusRigid[:, 2, 2],
    # PSCC,
    # error, iterations, returnStatus, deltaPhiNorm,
    # labelDilateList]).T

    # numpy.savetxt(args.OUT_DIR + "/" + args.PREFIX + "-discreteDVC-regsub.tsv",
    # outMatrix,
    # fmt='%.7f',
    # delimiter='\t',
    # newline='\n',
    # comments='',
    # header="Label\tZpos\tYpos\tXpos\t" +
    # "Zdisp\tYdisp\tXdisp\t" +
    # "Fzz\tFzy\tFzx\t" +
    # "Fyz\tFyy\tFyx\t" +
    # "Fxz\tFxy\tFxx\t" +
    # "PSCC\terror\titerations\treturnStatus\tdeltaPhiNorm\tLabelDilate")

    spam.helpers.writeGlyphsVTK(
        centresOfMassNoNans,
        VTKglyphDict,
        fileName=args.OUT_DIR + "/" + args.PREFIX + "-ddic.vtk",
    )
