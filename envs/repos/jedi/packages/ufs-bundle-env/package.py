# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class UfsBundleEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    homepage = "https://github.com/JCSDA-internal/ufs-bundle"
    git      = "https://github.com/JCSDA-internal/ufs-bundle.git"

    maintainers = ['climbfuji', 'mark-a-potts']

    version('main', branch='main')

    depends_on('base-env', type=('build', 'run'))

    depends_on('cmake', type=('build', 'run'))
    depends_on('ecbuild', type=('build', 'run'))
    depends_on('jedi-cmake', type=('build', 'run'))

    depends_on('zlib', type=('build', 'run'))
    depends_on('szip', type=('build', 'run'))
    depends_on('hdf5', type=('build', 'run'))
    depends_on('netcdf-c', type=('build', 'run'))
    depends_on('netcdf-fortran', type=('build', 'run'))
    depends_on('parallelio', type=('build', 'run'))
    depends_on('nccmp', type=('build', 'run'))

    depends_on('eigen', type=('build', 'run'))
    depends_on('gsl-lite', type=('build', 'run'))
    depends_on('udunits', type=('build', 'run'))

    depends_on('boost cxxstd=14 visibility=hidden', type=('build', 'run'))
    #depends_on('libbacktrace', type=('build', 'run'))
    #depends_on('cgal+header_only', type=('build', 'run'))

    depends_on('blas',  type=('build', 'run'))
    depends_on('eckit', type=('build', 'run'))
    depends_on('fckit', type=('build', 'run'))
    depends_on('atlas', type=('build', 'run'))

    depends_on('git', type='run')
    depends_on('git-lfs', type='run')

    depends_on('python@3.7:')

    depends_on('fms', type=('build', 'run'))
    depends_on('esmf', type=('build', 'run'))

    depends_on('jasper', type=('build', 'run'))
    depends_on('libpng', type=('build', 'run'))

    depends_on('bacio',  type=('build', 'run'))
    depends_on('crtm',   type=('build', 'run'))
    depends_on('g2',     type=('build', 'run'))
    depends_on('g2tmpl', type=('build', 'run'))
    depends_on('ip',     type=('build', 'run'))
    depends_on('sp',     type=('build', 'run'))
    depends_on('w3nco',  type=('build', 'run'))

    depends_on('gftl-shared', type=('build', 'run'))
    depends_on('yafyaml',     type=('build', 'run'))
    depends_on('mapl',        type=('build', 'run'))
