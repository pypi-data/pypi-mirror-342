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
DOC MESH
"""
import argparse
import os

import h5py
import numpy
import spam.helpers
import spam.label
import spam.mesh

numpy.seterr(all="ignore")


def meshParser(parser):
    #  mesh type: CUBE
    parser.add_argument(
        "-cube",
        "--createCuboid",
        nargs=6,
        type=float,
        # default=[0., 1., 0., 1., 0., 1.],
        dest="MESH_TYPE_CUBOID",
        help="Start and stop of the cuboid edges in the three directions (zyx)",
    )

    #  mesh type: CYLINDER
    parser.add_argument(
        "-cylinder",
        "--createCylinder",
        nargs=5,
        type=float,
        dest="MESH_TYPE_CYLINDER",
        help="Y center, X center, radius, Z start and Z end.",
    )

    #  characteristic length
    parser.add_argument(
        "-lc",
        "--characteristicLength",
        type=float,
        # default=1.,
        dest="CHARACTERISTIC_LENGTH",
        help="Characteristic length of the elements of the mesh",
    )

    parser.add_argument(
        "-pre",
        "--prefix",
        type=str,
        default=None,
        dest="PREFIX",
        help="Prefix for output files (without extension). Default is basename `spam-mesh`",
    )

    parser.add_argument(
        "-od",
        "--out-dir",
        type=str,
        default="./",
        dest="OUT_DIR",
        help="Output directory",
    )

    # parser.add_argument('-vtk',
    #                     '--VTKout',
    #                     action="store_true",
    #                     dest='VTK',
    #                     help='Activate VTK output format. Default = False')

    parser.add_argument(
        "-h5",
        "--hdf5",
        action="store_true",
        dest="HDF5",
        help="Activate HDF5 output format. Default = False",
    )

    parser.add_argument(
        "-ascii",
        "--asciiOut",
        action="store_true",
        dest="ASCII",
        help="Activate ascii output (useful for debugging but takes more disk space). Default = False",
    )

    args = parser.parse_args()

    # MAKE TESTS

    # test if mesh type
    if not any([args.MESH_TYPE_CUBOID, args.MESH_TYPE_CYLINDER]):
        print("WARNING: you need to enter at least one mesh type: -cube, -cylinder")
        exit()

    # test cuboid geometry:
    if args.MESH_TYPE_CUBOID:
        for i, x in zip(range(3), "zyx"):
            if args.MESH_TYPE_CUBOID[2 * i] >= args.MESH_TYPE_CUBOID[2 * i + 1]:
                print(f"WARNING: wrong cuboid geometry in direction {x}: start >= stop ({args.MESH_TYPE_CUBOID[2 * i]} >= {args.MESH_TYPE_CUBOID[2 * i + 1]})")
                exit()

    # needs lc
    if not args.CHARACTERISTIC_LENGTH:
        print("WARNING: you need to enter a characteristic length (maybe to a 1/10 of the mesh size)")
        exit()

    # Check existence of output directory
    if not os.path.isdir(args.OUT_DIR):
        os.makedirs(args.OUT_DIR)

    # Output file name prefix
    if args.PREFIX is None:
        if args.MESH_TYPE_CUBOID:
            args.PREFIX = "cuboid-mesh"
        elif args.MESH_TYPE_CYLINDER:
            args.PREFIX = "cylinder-mesh"
        else:
            args.PREFIX = "spam-mesh"
    args.PREFIX += f"-lc{args.CHARACTERISTIC_LENGTH}"

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="[spam-mesh] " + spam.helpers.optionsParser.GLPv3descriptionHeader + "WRITE DOC MESH\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = meshParser(parser)
    #
    print("[spam-mesh] Current Settings:")
    argsDict = vars(args)
    for key in sorted(argsDict):
        print(f"\t{key}: {argsDict[key]}")

    # common carachteristics
    lc = args.CHARACTERISTIC_LENGTH
    outDir = args.OUT_DIR
    vtkFile = os.path.join(outDir, args.PREFIX)
    binary = not args.ASCII

    if args.MESH_TYPE_CUBOID:
        origin = [
            args.MESH_TYPE_CUBOID[0],
            args.MESH_TYPE_CUBOID[2],
            args.MESH_TYPE_CUBOID[4],
        ]
        lengths = [
            args.MESH_TYPE_CUBOID[1] - origin[0],
            args.MESH_TYPE_CUBOID[3] - origin[1],
            args.MESH_TYPE_CUBOID[5] - origin[2],
        ]

        # create mesh
        points, connectivity = spam.mesh.createCuboid(lengths, lc, origin=origin, vtkFile=vtkFile, binary=binary)

    if args.MESH_TYPE_CYLINDER:
        center = args.MESH_TYPE_CYLINDER[0:2]
        radius = args.MESH_TYPE_CYLINDER[2]
        height = args.MESH_TYPE_CYLINDER[4] - args.MESH_TYPE_CYLINDER[3]
        zOrigin = args.MESH_TYPE_CYLINDER[3]
        points, connectivity = spam.mesh.createCylinder(center, radius, height, lc, zOrigin=zOrigin, vtkFile=vtkFile, binary=binary)

    # output HDF5 if needed
    if args.HDF5:
        with h5py.File(f"{os.path.join(outDir, args.PREFIX)}.h5", "w") as f_write:
            # write metadata to the hdf file
            for k, v in argsDict.items():
                try:
                    f_write.attrs[k] = v
                except TypeError:
                    f_write.attrs[k] = str(v)

            # write data sets
            data_sets = [
                ("mesh-points", points.astype("<f4")),
                ("mesh-connectivity", connectivity.astype("<u4")),
            ]

            for name, data in data_sets:
                # create dataset
                dset = f_write.create_dataset(name, data=data)
                # write metadata to each dataset
                # dset.attrs["TYPE"] = name
                # for k, v in argsDict.items():
                #     dset.attrs[k] = str(v)
