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
    version("2.9.0.20260319", commit="2886c75398b4b3bdd3a4235298af188370727c2e")
    version("2.9.0.20250805", commit="c6f8842648ea473eebc9f66d7c27e2204e5220d6")

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
