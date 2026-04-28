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
    version("0.0.1.20250830", commit="a91f432d9d50940910605e689cd1cf93a1ce3798")

    patch(
        "https://github.com/JCSDA/ioda-converters/commit/2c09857aac09b7dd9029fdd23e33f712933c40c4.patch?full_index=1",
        sha256="c31342a5bcffdcb77a99ee5f16a5ba2d74e9d822f1fe2d44b3ee772765800d83",
        when="@0.0.1.20250830",
    )

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

    # For running checks
    depends_on("nccmp", type=("build", "test"))
    depends_on("py-pycodestyle", type=("build", "test"))
    depends_on("py-eccodes", type=("build", "test"))
    depends_on("py-h5py", type=("build", "test"))
    depends_on("py-netcdf4", type=("build", "test"))
    depends_on("py-pandas", type=("build", "test"))
    depends_on("py-pyhdf", type=("build", "test"))
    depends_on("py-pyyaml", type=("build", "test"))
    depends_on("py-xarray", type=("build", "test"))

    def cmake_args(self):
        res = [
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return res

    def check(self):
        skipped_tests = None
        with when("@0.0.1.20250830"):
            skipped_tests = [
                # 52: Test timeout computed to be: 1500
                # 52: ECCODES ERROR   :  Key dataTime (unpack_long): Truncating time: non-zero seconds(41) ignored
                #  >> 2169    The following tests FAILED:
                # 52 - test_iodaconv_mrms (Timeout)                      iodaconv
                "test_iodaconv_mrms",
            ]

        ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
        with working_dir(self.build_directory):
            if skipped_tests:
                ctest("--timeout", "120", "-E", "|".join(skipped_tests))
            else:
                ctest("--timeout", "120")
