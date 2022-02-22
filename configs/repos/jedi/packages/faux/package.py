# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Faux(CMakePackage):
    """Faux is a collection of selected Fortran utility libraries, extracted from the IFS."""

    # DH* TODO UPDATE
    homepage = "https://github.com/JCSDA-internal/faux"
    git = "https://github.com/JCSDA-internal/faux.git"

    maintainers = ['climbfuji']

    version('develop', branch='develop', no_cache=True, preferred=True)
    #version('bugfix-compile-failures', branch='bugfix/fix_compile_failures', no_cache=True)

    variant('enable_mpi',   default=True, description='Use MPI?')
    variant('enable_omp',   default=True, description='Use OpenMP?')
    variant('enable_fckit', default=True, description='Use fckit?')
    #variant('enable_dr_hook_multi_precision_handles', default=False, description='Use deprecated single precision handles for DR_HOOK?')

    depends_on('ecbuild', type=('build'))
    depends_on('mpi',   when='+enable_mpi')
    depends_on('eckit', when='+enable_fckit')
    depends_on('fckit', when='+enable_fckit')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_OMP'),
            self.define_from_variant('ENABLE_MPI'),
            self.define_from_variant('ENABLE_FCKIT')
            #self.define_from_variant('ENABLE_DR_HOOK_MULTI_PRECISION_HANDLES')
        ]

        return args
