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
Based on a unique auxiliary mesh with periodic boundary condtions on opposite
faces, this script creates a global mesh by copying and translating the
auxiliary mesh in the z, y, and x directions, thus creating conforming
surfaces.
The script creates a single hdf5 file with all the mesh and, optionally, msh
and vtk files for each mesh.

$ spam-mesh-subdomains -cube 0 1 0 1 0 1 -lc 0.1 -r 2 3 4 -v 1 -vtk -gui
"""
import argparse
import logging
import gmsh
import h5py
import numpy
import spam.helpers
import spam.mesh

numpy.seterr(all="ignore")


def meshSubdomains(parser):
    #  mesh type: CUBE
    help = [
        "Origin and extent of the auxiliary mesh in zyx.",
    ]
    parser.add_argument(
        "-cube",
        nargs=6,
        type=float,
        # default=[0., 1., 0., 1., 0., 1.],
        metavar=("oz", "lz", "oy", "ly", "ox", "lx"),
        dest="MESH_TYPE_CUBOID",
        help="\n".join(help),
    )

    #  mesh type: CUBE
    help = [
        "Number of auxiliary meshes in zyx to build the global.",
        "Must be at least 1 1 1.",
    ]
    parser.add_argument(
        "-r",
        nargs=3,
        type=float,
        # default=[0., 1., 0., 1., 0., 1.],
        metavar=("nz", "ny", "nx"),
        dest="MESH_ROWS",
        help="\n".join(help),
    )

    #  characteristic length
    help = [
        "Characteristic length of auxiliary and global meshes.",
    ]
    parser.add_argument(
        "-lc1",
        type=float,
        # default=1.,
        metavar="lc",
        dest="CHARACTERISTIC_LENGTH_1",
        help="\n".join(help),
    )

    #  characteristic length
    help = [
        "Characteristic length of the patch mesh.",
        "If not set, the patches are not created.",
    ]
    parser.add_argument(
        "-lc2",
        type=float,
        # default=1.,
        metavar="lc",
        dest="CHARACTERISTIC_LENGTH_2",
        help="\n".join(help),
    )

    help = [
        "Prefix for output files (without extension, ie ./data/my-mesh).",
        "Default = spam-mesh.",
    ]
    parser.add_argument(
        "-pre",
        type=str,
        default=None,
        metavar="path/filename",
        dest="PREFIX",
        help="\n".join(help),
    )

    help = ["Create VTK outputs for each mesh.", "Default = False."]
    parser.add_argument("-vtk", action="store_true", dest="VTK", help="\n".join(help))

    help = ["Create MSH outputs for each mesh.", "Default = False."]
    parser.add_argument("-msh", action="store_true", dest="MSH", help="\n".join(help))

    help = [
        "Activate ascii output instead of binary (not suited for production).",
        "Default = False.",
    ]
    parser.add_argument("-ascii", action="store_true", dest="ASCII", help="\n".join(help))

    help = ["Launch gmsh graphical interface.", "Default = False."]
    parser.add_argument("-gui", action="store_true", dest="GUI", help="\n".join(help))

    help = [
        "Sets gmsh verbosity (from 0 to 5).",
        "Default = 0.",
    ]
    parser.add_argument(
        "-v",
        type=int,
        default=0,
        metavar="verbosity",
        dest="VERBOSITY",
        help="\n".join(help),
    )

    args = parser.parse_args()

    # MAKE TESTS

    # test if mesh type
    if not any([args.MESH_TYPE_CUBOID]):
        print("WARNING: you need to enter at least one mesh type: --createCuboid, ...")
        exit()

    # test cuboid geometry:
    if args.MESH_TYPE_CUBOID:
        for i, x in zip(range(3), "zyx"):
            if args.MESH_TYPE_CUBOID[2 * i] >= args.MESH_TYPE_CUBOID[2 * i + 1]:
                print(f"WARNING: wrong cuboid geometry in direction {x}: start >= stop ({args.MESH_TYPE_CUBOID[2 * i]} >= {args.MESH_TYPE_CUBOID[2 * i + 1]})")
                exit()

    # needs lc
    if not args.CHARACTERISTIC_LENGTH_1:
        print("WARNING: you need to enter a characteristic length (maybe to a 1/10 of the mesh size)")
        exit()

    # needs translation
    if not args.MESH_ROWS:
        print("WARNING: you need to enter number of rows of auxiliary meshes (-r 2 1 1)")
        exit()

    # cast to int
    args.MESH_ROWS = [int(r) for r in args.MESH_ROWS]
    # check at least 1
    if not all([r > 0 for r in args.MESH_ROWS]):
        print("WARNING: number of rows must be strictly positif")
        exit()

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = "spam-mesh"
    args.PREFIX += f'-{"x".join([str(r) for r in args.MESH_ROWS])}'
    args.PREFIX += f"-lc{args.CHARACTERISTIC_LENGTH_1}"
    if args.CHARACTERISTIC_LENGTH_2:
        args.PREFIX += f"-{args.CHARACTERISTIC_LENGTH_2}"

    return args


def script():
    # Define argument parser object
    doc = [
        spam.helpers.optionsParser.GLPv3descriptionHeader,
        "Based on a unique auxiliary mesh with periodic boundary condtions on",
        "opposite faces, this script creates a global mesh by copying and",
        "translating the auxiliary mesh in the z, y, and x directions, thus",
        "creating conforming surfaces.",
        "The script creates a single hdf5 file with all the mesh and,",
        "optionally, msh and vtk files for each mesh.",
    ]
    parser = argparse.ArgumentParser(description="\n".join(doc), formatter_class=argparse.RawTextHelpFormatter)

    # Parse arguments with external helper function
    args = meshSubdomains(parser)

    if args.MESH_TYPE_CUBOID:
        origin = [
            args.MESH_TYPE_CUBOID[0],
            args.MESH_TYPE_CUBOID[2],
            args.MESH_TYPE_CUBOID[4],
        ]
        lengths = [
            # args.MESH_TYPE_CUBOID[1] - origin[0],
            # args.MESH_TYPE_CUBOID[3] - origin[1],
            # args.MESH_TYPE_CUBOID[5] - origin[2]
            args.MESH_TYPE_CUBOID[1],
            args.MESH_TYPE_CUBOID[3],
            args.MESH_TYPE_CUBOID[5],
        ]

        # shortcuts
        lz, ly, lx = lengths
        oz, oy, ox = origin
        nz, ny, nx = args.MESH_ROWS
        lc1 = args.CHARACTERISTIC_LENGTH_1
        lc2 = args.CHARACTERISTIC_LENGTH_2
        prefix = args.PREFIX
        vtkFile = prefix if args.VTK else None
        mshFile = prefix if args.MSH else None
        binary = not args.ASCII
        verbosity = args.VERBOSITY
        gui = args.GUI

    else:
        raise NotImplementedError("Only cuboids are currently implemented.")

    # logging level
    logging.basicConfig(
        format="[%(asctime)s spam-mesh-subdomain %(levelname)8s] %(message)s",
        level=logging.DEBUG if verbosity else logging.INFO,
    )

    argsDict = vars(args)
    for key in sorted(argsDict):
        logging.info(f"Settings {key}: {argsDict[key]}")

    # HELPER FUNCTIONS
    # compute offsets of nodes / elements and entities
    # used to copy mesh
    def get_tag_offets(m, tag_offets=None):
        """Helper function to compute max tags of a mesh"""
        if tag_offets is None:
            tag_offets = {"nodes": 0, "elements": 0, "entities": {0: 0, 1: 0, 2: 0, 3: 0}}

        for e in m:
            tag_offets["nodes"] = max(tag_offets["nodes"], max(m[e][1][0]))
            tag_offets["elements"] = max(tag_offets["elements"], max(m[e][2][1][0]))
            tag_offets["entities"][e[0]] = max(tag_offets["entities"][e[0]], e[1])

        return tag_offets

    # get mesh nodes / elements and entities
    def get_mesh_data(max_dim=3):
        """Helper function to get gmsh mesh data"""
        m = {}
        for e in gmsh.model.getEntities():
            if e[0] <= max_dim:
                bnd = gmsh.model.getBoundary([e])
                nod = gmsh.model.mesh.getNodes(e[0], e[1])
                ele = gmsh.model.mesh.getElements(e[0], e[1])
                m[e] = (bnd, nod, ele)

        return m

    # transform the mesh and create new discrete entities to store it
    def transform(m, translation, tag_offset=None):
        """Helper fonction to translate gmsh mesh data with proper offset"""
        # get tag offsets
        if tag_offset is None:
            o = get_tag_offets(m)
        else:
            # get initial mesh offsets
            o = get_tag_offets(m)
            o["nodes"] = int(tag_offset * o["nodes"])
            o["elements"] = int(tag_offset * o["elements"])
            for k, v in o["entities"].items():
                o["entities"][k] = int(tag_offset * v)

        for e in sorted(m):
            # print(e, m[e][0])
            bnd = [numpy.sign(b[1]) * (abs(b[1]) + o["entities"][e[0]]) for b in m[e][0]]
            # print(e[0],  e[1] + offset_e, bnd)
            gmsh.model.addDiscreteEntity(e[0], e[1] + o["entities"][e[0]], bnd)

            coord = []
            for i in range(0, len(m[e][1][1]), 3):
                x = m[e][1][1][i + 0] + translation[0]
                y = m[e][1][1][i + 1] + translation[1]
                z = m[e][1][1][i + 2] + translation[2]
                coord.append(x)
                coord.append(y)
                coord.append(z)

            gmsh.model.mesh.addNodes(e[0], e[1] + o["entities"][e[0]], m[e][1][0] + o["nodes"], coord)

            if len(bnd) == 6:
                gmsh.model.mesh.addElements(
                    e[0],
                    e[1] + o["entities"][e[0]],
                    m[e][2][0],
                    [t + o["elements"] for t in m[e][2][1]],
                    [n + o["nodes"] for n in m[e][2][2]],
                )

    # format a translation (for periodicity)
    def tr(t):
        phi = [1, 0, 0, t[0], 0, 1, 0, t[1], 0, 0, 1, t[2], 0, 0, 0, 1]
        return phi

    # initialize gmsh
    gmsh.initialize()

    # STEP 1. create the auxiliary mesh
    logging.info("STEP 1. Create inital generic auxiliary mesh")
    gmsh.model.add("aux")

    # set general options
    gmsh.option.setNumber("General.Verbosity", verbosity)
    gmsh.option.setNumber("Mesh.Binary", binary)

    # mesh options
    gmsh.option.setNumber("Mesh.Algorithm", 1)  # is the delaunay one (it's the gmsh default)
    gmsh.option.setNumber("Mesh.Optimize", True)
    gmsh.option.setNumber("Mesh.OptimizeNetgen", True)

    # create cube geometry
    gmsh.model.occ.addBox(ox, oy, oz, lx, ly, lz)  # create cube
    gmsh.model.occ.synchronize()

    # set characteristic length (from nodes -> getEntities(0))
    gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc1)
    gmsh.model.occ.synchronize()

    # set periodicity
    # surface -> dim=2, surface 2 set as surface 1 based on translation lx 0 0
    gmsh.model.mesh.setPeriodic(2, [2], [1], tr([lx, 0, 0]))
    gmsh.model.mesh.setPeriodic(2, [4], [3], tr([0, ly, 0]))
    gmsh.model.mesh.setPeriodic(2, [6], [5], tr([0, 0, lz]))
    gmsh.model.occ.synchronize()

    # generate auxiliary mesh
    gmsh.model.mesh.generate(3)

    # get auxiliary mesh data
    aux = get_mesh_data()

    # Remove generic auxiliary model (we just keep the mesh data)
    # It will be rebuild in the coming loop
    gmsh.model.remove()

    if lc2:
        logging.info("STEP 2. Create inital generic patch mesh")
        # STEP 2. create the pacth mesh
        gmsh.model.add("patch")

        # set general options
        gmsh.option.setNumber("General.Verbosity", verbosity)
        gmsh.option.setNumber("Mesh.Binary", binary)

        # mesh options
        gmsh.option.setNumber("Mesh.Algorithm", 1)  # is the delaunay one (it's the gmsh default)
        gmsh.option.setNumber("Mesh.Optimize", True)
        gmsh.option.setNumber("Mesh.OptimizeNetgen", True)

        # create cube geometry
        gmsh.model.occ.addBox(ox, oy, oz, lx, ly, lz)  # create cube
        gmsh.model.occ.synchronize()

        # set characteristic length (from nodes -> getEntities(0))
        gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc2)
        gmsh.model.occ.synchronize()

        # set periodicity
        # surface -> dim=2, surface 2 set as surface 1 based on translation lx 0 0
        gmsh.model.mesh.setPeriodic(2, [2], [1], tr([lx, 0, 0]))
        gmsh.model.mesh.setPeriodic(2, [4], [3], tr([0, ly, 0]))
        gmsh.model.mesh.setPeriodic(2, [6], [5], tr([0, 0, lz]))
        gmsh.model.occ.synchronize()

        # generate auxiliary mesh
        gmsh.model.mesh.generate(3)

        # get auxiliary mesh data
        patch = get_mesh_data()

        # Remove generic auxiliary model (we just keep the mesh data)
        # It will be rebuild in the coming loop
        gmsh.model.remove()

    else:
        logging.info("STEP 2. Create inital generic patch mesh (skip)")

    # STEP 3. Create global and auxialiaries
    logging.info("STEP 3. Create global and auxiliaries meshes")
    gmsh.model.add("global")

    tag_offset = 0  # keep track of number of mesh created
    for z in range(nz):
        for y in range(ny):
            for x in range(nx):
                # NOTE: iteration 0 0 0 creates the same aux as the inital

                # define the translation (n times the length of the cuboid)
                translation = [x * lx, y * ly, z * lz]
                p = 100 * (tag_offset + 1) / (nz * ny * nx)
                t = [f"{str(_):>6}" for _ in translation]
                logging.debug(f'Translate mesh {" ".join(t)} ({p:03.0f}%)')

                # handle the global model
                gmsh.model.setCurrent("global")
                transform(aux, translation, tag_offset=tag_offset)

                # create auxiliary
                gmsh.model.add(f"aux_{tag_offset:04d}")
                transform(aux, translation, tag_offset=0)

                # create patch
                if lc2:
                    gmsh.model.add(f"patch_{tag_offset:04d}")
                    transform(patch, translation, tag_offset=0)

                # increment translation
                tag_offset += 1

    # remove duplicate nodes of the global mesh
    logging.info("STEP 4. Remove duplicate nodes")
    gmsh.model.setCurrent("global")
    gmsh.model.mesh.removeDuplicateNodes()
    # gmsh.model.occ.synchronize()

    # run GUI
    if gui:
        gmsh.model.setCurrent("global")
        gmsh.fltk.run()

    # generate outputs
    ext = [e for e in ["h5", "vtk" if vtkFile else None, "msh" if mshFile else None] if e]
    logging.info(f'STEP 5. Generate {"|".join(ext)} outputs ({prefix})')

    # output all meshes
    with h5py.File(f"{prefix}.h5", "w") as f_write:
        # write metadata to the hdf file
        for k, v in argsDict.items():
            try:
                f_write.attrs[k] = v
            except TypeError:
                f_write.attrs[k] = str(v)

        for i, model_name in enumerate(gmsh.model.list()):
            if not model_name:
                continue

            # set model
            p = 100 * i / (len(gmsh.model.list()) - 1)
            logging.debug(f"Generate outputs {model_name:>10} ({p:03.0f}%)")
            gmsh.model.setCurrent(model_name)
            if vtkFile:
                gmsh.write(f"{prefix}-{model_name}.vtk")
            if mshFile:
                gmsh.write(f"{prefix}-{model_name}.msh")

            points, connectivity = spam.mesh.gmshToSpam(
                gmsh.model.mesh.getElementsByType(4),
                gmsh.model.mesh.getNodesByElementType(4),
            )

            # write dataset in hdf5 file
            datasets = (
                (f"{model_name}-points", points.astype("<f4")),
                (f"{model_name}-connectivity", connectivity.astype("<u4")),
            )
            for name, data in datasets:
                dset = f_write.create_dataset(name, data=data)
                dset.attrs["model"] = model_name
                if model_name == "global":
                    dset.attrs["mesh-type"] = "global"
                    dset.attrs["mesh-id"] = 0
                else:
                    dset.attrs["mesh-type"] = model_name.split("_")[0]
                    dset.attrs["mesh-id"] = int(model_name.split("_")[1])

    # shut down gmsh
    gmsh.finalize()
