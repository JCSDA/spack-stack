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

    variant('mpi', default=True, description='Use MPI?')
    variant('openmp', default=True, description='Use OpenMP?')
    variant('fckit', default=True, description='Use fckit?')
    #variant('enable_dr_hook_multi_precision_handles', default=False, description='Use deprecated single precision handles for DR_HOOK?')

    depends_on('ecbuild', type=('build'))
    depends_on('mpi', when='+mpi')
    depends_on('eckit', when='+fckit')
    depends_on('fckit', when='+fckit')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_FCKIT', 'fckit')
            #self.define_from_variant('ENABLE_DR_HOOK_MULTI_PRECISION_HANDLES')
        ]

        return args
