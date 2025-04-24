"""
Library of SPAM image correlation functions.
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import multiprocessing

import numpy
import progressbar
import spam.label
from spambind.DIC.DICToolkit import pixelSearch as pixelSearchCPP


def _errorCalc(im1, im2):
    return numpy.nansum(numpy.square(numpy.subtract(im1, im2))) / numpy.nansum(im1)


def _pixelSearch(imagette1, imagette2, imagette1mask=None, imagette2mask=None, returnError=False):
    """
    This function performs a pixel-by-pixel search in 3D for a small reference imagette1 within a larger imagette2.

    The normalised correlation coefficient (NCC) is computed for EVERY combination of the displacements of imagette1 defined within imagette2.
    What is returned is the highest NCC value obtained and the position where it was obtained with respect to the origin in imagette2.

    Values of NCC > 0.99 can generally be trusted.

    Parameters
    ----------
        imagette1 : 3D numpy array of floats
            Imagette 1 is the smaller reference image

        imagette2 : 3D numpy array of floats
            Imagette 2 is the bigger image inside which to search

        imagette1mask : 3D numpy array of bools, optional
            A mask for imagette1 to define which pixels to include in the correlation
            (True = Correlate these pixels, False = Skip),
            Default = no mask

        imagette2mask : 3D numpy array of bools, optional
            A mask for imagette2 to define which pixels to include in the correlation
            (True = Correlate these pixels, False = Skip),
            Default = no mask

        returnError : bool, optional
            Return a normalised sum of squared differences error compatible with
            register() family of functions? If yes, it's the last returned variable
            Default = False

    Returns
    -------
        p : 3-component vector
            Z, Y, X position with respect to origin in imagette2 of imagette1 to get best NCC

        cc : float
            Normalised correlation coefficient, ~0.5 is random, >0.99 is very good correlation.
    """
    # Note
    # ----
    # It important to remember that the C code runs A BIT faster in its current incarnation when it has
    # a cut-out im2 to deal with (this is related to processor optimistaions).
    # Cutting out imagette2 to just fit around the search range might save a bit of time
    assert numpy.all(imagette2.shape >= imagette1.shape), "spam.DIC.pixelSearch(): imagette2 should be bigger or equal to imagette1 in all dimensions"

    if imagette1mask is not None:
        assert imagette1.shape == imagette1mask.shape, "spam.DIC.pixelSearch: imagette1mask ({}) should have same size as imagette1 ({})".format(imagette1mask.shape, imagette1.shape)
        imagette1 = imagette1.astype("<f4")
        imagette1[imagette1mask == 0] = numpy.nan

    if imagette2mask is not None:
        assert imagette2.shape == imagette2mask.shape, "spam.DIC.pixelSearch: imagette2mask ({}) should have same size as imagette2 ({})".format(imagette2mask.shape, imagette2.shape)
        imagette2 = imagette2.astype("<f4")
        imagette2[imagette2mask == 0] = numpy.nan

    # Run the actual pixel search
    returns = numpy.zeros(4, dtype="<f4")
    pixelSearchCPP(imagette1.astype("<f4"), imagette2.astype("<f4"), returns)

    if returnError:
        error = _errorCalc(
            imagette1,
            imagette2[
                int(returns[0]) : int(returns[0]) + imagette1.shape[0],
                int(returns[1]) : int(returns[1]) + imagette1.shape[1],
                int(returns[2]) : int(returns[2]) + imagette1.shape[2],
            ],
        )
        return numpy.array(returns[0:3]), returns[3], error

    else:
        return numpy.array(returns[0:3]), returns[3]


def pixelSearchDiscrete(
    lab1, im1, im2, searchRange, PhiField=None, labelsToCorrelate=None, boundingBoxes=None, centresOfMass=None, applyF="all", labelDilate=1, volThreshold=100, numProc=multiprocessing.cpu_count()
):
    """
    Discrete pixel search over all labels in a labelled volume, given a displacement search range.
    This is the python function called by spam-pixelSearch when given a labelled image.

    Parameters
    ----------
        lab1 : 2D or 3D numpy array of ints
            Array representing L labelled objects to search for in the reference configuration max(lab1) = L

        im1 : 2D or 3D numpy array of greylevels
            Array representing greylevels in the reference configuration, same size as lab1

        im2 : 2D or 3D numpy array of greylevels
            Array representing greylevels in the deformed configuration, same size as lab1

        searchRange : 1D numpy array of signed ints
            Array defining search range in [low Z, high Z, low Y, high Y, low X, high X]

        PhiField : L+1 x 4 x 4 numpy array of floats, optional
            Optional initial guess for Phi for each particle, default guess for each particle = identity matrix

        labelsToCorrelate : 1D numpy array of ints, optional
            Array containing which labels to correlate, default=all of them

        centresOfMass : L+1 x 3 numpy array of floats, optional
            Label centres of mass for particles as coming out of spam.label.boundingBoxes, default = it's recalculated on lab1

        boundingBoxes : L+1 x 3 numpy array of ints, optional
            Bounding boxes for particles as coming out of spam.label.boundingBoxes, default = it's recalculated on lab1

        applyF : string, optional
            Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "all" is default

        labelDilate : int, optional
            Number of times to dilate labels. Default = 1

        volThreshold : int, optional
            Volume threshold below which labels are ignored. Default = 100

        numProc : int, optional
            Number of processes to use for the calculation, default = multiprocessing.cpu_count()

    Returns
    -------
        Dictionary including the following keys for all labels, but only filled in correlated labels:
            - PhiField : L+1 x 4 x 4 numpy array of floats: Phi for each label
            - pixelSearchCC: L+1 numpy array of floats: Correlation Coefficient for each label bounded [0, 1]
            - error: L+1 numpy array of floats: SSQD per pixel for each label
            - returnStatus: L+1 numpy array of ints: returnStatus for each label
            - deltaPhiNorm: L+1 numpy array of floats: 1 for each label TODO decide if this is worth doing here
            - iterations: L+1 numpy array of ints: 1 for each label TODO decide if this is worth doing here
    """

    nLabels = numpy.max(lab1)

    if PhiField is None:
        PhiField = numpy.zeros((nLabels + 1, 4, 4), dtype="<f4")
        for label in range(nLabels + 1):
            PhiField[label] = numpy.eye(4)
    else:
        assert PhiField.shape[0] == nLabels + 1
        assert PhiField.shape[1] == 4
        assert PhiField.shape[2] == 4

    if labelsToCorrelate is None:
        labelsToCorrelate = numpy.arange(1, nLabels + 1)
    else:
        assert labelsToCorrelate.dtype.kind in numpy.typecodes["AllInteger"]
        assert numpy.min(labelsToCorrelate) >= 1
        assert numpy.max(labelsToCorrelate) <= nLabels

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab1)

    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab1)

    assert applyF in ["all", "no", "rigid"]

    # Create pixelSearchCC vector
    pixelSearchCC = numpy.zeros((nLabels + 1), dtype=float)
    # Error compatible with register()
    error = numpy.zeros((nLabels + 1), dtype=float)
    returnStatus = numpy.ones((nLabels + 1), dtype=int)
    # deltaPhiNorm = numpy.ones((nLabels+1), dtype=int)
    iterations = numpy.ones((nLabels + 1), dtype=int)

    numberOfNodes = len(labelsToCorrelate)

    # CHECK THIS
    # firstNode = 1
    # finishedNodes = 1
    returnStatus[0] = 0

    global _multiprocessingPixelSearchOneNodeDiscrete

    def _multiprocessingPixelSearchOneNodeDiscrete(nodeNumber):
        """
        Function to be called by multiprocessing parallelisation for pixel search in one position.
        This function will call getImagettes, or the equivalent for labels and perform the pixel search

        Parameters
        ----------
            nodeNumber : int
                node number to work on

        Returns
        -------
            List with:
                - nodeNumber (needed to write result in right place)
                - displacement vector
                - NCC value
                - error value
                - return Status
        """

        imagetteReturns = spam.label.getImagettesLabelled(
            lab1,
            nodeNumber,
            PhiField[nodeNumber].copy(),
            im1,
            im2,
            searchRange.copy(),
            boundingBoxes,
            centresOfMass,
            margin=labelDilate,
            labelDilate=labelDilate,
            applyF=applyF,
            volumeThreshold=volThreshold,
        )
        imagetteReturns["imagette2mask"] = None

        # If getImagettes was successful (size check and mask coverage check)
        if imagetteReturns["returnStatus"] == 1:
            PSreturns = _pixelSearch(
                imagetteReturns["imagette1"], imagetteReturns["imagette2"], imagette1mask=imagetteReturns["imagette1mask"], imagette2mask=imagetteReturns["imagette2mask"], returnError=True
            )
            pixelSearchOffset = imagetteReturns["pixelSearchOffset"]

            return (nodeNumber, PSreturns[0] + pixelSearchOffset, PSreturns[1], PSreturns[2], imagetteReturns["returnStatus"])

        # Failed to extract imagettes or something
        else:
            return (nodeNumber, numpy.array([numpy.nan] * 3), 0.0, numpy.inf, imagetteReturns["returnStatus"])

    print("\n\tStarting Pixel Search Discrete (with {} process{})".format(numProc, "es" if numProc > 1 else ""))

    widgets = [
        progressbar.FormatLabel(""),
        " ",
        progressbar.Bar(),
        " ",
        progressbar.AdaptiveETA(),
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
    pbar.start()
    finishedNodes = 0

    with multiprocessing.Pool(processes=numProc) as pool:
        for returns in pool.imap_unordered(_multiprocessingPixelSearchOneNodeDiscrete, labelsToCorrelate):
            finishedNodes += 1

            # Update progres bar if point is not skipped
            if returns[4] > 0:
                widgets[0] = progressbar.FormatLabel("  CC={:0>7.5f} ".format(returns[2]))
                pbar.update(finishedNodes)

            PhiField[returns[0], 0:3, -1] = returns[1]
            # Create pixelSearchCC vector
            pixelSearchCC[returns[0]] = returns[2]
            error[returns[0]] = returns[3]
            returnStatus[returns[0]] = returns[4]
        pool.close()
        pool.join()

    pbar.finish()

    return {
        "PhiField": PhiField,
        "pixelSearchCC": pixelSearchCC,
        "error": error,
        "returnStatus": returnStatus,
        # "deltaPhiNorm" : deltaPhiNorm,
        "iterations": iterations,
    }


def pixelSearchLocal(
    im1,
    im2,
    hws,
    searchRange,
    nodePositions,
    PhiField=None,
    # twoD=False,
    im1mask=None,
    im2mask=None,
    applyF="all",
    maskCoverage=0.5,
    greyLowThresh=-numpy.inf,
    greyHighThresh=numpy.inf,
    numProc=multiprocessing.cpu_count(),
):
    """
    Performs a series of pixel searches at given coordinates extracting a parallelepiped axis aligned box.

    Parameters
    ----------
        im1 :  2D or 3D numpy array of greylevels
            Array representing greylevels in the reference configuration

        im2 :  2D or 3D numpy array of greylevels
            Array representing greylevels in the reference configuration, same size as im1

        hws : a 3-element list of ints
            Z, Y, X extents of the "Half-window" size for extraction of the correlation window around the pixel of interest defined in nodePositions

        searchRange : 1D numpy array of signed ints
            Array defining search range in [low Z, high Z, low Y, high Y, low X, high X]

        nodePositions : N x 3 numpy array of ints
            Z, Y, X positions of points to correlate, around which to extract the HWS box

        PhiField : N x 4 x 4 numpy array of floats, optional
            Optional initial guess for Phi for each correlation point.
        Default = 4x4 identity matrix

        im1mask : 3D numpy array of bools, optional
            Binary array, same size as im1, which is True in for pixels in im1 that should be included in the correlation
            Default = all the pixels in im1

        im2mask : 3D numpy array of bools, optional
            Binary array, same size as im1, which is True in for pixels in im2 that should be included in the correlation
            Default = all the pixels in im2

        applyF : string, optional
            Apply the F part of Phi guess? Accepted values are:\n\t"all": apply all of F' + '\n\t"rigid": apply rigid part (mostly rotation) \n\t"no": don\'t apply it "all" is default

        maskCoverage : float, optional
            For a given correlation window, what fraction of pixels should be within the mask (if passed) to consider the correlation window for correlation,
            otherwise it will be skipped with return status = -5 as per spam.DIC.grid.getImagettes().
            Default = 0.5

        greyLowThresh : float, optional
            Mean grey value in im1 above which a correlation window will be correlated, below this value it will be skipped.
            Default = -numpy.inf

        greyHighThresh : float, optional
            Mean grey value in im1 below which a correlation window will be correlated, above this value it will be skipped.
            Default = numpy.inf

        numProc : int, optional
            Number of processes to use for the calculation, default = multiprocessing.cpu_count()

    Returns
    -------
        Dictionary including the following keys for all window, but only filled in correlated window:
            - PhiField : L+1 x 4 x 4 numpy array of floats: Phi for each window
            - pixelSearchCC: L+1 numpy array of floats: Correlation Coefficient for each window bounded [0, 1]
            - error: L+1 numpy array of floats: SSQD per pixel for each window
            - returnStatus: L+1 numpy array of ints: returnStatus for each window
            - deltaPhiNorm: L+1 numpy array of floats: 1 for each window TODO decide if this is worth doing here
            - iterations: L+1 numpy array of ints: 1 for each window TODO decide if this is worth doing here
    """
    numberOfNodes = nodePositions.shape[0]
    if len(im1.shape) == 2:
        twoD = True
    else:
        twoD = False

    # Create pixelSearchCC vector
    pixelSearchCC = numpy.zeros((numberOfNodes), dtype=float)
    # Error compatible with register()
    error = numpy.zeros((numberOfNodes), dtype=float)
    returnStatus = numpy.ones((numberOfNodes), dtype=int)
    deltaPhiNorm = numpy.ones((numberOfNodes), dtype=int)

    iterations = numpy.ones((numberOfNodes), dtype=int)

    firstNode = 0
    finishedNodes = 0

    global _multiprocessingPixelSearchOneNodeLocal

    def _multiprocessingPixelSearchOneNodeLocal(nodeNumber):
        """
        Function to be called by multiprocessing parallelisation for pixel search in one position.
        This function will call getImagettes, or the equivalent for labels and perform the pixel search

        Parameters
        ----------
            nodeNumber : int
                node number to work on

        Returns
        -------
            List with:
                - nodeNumber (needed to write result in right place)
                - displacement vector
                - NCC value
                - error value
                - return Status
        """
        imagetteReturns = spam.DIC.getImagettes(
            im1,
            nodePositions[nodeNumber],
            hws,
            PhiField[nodeNumber].copy(),
            im2,
            searchRange.copy(),
            im1mask=im1mask,
            im2mask=im2mask,
            minMaskCoverage=maskCoverage,
            greyThreshold=[greyLowThresh, greyHighThresh],
            applyF=applyF,
            twoD=twoD,
        )

        # If getImagettes was successful (size check and mask coverage check)
        if imagetteReturns["returnStatus"] == 1:
            PSreturns = _pixelSearch(
                imagetteReturns["imagette1"], imagetteReturns["imagette2"], imagette1mask=imagetteReturns["imagette1mask"], imagette2mask=imagetteReturns["imagette2mask"], returnError=True
            )
            pixelSearchOffset = imagetteReturns["pixelSearchOffset"]

            return (nodeNumber, PSreturns[0] + pixelSearchOffset, PSreturns[1], PSreturns[2], imagetteReturns["returnStatus"])

        # Failed to extract imagettes or something
        else:
            return (nodeNumber, numpy.array([numpy.nan] * 3), 0.0, numpy.inf, imagetteReturns["returnStatus"])

    print("\n\tStarting Pixel Search Local (with {} process{})".format(numProc, "es" if numProc > 1 else ""))

    widgets = [
        progressbar.FormatLabel(""),
        " ",
        progressbar.Bar(),
        " ",
        progressbar.AdaptiveETA(),
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
    pbar.start()
    # finishedNodes = 0

    with multiprocessing.Pool(processes=numProc) as pool:
        for returns in pool.imap_unordered(_multiprocessingPixelSearchOneNodeLocal, range(firstNode, numberOfNodes)):
            finishedNodes += 1

            # Update progres bar if point is not skipped
            if returns[4] > 0:
                widgets[0] = progressbar.FormatLabel("  CC={:0>7.5f} ".format(returns[2]))
                pbar.update(finishedNodes)

            PhiField[returns[0], 0:3, -1] = returns[1]
            # Create pixelSearchCC vector
            pixelSearchCC[returns[0]] = returns[2]
            error[returns[0]] = returns[3]
            returnStatus[returns[0]] = returns[4]
        pool.close()
        pool.join()

    pbar.finish()

    return PhiField, pixelSearchCC, error, returnStatus, deltaPhiNorm, iterations
