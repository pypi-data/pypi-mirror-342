"""
This python script computes a strain field from a displacement field defined on a regular grid (e.g., from spam-ldic) using SPAM functions
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
import os

import spam.deformation
import spam.DIC
import spam.helpers
import spam.mesh

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import multiprocessing  # noqa: E402

import numpy  # noqa: E402
import tifffile  # noqa: E402

try:
    multiprocessing.set_start_method("fork")
except RuntimeError:
    pass

numpy.seterr(all="ignore")


def regularStrainParser(parser):
    parser.add_argument(
        "inFile",
        metavar="inFile",
        type=argparse.FileType("r"),
        help="Path to TSV file containing the result of the correlation",
    )

    parser.add_argument(
        "-comp",
        "--strain-components",
        nargs="*",
        type=str,
        default=["vol", "dev"],
        dest="COMPONENTS",
        help="Selection of which strain components to save, options are:\
              vol (volumetric strain), dev (deviatoric strain), volss (volumetric strain in small strains), devss (deviatoric strain in small strains),\
              r (rotation vector), z (zoom vector), Up (principal strain vector), U (right-hand stretch tensor), e (strain tensor in small strains)",
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
        "-nomask",
        "--nomask",
        action="store_false",
        dest="MASK",
        help="Don't mask correlation points according to return status (use everything)",
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
        "-r",
        "--neighbourhood-radius-for-strain-calculation",
        type=float,
        default=1.5,
        dest="STRAIN_NEIGHBOUR_RADIUS",
        help="Radius (in units of nodeSpacing) inside which to select neighbours for displacement gradient calculation. Ignored if -cub is set. Default = 1.5",
    )

    parser.add_argument(
        "-cub",
        "-Q8",
        "--cubic-element",
        "--Q8",
        action="store_true",
        dest="Q8",
        help="Use Q8 element interpolation? More noisy and strain values not centred on displacement points",
    )

    parser.add_argument(
        "-raw",
        "--no-shape-function",
        action="store_true",
        dest="RAW",
        help="Just use F straight from the correlation windows instead of computing it from the displacement field.",
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

    parser.add_argument(
        "-vtkln",
        "--VTKleaveNANs",
        action="store_false",
        dest="VTKmaskNAN",
        help="Leave NaNs in VTK output? If this option is not set they are replaced with 0.0",
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
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0]

    if args.RAW and args.Q8:
        print("You can't ask for both F-from-correlation and F-from-Q8")
        exit()

    # Make sure at least one output format has been asked for
    if args.VTK + args.TIFF + args.TSV == 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV or TIFF          ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-regularStrain "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This script computes different components of strain, given a regularly-spaced displacement"
        + " field like that coming from spam-ldic. Both infinitesimal and finite strain frameworks"
        + " are implemented, and TSV, VTK and TIF output are possible",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # Parse arguments with external helper function
    args = regularStrainParser(parser)

    # Figure out processes if not passed
    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-regularStrain")

    print("\nspam-regularStrain: Loading data...")
    f = spam.helpers.readCorrelationTSV(args.inFile.name, readConvergence=args.MASK)

    # Get the dimensions and coordinates of the field
    dims = f["fieldDims"]
    fieldCoords = f["fieldCoords"]

    # Calculate node spacing for each direction
    # 2020-08-31 OS: safer calculation of node spacing
    nodeSpacing = numpy.array(
        [numpy.unique(fieldCoords[:, i])[1] - numpy.unique(fieldCoords[:, i])[0] if len(numpy.unique(fieldCoords[:, i])) > 1 else numpy.unique(fieldCoords[:, i])[0] for i in range(3)]
    )

    # Catch 2D case
    if dims[0] == 1:
        twoD = True
        print("spam-regularStrain: Detected 2D field")
    else:
        twoD = False

    dispFlat = f["PhiField"][:, :3, -1]

    # Check if a mask of points (based on return status of the correlation) is asked
    if args.MASK:
        mask = f["returnStatus"] < args.RETURN_STATUS_THRESHOLD
        print(f"\nspam-regularStrain: Excluding points based on return threshold < {args.RETURN_STATUS_THRESHOLD} (excluded {100*(1-numpy.mean(mask)):2.1f}%)")
        dispFlat[mask] = numpy.nan

    disp = dispFlat.reshape(dims[0], dims[1], dims[2], 3)

    print("\nspam-regularStrain: Computing F=I+du/dx")
    if args.Q8:
        Ffield = spam.deformation.FfieldRegularQ8(disp, nodeSpacing=nodeSpacing, nProcesses=args.PROCESSES, verbose=True)
    elif args.RAW:
        # Just take it straight form the file
        Ffield = f["PhiField"][:, :3, :3]
        if args.MASK:
            Ffield[mask] = numpy.nan
        Ffield = Ffield.reshape(dims[0], dims[1], dims[2], 3, 3)

    else:
        Ffield = spam.deformation.FfieldRegularGeers(disp, nodeSpacing=nodeSpacing, neighbourRadius=args.STRAIN_NEIGHBOUR_RADIUS, nProcesses=args.PROCESSES, verbose=True)

    # Now compute what's been asked for...
    print("\nspam-regularStrain: Decomposing F into ", args.COMPONENTS)
    decomposedFfield = spam.deformation.decomposeFfield(Ffield, args.COMPONENTS, twoD=twoD, nProcesses=args.PROCESSES, verbose=True)

    # Define base fileName
    if args.Q8:
        if twoD:
            fileNameBase = args.OUT_DIR + "/" + args.PREFIX + "-strain-Q4"
            mode = "Q4"
        else:
            fileNameBase = args.OUT_DIR + "/" + args.PREFIX + "-strain-Q8"
            mode = "Q8"
    elif args.RAW:
        fileNameBase = args.OUT_DIR + "/" + args.PREFIX + "-strain-raw"
        mode = "raw"
    else:
        fileNameBase = args.OUT_DIR + "/" + args.PREFIX + "-strain-Geers"
        mode = "Geers"

    # Save strain fields
    print("\nspam-regularStrain: Saving strain fields...")
    if args.TSV:

        # Positions for the centres of the Q8 elements are between the measurement points
        #   (so there is one number fewer compared to measurement points
        #   so we strip off last node points -- not Z ones in twoD for Q8 mode
        if args.Q8:
            if twoD:
                outputPositions = fieldCoords.copy().reshape(1, dims[1], dims[2], 3)[:, 0:-1, 0:-1, :]
            else:
                outputPositions = fieldCoords.copy().reshape(dims[0], dims[1], dims[2], 3)[0:-1, 0:-1, 0:-1, :]
            # Add a half-node spacing to the output field
            outputPositions[:, :, :, 0] += nodeSpacing[0] / 2.0
            outputPositions[:, :, :, 1] += nodeSpacing[1] / 2.0
            outputPositions[:, :, :, 2] += nodeSpacing[2] / 2.0
        else:
            # Positions for Geers and "raw" are the measurement points
            if twoD:
                outputPositions = fieldCoords.copy().reshape(1, dims[1], dims[2], 3)
            else:
                outputPositions = fieldCoords.copy().reshape(dims[0], dims[1], dims[2], 3)

        # Here we want to pass an Nx3 matrix of poitions:
        spam.helpers.writeStrainTSV(fileNameBase + ".tsv", outputPositions.reshape(-1, 3), decomposedFfield, firstColumn="StrainPointNumber")

    if args.TIFF:
        for component in args.COMPONENTS:
            axes = ["z", "y", "x"] if not twoD else ["y", "x"]

            if component == "vol" or component == "dev" or component == "volss" or component == "devss":
                tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-{}-{}.tif".format(component, mode), decomposedFfield[component].astype("<f4"))

            if component == "r" or component == "z" or component == "Up":
                if twoD:
                    for n, di in enumerate(axes, start=1):
                        tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-{}{}-{}.tif".format(component, di, mode), decomposedFfield[component][:, :, :, n].astype("<f4"))
                else:
                    for n, di in enumerate(axes):
                        tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-{}{}-{}.tif".format(component, di, mode), decomposedFfield[component][:, :, :, n].astype("<f4"))

            if component == "e" or component == "U":
                if twoD:
                    for n, di in enumerate(axes, start=1):
                        for m, dj in enumerate(axes, start=1):
                            if m >= n:
                                tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-{}{}{}-{}.tif".format(component, di, dj, mode), decomposedFfield[component][:, :, :, n, m].astype("<f4"))
                else:
                    for n, di in enumerate(axes):
                        for m, dj in enumerate(axes):
                            if m >= n:
                                tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + "-{}{}{}-{}.tif".format(component, di, dj, mode), decomposedFfield[component][:, :, :, n, m].astype("<f4"))

    if args.VTK:
        cellData = {}
        if not twoD:
            aspectRatio = nodeSpacing
        else:
            aspectRatio = [1, nodeSpacing[1], nodeSpacing[2]]

        # For geers strains are at the measurement points
        #   As per the displacements coming out of spam-ldic this will plot nicely if 2xHWS = NS
        if not args.Q8:
            origin = fieldCoords[0] - numpy.array(aspectRatio) / 2.0
        # Q8's centre is between measurement points, but corners fall on displacement points, obviously
        else:
            origin = fieldCoords[0]

        for component in args.COMPONENTS:
            tmp = decomposedFfield[component]
            if args.VTKmaskNAN:
                tmp[numpy.isnan(tmp)] = 0.0
            cellData[component] = tmp
        spam.helpers.writeStructuredVTK(origin=origin, aspectRatio=aspectRatio, cellData=cellData, fileName=fileNameBase + ".vtk")
