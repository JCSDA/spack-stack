# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class IodaData(CMakePackage):
    """Test data for IODA (Interface for Observation Data Access)"""

    homepage = "https://github.com/JCSDA-internal/ioda-data"
    git = "https://github.com/JCSDA-internal/ioda-data.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    version("2.9.0.20250805", commit="c6f8842648ea473eebc9f66d7c27e2204e5220d6")

#    patch("ioda_cmake_import.patch", when="@2.9.0.20250826")
#
#    variant("doc", default=False, description="Build IODA documentation")
#    # Let's always assume IODA_BUILD_LANGUAGE_FORTRAN=on.
#    # variant('fortran', default=True, description='Build the ioda Fortran interface')
#    variant("odc", default=True, description="Build ODC bindings")
#    # ioda has no explicit OpenMP calls, but header files from Eigen and oops do use openmp.
#    variant("openmp", default=True, description="Build with OpenMP support")
#    # Let's always BUILD_PYTHON_BINDINGS.
#    # variant('python', default=True, description='Build the ioda Python interface')

    generator("make")

    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))

    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@2.9:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@2.9:")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
        # JEDI dependencies expect ioda test data in subdirectory
        # ioda-data of the IODA_TESTFILES environment variable
        mkdirp(join_path(prefix, "ioda-data"))
        symlink(
            join_path(prefix, "testinput_tier_1"), 
            join_path(prefix, "ioda-data", "testinput_tier_1"),
        )
