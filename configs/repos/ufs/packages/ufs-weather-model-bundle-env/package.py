# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class UfsWeatherModelBundleEnv(BundlePackage):
    """Development environment for ufs-weathermodel-bundle"""

    homepage = "https://github.com/JCSDA-internal/fv3-bundle"
    git      = "https://github.com/JCSDA-internal/fv3-bundle.git"

    maintainers = ['kgerheiser', 'climbfuji']

    version('main', branch='main')

    depends_on('base-env', type=('build', 'run'))

    depends_on('esmf', type=('build', 'run'))
    depends_on('fms', type=('build', 'run'))
    
    depends_on('bacio', type=('build', 'run'))
    depends_on('crtm', type=('build', 'run'))
    depends_on('g2', type=('build', 'run'))
    depends_on('g2tmpl', type=('build', 'run'))
    depends_on('ip', type=('build', 'run'))
    depends_on('sp', type=('build', 'run'))
    depends_on('w3nco', type=('build', 'run'))
    
    depends_on('mapl', type=('build', 'run'))

