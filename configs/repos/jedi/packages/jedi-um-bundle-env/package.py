# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class JediUmBundleEnv(BundlePackage):
    """Development environment for um-bundle"""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/um-bundle"
    git      = "https://github.com/JCSDA-internal/um-bundle.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')

    depends_on('base-env', type=('build', 'run'))

    depends_on('ecbuild', type=('build', 'run'))
    depends_on('jedi-cmake', type=('build', 'run'))

    depends_on('eigen', type=('build', 'run'))
    depends_on('gsl-lite', type=('build', 'run'))
    depends_on('udunits', type=('build', 'run'))

    depends_on('boost', type=('build', 'run'))
    #depends_on('libbacktrace', type=('build', 'run'))
    #depends_on('cgal+header_only', type=('build', 'run'))

    depends_on('blas',  type=('build', 'run'))
    depends_on('eckit', type=('build', 'run'))
    depends_on('fckit', type=('build', 'run'))
    depends_on('atlas', type=('build', 'run'))

    depends_on('git-lfs', type='run')

    ##depends_on('py-cartopy', when='+python')
    #depends_on('py-click', when='+python')
    #depends_on('py-matplotlib', when='+python')
    #depends_on('py-numpy', when='+python')
    #depends_on('py-pip', when='+python')
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-pybind11', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-netcdf4',  type=('build', 'run'))
    depends_on('py-pycodestyle', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))

    depends_on('eccodes', type=('build', 'run'))
    depends_on('py-eccodes', type=('build', 'run'))

    depends_on('bufr', type=('build', 'run'))

    depends_on('shumlib', type=('build', 'run'))
    depends_on('faux', type=('build', 'run'))
    depends_on('trans', type=('build', 'run'))

    ##depends_on('py-pyproj', when='+python')
    #depends_on('py-pyshp', when='+python')
    #depends_on('py-ruamel-yaml', when='+python')
    #depends_on('py-scipy', when='+python')
    #depends_on('py-shapely', when='+python')
    #depends_on('py-yamlreader', when='+python')
    ## TODO: nceplibs-bufr python
    #
    #
    #def cmake_args(self):
    #    res = [] 
    #    return res
