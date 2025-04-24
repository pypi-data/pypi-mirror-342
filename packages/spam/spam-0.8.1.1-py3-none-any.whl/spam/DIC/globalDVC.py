# Library of SPAM image correlation functions.
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
Set of functions for performing mechanically regularised global DVC.
The regularisation implementation is taken from [Mendoza2019]_.

Here is how it can be used:

.. code-block:: python

    import spam.mesh
    import spam.DIC

    # Mesh
    points, connectivity = spam.mesh.createCylinder([-24, 27], 12.5, 97.3, 10, zOrigin=-4.2)

    # Regularisation: parameters
    myParameters = {
        "young": 10,
        "poisson": 0.25,
        "dirichlet": {
            "z_start": {"dof": [0]},
            "z_end": {"dof": [0]},
        },
    }
    p = spam.DIC.regularisationParameters(myParameters)

    # Regularisation step 1: get labels
    labels = spam.DIC.surfaceLabels(points, surfaces=p["surfaces"])

    # Regularisation step 2: build regularisation matrix
    regularisationMatrix, regularisationField = spam.DIC.regularisationMatrix(
        points,
        connectivity,
        young=p["young"],
        poisson=p["poisson"],
        xiBulk=p["xi"],
        dirichlet=p["dirichlet"],
        periods=p["periods"],
        labels=labels,
    )

    # Global DVC
    globalCorrelation(
        im1,
        im2,
        points,
        connectivity,
        regularisationMatrix=regularisationMatrix,
        regularisationField=regularisationField,
    )

.. [Mendoza2019] A. Mendoza, J. Neggers, F. Hild, S Roux (2019). Complete mechanical regularization applied to digital image and volume correlation.
    *Computer Methods in Applied Mechanics and Engineering*, Volume 355, 1 October 2019, Pages 27-43
    https://doi.org/10.1016/j.cma.2019.06.005

.. _RegularisationParameter: _static/gdvc-regularisation-parameters.yaml

    Note
    ----
        Make a link to the script

"""

import time  # for debug

import numpy
import spam.DIC
import spam.label
import spam.mesh
import tifffile

# 2017-05-29 ER and EA
# This is spam's C++ DIC toolkit, but since we're in the tools/ directory we can import it directly
from spambind.DIC.DICToolkit import (
    computeDICglobalMatrix,
    computeDICglobalVector,
    computeGradientPerTet,
)


def _check_symmetric(a, rtol=1e-05, atol=1e-08):
    """Helper function to check if a matrix is symmetric."""
    return numpy.allclose(a, a.T, rtol=rtol, atol=atol)


def _errorCalc(im1, im2, im2ref, meshPaddingSlice):
    """Helper function to compute the error between two images."""
    errorInitial = numpy.sqrt(numpy.square(im2ref[meshPaddingSlice] - im1[meshPaddingSlice]).sum())
    errorCurrent = numpy.sqrt(numpy.square(im2[meshPaddingSlice] - im1[meshPaddingSlice]).sum())
    return errorCurrent / errorInitial


def _computeFunctional(u, K, L=None):
    """Helper function to compute global DVC functional"""
    u = numpy.ravel(u)
    if L is None:
        return numpy.matmul(u.T, numpy.matmul(K.T, numpy.matmul(K, u)))
    else:
        return numpy.matmul(u.T, numpy.matmul(K.T, numpy.matmul(L, numpy.matmul(K, u))))


def _normalisedEnergies(v, Km, Ks, Ls):
    """Helper function to compute globale DVC normalised energies"""
    Em = _computeFunctional(v, Km)
    Es = [_computeFunctional(v, K, L=L) for K, L in zip(Ks, Ls)]
    return Em, Es


def _computeWeights(kMag, xiBulk, xiDirichlet):
    """Helper function to compute global DVC weights"""
    print(f"[regularisation] xi bulk = {xiBulk:.2f}")
    Wm = (xiBulk * kMag) ** 4
    Ws = []
    for i, xi in enumerate(xiDirichlet):
        print(f"[regularisation] xi dirichlet {i} = {xi:.2f}")
        Ws.append((xi * kMag) ** 4)

    return Wm, Ws


def surfaceLabels(points, surfaces=[], connectivity=None):
    """Creates a label for each points based on a list of keywords that corresponds to surfaces (`ie.` ``["z_start", "z_end"]``).
    The label value is based on the position of the surface in the list.

    Parameters
    ----------
        points: Nx3 array
            List of coordinates of the mesh nodes.

        surfaces: list of string
            A list of keywords corresponding to surfaces.

            - ``z_start``: plane at ``z == min(points[:,0])``
            - ``z_end``: plane at ``z == max(points[:,0])``
            - ``y_start``: plane at ``y == min(points[:,1])``
            - ``y_end``: plane at ``y == max(points[:,1])``
            - ``x_start``: plane at ``x == min(points[:,2])``
            - ``x_end``: plane at ``x == max(points[:,2])``
            - ``z_lateral``: lateral surface of a cylinder oriented in the first direction.
            - ``y_lateral``: lateral surface of a cylinder oriented in the second direction.
            - ``x_lateral``: lateral surface of a cylinder oriented in the third direction.

        connectivity: array (only for debug purposes)
            Connectivity matrix. If set, creates a VTK file with labels.

    Returns
    -------
        N x 1 array:
            Surface label for each points.

    Note
    ----
        - Surface labels start at 1, 0 corresponding to bulk or not specified surfaces.
        - Points belong to a single surface. The first surface in `surfaces` prevails.

    Example
    -------
        >>> import spam.mesh
        >>> import spam.DIC
        >>>
        >>> # create mesh
        >>> points, connectivity = spam.mesh.createCylinder([-24, 27], 12.5, 97.3, 10, zOrigin=-4.2)
        >>> # compute labels for bottom and top surface only
        >>> labels = spam.DIC.surfaceLabels(points, surfaces=["z_start", "z_end"], connectivity=connectivity)

    """

    def _belongs_to_lateral_surface(point, centre, radius, epsilon=1e-6):
        """Returns True if point belongs to the lateral surface of a cylinder"""
        d = ((centre[0] - point[1]) ** 2 + (centre[1] - point[2]) ** 2) ** 0.5
        return abs(d - radius) < epsilon

    def _belongs_to_plane(point, direction, coordinate, epsilon=1e-6):
        """Returns True if point belongs to a surface of position `coordinate` in direction `direction`"""
        return abs(point[direction] - coordinate) < epsilon

    # Get geometrical data from the points coordinates
    maxCoord = numpy.max(points, axis=0)
    minCoord = numpy.min(points, axis=0)
    centre = [0.0] * 3
    radii = [0.0] * 3
    for dz in range(3):
        dy = (dz + 1) % 3
        dx = (dz + 2) % 3
        centre[dz] = [0.5 * (minCoord[d] + maxCoord[d]) for d in [dy, dx]]
        radii[dz] = 0.25 * (maxCoord[dx] + maxCoord[dy] - minCoord[dx] - minCoord[dy])

    labels = numpy.zeros(points.shape[0], dtype=int)

    # Loop over the points
    for A, point in enumerate(points):

        # Loop over the surfaces to enforce order for edges and vertices
        for i, surface in enumerate(surfaces):

            direction, position = surface.split("_")
            direction = {"z": 0, "y": 1, "x": 2}[direction]  # direction as integer z: 0, y: 1, x: 2

            if position == "start" and _belongs_to_plane(point, direction, minCoord[direction]):
                labels[A] = i + 1
                break

            elif position == "end" and _belongs_to_plane(point, direction, maxCoord[direction]):
                labels[A] = i + 1
                break

            elif position == "lateral" and _belongs_to_lateral_surface(point, centre[direction], radii[direction]):
                labels[A] = i + 1
                break

    if connectivity is not None:  # debug
        spam.helpers.writeUnstructuredVTK(points, connectivity, pointData={"label": labels}, fileName="gdvc-labels.vtk")

    return labels


def projectionMatrices(points, connectivity, labels, dirichlet=[]):
    """Compute binary diagonal matrices and Laplace-Beltrami operator.
    Details on the meaning of these matrices can be found in [Mendoza2019]_ `eq. (12) to (14)` and `eq. (17) to (19)`.


    Parameters
    ----------
        points: Nx3 array
            List of coordinates of the mesh nodes.

        connectivity: Mx4 numpay array
            Connectivity matrice of the mesh (tetrahedra).

        labels: Nx1 array
            Surface labels for each points as defined in ``spam.DIC.surfaceLabels()``

        dirichlet: list of (int, list, )
            Each element of the list defines a surface with Dirichlet boundary conditions by a tuple.

            - The first element of the tuple is the surface label which should belong to `labels`.
            - The second element of the tuple is a list of degrees of freedom directions to consider for the Dirichlet boundary conditions.
            - Extra elements in the tuple are ignored.
            .. code-block:: python

                dirichlet = [
                    # surface 1, dof in x, y
                    (
                        1,
                        [1, 2],
                    ),
                    # surface 3, dof in z
                    (
                        3,
                        [0],
                    ),
                ]

    Returns
    -------
        3Nx3N array:
            :math:`D_m` The binary diagonal matrix corresponding to all dofs of the bulk and neumann surfaces nodes (ie the non dirichlet)
        List of 3Nx3N array:
            :math:`D_{S_i}` Binary diagonal matrices corresponding to the dofs of each Dirichlet surfaces
        List of 3Nx3N array:
            :math:`L_{S_i}` List of Laplace-Beltrami operators corresponding to the same Dirichlet surfaces.

    """
    if dirichlet is None:
        dirichlet = []

    # all matrices out here are of shape ndof x ndof (same as stiffness matrix)
    ndof = 3 * points.shape[0]

    print(f"[projectionMatrices] number of dirichlet surfaces: {len(dirichlet)} ({dirichlet})")

    # initialise list of A and B matrices in order to compute the L operator (size ndof x ndof)
    matricesA = [numpy.zeros((ndof, ndof)) for _ in dirichlet]
    matricesB = [numpy.zeros((ndof, ndof)) for _ in dirichlet]
    matricesD = [numpy.zeros((ndof, ndof)) for _ in dirichlet]

    # list of all nodes and dof numbers on dirichlet surfaces
    # NOTE: taking label == 0 (ie background) leads to singlular sub_A matrix
    dirichletSurfaces = [(numpy.where(labels == d[0])[0], d[1]) for d in dirichlet if d[0]]

    DEBUG_dirichlet_connectivity_all = []
    DEBUG_dirichlet_points_all = []
    for si, _ in enumerate(dirichlet):
        DEBUG_dirichlet_connectivity_all.append([])
        DEBUG_dirichlet_points_all.append([])

    # # loop over dirichlet matrix
    for si, (surfacePoints, dofDirections) in enumerate(dirichletSurfaces):
        dofs = [3 * A + d for A in surfacePoints for d in dofDirections]

        print(f"[projectionMatrices] Dirichlet #{si} label {dirichlet[si][0]}) #points = {len(surfacePoints)} dofs directions = {dofDirections} {len(dofs)} dofs")

        surfacePoints = set(surfacePoints)
        for tetra_connectivity in connectivity:
            tri_con = list(surfacePoints.intersection(tetra_connectivity))
            tri_nodes = [list(points[i]) for i in tri_con]
            if len(tri_con) != 3:
                # the element doesn't have a triangle a this surface
                continue

            # get 4th point of the tetrahedron to compute 3D shape functions
            point_4_n = list(set(tri_con).symmetric_difference(set(tetra_connectivity)))[0]
            _, tri_coefficients = spam.mesh.shapeFunctions(tri_nodes + [list(points[point_4_n])])
            # we've got a triangle on the surface!!!
            DEBUG_dirichlet_connectivity_all[si].append(list(tri_con))
            DEBUG_dirichlet_points_all[si].append(tri_nodes)

            # assemble the dirichlet connectivity matrix
            a = numpy.array(tri_coefficients[:3, 0])
            bcd = numpy.array(tri_coefficients[:3, 1:])
            B = numpy.array(tri_nodes).T

            def phi(i, L):
                return a[i] + numpy.matmul(bcd[i], numpy.matmul(B, L.T))

            def dphi(i):
                return bcd[i]

            # gauss points
            L_gp = numpy.array([[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])

            # STEP 3: compute the area
            area = 0.5 * numpy.linalg.norm(
                numpy.cross(
                    numpy.subtract(tri_nodes[1], tri_nodes[0]),
                    numpy.subtract(tri_nodes[2], tri_nodes[0]),
                )
            )

            # STEP 3: compute inner products of the shape functions
            for i in range(3):
                for j in range(3):
                    inner = 0.0
                    for L in L_gp:
                        # print(inner, i, j, L, phi(i, L), phi(j, L))
                        inner += phi(i, L) * phi(j, L)
                    inner *= area / 3.0  # the 1/3. comes from the weight
                    dinner = area * numpy.inner(dphi(i), dphi(j))
                    for d in dofDirections:
                        P = int(3 * tri_con[i] + d)
                        Q = int(3 * tri_con[j] + d)
                        matricesA[si][P, Q] += inner
                        matricesB[si][P, Q] += dinner

        # # invert matrix A
        # for si, (surfacePoints, dofDirections) in enumerate(dirichletSurfaces):
        dofs = [3 * A + d for A in surfacePoints for d in dofDirections]
        # 1. extract submatrix A from full size matricesA and invert
        sub_A = matricesA[si][:, dofs]
        sub_A = sub_A[dofs, :]

        sub_A = numpy.linalg.inv(sub_A)
        # 2. push back inverted submatrix into full size matricesA
        for i, P in enumerate(dofs):
            matricesD[si][P, P] = 1
            for j, Q in enumerate(dofs):
                matricesA[si][P, Q] = sub_A[i, j]

    # return also bulk + neumann binary diagonal projection matrices
    # Dm = Db + Dn = I - Sum(Dd)
    Dm = numpy.eye(ndof)
    for Ds in matricesD:
        Dm -= Ds

    # return a list of D and L = AxB for each dirichlet surface
    return Dm, matricesD, [numpy.matmul(A, B) for A, B in zip(matricesA, matricesB)]


def isochoricField(points, periods=3, connectivity=None):
    r"""Helper function to build the isochoric test function used to normalised the mechanical regularisation functionals.
    The function is a shear displacement field with its wave vector in the direction of the longest dimension of the mesh.

    .. math::

        \textbf{v}(\textbf{x}) = \sin(2 \pi \textbf{k}\cdot \textbf{x} )

    [Mendoza2019]_ `eq. (25)`.

    Parameters
    ----------
        points: Nx3 array
            List of coordinates of the mesh nodes.

        periods: int
            The number of periods of the shear wave.

        connectivity: array (only for debug purposes)
            Connectivity matrix. If set, creates a VTK file with the field.

    Returns
    -------
        float:
            The magnitude of the wave vector :math:`\bf{k}`.
        Nx3 array:
            The field :math:`\bf{v}` at each nodes.
    """

    sizes = [ma - mi for ma, mi in zip(numpy.max(points, axis=0), numpy.min(points, axis=0))]
    d = numpy.argmax(sizes)  # direction of largest size
    size = float(max(sizes))  # largest size
    mag = periods / size
    v = numpy.zeros_like(points)
    for i, point in enumerate(points):
        kdotx = mag * point[d]
        v[i][(d + 0) % 3] = 0
        v[i][(d + 1) % 3] = numpy.sqrt(0.5) * numpy.sin(2 * numpy.pi * kdotx)
        v[i][(d + 2) % 3] = numpy.sqrt(0.5) * numpy.sin(2 * numpy.pi * kdotx)

    if connectivity is not None:
        print("[isochoricField] plot vtk")
        spam.helpers.writeUnstructuredVTK(
            points,
            connectivity,
            elementType="tetra",
            pointData={"v": v},
            cellData={},
            fileName="gdvc-v.vtk",
        )

    return mag, v


def regularisationMatrix(points, connectivity, young=1, poisson=0.25, voxelSize=1, xiBulk=None, dirichlet=[], labels=[], periods=3):
    r"""Computes the mechanical regularisation matrix :math:`M_{reg}` for the global DVC:
    $$(M_{reg} + M_{c}) \\delta\\textbf{u} = \\textbf{b} - M_{reg} \\textbf{u} $$
    where
    $$M_{reg} = M_m + \\sum_{i} M_{S_i}$$
    corresponds to both bulk/Neuman and Dirichlet surfaces contributions ([Mendoza2019]_ `eq. (29) and (30)`).

    Parameters
    ----------
        points: Nx3 array
            List of coordinates of the mesh nodes.

        connectivity: Mx4 array
            Connectivity matrix of the mesh.

        young: float (optional)
            The Young modulus used to build the stiffness matrix :math:`K` from which :math:`M_m` and :math:`M_{S_i}` are derived.
            Default = 1 (it is useless to change this value if you don't impose forces with meaningful units on the Neumann surfaces)

        poisson: float (optional)
            The Poisson ratio used to build the stiffness matrix :math:`K` from which :math:`M_m` and :math:`M_{S_i}` are derived.
            Default = 0.25

        voxelSize: float (optional)
            The size of a voxel in the same unit used to set the Young modulus assuming that the mesh geometry is in voxels.
            This voxel size :math:`v_s` is used to convert the Young modulus in Newton per voxels squared.
            Default = 1 (it is useless to change this value if you don't impose forces with meaningful units on the Neumann surfaces).

        xiBulk: float (optional)
            The regularisation length :math:`\xi_m` of the bulk/Neumann contribution :math:`M_{reg}`.
            It has to be compared to the characteristic length of the mesh.
            The bigger the regularisation length the more important the regularisation contribution.
            If None it is taken to be equal to the mesh characteristic length.
            Default = None

        dirichlet: list of (int, list, float) (optional)
            Each element of the list defines a surface with Dirichlet boundary conditions by a tuple.

            - The first element of the tuple is the surface label which should belong to `labels`.
            - The second element of the tuple is a list of degrees of freedom directions to consider for the Dirichlet boundary conditions.
            - The third element of the tuple correspond to the regularisation length of the surface :math:`\xi_{S_i}`

            .. code-block:: python

                dirichlet = [
                    # surface 1, dof in x, y, xi = 0.1
                    [1, [1, 2], 0.1],
                    # surface 3, dof in z, xi not set
                    [3, [0], None],
                ]

        labels: Nx1 array (optional)
            Surface labels for each points as defined in ``spam.DIC.surfaceLabels()``. Mandatory only if ``dirichlet`` is set.

        periods: float (optional)
            Number of periods of the isochoric function :math:`v` used to compute the normalized energy ([Mendoza2019]_ `eq. (27)`).
            :math:`v` is computed with ``spam.DIC.isochoricField()`` with a default number of periods of 3.

    Returns
    -------
        3Nx3N array:
            :math:`M_{req}` the regularisation matrix.
        Nx3 array:
            :math:`v` the isochoric field at each nodes of the mesh.

    Note
    ----
        - The ``dirichlet`` argument is compatible with the one in ``spam.DIC.projectionMatrices()``
        - As long as you don't impose forces to the Neumann surfaces it is usless to set a specific Young modulus and a voxel size.
        - Imposing forces is not implemented yet :)

    Warning
    -------
        This function is not tested yet
    """

    def _imshow(matlist, title):
        from matplotlib import pyplot as plt

        if not isinstance(matlist, list):
            matlist = [matlist]

        for i, mat in enumerate(matlist):
            plt.imshow(mat)
            plt.title(f"{title} {i}")
            # plt.show()

    print(f"[regularisation] Young modulus using si: {young}")
    young *= voxelSize**2
    print(f"[regularisation] Young modulus using voxels: {young}")

    print("[regularisation] Build projection matrices")
    Dm, Ds, Ls = projectionMatrices(points, connectivity, labels, dirichlet=dirichlet)
    _imshow(Dm, "Dm")
    _imshow(Ds, "Ds")
    _imshow(Ls, "Ls")

    print("[regularisation] Build global stiffness matrix")
    K = spam.mesh.globalStiffnessMatrix(points, connectivity, young, poisson)
    print("[regularisation] Build bulk stiffness matrix")
    Km = numpy.matmul(Dm, K)
    print("[regularisation] Build dirichlet stiffness matrices")
    Ks = [numpy.matmul(Ds_i, K) for Ds_i in Ds]
    _imshow(K, "K")
    _imshow(Km, "Km")
    _imshow(Ks, "Ks")
    del K

    print("[regularisation] Build isochoric function")
    kMag, v = isochoricField(points, periods=periods)

    print("[regularisation] Compute normalised energy and weight")
    Em, Es = _normalisedEnergies(v, Km, Ks, Ls)
    print(f'[regularisation] Em = {Em:.3e}, Es = {" ".join([f"{_:.3e}" for _ in Es])}')

    lc = spam.mesh.getMeshCharacteristicLength(points, connectivity)
    print(f"[regularisation] mesh characteristic length lc = {lc}")

    xiBulk = lc if xiBulk is None else xiBulk
    xiDirichlet = [lc if _[2] is None else _[2] for _ in dirichlet]
    Wm, Ws = _computeWeights(kMag, xiBulk, xiDirichlet)
    print(f'[regularisation] Wm = {Wm:.2f}, Ws = {" ".join([f"{_:.2f}" for _ in Ws])}')

    print(f'[regularisation] Wm/Em = {Wm/Em:.3e} Ws/Es = {" ".join([f"{a/b:.3e}" for a, b in zip(Ws, Es)])}')

    # 5.4 compute Mreg
    Mreg = numpy.zeros_like(Km)
    Mreg = Wm * numpy.matmul(Km.T, Km) / Em
    for W, E, K, L in [(W, E, K, L) for W, E, K, L in zip(Ws, Es, Ks, Ls) if E]:
        Mreg += W * numpy.matmul(K.T, numpy.matmul(L, K)) / E

    _imshow(Mreg, "Mreg")
    return Mreg, v


def regularisationParameters(userParameters):
    """
    Convert a user friendly dictionary of parameters into a dictionary of variables compatible with the regularisation functions of this module.

    Parameters
    ----------
        userParameters: (str | dict)
            The user parameters for the mechanical regularisation scheme. It can be:

            - if ``str``: the path to a YAML file. A dummy example can be downloaded here:  `RegularisationParameter`_
            - if ``dict``: a dictionary containing the following keys and values:

            .. code-block:: python

                {
                    # bulk / Neumann regularisation
                    "young": 10,  # mandatory (the Young modulus)
                    "poisson": 0.25,  # mandatory (the Poisson ratio)
                    "xiBulk": 30,  # optional (the bulk/Neumann regularisation lentgh)
                    "periods": 3,  # the number of periods of the isochoric function (optional)
                    "voxelSize": 0.01,  # the voxel size (optional)
                    # Information about the Dirichlet surface regularisation
                    # Each surface is defined by a search keyword among
                    # z_start, z_end, y_start, y_end, x_start and x_end for plane lookups
                    # z_lateral, y_lateral, x_lateral for cylinder lateral surface lookups
                    "dirichlet": {
                        "z_start": {  # surface label 1
                            "xi": 5,  # the regularisation length (optional)
                            "dof": [0, 1, 2],  # mandatory
                        },
                        "z_end": {"dof": [0]},  # surface label 2  # mandatory
                    },
                }

    Returns
    -------
        dict:
            A dictionary with the variables needed for the regularisation functions.
            The dictionary keys are named to match the function's signatures:

            - ``surface``: the dirichlet surfaces for ``spam.DIC.surfaceLabels()``
            - ``dirichlet``: the dirichlet surfaces for ``spam.DIC.regularisationMatrix()``
            - ``young``: the Young modulus for ``spam.DIC.regularisationMatrix()``
            - ``poisson``: the Poisson ratio for ``spam.DIC.regularisationMatrix()``
            - ``xiBulk``: the bulk characteristic lentgh for ``spam.DIC.regularisationMatrix()``
            - ``periods``: the Poisson ratio for ``spam.DIC.regularisationMatrix()``
            - ``voxelSize``: the Poisson ratio for ``spam.DIC.regularisationMatrix()``
    """

    surfaces = [k for k in userParameters.get("dirichlet", {})]
    dirichlet = [(i + 1, surf["dof"], surf.get("xi")) for i, surf in enumerate(userParameters.get("dirichlet", {}).values())]
    young = userParameters["young"]
    poisson = userParameters["poisson"]
    xiBulk = userParameters.get("xiBulk")
    periods = userParameters.get("periods", 3)
    voxelSize = userParameters.get("voxelSize", 1.0)

    parameters = {"surfaces": surfaces, "young": young, "poisson": poisson, "xiBulk": xiBulk, "dirichlet": dirichlet, "periods": periods, "voxelSize": voxelSize}

    for k, v in parameters.items():
        print(f"[regularisation parameters] {k:<10}: {v}")
    return parameters


def globalCorrelation(
    im1,
    im2,
    points,
    connectivity,
    regularisationMatrix=None,
    regularisationField=None,
    initialDisplacements=None,
    convergenceCriterion=0.01,
    maxIterations=20,
    medianFilterEachIteration=False,
    debugFiles=False,
    prefix="globalCorrelation",
    nThreads=None,
):
    """
    Global DVC (works only with 3D images).

    Parameters
    ----------
        im1 : 3D array
            Reference image in which the mesh is defined

        im2 : 3D array
            Deformed image, should be same size as im1

        points :  M x 3 array
            M nodal coordinates in reference configuration

        connectivity : N x 4 array
            connectivityhedral connectivity generated by spam.mesh.triangulate() for example

        regularisationMatrix : 3N x 3N array (optional)
            Mechanical regularisation stiffness matrix. If None no mechanical regularisation is applied.
            First output of `spam.DIC.regularisationMatrix`


        regularisationField : N x 3 array (optional)
            Isochoric displacement field used to compute the normalisation energies.
            Second output of `spam.DIC.regularisationMatrix`

        initialDisplacements : M x 3 array of floats (optional)
            Initial guess for nodal displacements, must be coherent with input mesh
            Default = None

        convergenceCriterion : float
            Convergence criterion for change in displacements in px
            Default = 0.01

        maxIterations : int
            Number of iterations to stop after if convergence has not been reached
            Default = 20

        debugFiles : bool
            Write temporary results to file for debugging?
            Default = 'globalCorrelation'

        prefix : string
            Output file prefix for debugFiles
            Default = None

    Returns
    -------
        displacements : N x 3 array of floats
            (converged?) Nodal displacements

    Example
    -------
        >>> import spam.DIC
        >>> spam.DIC.globalCorrelation(
            imRef,
            imDef
        )
    """
    import multiprocessing

    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        pass

    import spam.helpers
    import spam.mesh

    # Global number of processes
    nThreads = multiprocessing.cpu_count() if nThreads is None else nThreads
    print(f"[globalCorrelation] C++ parallelisation on {nThreads} threads")

    print(f"[globalCorrelation] Convergence criterion = {convergenceCriterion}")
    print(f"[globalCorrelation] Max iterations = {maxIterations}")
    print("[globalCorrelation] Converting im1 to 32-bit float")
    im1 = im1.astype("<f4")

    points = points.astype("<f8")
    connectivity = connectivity.astype("<u4")

    maxCoord = numpy.amax(points, axis=0).astype("<u2")
    minCoord = numpy.amin(points, axis=0).astype("<u2")
    print(f"[globalCorrelation] Mesh box: min = {minCoord} max = {maxCoord}")

    meshPaddingSlice = (
        slice(minCoord[0], maxCoord[0]),
        slice(minCoord[1], maxCoord[1]),
        slice(minCoord[2], maxCoord[2]),
    )

    displacements = numpy.zeros((points.shape[0], 3), dtype="<f8")

    print(f"[globalCorrelation] Points: {points.shape}")
    print(f"[globalCorrelation] Displacements: {displacements.shape}")
    print(f"[globalCorrelation] Cells: {connectivity.shape}")
    print(f"[globalCorrelation] Padding: {meshPaddingSlice}")

    ###############################################################
    # Step 2-1 Apply deformation and interpolate pixels
    ###############################################################

    print("[globalCorrelation] Allocating 3D data (deformed image)")
    if initialDisplacements is None:
        im1Def = im1.copy()
        imTetLabel = spam.label.labelTetrahedra(im1.shape, points, connectivity, nThreads=nThreads)
    else:
        print("[globalCorrelation] Applying initial deformation to image")
        displacements = initialDisplacements.copy()
        tic = time.perf_counter()
        imTetLabel = spam.label.labelTetrahedra(im1.shape, points + displacements, connectivity, nThreads=nThreads)
        print(f"[globalCorrelation] Running labelTetrahedra: {time.perf_counter()-tic:.3f} seconds.")

        im1Def = spam.DIC.applyMeshTransformation(
            im1,
            points,
            connectivity,
            displacements,
            imTetLabel=imTetLabel,
            nThreads=nThreads,
        )
        if debugFiles:
            print("[globalCorrelation] Saving initial images")
            for name, image in [
                [f"{prefix}-def-init.tif", im1Def],
                [f"{prefix}-imTetLabel-init.tif", imTetLabel],
            ]:
                print(f"[globalCorrelation]\t{name}: {image.shape}")
                tifffile.imwrite(name, image)

    # print("[globalCorrelation] Correlating (MF)!")
    print("[globalCorrelation] Calculating gradient of IM TWO...")
    im2Grad = numpy.array(numpy.gradient(im2), dtype="<f4")

    print("[globalCorrelation] Computing global matrix")
    # This generates the globalMatrix (big Mc matrix) with imGrad as input
    Mc = numpy.zeros((3 * points.shape[0], 3 * points.shape[0]), dtype="<f8")

    if debugFiles:
        print("[globalCorrelation] Computing debug files fields")
        gradientPerTet = numpy.zeros((connectivity.shape[0], 3), dtype="<f8")
        IDPerTet = numpy.array([_ for _ in range(connectivity.shape[0])])

        computeGradientPerTet(
            imTetLabel.astype("<u4"),
            im2Grad.astype("<f4"),
            connectivity.astype("<u4"),
            (points + displacements).astype("<f8"),
            gradientPerTet,
        )

        spam.helpers.writeUnstructuredVTK(
            (points + displacements),
            connectivity,
            cellData={"meanGradient": gradientPerTet, "id": IDPerTet},
            fileName=f"{prefix}-gradient.vtk",
        )
        del gradientPerTet

    computeDICglobalMatrix(
        imTetLabel.astype("<u4"),
        im2Grad.astype("<f4"),
        connectivity.astype("<u4"),
        (points + displacements).astype("<f8"),
        Mc,
    )

    ###############################################################
    # Setup left hand vector
    ###############################################################
    if regularisationMatrix:
        regularisationField = isochoricField(points) if regularisationField is None else regularisationField
        Ec = _computeFunctional(regularisationField, Mc)
        regularisationMatrix *= Ec
        print(f"[regularisation] Wc/Ec = {1/Ec:.3e}")
        left_hand_inverse = numpy.linalg.inv(Mc + regularisationMatrix)
    else:
        print("[globalCorrelation] Skip regularisation")
        left_hand_inverse = numpy.linalg.inv(Mc)
    del Mc

    # error = _errorCalc(im2, im1Def, im1, meshPaddingSlice)
    # print("\[globalCorrelation] Initial Error (abs) = ", error)

    # We try to solve Md=F
    # while error > 0.1 and error < errorIn:
    # while error > 0.1 and i <= maxIterations and error < errorIn:
    dxNorm = numpy.inf
    i = 0
    while dxNorm > convergenceCriterion and i < maxIterations:
        i += 1

        # This function returns globalVector (F) taking in im1Def and im2 and the gradients
        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run computeDICglobalVector: ", end="")
        right_hand_vector = numpy.zeros((3 * points.shape[0]), dtype="<f8")
        computeDICglobalVector(
            imTetLabel.astype("<u4"),
            im2Grad.astype("<f4"),
            im1Def.astype("<f4"),
            im2.astype("<f4"),
            connectivity.astype("<u4"),
            (points + displacements).astype("<f8"),
            right_hand_vector,
        )
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run solve: ", end="")

        # solve: we can use solve here for sake of precision (over computing
        # M^-1). However solve takes quite a lot of time for "small" meshes).

        if regularisationMatrix:
            right_hand_vector -= numpy.matmul(regularisationMatrix, displacements.ravel())
        dx = numpy.matmul(left_hand_inverse, right_hand_vector).astype("<f8")
        # dx_solve = numpy.linalg.solve(
        #     Mc,
        #     right_hand_vector
        # ).astype('<f8')
        # print(numpy.linalg.norm(dx - dx_solve))

        displacements += dx.reshape(points.shape[0], 3)
        dxNorm = numpy.linalg.norm(dx)
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        if medianFilterEachIteration:
            # use connectivity to filter
            print("[globalCorrelation] [newton] Median filter of displacements...")
            for nodeNumber in range(points.shape[0]):
                # get rows of connectivity (i.e., tets) which include this point
                connectedTets = numpy.where(connectivity == nodeNumber)[0]
                neighbourPoints = numpy.unique(connectivity[connectedTets])
                diff = numpy.median(displacements[neighbourPoints], axis=0) - displacements[nodeNumber]
                displacements[nodeNumber] += 0.5 * diff

        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run labelTetrahedra: ", end="")

        imTetLabel = spam.label.labelTetrahedra(im1.shape, points + displacements, connectivity, nThreads=nThreads)
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        tic = time.perf_counter()
        # print("[globalCorrelation] [newton] run applyMeshTransformation: ", end="")
        im1Def = spam.DIC.applyMeshTransformation(
            im1,
            points,
            connectivity,
            displacements,
            imTetLabel=imTetLabel,
            nThreads=nThreads,
        )
        # print(f"{time.perf_counter()-tic:.3f} seconds.")

        if debugFiles:
            tifffile.imwrite(f"{prefix}-def-i{i:03d}.tif", im1Def)
            tifffile.imwrite(
                f"{prefix}-residual-cropped-i{i:03d}.tif",
                im1Def[meshPaddingSlice] - im2[meshPaddingSlice],
            )
            # tifffile.imwrite(f"{prefix}-imTetLabel-i{i:03d}.tif", imTetLabel)

            pointData = {
                "displacements": displacements,
                "initialDisplacements": initialDisplacements,
                "fluctuations": numpy.subtract(displacements, initialDisplacements),
            }

            # compute strain for each fields
            cellData = {}
            components = ["vol", "dev", "volss", "devss"]
            for fieldName, field in pointData.items():
                Ffield = spam.deformation.FfieldBagi(points, connectivity, field, verbose=False)
                decomposedFfield = spam.deformation.decomposeFfield(Ffield, components)
                for c in components:
                    cellData[f"{fieldName}-{c}"] = decomposedFfield[c]

            spam.helpers.writeUnstructuredVTK(
                points.copy(),
                connectivity.copy(),
                pointData=pointData,
                cellData=cellData,
                fileName=f"{prefix}-displacementFE-i{i:03d}.vtk",
            )

        # print("\t\[globalCorrelation] Error Out = %0.5f%%" % (error))
        # reshapedDispl = displacements.reshape(points.shape[0], 3)
        dMin = numpy.min(displacements, axis=0)
        dMed = numpy.median(displacements, axis=0)
        dMax = numpy.max(displacements, axis=0)
        strMin = f"Min={dMin[0]: .3f} {dMin[1]: .3f} {dMin[2]: .3f}"
        strMed = f"Med={dMed[0]: .3f} {dMed[1]: .3f} {dMed[2]: .3f}"
        strMax = f"Max={dMax[0]: .3f} {dMax[1]: .3f} {dMax[2]: .3f}"
        print(f"[globalCorrelation] [newton] i={i:03d}, displacements {strMin}, {strMed}, {strMax}, dx={dxNorm:.2f}")

    return displacements


if __name__ == "__main__":
    pass

    # create mesh
    print("Create mesh")
    # points, connectivity = spam.mesh.createCuboid([32.55, 72.1, 15.7], 20, origin=[-4.2, 12.5, 78.01])
    points, connectivity = spam.mesh.createCylinder([-24, 27], 12.5, 97.3, 10, zOrigin=-4.2)

    configuration = {
        # Information about the bulk regularisation
        "young": 10,  # mandatory (Young modulus)
        "poisson": 0.25,  # mandatory (Poisson ratio)
        # "xi": 30,  # optional
        # "periods": 3,  # optionnal (whatever...)
        # Information about the surface regularisation
        # (Dirichlet boundary conditions)
        # Each surface of the cuboid is labelled by the keywords
        # z_start: z == 0, z_end, y_start, y_end, x_start and x_end)
        # If a keyword is ommited the surface is not regularised.
        "dirichlet": {
            "z_start": {"xi": 30, "dof": [0, 1, 2]},  # optional  # mandatory
            "z_end": {"xi": 30, "dof": [0]},  # xi normalisation is 30
            "z_lateral": {"xi": 30, "dof": [1, 2]},  # xi normalisation is 30
        },
    }

    p = regularisationParameters(configuration)

    # STEP 1: get labels
    labels = surfaceLabels(points, surfaces=p["surfaces"])

    # STEP 2: build regularisation matrix
    Mreg, v = regularisationMatrix(points, connectivity, p["young"], p["poisson"], xiBulk=p["xi"], dirichlet=p["dirichlet"], labels=labels, periods=p["periods"])
