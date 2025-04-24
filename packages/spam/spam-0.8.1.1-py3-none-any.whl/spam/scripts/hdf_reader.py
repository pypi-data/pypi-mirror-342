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
Helper that displays the data within a HDF file.
"""

import argparse
import os

import h5py
import numpy
import spam.helpers
import spam.mesh

numpy.seterr(all="ignore")


def hdfReader(parser):
    parser.add_argument("FILE", metavar="FILE", type=str, help="path to the HDF file")

    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        dest="PREVIEW",
        help="Display a preview of the datases. Default = False",
    )

    args = parser.parse_args()

    # test if file exists
    if not os.path.isfile(args.FILE):
        raise FileNotFoundError(args.FILE)

    return args


def script():
    # Define argument parser object
    parser = argparse.ArgumentParser(
        description="spam-hdf-reader " + spam.helpers.optionsParser.GLPv3descriptionHeader + "Reads and display data within a HDF file\n",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parse arguments with external helper function
    args = hdfReader(parser)

    with h5py.File(args.FILE, "r") as f:
        print(f"File: {f.filename}")

        if len(f.attrs):
            print("\tMetadata:")
            for k, v in f.attrs.items():
                print(f"\t\t{k}: {v}")
            print()

        for k, v in f.items():
            print(f"\tDataset: {k}")
            print(f"\t\ttype: {v.dtype}")
            print(f"\t\tshape: {v.maxshape}")
            if len(v.attrs):
                print("\t\tMetadata:")
                for k2, v2 in v.attrs.items():
                    print(f"\t\t\t{k2}: {v2}")
                print()

            if args.PREVIEW:
                print(v[:])
            # print(k, v)
            print()
