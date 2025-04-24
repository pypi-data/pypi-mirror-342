# Library of SPAM functions for dealing with assembly maxtrix of unstructured 3D meshes made of tetrahedra
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
import numpy


def tetCentroid(points):
    """Compute coordinates of the centroid of a tetrahedron

    Parameters
    ----------
        points : 4x3 array
            Array of the 3D coordinates of the 4 points

    Returns
    -------
        3x1 array
            the coordinates of the centroid
    """

    centroid = numpy.zeros(3)
    for i in range(3):
        a = points[0][i]
        b = points[1][i]
        c = points[2][i]
        d = points[3][i]

        # mid point of AB (1/2 of A -> B)
        mid_ab = a + (b - a) / 2.0

        # centroid of ABC (1/3 of AB -> C median)
        face_centroid = mid_ab + (c - mid_ab) / 3.0

        # centroid of ABCD (1/4 of ABC -> D median)
        centroid[i] = face_centroid + (d - face_centroid) / 4.0

    return centroid


def tetVolume(points):
    """Compute the volume of a tetrahedron

    Parameters
    ----------
        points : 4x3 array
            Array of the 3D coordinates of the 4 points

    Returns
    -------
        float
            the volume of the tetrahedron
    """

    # compute the jacobian matrix by padding the points with a line of 1
    pad = numpy.array([[1], [1], [1], [1]])
    jacobian = numpy.hstack([pad, points])

    # the volume is 1/6 of the determinant of the jacobian matrix
    return numpy.linalg.det(jacobian) / 6.0


def shapeFunctions(points):
    """
    This function computes the shape coefficients matrux from the coordinates
    of the 4 nodes of a linear tetrahedron (see 4.11 in Zienkiewicz).

    .. code-block:: text

        coefficients_matrix = [
                a1 b1 c1 d1
                a2 b2 c2 d2
                a3 b3 c3 d3
                a4 b4 c4 d4
            ]
        with
        N1 = a1 + b1x + c1y + d1z
        N2 = a2 + b2x + c2y + d2z
        N3 = a3 + b3x + c3y + d3z
        N4 = a4 + b4x + c4y + d4z

    Parameters
    ----------
        points : 4x3 array
            Array of the 3D coordinates of the 4 points

    Returns
    -------
        volume : float
            The volume of the tetrahedron
        coefficients_matrix : 4x4 array
            The coefficients 4 coefficients of the 4 shape functions

    Note
    -----
        Pure python function.
    """
    # cast into numpy array and check shape
    points = numpy.array(points)
    if points.shape != (4, 3):
        raise ValueError("Points coordinates in bad format. Can I have a 4x3 please?")

    # jacobian matrix
    pad = numpy.array([[1], [1], [1], [1]])
    jacobian = numpy.hstack([pad, points])
    six_v = numpy.linalg.det(jacobian)
    volume = six_v / 6.0

    coefficients_matrix = numpy.zeros((4, 4))
    for l_number in range(4):  # loop over the 4 nodes
        for c_number in range(4):  # loop over the 4 coefficients for 1 node
            # create mask for the sub matrix (ie: [1, 2, 3], [0, 2, 3], ...)
            lines = [_ for _ in range(4) if _ != l_number]
            columns = [_ for _ in range(4) if _ != c_number]
            # creates the sub_jacobian (needs two runs for some numpy reason)
            sub_jacobian = jacobian[:, columns]
            sub_jacobian = sub_jacobian[lines, :]

            # compute the determinant and fill coefficients matrix
            det = numpy.linalg.det(sub_jacobian)
            sign = (-1.0) ** (l_number + c_number)
            coefficients_matrix[l_number, c_number] = sign * det / six_v

    return volume, coefficients_matrix


def elementaryStiffnessMatrix(points, young, poisson):
    """
    This function computes elementary stiffness matrix from the coordinates
    of the 4 nodes of a linear tetrahedron.

    .. code-block:: text

        D = [something with E and mu] (6x6)
        B = [B1, B2, B3, B4]          (4 times 6x3 -> 6x12)
        ke = V.BT.D.B                 (12x12)

    Parameters
    ----------
        points : 4x3 array
            Array of the 3D coordinates of the 4 points
        young: float
            Young modulus
        poisson: float
            Poisson ratio

    Returns
    -------
        stiffness_matrix : 12x12 array
            The stiffness matrix of the tetrahedron

    Note
    -----
        Pure python function.
    """

    # get volume and shape functions coefficients
    volume, N = shapeFunctions(points)

    # compute the full B matrix
    def Ba(N, a):
        return numpy.array(
            [
                [N[a, 1], 0, 0],
                [0, N[a, 2], 0],
                [0, 0, N[a, 3]],
                [0, N[a, 3], N[a, 2]],
                [N[a, 3], 0, N[a, 1]],
                [N[a, 2], N[a, 1], 0],
            ]
        )

    # initialise B with first Ba
    B = Ba(N, 0)
    for a in [1, 2, 3]:
        B = numpy.hstack([B, Ba(N, a)])

    # compute D matrix
    D = (1.0 - poisson) * numpy.eye(6)
    D[0, [1, 2]] = poisson
    D[1, [0, 2]] = poisson
    D[2, [0, 1]] = poisson
    D[3:, 3:] -= 0.5 * numpy.eye(3)
    D *= young / ((1 + poisson) * (1 - 2 * poisson))

    # compute stiffness matrix
    ke = volume * numpy.matmul(numpy.transpose(B), numpy.matmul(D, B))

    return ke


def globalStiffnessMatrix(points, connectivity, young, poisson):
    """
    This function assembles elementary stiffness matrices to computes an elastic
    (3 dof) global stiffness matrix for a 4 noded tetrahedra mesh

    Notations
    ---------
        neq: number of global equations
        nel: number of elements
        npo: number of points
        neq = 3 x npo

    Parameters
    ----------
        points : npo x 3 array
            Array of the 3D coordinates of the all nodes points
        connectivity : nel x 4 array
            Connectivity matrix
        young: float
            Young modulus
        poisson: float
            Poisson ratio

    Returns
    -------
        stiffness_matrix : neq x neq array
            The stiffness matrix of the tetrahedron

    Note
    -----
        Pure python function.
    """
    # cast to numpy array
    points = numpy.array(points)
    connectivity = numpy.array(connectivity)

    neq = 3 * points.shape[0]
    # nel = connectivity.shape[0]
    K = numpy.zeros((neq, neq), dtype=float)

    for e, element_nodes_number in enumerate(connectivity):
        # print(f'Element number {e}: {element_nodes_number}')

        # built local stiffness matrix (12x12)
        element_points = [points[A] for A in element_nodes_number]
        ke = elementaryStiffnessMatrix(element_points, young, poisson)

        # loop over stiffness matrix (lines and rows)
        for p1 in range(12):
            i1 = p1 % 3  # deduce degree of freedom
            a1 = (p1 - i1) // 3  # deduce local node number
            P1 = 3 * int(connectivity[e, a1]) + i1  # get global equation number
            for p2 in range(p1, 12):
                i2 = p2 % 3
                a2 = (p2 - i2) // 3
                P2 = 3 * int(connectivity[e, a2]) + i2
                K[P1, P2] += ke[p1, p2]

    K = K + K.transpose()
    K[numpy.diag_indices(neq)] *= 0.5

    return K


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import spam.mesh

    # points = [
    #     [0, 0, 0],
    #     [0, 1, 0],
    #     [0, 0, 1],
    #     [1, 0, 0]
    # ]
    #
    # coefficients_matrix = shapeFunctions(points)
    # ke = elementaryStiffnessMatrix(points, 1, 0.3)
    # print(f'Elementary connectivity matrix: {ke.shape}')
    # # print(ke)

    lengths = [1, 1, 1]
    lc = 0.2
    points, connectivity = spam.mesh.createCuboid(
        lengths,
        lc,
        origin=[0.0, 0.0, 0.0],
        periodicity=False,
        verbosity=1,
        gmshFile=None,
        vtkFile=None,
        binary=False,
        skipOutput=False,
    )

    K = globalStiffnessMatrix(points, connectivity, 1, 0.3)

    plt.imshow(numpy.log(K[:100, :100]))
    plt.show()

    # ID function
    def ID(i: int, A: int):
        """
        Defined as in Hughes: The Finite Element Method eq. 2.8.3
        WARNING: without the condition of dirichlet boundary conditions
        Takes
            - the degree of freedom: i = 0, 1 or 2
            - the node global number: A = 0, 1, 2, ... n_nodes
        Returns
            - the global equation number: P = 0, 1, 2 ... 3 * n_nodes
        """
        P = 3 * A + i
        return int(P)

    # for A, point in enumerate(points):
    #     for i in range(3):
    #         print(f'Node number {A} dof {i}: {ID(i, A)}')

    # IEN function
    def IEN(a: int, e: int, connectivity):
        """
        Defined as in Hughes: The Finite Element Method eq. 2.6.1
        Takes
            - the local node number: a = 0, 1, 2 or 3
            - the element number: e = 0, 1, 2, ... n_elem
        Returns
            - the node global number: A = 0, 1, 2, ... n_nodes
        Uses the connectivity matrix
        """
        # connectivity matrix shape: n_elem x 4
        A = connectivity[e, a]
        return int(A)

    # for e, _ in enumerate(connectivity):
    #     for a in range(4):
    #         print(f'Element number {e} node number {a}: {IEN(a, e, connectivity)}')

    # LM function
    def LM(i: int, a: int, e: int, connectivity):
        """
        Defined as in Hughes: The Finite Element Method eq. 2.10.1
        Takes
            - the degree of freedom: i = 0, 1 or 2
            - the local node number: a = 0, 1, 2 or 3
            - the element number: e = 0, 1, 2, ... n_elem
        Returns
            - the global equation number: P = 0, 1, 2 ... 3 * n_nodes
        Uses the connectivity matrix
        """
        P = ID(i, IEN(a, e, connectivity))
        return P

    # for e, _ in enumerate(connectivity):
    #     for a in range(4):
    #         for i in range(3):
    #             P = 3 * int(connectivity[e, a]) + i
    #             print(f'Element number {e} node number {a} dof {i}: {LM(i, a, e, connectivity)}')
    #
    #
    #     if e == 3:
    #         break
