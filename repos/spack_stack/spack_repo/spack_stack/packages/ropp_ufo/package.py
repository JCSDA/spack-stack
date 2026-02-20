# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class RoppUfo(CMakePackage):
    """Unified Forward Operator Interface for Radio Occultation Pre-processing package (ROPP)"""

    # DH* TODO CHANGE BACK TO JCSDA-INTERNAL ONCE THE NRL VERSION WAS MERGED BACK
    homepage = "https://github.nrlmry.navy.mil/jcsda/ropp-ufo"
    git = "https://github.nrlmry.navy.mil/jcsda/ropp-ufo.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    # this is the ropp-submodule branch ... update once merged
    version("11.0.20251022", commit="02e21ef0696e67675184797427af265c06973ecf", submodules=True)

    # Project doesn't list "c" as a dependency in CMakeLists.txt, but cmake step fails w/o it
    depends_on("c", type=("build"))
    depends_on("fortran", type=("build"))

    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@11:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@11:")
    depends_on("jedi-cmake", type=("build"))
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")

    # ropp-ufo currently has no tests, but we keep
    # this section for consistency with the other
    # JEDI packages and for future use.
    def check(self):
        skipped_tests = None
        #with when("@11.0.20251022"):
        #    skipped_tests = [
        #    ]
        #
        ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
        with working_dir(self.build_directory):
            if skipped_tests:
                ctest("--timeout", "120", "-E", "|".join(skipped_tests))
            else:
                ctest("--timeout", "120")
