# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class UfoData(CMakePackage):
    """Test data for UFO (Universal Forward Operator)"""

    homepage = "https://github.com/JCSDA-internal/ufo-data"
    git = "https://github.com/JCSDA-internal/ufo-data.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    version("2.9.0.20250821", commit="9078290c2eb68050af9941113a311200bb06aba8")

    generator("make")

    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))

    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@2.9:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@2.9:")

    patch("disable_tests.patch", when="@2.9.0.20250821")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
        # JEDI dependencies expect ufo test data in subdirectory
        # ufo-data of the UFO_TESTFILES environment variable
        mkdirp(join_path(prefix, "ufo-data"))
        symlink(
            join_path(prefix, "testinput_tier_1"), 
            join_path(prefix, "ufo-data", "testinput_tier_1"),
        )
