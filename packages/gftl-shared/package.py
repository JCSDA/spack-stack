# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GftlShared(CMakePackage):
    """
    Provides common gFTL containers of Fortran intrinsic types that
    are encountered frequently.

    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared"
    git = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared.git"

    maintainers = ['kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA']

    version('1.3.0', tag='v1.3.0', submodules=True)
    version('1.2.0', tag='v1.2.0', submodules=True)

    def cmake_args(self):
        args = []
        return args
