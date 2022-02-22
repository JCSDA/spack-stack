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
    #version('bugfix-compile-failures', branch='bugfix/fix_compile_failures', no_cache=True)

    variant('enable_mpi', default=True, description='Use MPI?')
    variant('enable_omp', default=True, description='Use OpenMP?')

    #variant('enable_double_precision', default=True, description='Enable double precision?')
    #variant('enable_single_precision', default=True, description='Enable single precision?')

    variant('enable_mkl',  default=True, description='Use MKL?')
    #variant('enable_fftw', default=True, description='Use FFTW?')
    #variant('enable_transi', default=True, description='Use TransI?')

    depends_on('ecbuild', type=('build'))
    depends_on('mpi',  when='+enable_mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api')
    #depends_on('fftw-api', when='+enable_fftw')
    depends_on('mkl',  when='+enable_mkl')

    depends_on('faux~enable_mpi',  when='~enable_mpi')
    depends_on('faux+enable_mpi',  when='+enable_mpi')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_MPI'),
            self.define_from_variant('ENABLE_OMP'),
            #self.define_from_variant('ENABLE_FFTW'),
            self.define_from_variant('ENABLE_MKL')
        ]

        #args.append(self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc))
        #args.append(self.define('CMAKE_CXX_COMPILER', self.spec['mpi'].mpicxx))
        #args.append(self.define('CMAKE_Fortran_COMPILER', self.spec['mpi'].mpifc))
        #
        #cflags = []
        #fflags = []
        #
        #if self.compiler.name in ['gcc', 'clang', 'apple-clang']:
        #    gfortran_major_version = int(spack.compiler.get_compiler_version_output(self.compiler.fc, '-dumpversion').split('.')[0])
        #    if gfortran_major_version>=10:
        #        fflags.append('-fallow-argument-mismatch')
        #
        #if '+pic' in self.spec:
        #    cflags.append(self.compiler.cc_pic_flag)
        #    fflags.append(self.compiler.fc_pic_flag)
        #
        #if cflags:
        #    args.append(self.define('CMAKE_C_FLAGS', ' '.join(cflags)))
        #if fflags:
        #    args.append(self.define('CMAKE_Fortran_FLAGS', ' '.join(fflags)))

        return args
