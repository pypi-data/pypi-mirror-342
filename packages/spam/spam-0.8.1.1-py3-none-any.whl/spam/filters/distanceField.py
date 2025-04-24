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


import numpy
import scipy


def distanceField(phases, phaseID=1):
    """
    This function tranforms an array/image of integers into a continuous field.
    It works for segmented binary/trinary 3D images or arrays of integers.
    It has to be run for each phase seperately.

    It uses of the **Distance Transform Algorithm**.
    For every voxel belonging to a phase a value indicating the distance
    (in voxels) of that point to the nearest background point is computed.
    The DTA is computed for the inverted image as well and the computed
    distances are setting to negative values.
    The 2 distance fields are merged into the final continuuos distance field
    where:

    .. code-block:: text

        - positive numbers: distances from the phase to the nearest background
        voxel
        - negative values: distances from the background to the nearest phase
        voxel
        - zero values: the interface between the considered phase and the
        background

    Parameters
    -----------
        phases : array
            The input image/array (each phase should be represented with only
            one number)

        phaseID : int, default=1
            The integer indicating the phase which distance field you want to
            calculate

    Returns
    --------
        distance field of the phase: array

    Example
    --------
        >>> import tifffile
        >>> import spam.filters
        >>> im = tifffile.imread( "mySegmentedImage.tif" )
        In this image the inclusions are labelled 1 and the matrix 0
        >>> di = spam.filters.distanceField( im, phase=1 )
        The resulting distance field is made of float between -1 and 1

    """
    # create binary image from phases and phaseID
    binary = numpy.zeros_like(phases, dtype=bool)
    binary[phases == phaseID] = True

    # Create the complementary binary image
    binaryNot = numpy.logical_not(binary)

    # Calculate the distance algorithm for the 2 binary images

    binaryDist = scipy.ndimage.distance_transform_edt(binary).astype("<f4")
    binaryNotDist = scipy.ndimage.distance_transform_edt(binaryNot).astype("<f4")

    # normalise if needed

    # if normalise:
    #     binaryDist = binaryDist / binaryDist.max()

    # if normalise:
    #     binaryNotDist = binaryNotDist.astype(float)
    #     binaryNotDist = binaryNotDist / binaryNotDist.max()

    # Step 5: Merge the 2 distance fields into the final one
    binaryNotDist = (-1.0) * binaryNotDist
    binaryNotDist = binaryNotDist + binaryDist

    return binaryNotDist
