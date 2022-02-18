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

    depends_on('base-env', type='run')

    depends_on('ecbuild', type='run')
    depends_on('jedi-cmake', type='run')

    depends_on('eigen', type='run')
    depends_on('gsl-lite', type='run')
    depends_on('udunits', type='run')

    depends_on('boost', type='run')
    #depends_on('libbacktrace', type='run')
    #depends_on('cgal+header_only', type='run')

    depends_on('blas',  type='run')
    depends_on('eckit', type='run')
    depends_on('fckit', type='run')
    depends_on('atlas', type='run')

    depends_on('git-lfs', type='run')

    ##depends_on('py-cartopy', when='+python')
    #depends_on('py-click', when='+python')
    #depends_on('py-matplotlib', when='+python')
    #depends_on('py-numpy', when='+python')
    #depends_on('py-pip', when='+python')
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

    depends_on('shumlib', type='run')
    depends_on('faux', type='run')
    depends_on('trans', type='run')

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
