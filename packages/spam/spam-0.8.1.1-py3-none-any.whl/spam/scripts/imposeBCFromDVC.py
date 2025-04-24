#!/usr/bin/env python


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
import spam.helpers
import spam.mesh

numpy.seterr(all="ignore")


def BCFromDVCParser(parser):
    parser.add_argument(
        "-gmshFile",
        dest="GMSHFILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to gmsh file containing the FE mesh. Default = None",
    )

    parser.add_argument(
        "-vtkFile",
        dest="VTKFILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to vtk file containing the FE mesh. Default = None",
    )

    parser.add_argument(
        "-tsvFile",
        dest="TSVDVCFILE",
        default=None,
        type=argparse.FileType("r"),
        help="Path to tsv file containing the result of a correlation. Default = None",
    )

    parser.add_argument(
        "-mask",
        "--mask",
        action="store_true",
        dest="MASK",
        help="Mask correlation points according to return status",
    )

    parser.add_argument(
        "-pixSize",
        "--pixel-size",
        type=float,
        default=1.0,
        dest="PIXEL_SIZE",
        help="Physical size of a pixel (i.e. mm/px). Default = 1",
    )

    parser.add_argument(
        "-tol",
        "--tolerance",
        type=float,
        default=1e-6,
        dest="TOL",
        help="Numerical tolerance for floats. Default = 1e-6",
    )

    parser.add_argument(
        "-meshType",
        "--mesh-type",
        type=str,
        default="cube",
        dest="MESHTYPE",
        help="The type of the input mesh (i.e. cube, cylinder etc). Default = cube",
    )

    parser.add_argument(
        "-topBottom",
        "--top-bottom",
        action="store_true",
        dest="TOP_BOTTOM",
        help="Apply BC only on top-bottom surfaces (i.e. z=zmin, z=zmax)",
    )

    parser.add_argument(
        "-cylCentre",
        "--cylinder-centre",
        nargs=2,
        type=float,
        default=[0, 0],
        dest="CYLCENTRE",
        help="The cente of the cylinder [x, y]. Default =[0, 0]",
    )

    parser.add_argument(
        "-cylRadius",
        "--cylinder-radius",
        type=float,
        default=1.0,
        dest="CYLRADIUS",
        help="The radius of the cylinder. Default = 1",
    )

    parser.add_argument(
        "-ni",
        "--neighbours-for-interpolation",
        type=int,
        default=4,
        dest="NEIGHBOURS_INT",
        help="Neighbours for field interpolation. Default = 4",
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
        "-feapBC",
        "--feap-boundary-conditions",
        action="store_true",
        dest="FEAPBC",
        help="Write the boundary conditions in FEAP format. Default = True",
    )

    parser.add_argument(
        "-saveVTK",
        "--VTKout",
        action="store_true",
        dest="SAVE_VTK",
        help="Save the BC field as VTK. Default = True",
    )

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        try:
            args.OUT_DIR = os.path.dirname(args.GMSHFILE.name)
        except BaseException:
            try:
                args.OUT_DIR = os.path.dirname(args.VTKFILE.name)
            except BaseException:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                try:
                    args.DIR_out = os.path.dirname(args.GMSHFILE.name)
                except BaseException:
                    try:
                        args.DIR_out = os.path.dirname(args.VTKFILE.name)
                    except BaseException:
                        print("\n***You need to input an unstructured mesh. Exiting...***")

        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        try:
            args.PREFIX = os.path.splitext(os.path.basename(args.GMSHFILE.name))[0]
        except BaseException:
            try:
                args.DIR_out = os.path.dirname(args.VTKFILE.name)
            except BaseException:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser()

    # Parse arguments with external helper function
    args = BCFromDVCParser(parser)

    spam.helpers.displaySettings(args, "spam-imposeBCfromDVC")
    
    print("\n\nLoading data...")
    # Get the meshNodes
    if args.GMSHFILE is not None:
        import meshio

        print("Read gmsh file: {}".format(args.GMSHFILE.name))
        gmsh = meshio.read(args.GMSHFILE.name)
        meshNodes = numpy.zeros((gmsh.points.shape[0], 4))
        for i, node in enumerate(gmsh.points):
            meshNodes[i] = [i + 1, node[2], node[1], node[0]]  # zyx
    elif args.VTKFILE is not None:
        points, connectivity, _, _ = spam.helpers.readUnstructuredVTK(args.VTKFILE.name)
        meshNodes = numpy.zeros((points.shape[0], 4))
        for i, node in enumerate(points):
            meshNodes[i] = [i + 1, node[0], node[1], node[2]]  # zyx
    else:
        print("You need to input an unstructured mesh")
        exit()

    # Get dvc field
    if args.TSVDVCFILE is not None:
        dvcField = spam.helpers.readCorrelationTSV(args.TSVDVCFILE.name)
        fieldCoords = dvcField["fieldCoords"]
        fieldDisp = dvcField["Ffield"][:, :3, -1]
        mask = None
        if args.MASK:
            mask = numpy.ones(fieldCoords.shape[0])
            mask[numpy.where(dvcField["returnStatus"] < -4)] = 0
        dvcField = numpy.hstack((fieldCoords, fieldDisp))
    else:
        print("You need to input a dvc grid displacement")
        exit()

    print("\nGetting the boundary conditions...")
    # Get boundary conditions
    bc = spam.mesh.BCFieldFromDVCField(
        meshNodes,
        dvcField,
        mask=mask,
        pixelSize=args.PIXEL_SIZE,
        meshType=args.MESHTYPE,
        centre=args.CYLCENTRE,
        radius=args.CYLRADIUS,
        topBottom=args.TOP_BOTTOM,
        neighbours=args.NEIGHBOURS_INT,
        tol=args.TOL,
    )

    # write BC conditions in FEAP format
    if args.FEAPBC:
        feapBC = args.OUT_DIR + "/" + args.PREFIX + "Itail"
        with open(feapBC, "w") as f:
            f.write("\nBOUN\n")
            for d in bc:
                f.write("{:.0f}, 0, 1, 1, 1\n".format(d[0]))
            f.write("\nDISP\n")
            for d in bc:
                f.write("{:.0f}, 0, {:.6f}, {:.6f}, {:.6f}\n".format(d[0], d[6], d[5], d[4]))  # xyz
            f.write("\nPROP\n")
            for d in bc:
                f.write("{:.0f}, 0, 1, 1, 1\n".format(d[0]))
            f.write("\nEND\n")

    # save mesh with BC as vtk
    if args.SAVE_VTK:
        if not args.VTKFILE:
            points, connectivity, _, _ = spam.helpers.readUnstructuredVTK(args.GMSHFILE.name)
        nodeDisp = numpy.zeros((points.shape[0], 3))
        bc[:, 0] -= 1
        edgeNodes = bc[:, 0].astype(int).tolist()
        nodeDisp[edgeNodes] = bc[:, 4:]

        spam.helpers.writeUnstructuredVTK(points, connectivity, pointData={"BCdisp": nodeDisp}, fileName=args.OUT_DIR + "/" + args.PREFIX + ".vtk")
