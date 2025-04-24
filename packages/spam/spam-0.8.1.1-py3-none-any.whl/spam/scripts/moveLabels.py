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
import spam.helpers
import spam.label
import tifffile

numpy.seterr(all="ignore")
os.environ["OPENBLAS_NUM_THREADS"] = "1"


def moveLabelsParser(parser):
    parser.add_argument(
        "LabFile",
        metavar="LabFile",
        type=argparse.FileType("r"),
        help="Path to the labelled TIFFfile to be moved",
    )

    parser.add_argument(
        "TSVFile",
        metavar="TSVFile",
        type=argparse.FileType("r"),
        help="Path to TSV file containing the Phis to apply to each label",
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
        help="Prefix for output TIFF file (without extension). Default is basename of input file",
    )

    parser.add_argument(
        "-com",
        "--apply-phi-centre-of-mass",
        action="store_true",
        dest="PHICOM",
        help="Apply Phi to centre of mass of particle? Otherwise it will be applied in the middle of the particle's bounding box",
    )

    parser.add_argument(
        "-thr",
        "--threshold",
        type=float,
        default=0.5,
        dest="THRESH",
        help="Greyscale threshold to keep interpolated voxels. Default = 0.5",
    )

    parser.add_argument(
        "-rst",
        "--return-status-threshold",
        type=int,
        default=None,
        dest="RETURN_STATUS_THRESHOLD",
        help="Return status in spam-ddic to consider the grain. Default = None, but 2 (i.e., converged) is recommended",
    )

    # parser.add_argument('-gf',
    # '--grey-file',
    # type=str,
    # default=None,
    # dest='GREY_FILE',
    # help='Input greylevel tiff file corresponding to the input labelled file. This option requires a threshold to be set with -thr')

    parser.add_argument(
        "-lm",
        "--label-margin",
        type=int,
        default=3,
        dest="MARGIN",
        help="Bounding box margin for each label to allow for rotation/strain of the label. Default = 3",
    )

    parser.add_argument(
        "-ld",
        "--label-dilate",
        type=int,
        default=0,
        dest="LABEL_DILATE",
        help="Number of times to dilate labels. Default = 0",
    )

    help = [
        "Ratio of binning level between loaded Phi file and labelled image.",
        "If the input Phi file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2.",
        "Default = 1.",
    ]
    parser.add_argument(
        "-pfb",
        "--phiFile-bin-ratio",
        type=float,
        default=1.0,
        dest="PHIFILE_BIN_RATIO",
        help="\n".join(help),
    )

    parser.add_argument(
        "-np",
        "--number-parallel-process",
        type=int,
        default=None,
        dest="PROCESSES",
        help="Number of parallel processes to use (shared mem parallelisation). Default = 1",
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
        args.OUT_DIR = os.path.dirname(args.LabFile.name)
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
        args.PREFIX = os.path.splitext(os.path.basename(args.LabFile.name))[0] + "-displaced"

    # if args.GREY_FILE is not None and args.THRESH == 0.5:
    # print("\n\nWARNING: You set a greyfile and your threshold is 0.5 -- I hope this is the right threshold for the greylevel image!\n\n")

    if args.LABEL_DILATE > 0 and args.GREY_FILE is None:
        print("\n\nWARNING: You are dilating labels but haven't loaded a grey image, everything's going to expand a lot!\n\n")

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-moveLabels "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script applies discretely measured deformation functions (Phi) coming from 'spam-ddic' to a labelled image, "
        + "thus generating the deformed labelled image.\n\nWarning: since we're moving labels, "
        + "nearest neighbour interpolation must be used, and thus the shapes of the labels will be slightly damaged",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with helper function
    args = moveLabelsParser(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-moveLabels")
    
    if args.RETURN_STATUS_THRESHOLD is None:
        DVC = spam.helpers.readCorrelationTSV(args.TSVFile.name, readConvergence=False)
        RS = None
    else:
        DVC = spam.helpers.readCorrelationTSV(args.TSVFile.name, readConvergence=True)
        RS = DVC["returnStatus"]

    # Read labelled image
    lab = tifffile.imread(args.LabFile.name)

     # Load images 
    if args.LAZYLOAD:
        try:
            lab = tifffile.memmap(args.LabFile.name)
        except:
            print("\nmoveLabels: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        lab = tifffile.imread(args.LabFile.name)

    labOut = spam.label.moveLabels(
        lab,
        DVC["PhiField"],
        returnStatus=RS,
        margin=args.MARGIN,
        PhiCOM=args.PHICOM,
        threshold=args.THRESH,
        labelDilate=args.LABEL_DILATE,
        nProcesses=args.PROCESSES,
    )

    print("\nSaving labelled image with displaced grains...", end="")
    tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + ".tif", labOut.astype(lab.dtype))
    print("done")
