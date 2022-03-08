# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Trans(CMakePackage):
    """Trans is the global spherical Harmonics transforms library, extracted from the IFS.
    It is using a hybrid of MPI and OpenMP parallelisation strategies. The package contains
    both single- and double precision Fortran libraries (trans_sp, trans_dp), as well as a
    C interface to the double-precision version (transi_dp)."""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/trans"
    git = "https://github.com/JCSDA-internal/trans.git"

    maintainers = ['climbfuji']

    version('develop', branch='develop', no_cache=True, preferred=True)

    variant('mpi', default=True, description='Use MPI?')
    variant('openmp', default=True, description='Use OpenMP?')

    variant('mkl',  default=False, description='Use MKL?')
    variant('fftw', default=True, description='Use FFTW?')

    #variant('double_precision', default=True, description='Enable double precision?')
    #variant('single_precision', default=True, description='Enable single precision?')
    #variant('transi', default=True, description='Use TransI?')

    depends_on('ecbuild', type=('build'))
    depends_on('mpi',  when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api', when='+fftw')
    depends_on('mkl', when='+mkl')

    depends_on('faux~mpi',  when='~mpi')
    depends_on('faux+mpi',  when='+mpi')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            self.define_from_variant('ENABLE_FFTW', 'fftw'),
            self.define_from_variant('ENABLE_MKL', 'mkl')
        ]

        return args
