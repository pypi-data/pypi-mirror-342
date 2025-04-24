# Library of SPAM functions for projecting morphological field onto tetrahedral
# meshes
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
    The ``spam.mesh.projection`` module offers a two functions that enables the construction of three dimensional unstructured meshes (four noded tetrahedra) that embbed heterogeneous data
    (namely, **subvolumes** and interface **orientation**) based on eihter:
        - the distance field of an **segmented images** (see ``spaM.filters.distanceField``),
        - ideal **geometrical objects** (see ``spam.filters.objects``).

    >>> import spam.mesh
    >>> spam.mesh.projectField(mesh, fields)
    >>> spam.mesh.projectObjects(mesh, objects)

    NOTE
    ----

        Objects array conventions:

            - Sphere: ``[radius, centerX, centerY, centerZ, phase]``
            - Cylinder: ``[radius, centerX, centerY, centerZ, directionX, directionY, directionZ, phase]``

        Distance field and orientation convention:

            - The distance fields inside connected components have positive values
            - The normal vectors are pointing outside (to negative values)
            - The subvolumes returned correspond to the outside (negative part)

"""

import numpy
from spambind.mesh.meshToolkit import projmorpho


def _refactor_mesh(mesh):
    """
    Helper private function for projection.
    Remove additional nodes and change connectivity matrix accordingly.
    """
    points = mesh["points"]
    cells = mesh["cells"]

    # DEBUG: Artificially add unused node
    # points = numpy.insert(points, 10, [-1.0,-1.0,-1.0], axis=0)
    # for i, node_number_x4 in enumerate(cells):
    #     for j, node_number in enumerate(node_number_x4):
    #         if cells[i, j] >= 10:
    #             cells[i, j] += 1

    # test if unused nodes
    cells_set = set(cells.ravel())  # ordered numbering in connectivity
    n_points_used = len(cells_set)

    if n_points_used != points.shape[0]:
        print("Deleting points before projection")

        # removing unused nodes
        points_to_delete = []
        n_deleted = 0
        for new, old in enumerate(cells_set):
            # check if holes in the connectivity matrix
            if new != old - n_deleted:
                points_to_delete.append(new + n_deleted)
                n_deleted += 1
                # print(new, old, n_deleted, old - n_deleted)
        points = numpy.delete(points, points_to_delete, axis=0)

        print("Renumbering connectivity matrix")
        # renumbering connectivity matrix accordingly
        new_node_numbering = {old: new + 1 for new, old in enumerate(cells_set)}
        for i, node_number_x4 in enumerate(cells):
            for j, node_number in enumerate(node_number_x4):
                if new_node_numbering[cells[i, j]] != cells[i, j]:
                    cells[i, j] = new_node_numbering[cells[i, j]]
    del cells_set

    # check if cell number start by 1 or 0
    if cells.min() == 0:
        print("Shift connectivity by 1 to start at 1")
        cells += 1

    return points, cells


def projectObjects(
    mesh,
    objects,
    analyticalOrientation=True,
    cutoff=1e-6,
    writeConnectivity=None,
    vtkMesh=False,
):
    """
    This function project a set of objects onto an unstructured mesh.
    Each objects can be attributed a phase.

    Parameters
    ----------
        mesh: dict
            Dictionary containing points coordinates and mesh connectivity.

            .. code-block:: python

                mesh = {
                    # numpy array of size number of nodes x 3
                    "points": points,
                    # numpy array of size number of elements x 4
                    "cells": connectivity,
                }

        objects: 2D array
            The list of objects. Each line corresponds to an object encoded as follow:

            .. code-block:: text

                - spheres: radius, oZ, oY, oX, phase
                - cylinders: radius, oZ, oY, oX, nZ, nY, nX, phase

        analyticalOrientation: bool, default=True
            Change how the interface's normals are computed:

            - `True`: as the direction from the centroid of the tetrahedron to the closest highest value of the object distance field (ie, the center of a sphere, the axis of a cylinder).
            - `False`: as the normals of the facets which points lie on the object surface.

        cutoff: float, default=1e-6
            Volume ratio below wich elements with interfaces are ignored and considered being part of a single phase.

        writeConnectivity: string, default=None
            When not None, it writes a text file called `writeConnectivity` the
            list of node and the list of elements
                    which format is:

                    .. code-block:: text

                        COORdinates ! number of nodes
                        nodeId, 0, x, y, z
                        ...

                        ELEMents ! number of elemens
                        elemId, 0, elemType, n1, n2, n3, n4, subVol(-), normalX,
                        normalY, normalZ
                        ...

                    where:

                        - ``n1, n2, n3, n4`` is the connectivity (node numbers).
                        - ``subVol(-)`` is the sub volume of the terahedron inside the inclusion.
                        - ``normalX, normalY, normalZ`` are to components of the interface normal vector.
                        - ``elemType`` is the type of element. Their meaning depends on the their phase.
                        Correspondance can be found in the function output
                        after the key word **MATE** like:

                        .. code-block:: text

                            <projmorpho::set_materials
                            .        field 1
                            .        .       MATE,1: background
                            .        .       MATE,2: phase 1
                            .        .       MATE,3: interface phase 1 with
                            background
                            .        field 2
                            .        .       MATE,1: background
                            .        .       MATE,4: phase 2
                            .        .       MATE,5: interface phase 2 with
                            background
                            >

                    Sub volumes and interface vector are only relevant for interfaces. Default value is 0 and [1, 0, 0].

        vtkMesh: bool, default=False
            Writes the VTK of interpolated fields and materials. The files take the same name as ``writeConnectivity``.

    Returns
    -------
        (nElem x 5) array
            For each element: ``elemType, subVol(-), normalX, normalY, normalZ`` (see outputFile for details).

    NOTE
    ----
        Only four noded tetrahedra meshes are supported.

    >>> import spam.mesh
    >>> # unstructured mesh
    >>> points, cells = spam.mesh.createCuboid([1, 1, 1], 0.1)
    >>> mesh = {"points": points, "cells": cells}
    >>> # one centered sphere (0.5, 0.5, 0.5) of radius 0.2 (phase 1)
    >>> sphere = [[0.2, 0.8, 0.1, 0.1, 1]]
    >>> # projection
    >>> materials = spam.mesh.projectObjects(mesh, sphere, writeConnectivity="mysphere", vtkMesh=True)

    """

    # init projmorpho
    pr = projmorpho(
        name="spam" if writeConnectivity is None else writeConnectivity,
        cutoff=cutoff,
    )

    # STEP 1: objects
    objects = numpy.array(objects)

    # if objects.shape[1] == 5:
    #     swaps = [
    #         [1, 3],  # swap ox <-> oz
    #     ]
    #     for a, b in swaps:
    #         # swap axis for origin point
    #         tmp = objects[:, a].copy()
    #         objects[:, a] = objects[:, b]
    #         objects[:, b] = tmp
    # elif objects.shape[1] == 7:
    #     # swap axis ellipsoids
    #     tmp = objects[:, 0].copy()
    #     objects[:, 0] = objects[:, 2]
    #     objects[:, 2] = tmp
    #     tmp = objects[:, 3].copy()
    #     objects[:, 3] = objects[:, 5]
    #     objects[:, 5] = tmp
    # elif objects.shape[1] == 8:  # cylinders
    #     swaps = [
    #         [1, 3],  # swap ox <-> oz
    #         [4, 6],  # swap nx <-> nz
    #     ]
    #     for a, b in swaps:
    #         # swap axis for origin point
    #         tmp = objects[:, a].copy()
    #         objects[:, a] = objects[:, b]
    #         objects[:, b] = tmp

    pr.setObjects(objects)

    # STEP 2: Mesh
    points, cells = _refactor_mesh(mesh)
    pr.setMesh(points, cells.ravel())

    # STEP 3: projection
    pr.computeFieldFromObjects()
    pr.projection(analytical_orientation=analyticalOrientation)

    # STEP 4: write VTK
    if writeConnectivity:
        pr.writeFEAP()
    if vtkMesh:
        pr.writeVTK()
        pr.writeInterfacesVTK()

    return numpy.array(pr.getMaterials())


def projectField(mesh, fields, thresholds=[0.0], cutoff=1e-6, writeConnectivity=None, vtkMesh=False):
    """
    This function project a set of distance fields onto an unstructured mesh.
    Each distance field corresponds to a phase and the interface between
    the two phases is set by the thresholds.

    Parameters
    ----------
        mesh: dict
            Dictionary containing points coordinates and mesh connectivity.

            .. code-block:: python

                mesh = {
                    # numpy array of size number of nodes x 3
                    "points": points,
                    # numpy array of size number of elements x 4
                    "cells": connectivity,
                }

        fields: list of dicts
            The fields should be continuous (like a distance
            field) for a better projection. They are discretised over a regular
            mesh (lexicographical order) and eahc one corresponds to a phase.
            The dictionary containing the fields data is defined as follow

            .. code-block:: python

                fields = {
                    # coordinates of the origin of the field (3 x 1)
                    "origin": origin,
                    # lengths of fields domain of definition  (3 x 1)
                    "lengths": lengths,
                    #  list of fields values (list of 3D arrays)
                    "values": [phase1, phase2],
                }

        thresholds: list of floats, default=[0]
            The list of thresholds.

        cutoff: float, default=1e-6
            Volume ratio below wich elements with interfaces are ignored and considered being part of a single phase.

        writeConnectivity: string, default=None
            When not None, it writes a text file called `writeConnectivity` the
            list of node and the list of elements
                    which format is:

                    .. code-block:: text

                        COORdinates ! number of nodes
                        nodeId, 0, x, y, z
                        ...

                        ELEMents ! number of elemens
                        elemId, 0, elemType, n1, n2, n3, n4, subVol(-), normalX,
                        normalY, normalZ
                        ...

                    where:

                        - ``n1, n2, n3, n4`` is the connectivity (node numbers).
                        - ``subVol(-)`` is the sub volume of the terahedron inside the inclusion.
                        - ``normalX, normalY, normalZ`` are to components of the interface normal vector.
                        - ``elemType`` is the type of element. Their meaning depends on the their phase.
                        Correspondance can be found in the function output
                        after the key word **MATE** like:

                        .. code-block:: text

                            <projmorpho::set_materials
                            .        field 1
                            .        .       MATE,1: background
                            .        .       MATE,2: phase 1
                            .        .       MATE,3: interface phase 1 with
                            background
                            .        field 2
                            .        .       MATE,1: background
                            .        .       MATE,4: phase 2
                            .        .       MATE,5: interface phase 2 with
                            background
                            >

                    Sub volumes and interface vector are only relevant for interfaces. Default value is 0 and [1, 0, 0].

        vtkMesh: bool, default=False
            Writes the VTK of interpolated fields and materials. The files take the same name as ``writeConnectivity``.

    Returns
    -------
        (nElem x 5) array
            For each element: ``elemType, subVol(-), normalX, normalY, normalZ`` (see outputFile for details).

    NOTE
    ----
        Only four noded tetrahedra meshes are supported.

    >>> import spam.mesh
    >>> import spam.kalisphera
    >>> # unstructured mesh
    >>> points, cells = spam.mesh.createCuboid([1, 1, 1], 0.1)
    >>> mesh = {"points": points, "cells": cells}
    >>> # create an image of a sphere and its distance field
    >>> sphereBinary = numpy.zeros([101] * 3, dtype=float)
    >>> spam.kalisphera.makeSphere(sphereBinary, [50.5] * 3, 20)
    >>> sphereField = spam.mesh.distanceField(one_sphere_binary.astype(bool).astype(int))
    >>> # format field object
    >>> fields = {
    >>>     # coordinates of the origin of the field (3 x 1)
    >>>     "origin": [0] * 3,
    >>>     # lengths of fields domain of definition  (3 x 1)
    >>>     "lengths": [1] * 3,
    >>>     # list of fields
    >>>     "values": [sphereField],
    >>> }
    >>> # projection
    >>> materials = spam.mesh.projectField(mesh, fields, writeConnectivity="mysphere", vtkMesh=True)

    """
    # init projmorpho
    pr = projmorpho(
        name="spam" if writeConnectivity is None else writeConnectivity,
        thresholds=thresholds,
        cutoff=cutoff,
    )

    # STEP 1: Fields

    # origin
    # origin = [_ for _ in reversed(fields["origin"])]
    origin = [_ for _ in fields["origin"]]
    # nPoints
    # nPoints = [n for n in reversed(fields["values"][0].shape)]
    nPoints = [n for n in fields["values"][0].shape]
    # field size
    # lengths = [_ for _ in reversed(fields["lengths"])]
    lengths = [_ for _ in fields["lengths"]]
    # ravel fields values (ravel in F direction to swap zyx to xyz)
    values = [v.flatten(order="F") for v in fields["values"]]
    # values = [v.flatten(order='C') for v in fields["values"]]

    pr.setImage(values, lengths, nPoints, origin)

    # STEP 2: Mesh
    points, cells = _refactor_mesh(mesh)
    pr.setMesh(points, cells.ravel())

    # STEP 3: projection
    pr.computeFieldFromImages()
    pr.projection()

    # STEP 4: write VTK
    if writeConnectivity:
        pr.writeFEAP()
    if vtkMesh:
        pr.writeVTK()
        pr.writeInterfacesVTK()

    return numpy.array(pr.getMaterials())
