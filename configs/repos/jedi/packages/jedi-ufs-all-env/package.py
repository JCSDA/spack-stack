# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUfsAllEnv(BundlePackage):
    """On-stop development environment for all applications"""

    homepage = "https://github.com/NOAA-EMC/spack-stack"
    git      = "https://github.com/NOAA-EMC/spack-stack.git"

    maintainers = ['climbfuji', 'kgerheiser']

    version('main', branch='main')

    depends_on('jedi-ewok-env')
    depends_on('jedi-fv3-bundle-env')
    depends_on('jedi-ufs-bundle-env')
    depends_on('jedi-um-bundle-env')
    depends_on('nceplibs-bundle')
    depends_on('soca-bundle-env')
    depends_on('ufs-weather-model-env')

    # jedi-tools-env doesn't build with Intel, and is not needed on HPCs
    depends_on('jedi-tools-env', when='%gcc')
    depends_on('jedi-tools-env', when='%clang')
    depends_on('jedi-tools-env', when='%apple-clang')
