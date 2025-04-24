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
import spam.label
import tifffile

numpy.seterr(all="ignore")


def ITKwatershedParser(parser):
    parser.add_argument(
        "inFile",
        metavar="inFile",
        type=argparse.FileType("r"),
        help="Path to binary TIFF file to be segmented",
    )

    parser.add_argument(
        "-ld",
        "--label-dilate",
        type=int,
        default=0,
        dest="LABEL_DILATE",
        help="Number of times to dilate labels. Default = 0, Normally you want this to be negative",
    )

    parser.add_argument(
        "-mf",
        "--marker-file",
        type=str,
        default=None,
        dest="MARKER_FILE",
        help="Path to labelled TIFF file to use as markers",
    )

    parser.add_argument(
        "-pre",
        "--prefix",
        type=str,
        default=None,
        dest="PREFIX",
        help="Prefix for output files (without extension). Default is basename of input file plus watershed at the end",
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
        "-v",
        action="store_true",
        dest="VERBOSE",
        help="Print the evolution of the process (0 -> False, 1 -> True). Defalut is 0",
    )

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
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
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0] + "-watershed"

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-ITKwatershed "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script performs the segmentation of a binary image using the ITK watershed library."
        + "\nSee for more details: https://www.spam-project.dev/docs/tutorials/tutorial-03-labelToolkit.html",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with helper function
    args = ITKwatershedParser(parser)

    if args.VERBOSE:
        print("-> Loading binary image...", end="")
    binVol = tifffile.imread(args.inFile.name)
    if args.VERBOSE:
        print("done.")

    if args.MARKER_FILE is not None:
        if args.VERBOSE:
            print("-> Loading marker image...", end="")
        markerVol = tifffile.imread(args.MARKER_FILE)
        if args.VERBOSE:
            print("done.")

        # 2019-09-07 EA: changing dilation/erosion into a single pass by a spherical element, rather than repeated
        # iterations of the standard.
        if args.LABEL_DILATE != 0:
            BB = spam.label.boundingBoxes(markerVol)
            COM = spam.label.centresOfMass(markerVol, boundingBoxes=BB)
            # plt.imshow(imLab[25]); plt.show()
            tmp = numpy.zeros_like(markerVol)
            for label in range(1, markerVol.max() + 1):
                gl = spam.label.getLabel(
                    markerVol,
                    label,
                    labelDilate=args.LABEL_DILATE,
                    boundingBoxes=BB,
                    centresOfMass=COM,
                )
                if gl is not None:
                    tmp[gl["slice"]] = gl["subvol"] * label
        markerVol = tmp
    else:
        markerVol = None

    # Run the function
    lab = spam.label.watershed(binVol, markers=markerVol)
    if args.VERBOSE:
        print("-> Saving labelled image...", end="")
    tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + ".tif", lab)
    if args.VERBOSE:
        print("done.")
