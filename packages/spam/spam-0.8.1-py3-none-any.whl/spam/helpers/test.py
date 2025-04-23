# SPAM test class based on unitest.TestCase.
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

import os
import shutil
import time
import unittest
from pathlib import Path

import numpy


class TestSpam(unittest.TestCase):
    """
    Overwrites setUp and tearDown of unitest.TestCase
    to create and delete a .dump folder for files created during tests.
    """

    # DEBUG mode
    # if True:
    #   - deletes .dump/* before
    #   - does not delete .dump after
    # can be modify in test file
    # >>> if __name__ == "__main__":
    # >>>    spam.helpers.TestSpam.DEBUG = False
    # >>>    unittest.main()
    DEBUG = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dump_folder = ".dump" if self.DEBUG else f".dump-{int(time.clock_gettime(0))}-{numpy.random.randint(65535)}"

    def setUp(self):
        # check if working directory is ".dump"
        wd = os.getcwd()
        if os.path.basename(wd) == self.dump_folder:
            # we're already in ".dump"
            pass
        else:
            # create .dump or delete .dump/*
            d = os.path.join(wd, self.dump_folder)
            if not os.path.isdir(d):
                # print(f"TestSpam.setUp: create .dump directory {self.dump_folder}")
                os.makedirs(d)
            else:
                for filename in os.listdir(d):
                    file_path = os.path.join(d, filename)
                    # print(f"TestSpam.setUp: delete file {file_path}")
                    os.remove(file_path)
            os.chdir(d)

        wd = os.getcwd()

    def tearDown(self):
        # check if working directory is ".dump"
        wd = os.getcwd()
        if os.path.basename(wd) == self.dump_folder:
            # step back
            d = Path(wd).resolve().parent
            os.chdir(d)

        else:
            # print(f"TestSpam.tearDown: ERROR wrong working directory ({wd} instead of {self.dump_folder})")
            # working directory is not ".dump" (that shouldn't happen)
            pass

        wd = os.getcwd()

        # remove ".dump"
        if not self.DEBUG:
            if os.path.isdir(self.dump_folder):
                # print(f"TestSpam.tearDown: delete .dump directory {self.dump_folder}")
                shutil.rmtree(self.dump_folder)
