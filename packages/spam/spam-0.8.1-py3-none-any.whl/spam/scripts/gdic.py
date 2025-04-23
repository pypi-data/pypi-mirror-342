# This python script (under development) performs Global Digital Image Correlation using SPAM functions
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

import h5py
import spam.deformation
import spam.DIC
import spam.helpers
import spam.helpers.optionsParser
import spam.mesh
import yaml

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import numpy

numpy.seterr(all="ignore")

import multiprocessing  # noqa: E402

import tifffile  # noqa: E402

try:
    multiprocessing.set_start_method("fork")
except RuntimeError:
    pass


def gdicParser(parser):
    parser.add_argument(
        "imFiles",
        nargs=2,
        type=argparse.FileType("r"),
        help="A space-separated list of two 3D greyscale tiff files to correlate, in order",
    )

    parser.add_argument(
        dest="meshFile",
        default=None,
        type=argparse.FileType("r"),
        help="Path to VTK file containing mesh data needed for the correlation (points, connectivity)",
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
        "-d",
        "--debug",
        action="store_true",
        dest="DEBUG_FILES",
        help="Output debug files during iterations? Default = False",
    )

    parser.add_argument(
        "-it",
        "--max-iterations",
        type=int,
        default=25,
        dest="MAX_ITERATIONS",
        help="Max iterations for global correlation. Default = 25",
    )

    parser.add_argument(
        "-cc",
        "--convergence-criterion",
        type=float,
        default=0.01,
        dest="CONVERGENCE_CRITERION",
        help="Displacement convergence criterion in pixels (norm of incremental displacements). Default = 0.01",
    )

    parser.add_argument(
        "-str",
        "--calculate-strain",
        action="store_true",
        dest="STRAIN",
        help="Calculate strain? This is added to the VTK output files",
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
        "-r",
        "--regularisation",
        dest="REGULARISATION_FILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to YAML file containing the regularisation parameters. Default = None (no regularisation)",
    )

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.imFiles[0].name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.imFiles[0].name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        f1 = os.path.splitext(os.path.basename(args.imFiles[0].name))[0]
        f2 = os.path.splitext(os.path.basename(args.imFiles[1].name))[0]
        args.PREFIX = f"{f1}-{f2}-GDIC"

    if type(args.MAX_ITERATIONS) == list:
        args.MAX_ITERATIONS = args.MAX_ITERATIONS[0]

    # parse regularisation
    if args.REGULARISATION_FILE:
        # Load regularisation parameters
        with args.REGULARISATION_FILE as stream:
            try:
                args.REGULARISATION = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    else:  # no regularisation file
        args.REGULARISATION = {}

    return args


def script():
    parser = argparse.ArgumentParser(
        description="spam-gdic "
        + spam.helpers.optionsParser.GLPv3descriptionHeader
        + "This BETA TEST script performs Global Digital Image Correlations between two 3D greyscale images."
        + "Displacements are solved as a global problems of nodal displacements on a mesh",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    args = gdicParser(parser)

    processes = multiprocessing.cpu_count()

    spam.helpers.displaySettings(args, "spam-gdic")
    
    # Load reference image
    im1 = tifffile.imread(args.imFiles[0].name).astype("<f4")
    im2 = tifffile.imread(args.imFiles[1].name).astype("<f4")

    #################################################
    # STEP 1: REQUIRED loading mesh from VTK file  #
    #################################################
    # load it and check that it has the labelled tet image in it
    # check that the labelled tet image is the SAME SIZE as im1 and im2 above
    # unpack mesh variables
    print(f"[spam-gdic] Loading H5 mesh file: {args.meshFile.name}")
    with h5py.File(args.meshFile.name, "r") as f:
        print(f"[spam-gdic]\t{f.filename}")

        if len(f.attrs):
            print("[spam-gdic]\tMetadata:")
            for k, v in f.attrs.items():
                print(f"[spam-gdic]\t\t{k}: {v}")

        for k, v in f.items():
            print(f"[spam-gdic]\tDataset: {k}")
            print(f"[spam-gdic]\t\ttype: {v.dtype}")
            print(f"[spam-gdic]\t\tshape: {v.maxshape}")
            if len(v.attrs):
                print("[spam-gdic]\t\tMetadata:")
                for k2, v2 in v.attrs.items():
                    print(f"\t\t\t{k2}: {v2}")

        points = f["mesh-points"][:]
        connectivity = f["mesh-connectivity"][:]
    print(f"[spam-gdic]\tPoints:       {points.shape}")
    print(f"[spam-gdic]\tConnectivity: {connectivity.shape}")

    #################################################
    # STEP 2: optional loading of Phi or PhiField  #
    #################################################

    # if Phi      -> spam.DIC.kinematics.applyRegistrationToPoints() to mesh points
    # if PhiField -> spam.DIC.kinematics.interpolatePhiField() to mesh points

    if args.PHIFILE is not None:
        PhiFromFile = spam.helpers.readCorrelationTSV(args.PHIFILE.name, fieldBinRatio=args.PHIFILE_BIN_RATIO)

        if PhiFromFile is None:
            print(f"[spam-gdic] Failed to read your TSV file passed with -pf {args.PHIFILE.name}")
            exit()

        # If the read Phi-file has only one line -- it's a single point registration!
        if PhiFromFile["fieldCoords"].shape[0] == 1:
            PhiInit = PhiFromFile["PhiField"][0]
            print(f"[spam-gdic] Reading registration from a file in binning {args.PHIFILE_BIN_RATIO}")

            decomposedPhiInit = spam.deformation.decomposePhi(PhiInit)
            print(f'[spam-gdic]\tTranslations (px) {decomposedPhiInit["t"]}')
            print(f'[spam-gdic]\tRotations (deg)   {decomposedPhiInit["r"]}')
            print(f'[spam-gdic]\tZoom              {decomposedPhiInit["z"]}')

            PhiField = spam.DIC.applyRegistrationToPoints(
                PhiInit.copy(),
                PhiFromFile["fieldCoords"][0],  # centre of the registration
                points,
                applyF="no",  # no need to copy F into PhiField, we'll discard it anyway
                nProcesses=processes,
                # verbose=True,
            )
            initialDisplacements = PhiField[:, 0:3, -1]

            del PhiField, PhiInit, PhiFromFile, decomposedPhiInit

        else:  # we have a Phi field and not a registration
            nNeighbours = 8
            print(f"[spam-gdic] Interpolating PhiField onto the mesh points (nNeighbours = {nNeighbours}).")
            PhiField = spam.DIC.interpolatePhiField(
                PhiFromFile["fieldCoords"],
                PhiFromFile["PhiField"],
                points,
                nNeighbours=nNeighbours,
                interpolateF="no",  # we only want displacements
                neighbourDistanceWeight="inverse",
                checkPointSurrounded=False,
                nProcesses=processes,
                verbose=True,
            )
            initialDisplacements = PhiField[:, 0:3, -1]

    else:
        initialDisplacements = numpy.zeros_like(points)

    if args.DEBUG_FILES and (initialDisplacements is not None):
        print("[spam-gdic] Plot intial displacements")
        spam.helpers.writeUnstructuredVTK(
            points,
            connectivity,
            pointData={"registration": initialDisplacements},
            fileName=f"{os.path.join(args.OUT_DIR, args.PREFIX)}-registration.vtk",
        )

    ############################
    # STEP 3: regularisation   #
    ############################
    if args.REGULARISATION:
        p = spam.DIC.regularisationParameters(args.REGULARISATION)
        labels = spam.DIC.surfaceLabels(points, p["surfaces"])
        regularisationMatrix, regularisationField = spam.DIC.regularisationMatrix(
            points, connectivity, p["young"], p["poisson"], ksiBulk=p["ksi"], dirichlet=p["dirichlet"], labels=labels, periods=p["periods"], voxelSize=p["voxel"]
        )
    else:
        regularisationMatrix = None
        regularisationField = None

    ################################
    # STEP 4: global correlation   #
    ################################
    displacements = spam.DIC.globalCorrelation(
        im1,
        im2,
        points,
        connectivity,
        regularisationMatrix=regularisationMatrix,
        regularisationField=regularisationField,
        initialDisplacements=initialDisplacements,
        maxIterations=args.MAX_ITERATIONS,
        convergenceCriterion=args.CONVERGENCE_CRITERION,
        debugFiles=args.DEBUG_FILES,
        prefix=os.path.join(args.OUT_DIR, args.PREFIX),
    )

    pointData = {"displacements": displacements, "registration": initialDisplacements, "fluctuations": numpy.subtract(displacements, initialDisplacements)}

    components = ["vol", "dev", "volss", "devss"]
    if args.STRAIN:
        print("[spam-gdic] Computing strains")
        Ffield = spam.deformation.FfieldBagi(points, connectivity, displacements)
        decomposedFfield = spam.deformation.decomposeFfield(Ffield, components)
        cellData = {c: decomposedFfield[c] for c in components}
    else:
        cellData = {}

    spam.helpers.writeUnstructuredVTK(
        points,
        connectivity,
        pointData=pointData,
        cellData=cellData,
        fileName=f"{os.path.join(args.OUT_DIR, args.PREFIX)}.vtk",
    )
