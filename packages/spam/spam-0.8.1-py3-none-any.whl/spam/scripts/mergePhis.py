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

numpy.seterr(all="ignore")
os.environ["OPENBLAS_NUM_THREADS"] = "1"


def mergeTSVParser(parser):

    parser.add_argument(
        "totalTSVFile",
        metavar="totalTSVFile",
        type=argparse.FileType("r"),
        help="Path to total TSV file",
    )

    parser.add_argument(
        "incrementalTSVFile",
        metavar="incrementalTSVFile",
        type=argparse.FileType("r"),
        help="Path to incremental TSV file",
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
        help="Prefix for output TSV file (without extension). Default is basename of input files",
    )

    parser.add_argument(
        "-rst",
        "--return-status-threshold",
        type=int,
        default=2,
        dest="RETURN_STATUS_THRESHOLD",
        help="Lowest return status value to preserve in input PhiField. Default = 2",
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
        "-np",
        "--number-of-processes",
        default=None,
        type=int,
        dest="PROCESSES",
        help="Number of parallel processes to use. Default = multiprocessing.cpu_count()",
    )

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.totalTSVFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.totalTSVFile.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.totalTSVFile.name))[0] + "-" + os.path.splitext(os.path.basename(args.incrementalTSVFile.name))[0]

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-mergePhis "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script merges a total DVC (step n -> step m) and an incremental TSV (step m -> step m+1), resulting on a new total TSV file (step n -> step m+1)."
        + "The input TSV can come from a registration (single line), DDIC or LDIC."
        + "\n[WARNING]: The operation is non-commutative. Displacement and rotations need to be multiplied in, "
        + "the correct order. The first argument should be the total TSV, while the second argument should be the incremental TSV.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with helper function
    args = mergeTSVParser(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    print("")
    spam.helpers.displaySettings(args, "spam-mergePhis")
    print("")

    # 1. Read the TSV and pre-process

    incrementalTSV = spam.helpers.readCorrelationTSV(args.incrementalTSVFile.name, readConvergence=True, readPixelSearchCC=True, readError=True, readLabelDilate=True, verbose=False)
    if incrementalTSV is None:
        print(f"\tERROR: Failed to read your incremental TSV file {args.incrementalTSVFile.name}. Exit()\n")
        exit()

    totalTSV = spam.helpers.readCorrelationTSV(args.totalTSVFile.name, readConvergence=True, readPixelSearchCC=True, readError=True, readLabelDilate=True, verbose=False)
    if totalTSV is None:
        print(f"\tERROR: Failed to read your total TSV file {args.totalTSVFile.name}. Exit()\n")
        exit()

    # Check if it a single single TSV, discrete or gridded field
    singleTSV = False
    discrete = False
    if totalTSV["fieldCoords"].shape[0] == 1:
        singleTSV = True
    else:
        if totalTSV["numberOfLabels"] != 0:
            discrete = True

    # Solve for each type of input TSV
    if singleTSV:
        # Check that we have the same number of nodes on both files
        if incrementalTSV["PhiField"].shape != totalTSV["PhiField"].shape:
            print("\tERROR: The number of nodes on the TSV files do not match. Exit()\n")
            exit(1)

        # Initialise variable for new Phi matrix
        newPhi = numpy.zeros_like(totalTSV["PhiField"])

        # Multiplication of Phi matrices in the *right* order
        for i in range(newPhi.shape[0]):
            newPhi[i, :, :] = numpy.dot(incrementalTSV["PhiField"][i], totalTSV["PhiField"][i])

        # Done, now save the output TSV

        # Save
        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\treturnStatus\terror\tdeltaPhiNorm\titerations"
        outMatrix = numpy.array(
            [
                [1],
                totalTSV["fieldCoords"][:, 0],
                totalTSV["fieldCoords"][:, 1],
                totalTSV["fieldCoords"][:, 2],
                newPhi[:, 0, 0],
                newPhi[:, 0, 1],
                newPhi[:, 0, 2],
                newPhi[:, 0, 3],
                newPhi[:, 1, 0],
                newPhi[:, 1, 1],
                newPhi[:, 1, 2],
                newPhi[:, 1, 3],
                newPhi[:, 2, 0],
                newPhi[:, 2, 1],
                newPhi[:, 2, 2],
                newPhi[:, 2, 3],
                [1],
                [0],
                [0],
                [0],
            ]
        ).T

        numpy.savetxt(args.OUT_DIR + "/" + args.PREFIX + "-merge.tsv", outMatrix, fmt="%.7f", delimiter="\t", newline="\n", comments="", header=TSVheader)

    elif discrete:
        # The input TSV are from DDIC

        # Check that we have the same number of particles on both files
        if incrementalTSV["PhiField"].shape != totalTSV["PhiField"].shape:
            print("\tERROR: The number of particles on the TSV files do not match. Exit()\n")
            exit(1)
        # Determine the number of labels
        numberOfLabels = incrementalTSV["PhiField"].shape[0]

        # TODO: Check that all the particles converged! args.RETURN_STATUS_THRESHOLD

        # Check that the deformed positions of the particles from totalTSV match those of incrementalTSV
        for i in range(1, numberOfLabels):
            # Get the coordinates
            coordInc = incrementalTSV["fieldCoords"][i]
            coordTotal = totalTSV["fieldCoords"][i]
            dispTotal = totalTSV["PhiField"][i][:-1, -1]
            coordTotalDef = coordTotal + dispTotal
            if not numpy.allclose(coordInc, coordTotalDef, atol=1):
                print(
                    "\tERROR: The center of the particles "
                    + str(i)
                    + " in both TSV files are not within 1px. Perhaps there is a different labeling system, or the TSV files are not in the correct order. Exit()\n"
                )
                exit(1)

        # Initialise variable for new Phi matrix
        newPhi = numpy.zeros_like(totalTSV["PhiField"])

        # Multiplication of Phi matrices in the *right* order
        for i in range(newPhi.shape[0]):
            newPhi[i, :, :] = numpy.dot(incrementalTSV["PhiField"][i], totalTSV["PhiField"][i])

        # Done, now save the output TSV
        outMatrix = numpy.array(
            [
                numpy.array(range(numberOfLabels)),
                totalTSV["fieldCoords"][:, 0],
                totalTSV["fieldCoords"][:, 1],
                totalTSV["fieldCoords"][:, 2],
                newPhi[:, 0, 3],
                newPhi[:, 1, 3],
                newPhi[:, 2, 3],
                newPhi[:, 0, 0],
                newPhi[:, 0, 1],
                newPhi[:, 0, 2],
                newPhi[:, 1, 0],
                newPhi[:, 1, 1],
                newPhi[:, 1, 2],
                newPhi[:, 2, 0],
                newPhi[:, 2, 1],
                newPhi[:, 2, 2],
                numpy.zeros_like(totalTSV["pixelSearchCC"]),
                numpy.zeros_like(totalTSV["error"]),
                numpy.zeros_like(totalTSV["iterations"]),
                numpy.zeros_like(totalTSV["returnStatus"]) + 1.0,
                numpy.zeros_like(totalTSV["deltaPhiNorm"]),
                numpy.zeros_like(totalTSV["LabelDilate"]),
            ]
        ).T

        numpy.savetxt(
            args.OUT_DIR + "/" + args.PREFIX + "-merge.tsv",
            outMatrix,
            fmt="%.7f",
            delimiter="\t",
            newline="\n",
            comments="",
            header="Label\tZpos\tYpos\tXpos\t"
            + "Zdisp\tYdisp\tXdisp\t"
            + "Fzz\tFzy\tFzx\t"
            + "Fyz\tFyy\tFyx\t"
            + "Fxz\tFxy\tFxx\t"
            + "PSCC\terror\titerations\treturnStatus\tdeltaPhiNorm\tLabelDilate",
        )

        # TODO: ADD VTK!
    else:
        # Grid TSV

        # Check that we have the same number of nodes on both files
        if incrementalTSV["PhiField"].shape != totalTSV["PhiField"].shape:
            print("\tERROR: The number of nodes on the TSV files do not match. Exit()\n")
            exit(1)

        # 1. Deform the coordinates of the total totalTSV
        totalCoordHom = numpy.ones((totalTSV["fieldCoords"].shape[0], 4))
        totalCoordHom[:, :3] = totalTSV["fieldCoords"]
        # Apply the Phi to each of them
        totalDefCoord = numpy.zeros_like(totalCoordHom)
        # Loop
        for i in range(totalDefCoord.shape[0]):
            totalDefCoord[i] = numpy.dot(totalTSV["PhiField"][i], totalCoordHom[i])
        totalDefCoord = totalDefCoord[:, :3]  # undo the homogeneous

        # 2. Interpolate the incremental Phi field onto the new deformed coordinates

        intermediateNumberOfNodes = totalDefCoord.shape[0]
        intermediatePhiField = numpy.zeros((intermediateNumberOfNodes, 4, 4))
        # Interpolate these?
        pixelSearchCC = numpy.zeros((intermediateNumberOfNodes), dtype=float)
        error = numpy.zeros((intermediateNumberOfNodes), dtype=float)
        returnStatus = numpy.ones((intermediateNumberOfNodes), dtype=int)
        deltaPhiNorm = numpy.ones((intermediateNumberOfNodes), dtype=int)
        iterations = numpy.ones((intermediateNumberOfNodes), dtype=int)
        # Filter the incremental Phi field by getting only the converged nodes
        goodIncrementalPointsMask = numpy.where(incrementalTSV["returnStatus"] >= args.RETURN_STATUS_THRESHOLD)[0]
        goodIncrementalNodePositions = incrementalTSV["fieldCoords"][goodIncrementalPointsMask]
        goodIncrementalPhiField = incrementalTSV["PhiField"][goodIncrementalPointsMask]

        # Check neighbour inputs, either args.NEIGHBOUR_RADIUS or args.NUMBER_OF_NEIGHBOURS should be set.
        if args.NEIGHBOUR_RADIUS is not None and args.NUMBER_OF_NEIGHBOURS is not None:
            print("Both number of neighbours and neighbour radius are set, I'm taking the radius and ignoring the number of neighbours")
            args.NUMBER_OF_NEIGHBOURS = None
        # Neither are set... compute a reasonable default
        if args.NEIGHBOUR_RADIUS is None and args.NUMBER_OF_NEIGHBOURS is None:
            # Compute the node spacing of the grid
            nodeSpacingTotal = numpy.mean(totalTSV["fieldCoords"][0])
            nodeSpacingIncremental = numpy.mean(incrementalTSV["fieldCoords"][0])
            # We should use the distance of the grid with the maximum node spacing to interpolate into the grid with smaller node spacing.
            args.NEIGHBOUR_RADIUS = 2 * int(max(numpy.mean(nodeSpacingTotal), numpy.mean(nodeSpacingIncremental)) // 1)
            print(f"Neither number of neighbours nor neighbour distance set, using default distance of 2*mean(NS) = {args.NEIGHBOUR_RADIUS}")
        # Interpolate the field
        intermediatePhiField = spam.DIC.interpolatePhiField(
            goodIncrementalNodePositions,
            goodIncrementalPhiField,
            totalDefCoord,
            nNeighbours=args.NUMBER_OF_NEIGHBOURS,
            neighbourRadius=args.NEIGHBOUR_RADIUS,
            interpolateF="all",
            nProcesses=args.PROCESSES,
        )

        # 3. Multiply the total PhiField and the intermediatePhiField

        # Initialise variable for new Phi matrix
        newPhi = numpy.zeros_like(totalTSV["PhiField"])
        # Multiplication of Phi matrices in the *right* order
        for i in range(newPhi.shape[0]):
            newPhi[i, :, :] = numpy.dot(intermediatePhiField[i], totalTSV["PhiField"][i])

        # Done, now save the output TSV

        # Save
        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tFzz\tFzy\tFzx\tZdisp\tFyz\tFyy\tFyx\tYdisp\tFxz\tFxy\tFxx\tXdisp\tpixelSearchCC\treturnStatus\terror\tdeltaPhiNorm\titerations"
        outMatrix = numpy.array(
            [
                numpy.array(range(intermediateNumberOfNodes)),
                totalTSV["fieldCoords"][:, 0],
                totalTSV["fieldCoords"][:, 1],
                totalTSV["fieldCoords"][:, 2],
                newPhi[:, 0, 0],
                newPhi[:, 0, 1],
                newPhi[:, 0, 2],
                newPhi[:, 0, 3],
                newPhi[:, 1, 0],
                newPhi[:, 1, 1],
                newPhi[:, 1, 2],
                newPhi[:, 1, 3],
                newPhi[:, 2, 0],
                newPhi[:, 2, 1],
                newPhi[:, 2, 2],
                newPhi[:, 2, 3],
                pixelSearchCC,
                returnStatus,
                error,
                deltaPhiNorm,
                iterations,
            ]
        ).T

        numpy.savetxt(
            args.OUT_DIR + "/" + args.PREFIX + "-merge.tsv",
            outMatrix,
            fmt="%.7f",
            delimiter="\t",
            newline="\n",
            comments="",
            header=TSVheader,
        )

        # TODO: ADD VTK!
