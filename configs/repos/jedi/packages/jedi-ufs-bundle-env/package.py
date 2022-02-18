# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUfsBundleEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    homepage = "https://github.com/JCSDA-internal/ufs-bundle"
    git      = "https://github.com/JCSDA-internal/ufs-bundle.git"

    maintainers = ['climbfuji', 'mark-a-potts']

    version('main', branch='main')

    depends_on('base-env', type='run')

    depends_on('ecbuild', type='run')
    depends_on('jedi-cmake', type='run')

    depends_on('eigen', type='run')
    depends_on('gsl-lite', type='run')
    depends_on('udunits', type='run')

    depends_on('boost cxxstd=14 visibility=hidden', type='run')
    #depends_on('libbacktrace', type='run')
    #depends_on('cgal+header_only', type='run')

    depends_on('blas',  type='run')
    depends_on('eckit', type='run')
    depends_on('fckit', type='run')
    depends_on('atlas', type='run')

    depends_on('git-lfs', type='run')

    depends_on('fms', type='run')
    depends_on('esmf', type='run')

    depends_on('jasper', type='run')
    depends_on('libpng', type='run')

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

    depends_on('py-pandas', type='run')
    depends_on('py-scipy', type='run')
    depends_on('py-pybind11', type='run')
    depends_on('py-h5py', type='run')
    depends_on('py-netcdf4',  type='run')
    depends_on('py-pycodestyle', type='run')
    depends_on('py-pyyaml', type='run')
    depends_on('py-python-dateutil', type='run')

    depends_on('eccodes', type='run')
    depends_on('py-eccodes', type='run')

    depends_on('bufr', type='run')
