# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class IodaConverters(CMakePackage):
    """Interface for Observation Data Access"""

    homepage = "https://github.com/JCSDA/ioda-converters"
    git = "https://github.com/JCSDA/ioda-converters.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    version("0.0.1.20260120", commit="a91f432d9d50940910605e689cd1cf93a1ce3798")

    generator("make")

    # Project doesn't list "c" as a dependency in CMakeLists.txt, but cmake step fails w/o it
    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("fortran", type=("build"))

    extends("python")

    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@0.0.1:")

    depends_on("bufr@12:")
    depends_on("eccodes")
    depends_on("eckit")
    depends_on("eigen@3")
    depends_on("gsl-lite")
    depends_on("ioda")
    depends_on("jedi-cmake", type=("build"))
    depends_on("mpi")
    depends_on("netcdf-cxx")
    depends_on("netcdf-fortran")
    depends_on("oops")
    depends_on("py-cartopy")
    depends_on("py-pybind11")
