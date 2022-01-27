# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from spack import *

class Fv3BundleEnv(BundlePackage):
    """Development environment for fv3-bundle"""

    homepage = "https://github.com/JCSDA-internal/fv3-bundle"
    git      = "https://github.com/JCSDA-internal/fv3-bundle.git"

    maintainers = ['climbfuji', 'rhoneyager']

    version('main', branch='main')

    depends_on('cmake', type=('build', 'run'))
    depends_on('ecbuild', type=('build', 'run'))
    depends_on('jedi-cmake', type=('build', 'run'))

    depends_on('zlib', type=('build', 'run'))
    depends_on('szip', type=('build', 'run'))
    depends_on('hdf5', type=('build', 'run'))
    depends_on('netcdf-c', type=('build', 'run'))
    depends_on('netcdf-fortran', type=('build', 'run'))
    depends_on('nccmp', type=('build', 'run'))

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

    depends_on('git', type='run')
    depends_on('git-lfs', type='run')

    depends_on('python@3.7:')

    depends_on('fms-jcsda@release-stable')

    ##depends_on('py-cartopy', when='+python')
    #depends_on('py-click', when='+python')
    #depends_on('py-matplotlib', when='+python')
    #depends_on('py-netcdf4', when='+python')
    #depends_on('py-numpy', when='+python')
    #depends_on('py-pandas', when='+python')
    #depends_on('py-pip', when='+python')
    #depends_on('py-pybind11', when='+python')
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
