# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUfsBundleEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/ufs-bundle"
    git      = "https://github.com/JCSDA-internal/ufs-bundle.git"

    maintainers = ['climbfuji', 'mark-a-potts']

    version('main', branch='main')

    depends_on('base-env', type='run')
    depends_on('jedi-base-env', type='run')

    depends_on('jasper', type='run')
    depends_on('libpng', type='run')

    depends_on('fms', type='run')
    depends_on('esmf', type='run')

    depends_on('bacio',  type='run')
    depends_on('crtm',   type='run')
    depends_on('g2',     type='run')
    depends_on('g2tmpl', type='run')
    depends_on('ip',     type='run')
    depends_on('sp',     type='run')
    depends_on('w3nco',  type='run')

    depends_on('gftl-shared', type='run')
    depends_on('yafyaml',     type='run')
    depends_on('mapl',        type='run')
