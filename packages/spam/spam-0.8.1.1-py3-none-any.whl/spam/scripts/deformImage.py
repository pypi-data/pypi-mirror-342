# This script deforms an image according to an input deformation field using SPAM functions
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
This script can be very useful for generating deformed images to calculate a residual field

The current implementation will mesh correlation points with tetrahedra and deform them with displacements,
this has the advantage of speed, but the interpolation of displacements is approximative.

We don't use the more accurate `spam.DIC.deformationFunction.applyPhiField` which is slow for large images
"""

import argparse
import multiprocessing
import os

import numpy
import spam.deformation
import spam.DIC
import spam.helpers
import spam.label
import spam.mesh
import tifffile

numpy.seterr(all="ignore")


def deformImageParser(parser):
    parser.add_argument(
        "inFile",
        metavar="inFile",
        type=argparse.FileType("r"),
        help="Path to TIFF file containing the image to deform",
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
        "-np",
        "--number-of-processes",
        default=None,
        type=int,
        dest="PROCESSES",
        help="In the case that -tet is not activated, Number of parallel processes to use. Default = multiprocessing.cpu_count()",
    )

    parser.add_argument(
        "-nn",
        "--number-of-neighbours",
        type=int,
        default=8,
        dest="NUMBER_OF_NEIGHBOURS",
        help="In the case that -tet is not activated, number of neighbours for field interpolation. Default = 8",
    )

    parser.add_argument(
        "-mf2",
        "--maskFile2",
        dest="MASK2",
        default=None,
        type=argparse.FileType("r"),
        help="In the case that -tet is not activated, Path to tiff file containing the mask of image 2 -- THIS IS THE DEFORMED STATE --\
              pixels not to interpolate should be == 0",
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
        "-disp",
        "-interpolateDisplacements",
        action="store_true",
        dest="INTERPOLATE_DISPLACEMENTS",
        help="In the case that -tet is not activated, force 'displacement interpolation' mode for each pixel instead of applying the neighbour's Phis to the pixel.",
    )

    parser.add_argument(
        "-tet",
        "-triangulation",
        "-mesh-transformation",
        action="store_true",
        dest="MESH_TRANSFORMATION",
        help="Use a tetrahedral mesh between measurement points to interpolate displacements? Very fast but approximate. Default off",
    )

    parser.add_argument(
        "-a",
        "-triangulation-alpha-value",
        type=float,
        default=0.0,
        dest="MESH_ALPHA",
        help="CGAL Alpha value for triangulation cleanup (negative = auto, zero = no cleanup, positive = userval). Default = 0",
    )

    parser.add_argument(
        "-cgs",
        action="store_true",
        dest="CORRECT_GREY_FOR_STRAIN",
        help="Only for field mode: Apply a correction to the greyvalues according to strain in tetrahedon?\
              For a dry sample, greyvalues of vacuum should be =0 (Stavropoulou et al. 2020 Frontiers Eq. 12 with mu_w=0). Default = False",
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
        "-rad",
        "--radius-limit",
        type=float,
        default=None,
        dest="RADIUS",
        help="Assume a sample which is a cylinder with the axis in the z-direction. Exclude points outside a given radius. Use Default = None",
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
        "-rr",
        action="store_true",
        dest="RIGID",
        help="Apply only rigid part of the registration?",
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

    if args.CORRECT_GREY_FOR_STRAIN and not args.MESH_TRANSFORMATION:
        print("spam-deformImage: the -cgs option is currently only implemented for a mesh transformation, so please specify -tet")
        exit()

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-deformImage "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This deforms our input image according to some measured kinematics.\n"
        + "If a registration is given, it is wholly applied, otherwise if a displacement"
        + "field is given, it is triangulated and the displacements are applied",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = deformImageParser(parser)

    if args.PROCESSES is None:
        args.PROCESSES = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-deformImage")
    
    # Read displacements file
    TSV = spam.helpers.readCorrelationTSV(args.PHIFILE.name, fieldBinRatio=args.PHIFILE_BIN_RATIO, readConvergence=True)

    # Load images 
    if args.LAZYLOAD:
        try:
            im = tifffile.memmap(args.inFile.name)
        except:
            print("\ndeformImage: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
            exit()
    else:
        im = tifffile.imread(args.inFile.name)

    # Detect unpadded 2D image:
    if len(im.shape) == 2:
        im = im[numpy.newaxis, ...]
        twoD = True
        if args.MESH_TRANSFORMATION:
            print("\nspam-deformImage: the -tet option is only implemented for a 3D image. Forcing per-pixel interpolation.")
            args.MESH_TRANSFORMATION = False
    else:
        twoD = False

    # in case of a registration (assuming it's applied in the middle of the volume)
    if TSV["PhiField"].shape[0] == 1:
        print(f"\nRegistration mode, applying Phi at {TSV['fieldCoords'][0]}")
        args.PREFIX += "-reg-def"

        Phi = TSV["PhiField"][0]
        if args.RIGID:
            PhiDecomposed = spam.deformation.decomposePhi(Phi)
            Phi = spam.deformation.computePhi({"t": PhiDecomposed["t"], "r": PhiDecomposed["r"]})
            print("Using only rigid part of the registration")
        if twoD:
            imdef = spam.DIC.applyPhiPython(im, Phi=Phi, PhiCentre=TSV["fieldCoords"][0])[0]
        else:
            imdef = spam.DIC.applyPhi(im, Phi=Phi, PhiCentre=TSV["fieldCoords"][0])

    else:
        # ### BIG SWITCH between meshTransformation and per-pixel displacement
        print("\nIn PhiField mode.")
        # Accept points based on return stat
        mask = TSV["returnStatus"] >= args.RETURN_STATUS_THRESHOLD
        print(f"\nspam-deformImage: excluding points based on return threshold < {args.RETURN_STATUS_THRESHOLD} (excluded {100*(1-numpy.mean(mask)):2.1f}%)")

        if args.RADIUS is not None:
            # Also exclude based on radius
            args.RADIUS
            y = TSV["fieldCoords"][:, 1].copy()
            y -= (im.shape[1] - 1) / 2.0
            x = TSV["fieldCoords"][:, 2].copy()
            x -= (im.shape[2] - 1) / 2.0
            r = numpy.sqrt(numpy.square(x) + numpy.square(y))
            mask[r > args.RADIUS] = False

        # print("Proportion of correlation points included {:0.0f}%".format(100*(mask.sum()/(len(mask)-1))))

        # update points
        points = TSV["fieldCoords"][mask]
        # update displacements
        disp = TSV["PhiField"][mask][:, 0:3, -1]
        print("\tnPoints = ", points.shape[0])

        if args.MESH_TRANSFORMATION:
            args.PREFIX += "-tetMesh-def"

            # 2019-12-10 EA and OS: triangulate in the deformed configuration
            conn = spam.mesh.triangulate(points + disp, alpha=args.MESH_ALPHA)
            print("\tnTets = ", conn.shape[0])

            # Let's make the tet image here, in case we want to recycle it for the cgs
            imTetLabel = spam.label.labelTetrahedra(im.shape, points + disp, conn, nThreads=args.PROCESSES)

            print("Interpolating image... ", end="")
            # 2019-12-10 EA and OS: look up pixels, remember im is the reference configuration that we are deforming
            imdef = spam.DIC.applyMeshTransformation(im, points, conn, disp, imTetLabel=imTetLabel, nThreads=args.PROCESSES)
            print("done")

            if args.CORRECT_GREY_FOR_STRAIN:
                print(
                    "Correcting greyvalues for strain, assuming that vacuum greylevel = 0.0",
                    end="",
                )
                # We're going to pre-deform the greylevels using the tetLabel as a mask
                volumesRef = spam.mesh.tetVolumes(points, conn)
                volumesDef = spam.mesh.tetVolumes(points + disp, conn)
                volStrain = volumesDef / volumesRef
                volStrain[volumesRef == 0] = 0.0
                correction = spam.label.convertLabelToFloat(imTetLabel, volStrain)
                imdef /= correction
                del correction
                print("done")
        else:
            # ### "Exact mode"
            print("Per-pixel displacement interpolation mode")
            if args.INTERPOLATE_DISPLACEMENTS:
                args.PREFIX += "-disp"
            args.PREFIX += "-def"
            if args.MASK2 is not None:
                print("\tLoading im2 mask")
                # Load images 
                if args.LAZYLOAD:
                    try:
                        imMaskDef = tifffile.memmap(args.MASK2.name) > 0
                    except:
                        print("\ndeformImage: Problem with tifffile.memmap. Most probably your image is not compatible with memory mapping. Remove -lazy (or --lazy-load) and try again. Exiting.")
                        exit()
                else:
                    imMaskDef = tifffile.imread(args.MASK2.name) > 0
                if len(imMaskDef.shape) == 2:
                    imMaskDef = imMaskDef[numpy.newaxis, ...]
            else:
                imMaskDef = None

            imdef = spam.DIC.applyPhiField(
                im,
                points,
                TSV["PhiField"][mask],
                imMaskDef=imMaskDef,
                nNeighbours=args.NUMBER_OF_NEIGHBOURS,
                interpolationOrder=args.INTERPOLATION_ORDER,
                nProcesses=args.PROCESSES,
                displacementMode="interpolate" if args.INTERPOLATE_DISPLACEMENTS else "applyPhi",
                verbose=True,
            )

    print("Saving deformed image:\n\t{}".format(args.OUT_DIR + "/" + args.PREFIX + ".tif"))
    tifffile.imwrite(args.OUT_DIR + "/" + args.PREFIX + ".tif", imdef.astype(im.dtype))
