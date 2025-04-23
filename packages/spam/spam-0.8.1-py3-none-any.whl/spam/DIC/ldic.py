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

import multiprocessing
import os

import numpy
import progressbar
import spam.deformation
import spam.DIC
import spam.helpers

os.environ["OPENBLAS_NUM_THREADS"] = "1"

numpy.seterr(all="ignore")


def ldic(
    im1,
    im2,
    nodePositions,
    hws,
    skipNodesMask=None,  # This will not work until we can recv returnStatus as input
    processes=None,
    im1mask=None,
    PhiField=None,  # Will be modified in situ!!
    margin=[-3, 3, -3, 3, -3, 3],
    maskCoverage=0.5,
    greyThreshold=[-numpy.inf, numpy.inf],
    applyF="all",
    maxIterations=50,
    deltaPhiMin=0.001,
    PhiRigid=False,
    updateGradient=False,
    interpolationOrder=1,
):
    """
    Function to perform local DIC/DVC (`i.e.`, running the spam.DIC.register function)
    correlating many 2D/3D boxes spread out typically on a regular grid of "nodes".

    Parameters
    ----------
        - im1 : 2/3D numpy array
            Reference image in which the nodes are defined, and from which the output Phi field is measured

        - im2 : 2/3D numpy array
            Deformed image

        - nodePositions : 2D numpy array of ints
            Nx2 or Nx3 matrix defining centres of boxes.
            This can be generated with `nodePositions, nodesDim = spam.DIC.makeGrid(im1.shape, nodeSpacing)`

        - hws : 3-component numpy array of ints
            This defines the half-size of the correlation window,
            i.e., how many pixels to extract in Z, Y, X either side of the centre.
            Note: for 2D Z = 0

        - skipNodes : 1D numpy array of bools, optional
            Vector of N bools which are true when nodes should be skipped.
            They will simply not be correlated, so ignore the outputs related to these nodes.
            If you have guesses for them, remember to merge them with the outputs for this function

        - processes : int, optional
            Number of processes to run the ldic on, by default it's the number of detected threads on your machine

        - for all other parameters see `spam.DIC.register()`
    """
    # Detect unpadded 2D image first:
    if len(im1.shape) == 2:
        im1 = im1[numpy.newaxis, ...]
    if im1.shape[0] == 1:
        twoD = True
    else:
        twoD = False

    numberOfNodes = nodePositions.shape[0]

    if processes is None:
        processes = multiprocessing.cpu_count()

    PhiFieldOut = numpy.zeros((numberOfNodes, 4, 4))
    if PhiField is None:
        for node in range(numberOfNodes):
            PhiFieldOut[node] = numpy.eye(4)
    else:
        PhiFieldOut = PhiField.copy()

    error = numpy.zeros(numberOfNodes)
    iterations = numpy.zeros(numberOfNodes)
    returnStatus = numpy.zeros(numberOfNodes)
    deltaPhiNorm = numpy.zeros(numberOfNodes)

    # Bad to redefine this for every loop, so it's defined here, to be called by the pool
    global _multiprocessingCorrelateOneNode

    # Bad to redefine this for every loop, so it's defined here, to be called by the pool
    def _multiprocessingCorrelateOneNode(nodeNumber):
        """
        This function does a correlation at one point and returns:

        Returns
        -------
            List of:
            - nodeNumber
            - Phi
            - returnStatus
            - error
            - iterations
            - deltaPhiNorm
        """
        PhiInit = PhiFieldOut[nodeNumber]
        if numpy.isfinite(PhiInit).sum() == 16:
            imagetteReturns = spam.DIC.getImagettes(
                im1,
                nodePositions[nodeNumber],
                hws,
                PhiInit.copy(),
                im2,
                margin,
                im1mask=im1mask,
                minMaskCoverage=maskCoverage,
                greyThreshold=greyThreshold,
                applyF="no",  # Needs to be "no"?
                twoD=twoD,
            )

            if imagetteReturns["returnStatus"] == 1:
                # compute displacement that will be taken by the getImagettes
                initialDisplacement = numpy.round(PhiInit[0:3, 3]).astype(int)
                PhiInit[0:3, -1] -= initialDisplacement

                registerReturns = spam.DIC.register(
                    imagetteReturns["imagette1"],
                    imagetteReturns["imagette2"],
                    im1mask=imagetteReturns["imagette1mask"],
                    PhiInit=PhiInit,  # minus initial displacement above, which is in the search range and thus taken into account in imagette2
                    margin=1,  # see top of this file for compensation
                    maxIterations=maxIterations,
                    deltaPhiMin=deltaPhiMin,
                    PhiRigid=PhiRigid,
                    updateGradient=updateGradient,
                    interpolationOrder=interpolationOrder,
                    verbose=False,
                    imShowProgress=False,
                )
                goodPhi = registerReturns["Phi"]
                goodPhi[0:3, -1] += initialDisplacement
                return nodeNumber, goodPhi, registerReturns["returnStatus"], registerReturns["error"], registerReturns["iterations"], registerReturns["deltaPhiNorm"]

            else:
                badPhi = numpy.eye(4)
                badPhi[0:3, 3] = numpy.nan
                return nodeNumber, badPhi, imagetteReturns["returnStatus"], numpy.inf, 0, numpy.inf
        else:
            # Phi has nans or infs
            badPhi = numpy.eye(4)
            badPhi[0:3, 3] = numpy.nan
            return nodeNumber, badPhi, -7, numpy.inf, 0, numpy.inf

    finishedNodes = 0

    # GP: Adding the skip function. TODO: returnStatus needs to be fed as an input to preserve it, otherwise is returned as 0.
    nodesToCorrelate = numpy.arange(0, numberOfNodes)

    if skipNodesMask is not None:
        nodesToCorrelate = nodesToCorrelate[numpy.logical_not(skipNodesMask)]
        numberOfNodes = numpy.sum(numpy.logical_not(skipNodesMask))

    print(f"\n\tStarting local dic for {numberOfNodes} nodes (with {processes} process{'es' if processes > 1 else ''})")

    widgets = [progressbar.FormatLabel(""), " ", progressbar.Bar(), " ", progressbar.AdaptiveETA()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=numberOfNodes)
    pbar.start()
    finishedNodes = 0

    with multiprocessing.Pool(processes=processes) as pool:
        for returns in pool.imap_unordered(_multiprocessingCorrelateOneNode, nodesToCorrelate):
            finishedNodes += 1

            # Update progres bar if point is not skipped
            if returns[2] > 0:
                widgets[0] = progressbar.FormatLabel(f"  it={returns[4]:0>3d}  dPhiNorm={returns[5]:0>6.4f}  rs={returns[2]:+1d} ")
                pbar.update(finishedNodes)
            nodeNumber = returns[0]
            PhiFieldOut[nodeNumber] = returns[1]
            returnStatus[nodeNumber] = returns[2]
            error[nodeNumber] = returns[3]
            iterations[nodeNumber] = returns[4]
            deltaPhiNorm[nodeNumber] = returns[5]

    pbar.finish()

    print("\n")

    return PhiFieldOut, returnStatus, error, iterations, deltaPhiNorm
