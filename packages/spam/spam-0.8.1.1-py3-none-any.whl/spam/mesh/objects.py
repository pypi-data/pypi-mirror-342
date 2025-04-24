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
    The ``objects`` module offers functions that enables to generate and manipulates geometrical objects in order to represent various phases of materials.

    >>> import spam.mesh
    >>> spam.mesh.packSpheres()
    >>> spam.mesh.packSpheresFromList()

    NOTE
    ----

        Objects array conventions:

            - Sphere: ``[radius, centerX, centerY, centerZ, phase]``
            - Cylinder: ``[radius, centerX, centerY, centerZ, directionX, directionY, directionZ, phase]``

    WARNING
    -------

        This submodule will move to a different module in the near future.

"""

import numpy
from spambind.mesh.meshToolkit import crpacking


def packSpheres(
    totalVolumeFraction,
    rejectionLength,
    phases,
    origin=[0.0] * 3,
    lengths=[1.0] * 3,
    inside=True,
    domain="cube",
    vtk=None,
):
    """This function packs one or several sets (phase) of spheres of different
    radii and create the corresponding distance fields (one per set).

    `The packing algorithm is an iterative process based collective
    rearrangement.`

    Parameters
    ----------
        totalVolumeFraction: float
            The total volume fraction of all the phases
        rejectionLength: float
            The minimal distance between two sphere surfaces
        phases: (nPhase x 3) array
            A 2D array containing the phases parameteres.
            A line corresponds to a phase and a column to a parameter:

            .. code-block:: text

                column 0: the minimal ray of the spheres of the phase
                column 1: the maximal ray of the spheres of the phase
                column 2: the relative volume fraction of the phase

        inside: bool, default=True
            Defines whether or not the spheres have to be completly inside the domain or if they can intersect it (centres always remain inside).
        lengths: array, default=[1, 1, 1]
            The size of the domain the spheres are packed into.
        origin: array, default=[0, 0, 0]
            The origin of the domain.
        domain: string, default='cube'
            The domain type the spheres are packed into. Options are:

                - `cube``: which corresponds to a cuboid. ``lengths`` is then
                the length of the cuboids.

                - ``cylinder``: which corresponds to a cylinder of diameter ``lengths[0]`` and height ``lengths[2]``.

        vtk: string, default=None
            Save vtk files of the spheres for each iterations of the packing
            algorithm under base name `vtk`.

    Returns
    -------
        (nSpheres x 4) array
            For each sphere: ``[radius, ox, oy, oz, phase]``

    >>> import spam.mesh
    >>> volumeFraction = 0.1
    >>> rejectionLength = 1.0
    >>> # phase 1: rmin = 5, rmax = 6.5, volume fraction = 0.6 (of total volume fraction)
    >>> # phase 2: rmin = 6.5, rmax = 8, volume fraction = 0.4 (of total volume fraction)
    >>> phases = [[5.0, 6.5, 0.6], [6.5, 8.0, 0.4]]
    >>> # cylinder going from -5 to 135 in z
    >>> # with a base radius 50 and center [50, 60
    >>> domain = "cylinder"
    >>> lengths = [100, 0, 140]
    >>> origin = [0, 10, -5]
    >>> # generate and pack spheres
    >>> spheres = spam.mesh.packSpheres(volumeFraction, rejectionLength, phases, domain=domain, origin=origin, lengths=lengths, vtk="packing-1")

    NOTE
    ----
        The output of this function can directly be used by the function ``spam.mesh.projectObjects``.

    """

    # if simple table (one phase) convert to table of table anyway
    param = [totalVolumeFraction, rejectionLength]
    for iPhase, phase in enumerate(phases):
        if len(phase) not in [3, 4]:
            raise ValueError("Each phase should have at least 3 parameters: [radius, ox, oy, oz]")

        if len(phase) == 3:
            phase.append(iPhase + 1)

        param += phase

    # fileName
    fileName = vtk if vtk else "crpacking"
    cr = crpacking(param, lengths, origin, int(inside), fileName, domain)

    cr.createSpheres()
    spheres = cr.packSpheres()
    if fileName:
        cr.writeSpheresVTK()

    return spheres


def packObjectsFromList(
    objects,
    rejectionLength,
    origin=[0.0] * 3,
    lengths=[1.0] * 3,
    inside=True,
    domain="cube",
    vtk=None,
):
    """This function packs a set of predefine spheres.

    `The packing algorithm is an iterative process based collective
    rearrangement.`

    Parameters
    ----------
        objects: (nSpheres x nPram) array
            The list of objects. Each line corresponds to:

                - for spheres: `[radius, ox, oy, oz, phase]`

        rejectionLength: float
            The minimal distance between two spheres surfaces
        inside: bool, default=True
            Defines whether or not the spheres have to be completly inside the domain or if they can intersect it (centres always remain inside).
        lengths: array, default=[1.0, 1.0, 1.0]
            The size of the domain the spheres are packed into.
        origin: array, default=[0.0, 0.0, 0.0]
            The origin of the domain.
        domain: string, default='cube'
            The domain type the spheres are packed into. Options are:

                - `cube``: which corresponds to a cuboid. ``lengths`` is then
                the length of the cuboids.

                - ``cylinder``: which corresponds to a cylinder of diameter ``lengths[0]`` and height ``lengths[2]``.

        vtk: string, default=None
            Save vtk files of the spheres for each iterations of the packing
            algorithm under base name `vtk`.

    Returns
    -------
        (nSpheres x 4) array
            For each sphere: ``[radius, ox, oy, oz, phase]``

    NOTE
    ----
        The output of this function can directly be used by the function ``spam.mesh.projectObjects``.

    """
    # condition inputs for crPacking c++ constructor
    param = [0.0, rejectionLength, 1.0, 1.0, 1.0, 1.0]

    # test objects size
    objects = numpy.array(objects)
    if objects.shape[1] not in [5]:
        raise NotImplementedError("Objects with {objects.shape[1]} parameters are not implemented.")

    # fileName
    fileName = vtk if vtk else "crpacking"
    cr = crpacking(param, lengths, origin, int(inside), fileName, domain)

    cr.setObjects(objects)
    spheres = cr.packSpheres()
    if fileName:
        cr.writeSpheresVTK()

    return spheres
