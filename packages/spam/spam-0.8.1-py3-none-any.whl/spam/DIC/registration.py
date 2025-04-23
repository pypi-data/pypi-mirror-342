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

import numpy
import progressbar
import spam.deformation
import spam.DIC
import spam.label  # for im1mask

# 2017-05-29 ER and EA
# This is spam's C++ DIC toolkit, but since we're in the tools/ directory we can import it directly
from spambind.DIC.DICToolkit import computeDICjacobian, computeDICoperators

# numpy.set_printoptions(precision=3, suppress=True)


def _errorCalc(im1, im2):
    return numpy.nansum(numpy.square(numpy.subtract(im1, im2))) / numpy.nansum(im1)


def register(
    im1,
    im2,
    im1mask=None,
    returnPhiMaskCentre=False,
    PhiInit=None,
    PhiRigid=False,
    PhiInitBinRatio=1.0,
    margin=None,
    maxIterations=25,
    deltaPhiMin=0.001,
    updateGradient=False,
    interpolationOrder=1,
    interpolator="python",
    verbose=False,
    imShowProgress=False,
    imShowProgressNewFig=False,
    imShowProgressPause=0.01,
):
    r"""
    Perform subpixel image correlation between im1 and im2.

    The result of register(im1, im2) will give a deformation function :math:`\Phi` which maps im1 into im2.
    The Phi function used here allows the measurement of sub-pixel displacements, rotation, and linear straining of the whole image.
    However, this function will numerically deform im2 until it best matches im1.

    :math:`im1(x) = im2(\Phi.x)`

    If im1 and im2 follow each other in time, then the resulting Phi is im1 -> im2 which makes sense in most cases.
    "Discrete correlation" can be performed by masking im1.

    im1 and im2 do not necessarily have to be the same size (`i.e.`, im2 can be bigger) -- this is good since there
    is a zone to accommodate movement. In the case of a bigger im2, im1 and im2 are assumed to be centred with respect to each other.

    Parameters
    ----------
        im1 : 3D numpy array
            The greyscale image that will not move -- must not contain NaNs

        im2 : 3D numpy array
            The greyscale image that will be deformed -- must not contain NaNs

        im1mask : 3D boolean numpy array, optional
            A mask for the zone to correlate in im1 with `False` in the zone to not correlate.
            Default = None, `i.e.`, correlate all of im1 minus the margin.
            If this is defined, the Phi returned is in the centre of mass of the mask

        returnPhiMaskCentre : bool, optional
            In case a mask is passed, should the Phi be returned at the centre of mass of the mask?
            Default = False

        PhiInit : 4x4 numpy array, optional
            Initial deformation to apply to im1.
            Default = numpy.eye(4), `i.e.`, no transformation

        PhiRigid : bool, optional
            Run a rigid correlation? Only the rigid part of your PhiInit will be kept.
            Default = False

        PhiInitBinRatio : float, optional
            Change translations in PhiInit, if it's been calculated on a differently-binned image. Default = 1

        margin : int, optional
            Margin, in pixels, to take in im1.
            Can also be a N-component list of ints, representing the margin in ND.
            If im2 has the same size as im1 this is strictly necessary to allow space for interpolation and movement
            Default = None (`i.e.`, 10% of max dimension of im1)

        maxIterations : int, optional
            Maximum number of quasi-Newton iterations to perform before stopping. Default = 25

        deltaPhiMin : float, optional
            Smallest change in the norm of Phi (the transformation operator) before stopping. Default = 0.001

        updateGradient : bool, optional
            Should the gradient of the image be computed (and updated) on the deforming im2?
            Default = False (it is computed once on im1)

        interpolationOrder : int, optional
            Order of the greylevel interpolation for applying Phi to im1 when correlating. Recommended value is 3, but you can get away with 1 for faster calculations. Default = 3

        interpolator : string, optional
            Which interpolation function to use from `spam`.
            Default = 'python'. 'C' is also an option

        verbose : bool, optional
            Get to know what the function is really thinking, recommended for debugging only.
            Default = False

        imShowProgress : bool, optional
            Pop up a window showing a ``imShowProgress`` slice of the image differences (im1-im2) as im1 is progressively deformed.
            Default = False

        imShowProgressNewFig : bool, optional (defaul = False)
                Make a new plt.figure for each iteration, useful for examples gallery

        imShowProgressPause : float, optional (defaul = 0.01)
                Seconds to pause between imShowProgress updates

    Returns
    -------
        Dictionary :

            'Phi' : 4x4 float array
                Deformation function defined at the centre of the image

            'returnStatus' : signed int
                Return status from the correlation:

                2 : Achieved desired precision in the norm of delta Phi

                1 : Hit maximum number of iterations while iterating

                -1 : Error is more than 80% of previous error, we're probably diverging

                -2 : Singular matrix M (most probably image texture problem)

                -3 : Displacement > 5*margin

                -4 : Singular Phi matrix (most probably due to divergence)

                -5 : Not used in this funciton but reserved for the script (correlation skipped)

            'error' : float
                Error float describing mismatch between images, it's the sum of the squared difference divided by the sum of im1

            'iterations' : int
                Number of iterations

            'deltaPhiNorm' : float
                Norm of deltaPhi

    Note
    ----
        This correlation was written in the style of S. Roux (especially "An extension of Digital Image Correlation for intermodality image registration")
        especially equations 12 and 13.
    """
    # Explicitly set input images to floats
    im1 = im1.astype("<f4")
    im2 = im2.astype("<f4")

    # initialise exit clause for singular "M" and Phi matrices
    singularM = False
    singularPhi = False

    # 2022-06-03 GP: Setting deltaPhiMin to only positive values
    deltaPhiMin = numpy.abs(deltaPhiMin)

    # Detect unpadded 2D image first:
    if im1.ndim == 2:
        # pad them
        im1 = im1[numpy.newaxis, ...]
        im2 = im2[numpy.newaxis, ...]
        if im1mask is not None:
            im1mask = im1mask[numpy.newaxis, ...]

    # Detect 2D images
    if im1.shape[0] == 1:
        twoD = True

        # Override interpolator for python in 2D
        interpolator = "python"

        # Define masks for M and A in 2D since we'll ignore the Z components
        # Components of M and A which don't include Z
        twoDmaskA = numpy.zeros((12), dtype=bool)
        for i in [5, 6, 7, 9, 10, 11]:
            twoDmaskA[i] = True

        twoDmaskM = numpy.zeros((12, 12), dtype=bool)
        for y in range(12):
            for x in range(12):
                if twoDmaskA[y] and twoDmaskA[x]:
                    twoDmaskM[y, x] = True

    else:
        twoD = False

    if interpolationOrder > 1:
        # Override interpolator for python for higher than linear
        interpolator = "python"

    # Automatically calculate margin if none is passed
    # Detect default case and calculate maring necessary for a 45deg rotation with no displacement
    if margin is None:
        if twoD:
            # z-margin will be overwritten below
            margin = [1 + int(0.1 * min(im1.shape[1:]))] * 3
        else:
            margin = [1 + int(0.1 * min(im1.shape))] * 3
    elif type(margin) == list:
        pass
    else:
        # Make sure margin is an int
        margin = int(margin)
        margin = [margin] * 3

    # Make sure im2 is bigger than im1 and check difference in size
    # Get difference in image sizes. This should be positive, since we must always have enough data for im2 interpolation
    im1im2sizeDiff = numpy.array(im2.shape) - numpy.array(im1.shape)

    # Check im2 is bigger or same size
    if (im1im2sizeDiff < 0).any():
        print("\tcorrelate.register(): im2 is smaller than im1 in at least one dimension: im2.shape: {}, im1.shape: {}".format(im2.shape, im1.shape))
        raise ValueError("correlate.register():DimProblem")

    # Make sure margin is at least 1 for the gradient calculation
    if twoD:
        margin[0] = 0
    elif min(margin) < 1 and min(im1im2sizeDiff) == 0:
        margin = [1] * 3

    # Calculate crops -- margin for im2 and more for im1 if it is bigger
    # Margin + half the difference in size for im2 -- im1 will start in the middle.
    crop2 = (
        slice(
            int(im1im2sizeDiff[0] / 2 + margin[0]),
            int(im1im2sizeDiff[0] / 2 + im1.shape[0] - margin[0]),
        ),
        slice(
            int(im1im2sizeDiff[1] / 2 + margin[1]),
            int(im1im2sizeDiff[1] / 2 + im1.shape[1] - margin[1]),
        ),
        slice(
            int(im1im2sizeDiff[2] / 2 + margin[2]),
            int(im1im2sizeDiff[2] / 2 + im1.shape[2] - margin[2]),
        ),
    )

    # Get subvolume crops from both images -- just the margin for im1
    crop1 = (
        slice(int(margin[0]), int(im1.shape[0] - margin[0])),
        slice(int(margin[1]), int(im1.shape[1] - margin[1])),
        slice(int(margin[2]), int(im1.shape[2] - margin[2])),
    )

    # Create im1 crop to shift less data
    im1crop = im1[crop1].copy()

    # Calculate effective margin
    # to calculate displacement divergence
    # using max for the margin -- subjective choice
    max(margin) + min(im1im2sizeDiff) / 2
    # print( "\tcorrelate.register(): realMargin is:", realMargin)

    # If live plot is asked for, initialise canvas
    if imShowProgress:
        import matplotlib.pyplot as plt

        # Plot ranges for signed residual
        vmin = -im1crop.max()
        vmax = im1crop.max()
        if not imShowProgressNewFig:
            if twoD:
                plt.subplot(1, 3, 1)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])
                plt.subplot(1, 3, 2)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])
                plt.subplot(1, 3, 3)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])

            else:  # 3D
                plt.subplot(3, 3, 1)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])
                plt.subplot(3, 3, 2)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])
                plt.subplot(3, 3, 3)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[1], 0])

                plt.subplot(3, 3, 4)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[0], 0])
                plt.subplot(3, 3, 5)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[0], 0])
                plt.subplot(3, 3, 6)
                plt.axis([im1crop.shape[2], 0, im1crop.shape[0], 0])

                plt.subplot(3, 3, 7)
                plt.axis([im1crop.shape[1], 0, im1crop.shape[0], 0])
                plt.subplot(3, 3, 8)
                plt.axis([im1crop.shape[1], 0, im1crop.shape[0], 0])
                plt.subplot(3, 3, 9)
                plt.axis([im1crop.shape[1], 0, im1crop.shape[0], 0])
                plt.ion()

    ###########################################################
    # Important -- since we're moving im2, initial Phis will be
    # pointing the wrong way, they need to be inversed
    ###########################################################
    # If there is no initial Phi, initalise it and im1defCrop to zero.
    if PhiInit is None:
        Phi = numpy.eye(4)
        im2def = im2.copy()

    else:
        # 2020-03-17 in isolation from COVID-19 EA and OS: Apparently this changes the PhiInit outside this function,
        #   Copying into different variable
        # Apply binning on displacement
        Phi = PhiInit.copy()

        # If we're in rigid mode, keep only translations and rotations for this guess
        # If you don't do this it goes mad (i.e., rigid updates to non-rigid guess don't seem to work)
        if PhiRigid:
            Phi = spam.deformation.computeRigidPhi(Phi.copy())
        Phi[0:3, -1] *= PhiInitBinRatio

        # invert PhiInit to apply it to im2
        try:
            PhiInv = numpy.linalg.inv(Phi.copy())
        except numpy.linalg.LinAlgError:
            PhiInv = numpy.eye(4)

        # Since we are now using Fcentred for iterations, do nothing
        # call decomposePhi to apply PhiInit (calculated on the centre of the image) to the origin (0,0,0)
        if interpolator == "C":
            im2def = spam.DIC.applyPhi(im2, Phi=PhiInv, interpolationOrder=interpolationOrder)

        elif interpolator == "python":
            im2def = spam.DIC.applyPhiPython(im2, Phi=PhiInv, interpolationOrder=interpolationOrder)

    def computeGradient(im, twoD):
        # Function to compute gradients
        if twoD:
            # If 2D image we have no gradients in the 1st direction
            # if verbose: print("Calculating gradients...", end="")
            imGradY, imGradX = numpy.gradient(im[0])
            imGradX = imGradX[numpy.newaxis, ...]
            imGradY = imGradY[numpy.newaxis, ...]
            imGradZ = numpy.zeros_like(imGradX)
            # if verbose: print("done")
        else:
            # if verbose: print("Calculating gradients...", end="")
            imGradZ, imGradY, imGradX = numpy.gradient(im)
            # if verbose: print("done ")
        return imGradZ, imGradY, imGradX

    # Apply stationary im1 mask
    if im1mask is not None:
        im1crop[im1mask[crop1] == 0] = numpy.nan

    # Initialise iteration variables
    iterations = 0
    returnStatus = 0
    # Big value to start with to ensure the first iteration
    deltaPhiNorm = 100.0
    error = _errorCalc(im1crop, im2def[crop2])

    if verbose:
        print("Start correlation with Error = {:0.2f}".format(error))

        widgets = [
            "    Iteration Number:",
            progressbar.Counter(),
            " ",
            progressbar.FormatLabel(""),
            " (",
            progressbar.Timer(),
            ")",
        ]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=maxIterations)
        # widgets = [progressbar.FormatLabel(''), ' ', progressbar.Bar(), ' ', progressbar.AdaptiveETA()]
        # pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
        pbar.start()

    # --- Start Iterations ---
    while iterations < maxIterations and deltaPhiNorm > deltaPhiMin:
        errorPrev = error

        # On first iteration, compute hessian and jacobian in any case
        #   ...or if we've been asked to update Gradient
        if iterations == 0 or updateGradient:
            # If we've been asked to update gradient, compute it on im2, which is moving
            if updateGradient:
                imGradZ, imGradY, imGradX = computeGradient(im2def, twoD)
                crop = crop2
            # Otherwise compute it once and for all on the non-moving im1
            else:
                imGradZ, imGradY, imGradX = computeGradient(im1, twoD)
                crop = crop1

            M = numpy.zeros((12, 12), dtype="<f8")
            A = numpy.zeros((12), dtype="<f8")

            # Compute both DIC operators A and M with C library
            computeDICoperators(
                im1crop.astype("<f4"),
                im2def[crop2].astype("<f4"),
                imGradZ[crop].astype("<f4"),
                imGradY[crop].astype("<f4"),
                imGradX[crop].astype("<f4"),
                M,
                A,
            )
        else:
            # just update jacobian A
            A = numpy.zeros((12), dtype="<f8")
            computeDICjacobian(
                im1crop.astype("<f4"),
                im2def[crop2].copy().astype("<f4"),
                imGradZ[crop].copy().astype("<f4"),
                imGradY[crop].copy().astype("<f4"),
                imGradX[crop].copy().astype("<f4"),
                A,
            )

        # Solve for delta Phi
        if twoD:
            # If a twoD image, cut out the bits of the M and A matrices that interest us
            #   This is necessary since the rest is super singular
            # Solve for delta Phi
            try:
                deltaPhi = numpy.dot(numpy.linalg.inv(M[twoDmaskM].reshape(6, 6)), A[twoDmaskA])
            except numpy.linalg.LinAlgError:
                singularM = True
                break
            # ...and now put deltaPhi components back in place for a 3D deltaPhi
            deltaPhinew = numpy.zeros((12), dtype=float)
            deltaPhinew[twoDmaskA] = deltaPhi
            del deltaPhi
            deltaPhi = deltaPhinew
        else:
            # Solve for delta Phi
            try:
                deltaPhi = numpy.dot(numpy.linalg.inv(M), A)
            except numpy.linalg.LinAlgError:
                singularM = True
                break

        # If we're doing a rigid registration...
        if PhiRigid:
            # Add padding zeros
            deltaPhi = numpy.hstack([deltaPhi, numpy.zeros(4)]).reshape((4, 4))

            deltaPhiPlusI = numpy.eye(4) + deltaPhi
            # Keep only rigid part of deltaPhi
            deltaPhiPlusIrigid = spam.deformation.computeRigidPhi(deltaPhiPlusI.copy())

            # Subtract I from the rigid dPhi+1, and compute norm only on first 3 rows
            # ...basically recompute deltaPhiNorm only on rigid part
            deltaPhiNorm = numpy.linalg.norm((deltaPhiPlusIrigid - numpy.eye(4))[0:3].ravel())

            # Apply Delta Phi correction to Phi In Roux X-N paper equation number 11
            Phi = numpy.dot(Phi, deltaPhiPlusIrigid)

        else:
            # The general, non-rigid case
            deltaPhiNorm = numpy.linalg.norm(deltaPhi)

            # Add padding zeros
            deltaPhi = numpy.hstack([deltaPhi, numpy.zeros(4)]).reshape((4, 4))

            # Update Phi
            Phi = numpy.dot(Phi, (numpy.eye(4) + deltaPhi))

        try:
            PhiInv = numpy.linalg.inv(Phi.copy())
        except numpy.linalg.LinAlgError:
            singularPhi = True
            break

        # reset im1def as emtpy matrix for deformed image
        if interpolator == "C":
            im2def = spam.DIC.applyPhi(im2, Phi=PhiInv, interpolationOrder=interpolationOrder)
        elif interpolator == "python":
            im2def = spam.DIC.applyPhiPython(im2, Phi=PhiInv, interpolationOrder=interpolationOrder)

        # Error calculation
        error = _errorCalc(im1crop, im2def[crop2])

        # Keep interested people up to date with what's happening
        # if verbose:
        # print("Error = {:0.2f}".format(error)),
        # print("deltaPhiNorm = {:0.4f}".format(deltaPhiNorm))

        # Catch divergence condition after half of the max iterations
        if errorPrev < error * 0.8 and iterations > maxIterations / 2:
            # undo this bad Phi which has increased the error:
            # Phi = numpy.dot((numpy.eye(4) + deltaPhi), Phi)
            returnStatus = -1
            if verbose:
                print("\t -> diverging on error condition (returning -1)")
            break

        # Second divergence criterion on displacement (Issue #62)
        #   If any displcement is bigger than 5* the margin...
        # if (numpy.abs(spam.deformation.decomposePhi(Phi.copy())['t']) > 5 * realMargin).any():
        # if verbose: print("\t -> diverging on displacement condition")
        # returnStatus = -3
        # break

        # 2018-10-02 - EA: Add divergence condition on U
        trans = spam.deformation.decomposePhi(Phi.copy())
        try:
            volumeChange = numpy.linalg.det(trans["U"])
            if volumeChange > 3 or volumeChange < 0.2:
                if verbose:
                    print("\t -> diverging on volumetric change condition (returning -3)")
                returnStatus = -3
                break
        except Exception:
            print("\t -> can't compute det(U) (returning -3)")
            returnStatus = -3
            break

        if imShowProgress:
            if imShowProgressNewFig:
                plt.figure()
            else:
                plt.clf()

            if twoD:
                plt.suptitle("Iteration Number = {}".format(iterations), fontsize=10)
                plt.subplot(1, 3, 1)
                plt.title("im1")
                plt.imshow(im1crop[im1crop.shape[0] // 2, :, :], cmap="Greys_r", vmin=0, vmax=vmax)
                plt.subplot(1, 3, 2)
                plt.title("im2def")
                plt.imshow(
                    im2def[crop2][im1crop.shape[0] // 2, :, :],
                    cmap="Greys_r",
                    vmin=0,
                    vmax=vmax,
                )
                plt.subplot(1, 3, 3)
                plt.title("im1-im2def")
                plt.imshow(
                    numpy.subtract(im1crop, im2def[crop2])[im1crop.shape[0] // 2, :, :],
                    cmap="coolwarm",
                    vmin=vmin,
                    vmax=vmax,
                )
                plt.pause(imShowProgressPause)

            else:  # 3D
                plt.suptitle("Iteration Number = {}".format(iterations), fontsize=10)
                plt.subplot(3, 3, 1)
                plt.title("im1 Z-slice")
                plt.imshow(im1crop[im1crop.shape[0] // 2, :, :], cmap="Greys_r", vmin=0, vmax=vmax)
                plt.subplot(3, 3, 2)
                plt.title("im2def Z-slice")
                plt.imshow(
                    im2def[crop2][im1crop.shape[0] // 2, :, :],
                    cmap="Greys_r",
                    vmin=0,
                    vmax=vmax,
                )
                plt.subplot(3, 3, 3)
                plt.title("im1-im2def Z-slice")
                plt.imshow(
                    numpy.subtract(im1crop, im2def[crop2])[im1crop.shape[0] // 2, :, :],
                    cmap="coolwarm",
                    vmin=vmin,
                    vmax=vmax,
                )
                plt.subplot(3, 3, 4)
                plt.title("im1 Y-slice")
                plt.imshow(im1crop[:, im1crop.shape[1] // 2, :], cmap="Greys_r", vmin=0, vmax=vmax)
                plt.subplot(3, 3, 5)
                plt.title("im2def Y-slice")
                plt.imshow(
                    im2def[crop2][:, im1crop.shape[1] // 2, :],
                    cmap="Greys_r",
                    vmin=0,
                    vmax=vmax,
                )
                plt.subplot(3, 3, 6)
                plt.title("im1-im2def Y-slice")
                plt.imshow(
                    numpy.subtract(im1crop, im2def[crop2])[:, im1crop.shape[1] // 2, :],
                    cmap="coolwarm",
                    vmin=vmin,
                    vmax=vmax,
                )
                # if imShowProgress == "X" or imShowProgress == "x":
                # if imShowProgressNewFig: plt.figure()
                # else:                    plt.clf()
                plt.subplot(3, 3, 7)
                plt.title("im1 X-slice")
                plt.imshow(im1crop[:, :, im1crop.shape[2] // 2], cmap="Greys_r", vmin=0, vmax=vmax)
                plt.subplot(3, 3, 8)
                plt.title("im2def X-slice")
                plt.imshow(
                    im2def[crop2][:, :, im1crop.shape[2] // 2],
                    cmap="Greys_r",
                    vmin=0,
                    vmax=vmax,
                )
                plt.subplot(3, 3, 9)
                plt.title("im1-im2def X-slice")
                plt.imshow(
                    numpy.subtract(im1crop, im2def[crop2])[:, :, im1crop.shape[2] // 2],
                    cmap="coolwarm",
                    vmin=vmin,
                    vmax=vmax,
                )
                plt.pause(imShowProgressPause)

        iterations += 1

        if verbose:
            decomposedPhi = spam.deformation.decomposePhi(Phi.copy())
            widgets[3] = progressbar.FormatLabel(
                "  dPhiNorm={:0>7.5f}   error={:0>4.2f}   t=[{:0>5.3f} {:0>5.3f} {:0>5.3f}]   r=[{:0>5.3f} {:0>5.3f} {:0>5.3f}]   z=[{:0>5.3f} {:0>5.3f} {:0>5.3f}]".format(
                    deltaPhiNorm,
                    error,
                    decomposedPhi["t"][0],
                    decomposedPhi["t"][1],
                    decomposedPhi["t"][2],
                    decomposedPhi["r"][0],
                    decomposedPhi["r"][1],
                    decomposedPhi["r"][2],
                    decomposedPhi["z"][0],
                    decomposedPhi["z"][1],
                    decomposedPhi["z"][2],
                )
            )
            pbar.update(iterations)

    # Positive return status is a healthy end of while loop:
    if iterations >= maxIterations:
        returnStatus = 1
    if deltaPhiNorm <= deltaPhiMin:
        returnStatus = 2

    if singularM:
        returnStatus = -2
    elif singularPhi:
        returnStatus = -4

    if verbose:
        print()
        # pbar.finish()
        if iterations > maxIterations:
            print("\t -> No convergence before max iterations")
        if deltaPhiNorm <= deltaPhiMin:
            print("\t -> Converged")
        if singularM:
            print("\t -> Singular matrix M (most probably image texture problem)")
        if singularPhi:
            print("\t -> Singular Phi matrix (most probably due to divergence)")

    if im1mask is not None and returnPhiMaskCentre:
        # If a mask on im1 is defined, return an Phi at the centre of the mass
        maskCOM = spam.label.centresOfMass(im1mask[crop1])[-1]
        # print("Mask COM", maskCOM)
        # print( "\nNormal Phi:\n", Phi)
        Phi[0:3, -1] = spam.deformation.decomposePhi(
            Phi.copy(),
            PhiCentre=(numpy.array(im1crop.shape) - 1) / 2.0,
            PhiPoint=maskCOM,
        )["t"]
        # print( "\nPhi in mask:\n", Phi)

    return {
        "error": error,
        "Phi": Phi,
        "returnStatus": returnStatus,
        "iterations": iterations,
        "deltaPhiNorm": deltaPhiNorm,
    }


def registerMultiscale(
    im1,
    im2,
    binStart,
    binStop=1,
    im1mask=None,
    returnPhiMaskCentre=False,
    PhiInit=None,
    PhiRigid=False,
    PhiInitBinRatio=1.0,
    margin=None,
    maxIterations=100,
    deltaPhiMin=0.0001,
    updateGradient=False,
    interpolationOrder=1,
    interpolator="C",
    verbose=False,
    imShowProgress=False,
    forceChangeScale=False,
):
    """
    Perform multiscale subpixel image correlation between im1 and im2.

    This means applying a downscale (binning) to the images, performing a Lucas and Kanade at that level,
    and then improving it on a 2* less downscaled image, all the way back to the full scale image.

    If your input images have multiple scales of texture, this should save significant time.

    Please see the documentation for `register` for the rest of the documentation.

    Parameters
    ----------
        im1 : 3D numpy array
            The greyscale image that will not move -- must not contain NaNs

        im2 : 3D numpy array
            The greyscale image that will be deformed -- must not contain NaNs

        binStart : int
            Maximum amount of binning to apply, please input a number which is 2^int

        binStop : int, optional
            Which binning level to stop upscaling at.
            The value of 1 (full image resolution) is almost always recommended (unless memory/time problems).
            Default = 1

        im1mask : 3D boolean numpy array, optional
            A mask for the zone to correlate in im1 with `False` in the zone to not correlate.
            Default = None, `i.e.`, correlate all of im1 minus the margin.
            If this is defined, the Phi returned is in the centre of mass of the mask

        PhiInit : 4x4 numpy array, optional
            Initial deformation to apply to im1, by default at bin1 scale
            Default = numpy.eye(4), `i.e.`, no transformation

        PhiRigid : bool, optional
            Run a rigid correlation? Only the rigid part of your PhiInit will be kept.
            Default = False

        PhiInitBinRatio : float, optional
            Change translations in PhiInit, if it's been calculated on a differently-binned image. Default = 1

        margin : int, optional
            Margin, in pixels, to take in im1.
            Can also be a N-component list of ints, representing the margin in ND.
            If im2 has the same size as im1 this is strictly necessary to allow space for interpolation and movement
            Default = 0 (`i.e.`, 10% of max dimension of im1)

        maxIterations : int, optional
            Maximum number of quasi-Newton iterations to perform before stopping. Default = 25

        deltaPhiMin : float, optional
            Smallest change in the norm of Phi (the transformation operator) before stopping. Default = 0.001

        updateGradient : bool, optional
            Should the gradient of the image be computed (and updated) on the deforming im2?
            Default = False (it is computed once on im1)

        interpolationOrder : int, optional
            Order of the greylevel interpolation for applying Phi to im1 when correlating. Recommended value is 3, but you can get away with 1 for faster calculations. Default = 3

        interpolator : string, optional
            Which interpolation function to use from `spam`.
            Default = 'python'. 'C' is also an option

        verbose : bool, optional
            Get to know what the function is really thinking, recommended for debugging only. Default = False

        returnPhiMaskCentre : bool, optional
            In case a mask is passed, should the Phi returned by the function be returned at the centre of mass of the mask? If False, it's returned (as per no mask) in the centre of the image.
            Default = True

        imShowProgress : bool, optional
            Pop up a window showing a ``imShowProgress`` slice of the image differences (im1-im2) as im1 is progressively deformed.
            Default = False

        forceChangeScale : bool, optional
            Change up a scale even if not converged?
            Default = False

    Returns
    -------
        Dictionary:

            'Phi': 4x4 float array
                Deformation function defined at the centre of the image

            'returnStatus': signed int
                Return status from the correlation:

                2 : Achieved desired precision in the norm of delta Phi

                1 : Hit maximum number of iterations while iterating

                -1 : Error is more than 80% of previous error, we're probably diverging

                -2 : Singular matrix M (most probably image texture problem)

                -3 : Displacement > 5*margin

                -4 : Singular Phi matrix (most probably due to divergence)

                -5 : Not used in this funciton but reserved for the script (correlation skipped)

            'error': float
                Error float describing mismatch between images, it's the sum of the squared difference divided by the sum of im1

            'iterations': int
                Number of iterations
    """
    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        # pad them
        im1 = im1[numpy.newaxis, ...]
        im2 = im2[numpy.newaxis, ...]
        if im1mask is not None:
            im1mask = im1mask[numpy.newaxis, ...]

    # Detect 2D images
    if im1.shape[0] == 1:
        twoD = True
    else:
        twoD = False

    logbinstart = numpy.log2(binStart)
    if not logbinstart.is_integer():
        print(
            "spam.DIC.registerMultiscale(): You asked for an initial binning of",
            binStart,
            ",rounding it to ",
            end="",
        )
        binStart = 2 ** numpy.round(logbinstart)
        print(binStart)

    logbinstop = numpy.log2(binStop)
    if not logbinstop.is_integer():
        print(
            "spam.DIC.registerMultiscale(): You asked for a final binning of",
            binStop,
            ",rounding it to ",
            end="",
        )
        binStop = 2 ** numpy.round(logbinstop)
        print(binStop)

    # If there is no initial Phi, initalise it and im1defCrop to zero.
    if PhiInit is None:
        reg = {"Phi": numpy.eye(4)}
    else:
        # Apply binning on displacement   -- the /2 is to be able to *2 it in the LK call
        tmp = PhiInit.copy()
        tmp[0:3, -1] *= PhiInitBinRatio / 2.0 / float(binStart)
        reg = {"Phi": tmp}

    if im1mask is not None:
        # Multiply up to 100 so we can apply a threshold below on binning in %
        im1mask = im1mask.astype("<u1") * 100

    # Sorry... This generates a list of binning levels, if binStart=8 and binStop=2 this will be [8, 4 ,2]
    binLevels = 2 ** numpy.arange(numpy.log2(binStart), numpy.log2(binStop) - 1, -1).astype(int)
    for binLevel in binLevels:
        if verbose:
            print(
                "spam.DIC.registerMultiscale(): working on binning: ",
                binLevel,
            )
        if binLevel > 1:
            if twoD:
                import scipy.ndimage

                im1b = scipy.ndimage.zoom(im1[0], 1 / binLevel, order=1)
                im2b = scipy.ndimage.zoom(im2[0], 1 / binLevel, order=1)
                # repad them
                im1b = im1b[numpy.newaxis, ...]
                im2b = im2b[numpy.newaxis, ...]
                if im1mask is not None:
                    im1maskb = scipy.ndimage.zoom(im1mask[0], 1 / binLevel, order=1)
                    im1maskb = im1maskb[numpy.newaxis, ...]
                else:
                    im1maskb = None
            else:
                im1b = spam.DIC.binning(im1, binLevel)
                im2b = spam.DIC.binning(im2, binLevel)
                if im1mask is not None:
                    im1maskb = spam.DIC.binning(im1mask, binLevel) > 0
                else:
                    im1maskb = None
        else:
            im1b = im1
            im2b = im2
            if im1mask is not None:
                im1maskb = im1mask > 0
            else:
                im1maskb = None

        # Automatically calculate margin if none is passed
        # Detect default case and calculate margin necessary for a 45deg rotation with no displacement
        if margin is None:
            if twoD:
                # z-margin will be overwritten below
                marginB = [1 + int(0.1 * min(im1b.shape[1:]))] * 3
            else:
                marginB = [1 + int(0.1 * min(im1b.shape))] * 3

        elif type(margin) == list:
            marginB = (numpy.array(margin) // binLevel).tolist()

        else:
            # Make sure margin is an int
            margin = int(margin)
            margin = [margin] * 3
            marginB = (numpy.array(margin) // binLevel).tolist()

        reg = spam.DIC.register(
            im1b,
            im2b,
            im1mask=im1maskb,
            returnPhiMaskCentre=returnPhiMaskCentre,
            PhiInit=reg["Phi"],
            PhiRigid=PhiRigid,
            PhiInitBinRatio=2.0,
            margin=marginB,
            maxIterations=maxIterations,
            deltaPhiMin=deltaPhiMin,
            updateGradient=updateGradient,
            interpolationOrder=interpolationOrder,
            interpolator=interpolator,
            verbose=verbose,
            imShowProgress=imShowProgress,
        )

        if reg["returnStatus"] != 2 and not forceChangeScale:
            if verbose:
                print("spam.DIC.registerMultiscale(): binning {} did not converge (return Status = {}), not continuing".format(binLevel, reg["returnStatus"]))
                # Multiply up displacement and return bad result
            reg["Phi"][0:3, -1] *= float(binLevel)
            return reg

        binLevel = int(binLevel / 2)

    # Return displacments at bin1 scale
    reg["Phi"][0:3, -1] *= float(binStop)
    return reg
