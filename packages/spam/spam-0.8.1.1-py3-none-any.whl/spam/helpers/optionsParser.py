"""
Library of SPAM functions for parsing inputs to the scripts
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

import argparse

import tifffile


# Nice str2bool suggestion from Maxim (https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse)
def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


description = [
    "Copyright (C) 2020 SPAM developers",
    "This program comes with ABSOLUTELY NO WARRANTY.",
    "",
    "This is free software, and you are welcome to redistribute it under certain conditions",
    "",
    "",
]
GLPv3descriptionHeader = "\n".join(description)


def isTwoDtiff(filename):
    """
    Returns true if the passed TIFF file is 2D, this function inspects the header but does not load the image
    """
    # 2018-03-24 check for 2D without loading images
    # try:
    # except BaseException:
    #     print("DICregularGrid: Input TIFF files need to be writeable in order to guess their dimensionality")
    #     exit()
    # 2019-03-21 EA: better check for dimensions, doesn't depend on writability of files
    tiff = tifffile.TiffFile(filename)
    # imagejSingleSlice = True
    # if tiff.imagej_metadata is not None:
    #     if 'slices' in tiff.imagej_metadata:
    #         if tiff.imagej_metadata['slices'] > 1:
    #             imagejSingleSlice = False

    #
    # # 2019-04-05 EA: 2D image detection approved by Christophe Golke, update for shape 2019-08-29
    # if len(tiff.pages) == 1 and len(tiff.series[0].shape) == 2:
    #     twoD = True
    # else:
    #     twoD = False

    # 2024-02-07 New attempt since a 2D OME-tiff with a pyramid defeats the above test
    if tiff.series[0].axes == "YX":
        twoD = True
    elif tiff.series[0].axes == "ZYX":
        twoD = False
    else:
        print("spam.helpers.optionsParser.isTwoDtiff(): Unknown condition")
        twoD = None
    tiff.close()
    return twoD


def displaySettings(args, scriptName):
    def _displayed_value(v):
        return [getattr(item, "name", item) if hasattr(item, "name") else item for item in v] if isinstance(v, list) else getattr(v, "name", v)

    print(f"[{scriptName}] Current Settings:")
    
    for key, value in vars(args).items():
        print(f"\t{key}: {_displayed_value(value)}")
    