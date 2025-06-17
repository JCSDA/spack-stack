# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RoppUfo(CMakePackage):
    """Unified Forward Operator Interface for Radio Occultation Pre-processing package (ROPP)"""

    # DH* TODO CHANGE BACK TO JCSDA-INTERNALq
    homepage = "https://github.nrlmry.navy.mil/jcsda/ropp-ufo"
    git = "https://github.nrlmry.navy.mil/jcsda/ropp-ufo.git"

    maintainers = ["climbfuji"]

    version("develop", branch="develop", no_cache=True)
    # this is the ropp-submodule branch ... update once merged
    version("11.0.20250612", commit="6a0bea80795a1bb50e5466a8f02ab6823b39d23b", submodules=True)

    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@11:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@11:")
    depends_on("jedi-cmake", type=("build"))
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
