# This python script is a graphical tool for aligning 3D images by eye using QT5 and SPAM functions
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

# import spam.helpers.optionsParser
import argparse
import os
import sys

import numpy
import spam.helpers
import spam.visual.visualClass as visual
import tifffile
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QWidget
import spam.DIC

def eregParser(parser):
    parser.add_argument(
        "inFile1",
        nargs="?",
        default=None,
        type=argparse.FileType("r"),
        help="A first 3D greyscale tiff files to eye-register",
    )

    parser.add_argument(
        "inFile2",
        nargs="?",
        default=None,
        type=argparse.FileType("r"),
        help="A second 3D greyscale tiff files to eye-register",
    )

    parser.add_argument(
        "-pf",
        "--phiFile",
        dest="PHIFILE",
        default=None,
        type=argparse.FileType("r"),
        help="path to TSV file containing the deformation function field",
    )

    parser.add_argument(
        "-df",
        "--defaultFolder",
        dest="FOLDER",
        default=os.getcwd(),
        type=str,
        help="path to the default folder used when selecting the files",
    )

    parser.add_argument(
        "-bin",
        "--binning",
        dest="BINNING",
        default=1,
        type=int,
        help="Binning level to load the images",
    )

    args = parser.parse_args()

    return args


def script():
    parser = argparse.ArgumentParser(
        description=f"spam-ereg: {spam.helpers.optionsParser.GLPv3descriptionHeader}",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    args = eregParser(parser)

    # GP 2024-12-05: Adding binning options
    if isinstance(args.BINNING, int) and args.BINNING > 0:
        pass
    else:
        print(f"[spam-ereg] Binning level is not int or not greater than 0")
        exit()

    spam.helpers.optionsParser.displaySettings(args, "spam-ereg")

    app = QApplication(["Eye registration"])

    # helper function that loads an image from arg or window
    def _getImage(arg, name, dir, binning):
        if arg:
            imPath = os.path.join(os.getcwd(), arg.name)
        else:
            imPath = QFileDialog.getOpenFileName(None, f"Open {name}", dir, "Image Files (*.tif *.tiff)")[0]

        imName = os.path.basename(imPath)
        im = tifffile.imread(imPath)
        # GP 2024-12-05: Adding binning options
        if binning > 1:
            im = spam.DIC.binning(im, binning)

        print(f"[spam-ereg] {name}:")
        print(f"[spam-ereg] \t path: {imPath}")
        print(f"[spam-ereg] \t name: {imName}")
        print(f"[spam-ereg] \t shape: {im.shape}")

        return imPath, imName, im

    # helper function that loads phi file
    def _getPhi(arg, dir):
        if arg:
            phiPath = os.path.join(os.getcwd(), arg.name)
        else:
            phiPath = QFileDialog.getOpenFileName(None, "Open Phi TSV (optional)", dir, "Image Files (*.tsv)")[0]

        if not os.path.isfile(phiPath):
            print(f"[spam-ereg] Initial Phi: no files found {phiPath}")
            return numpy.eye(4)

        print(f"[spam-ereg] Initial Phi: loaded from {phiPath}")
        return spam.helpers.readCorrelationTSV(phiPath)["PhiField"][0]

    # setup default directory for QFile path
    dirForQFile = args.FOLDER

    # load image 1 and update directory
    imPath1, imName1, im1 = _getImage(args.inFile1, "Image 1", dirForQFile, args.BINNING)
    dirForQFile = os.path.dirname(imPath1)

    # load image 2 and update directory
    imPath2, imName2, im2 = _getImage(args.inFile2, "Image 2", dirForQFile, args.BINNING)
    dirForQFile = os.path.dirname(imPath2)

    # load phi
    Phi = _getPhi(args.PHIFILE, dirForQFile)

    window = QWidget()
    mainWindowGrid = QGridLayout(window)
    eregWidget = visual.ereg([im1, im2], Phi, [imName1, imName2], binning=args.BINNING)
    mainWindowGrid.addWidget(eregWidget, 1, 1)
    window.show()
    eregWidget.show()
    sys.exit(app.exec_())
