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


def ddic(
    im1,
    im2,
    lab1,
    labelsToCorrelate=None,
    PhiField=None,
    boundingBoxes=None,
    centresOfMass=None,
    processes=None,
    labelDilate=1,
    margin=5,
    maskOthers=True,
    volThreshold=100,
    multiScaleBin=1,
    updateGrad=False,
    correlateRigid=True,
    maxIter=50,
    deltaPhiMin=0.001,
    interpolationOrder=1,
    debug=False,
    twoD=False,
):
    numberOfLabels = lab1.max()

    if labelsToCorrelate is None:
        labelsToCorrelate = numpy.arange(1, numberOfLabels)

    PhiFieldOut = numpy.zeros([numberOfLabels, 4, 4])
    if PhiField is None:
        for i in range(numberOfLabels):
            PhiFieldOut[i] = numpy.eye(4)
    else:
        PhiFieldOut = PhiField.copy()

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab1)

    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab1)

    if processes is None:
        processes = multiprocessing.cpu_count()

    if debug:
        print("spam.DIC.ddic(): I was passed debug=True, so setting #processes to 1")
        processes = 1

    numberOfLabels = (lab1.max() + 1).astype("u4")
    PSCC = numpy.zeros((numberOfLabels), dtype="<f4")
    error = numpy.zeros((numberOfLabels), dtype="<f4")
    iterations = numpy.zeros((numberOfLabels), dtype="<u2")
    returnStatus = numpy.zeros((numberOfLabels), dtype="<i2")
    deltaPhiNorm = numpy.zeros((numberOfLabels), dtype="<f4")
    labelDilateList = numpy.zeros((numberOfLabels), dtype="<u2")

    global _multiprocessingCorrelateOneLabel

    def _multiprocessingCorrelateOneLabel(label):
        # label, labelDilateCurrent = q.get()

        # WARNING HACK BAD FIXME
        labelDilateCurrent = labelDilate
        initialDisplacement = numpy.round(PhiFieldOut[label][0:3, 3]).astype(int)

        if debug:
            print("\n\n\nWorking on label:", label, "\n")
        if debug:
            print("Position (ZYX):", centresOfMass[label])

        imagetteReturns = spam.label.getImagettesLabelled(
            lab1,
            label,
            PhiFieldOut[label],
            im1,
            im2,
            [0, 0, 0, 0, 0, 0],  # Search range, don't worry about it
            boundingBoxes,
            centresOfMass,
            margin=margin,
            labelDilate=labelDilateCurrent,
            maskOtherLabels=maskOthers,
            applyF="no",
            volumeThreshold=volThreshold,
        )

        if twoD:
            imagetteReturns["imagette1"] = imagetteReturns["imagette1"][int(imagetteReturns["imagette1"].shape[0] - 1) // 2, :, :]
            imagetteReturns["imagette2"] = imagetteReturns["imagette2"][int(imagetteReturns["imagette2"].shape[0] - 1) // 2, :, :]
            imagetteReturns["imagette1mask"] = imagetteReturns["imagette1mask"][int(imagetteReturns["imagette1mask"].shape[0] - 1) // 2, :, :]

        badPhi = numpy.eye(4)
        badPhi[0:3, 3] = numpy.nan

        # In case the label is missing or the Phi is duff
        if imagetteReturns["returnStatus"] != 1 or not numpy.all(numpy.isfinite(PhiFieldOut[label])):
            return label, badPhi, -7, numpy.inf, 0, numpy.inf, labelDilateCurrent

        else:
            # Remove int() part of displacement since it's already used to extract imagette2
            PhiTemp = PhiFieldOut[label].copy()
            PhiTemp[0:3, -1] -= initialDisplacement
            if debug:
                print("Starting lk iterations with Phi - int(disp):\n", PhiTemp)
            if debug:
                print("\nStarting lk iterations with int(disp):\n", initialDisplacement)

            registerReturns = spam.DIC.registerMultiscale(
                imagetteReturns["imagette1"],
                imagetteReturns["imagette2"],
                multiScaleBin,
                im1mask=imagetteReturns["imagette1mask"],
                margin=1,
                PhiInit=PhiTemp,
                PhiRigid=correlateRigid,
                updateGradient=updateGrad,
                maxIterations=maxIter,
                deltaPhiMin=deltaPhiMin,
                interpolationOrder=interpolationOrder,
                verbose=debug,
                imShowProgress=debug,
            )
            goodPhi = registerReturns["Phi"]
            goodPhi[0:3, -1] += initialDisplacement
            return (
                label,
                goodPhi,
                registerReturns["returnStatus"],
                registerReturns["error"],
                registerReturns["iterations"],
                registerReturns["deltaPhiNorm"],
                labelDilateCurrent,
            )

    print(f"\n\tStarting discrete dic for {len(labelsToCorrelate)} labels (with {processes} process{'es' if processes > 1 else ''})")
    widgets = [
        progressbar.FormatLabel(""),
        " ",
        progressbar.Bar(),
        " ",
        progressbar.AdaptiveETA(),
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=len(labelsToCorrelate))
    pbar.start()

    finishedLabels = 0

    with multiprocessing.Pool(processes=processes) as pool:
        for returns in pool.imap_unordered(_multiprocessingCorrelateOneLabel, labelsToCorrelate):
            finishedLabels += 1

            # Update progres bar if point is not skipped
            if returns[2] > 0:
                widgets[0] = progressbar.FormatLabel("  it={:0>3d}  dPhiNorm={:0>6.4f}  rs={:+1d} ".format(returns[4], returns[5], returns[2]))
                pbar.update(finishedLabels)
            label = returns[0]
            PhiFieldOut[label] = returns[1]
            returnStatus[label] = returns[2]
            error[label] = returns[3]
            iterations[label] = returns[4]
            deltaPhiNorm[label] = returns[5]
            labelDilateList[label] = returns[6]

    pbar.finish()

    print("\n")

    return PhiFieldOut, returnStatus, error, iterations, deltaPhiNorm, labelDilateList, PSCC
