# Library of SPAM image correlation functions.
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

import numpy
import spam.deformation
import spam.DIC
import spam.label  # for im1mask


def registerParser(parser):
    import os

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
        "-mf1",
        "--maskFile1",
        dest="MASK1",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tiff file containing the mask of image 1 -- masks zones not to correlate, which should be == 0",
    )

    parser.add_argument(
        "-rmc",
        "--returnPhiMaskCentre",
        dest="RETURN_PHI_MASK_CENTRE",
        action="store_true",
        default=False,
        help="Should the Phi be returned at the centre of mass of the mask? Default = False",
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
        "-rig",
        "--rigid",
        action="store_true",
        dest="RIGID",
        help="Only do a rigid registration (i.e., displacements and rotations)?",
    )

    parser.add_argument(
        "-bb",
        "--binning-begin",
        type=int,
        default=4,
        dest="BIN_BEGIN",
        help="Initial binning to apply to input images for initial registration. Default = 4",
    )

    parser.add_argument(
        "-be",
        "--binning-end",
        type=int,
        default=1,
        dest="BIN_END",
        help="Binning level to stop at for initial registration. Default = 1",
    )

    parser.add_argument(
        "-m",
        "-mar",
        "--margin",
        type=float,
        default=None,
        dest="MARGIN",
        help="Interpolation margin in pixels. Default is the default for spam.DIC.registerMultiscale",
    )

    parser.add_argument(
        "-m3",
        "-mar3",
        "--margin3",
        nargs=3,
        type=int,
        default=None,
        dest="MARGIN",
        help="ZYX interpolation margin in pixels. Default is the default for spam.DIC.registerMultiscale",
    )

    parser.add_argument(
        "-ug",
        "--update-gradient",
        action="store_true",
        dest="UPDATE_GRADIENT",
        help="Update gradient during newton iterations? More computation time but sometimes more robust and possibly fewer iterations. Default = False",
    )

    parser.add_argument(
        "-it",
        "--max-iterations",
        type=int,
        default=50,
        dest="MAX_ITERATIONS",
        help="Maximum number of iterations. Default = 50",
    )

    parser.add_argument(
        "-dp",
        "--min-delta-phi",
        type=float,
        default=0.0001,
        dest="MIN_DELTA_PHI",
        help="Minimum delta Phi for convergence. Default = 0.0001",
    )

    parser.add_argument(
        "-o",
        "--interpolation-order",
        type=int,
        default=1,
        dest="INTERPOLATION_ORDER",
        help="Image interpolation order. Default = 1, i.e., linear interpolation",
    )

    parser.add_argument(
        "-g",
        "--graph",
        action="store_true",
        default=False,
        dest="GRAPH",
        help="Activate graphical mode to look at iterations",
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

    parser.add_argument(
        "-def",
        "--save-deformed-image1",
        action="store_true",
        default=False,
        dest="DEF",
        help="Activate the saving of a deformed image 1 (as <im1>-reg-def.tif)",
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
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0] + "-registration"
    else:
        args.PREFIX += "-registration"

    return args


def script():
    import os

    import tifffile

    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-register " + spam.helpers.optionsParser.GLPv3descriptionHeader + "This script tries to measure Phi from im1 to im2\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = registerParser(parser)

    spam.helpers.displaySettings(args, "spam-register")

    # Load reference image
    if args.LAZYLOAD:
        try:
            im1 = tifffile.memmap(args.im1.name)
        except:
            print("\nregistration: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im1 = tifffile.imread(args.im1.name)

    PhiCentre = (numpy.array(im1.shape) - 1) / 2.0

    if args.MASK1:
        if args.LAZYLOAD:
            try:
                im1mask = tifffile.memmap(args.MASK1.name) != 0
            except:
                print("\nregistration: Problem with tifffile.memmap. Boolean arrays are not supported, try saving your mask1 in a 8-bit format. Exiting.")
                exit()
        else:
            im1mask = tifffile.imread(args.MASK1.name) != 0 # !=0 to be removed?

        assert im1.shape == im1mask.shape, "\nim1 and im1mask must have the same size! Exiting."
        if args.RETURN_PHI_MASK_CENTRE:
            PhiCentre = spam.label.centresOfMass(im1mask)[-1]
    else:
        im1mask = None

    # Load reference image
    if args.LAZYLOAD:
        try:
            im2 = tifffile.memmap(args.im2.name)
        except:
            print("\nregistration: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im2 = tifffile.imread(args.im2.name)

    assert im1.shape == im2.shape, "\nim1 and im2 must have the same size! Exiting."

    if args.PHIFILE is not None:
        PhiFromFile = spam.helpers.readCorrelationTSV(args.PHIFILE.name, fieldBinRatio=args.PHIFILE_BIN_RATIO)
        # If the read Phi-file has only one line -- it's a single point registration!
        if PhiFromFile["fieldCoords"].shape[0] == 1:
            PhiInit = PhiFromFile["PhiField"][0]
            # regCentre = PhiFromFile['fieldCoords'][0]
            # print("\tI read a registration from a file in binning {} at centre {} at this scale".format(args.PHIFILE_BIN_RATIO, regCentre) )
            print("\tI read a registration from a file in binning {}".format(args.PHIFILE_BIN_RATIO))

            decomposedPhiInit = spam.deformation.decomposePhi(PhiInit)

            print("\tTranslations (px)")
            print("\t\t", decomposedPhiInit["t"])
            print("\tRotations (deg)")
            print("\t\t", decomposedPhiInit["r"])
            print("\tZoom")
            print("\t\t", decomposedPhiInit["z"])

        # If the read F-file contains multiple lines it's an F field!
        else:
            print("You can't pass a field to register!!!")
            exit()
    else:
        PhiInit = None

    if args.INTERPOLATION_ORDER == 1:
        # Override interpolator to save memory
        interpolator = "C"
    else:
        interpolator = "python"

    regReturns = spam.DIC.registerMultiscale(
        im1,
        im2,
        args.BIN_BEGIN,
        binStop=args.BIN_END,
        margin=args.MARGIN,
        PhiInit=PhiInit,
        PhiRigid=args.RIGID,
        im1mask=im1mask,
        returnPhiMaskCentre=args.RETURN_PHI_MASK_CENTRE,
        interpolationOrder=args.INTERPOLATION_ORDER,
        maxIterations=args.MAX_ITERATIONS,
        deltaPhiMin=args.MIN_DELTA_PHI,
        updateGradient=args.UPDATE_GRADIENT,
        interpolator=interpolator,
        verbose=True,
        imShowProgress=args.GRAPH,
    )

    if regReturns["returnStatus"] == 2:
        print("\n\nRegistration converged, great... saving")

    if regReturns["returnStatus"] == 1:
        print("\n\nRegistration hit max iterations, OK... saving")

    if regReturns["returnStatus"] > 0 and args.DEF:
        if im1.ndim == 2:
            im1 = im1[numpy.newaxis, ...]
            tifffile.imwrite(
                args.OUT_DIR + "/" + os.path.splitext(os.path.basename(args.im1.name))[0] + "-reg-def.tif",
                spam.DIC.applyPhiPython(im1, Phi=regReturns["Phi"])[0].astype(im1.dtype),
            )
        else:
            tifffile.imwrite(
                args.OUT_DIR + "/" + os.path.splitext(os.path.basename(args.im1.name))[0] + "-reg-def.tif",
                spam.DIC.applyPhi(im1, Phi=regReturns["Phi"]).astype(im1.dtype),
            )

    if regReturns["returnStatus"] < 0:
        print("\n\nWe're saving this registration but we don't trust it at all")

    spam.helpers.writeRegistrationTSV(
        args.OUT_DIR + "/" + args.PREFIX + ".tsv",
        PhiCentre,
        regReturns,
    )
