# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Oops(CMakePackage):
    """Object Oriented Prediction System"""

    homepage = "https://github.com/JCSDA/oops"
    git = "https://github.com/JCSDA/oops.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    # This commit plus the patch below accounts for commit
    # 2340e9b664f82de9fa01c136c3a31d87e4a0bec9 in NRL GitHub
    version("1.10.0.20250827", commit="91889ad09d3789f14a1184701dd80a4913d3ce3e")

    patch("include_algorithm.patch", when="@1.10.0.20250827")

    variant("l95", default=True, description="Build LORENZ95 toy model")
    variant("mkl", default=False, description="Use MKL for LAPACK implementation (if available)")
    variant("openmp", default=True, description="Build oops with OpenMP support")
    variant("qg", default=True, description="Build QG toy model")
    variant('gptl', default=False, description='Use GPTL profiling library (if available)')

    generator("make")

    # Project doesn't list "c" as a dependency in CMakeLists.txt, but cmake step fails w/o it
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("boost@1.64:")
    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@1.10:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@1.10:")
    depends_on("eckit")
    depends_on("eckit@1.24.4:", when="@1.10:")
    depends_on("ecmwf-atlas")
    depends_on("ecmwf-atlas@0.35.0:", when="@1.10:")
    depends_on("eigen")
    depends_on("fckit")
    depends_on("fckit@0.11.0:", when="@1.10:")
    depends_on('gptl', when='+gptl')
    depends_on("jedi-cmake", type=("build"))
    depends_on("lapack", when="~mkl")
    depends_on("mkl", when="+mkl")
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "link", "run"))
    depends_on("mpi")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")
    depends_on("nlohmann-json")
    depends_on("nlohmann-json-schema-validator")

    def cmake_args(self):
        res = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("ENABLE_LORENZ95_MODEL", "l95"),
            self.define_from_variant("ENABLE_QG_MODEL", "qg"),
            self.define_from_variant("ENABLE_MKL", "mkl"),
            self.define_from_variant("OPENMP", "openmp"),
            self.define_from_variant("ENABLE_GPTL", "gptl"),
        ]
        return res

    def check(self):
        skipped_tests = None
        with when("@1.10.0.20250827"):
            skipped_tests = [
                "qg_rescale_ens_perts",
                "qg_4densvar_single-obs_loc_4d",
                "qg_4densvar_single-obs_no_loc",
            ]
            if self.spec.satisfies("%oneapi"):
                skipped_tests += [
                    "test_qg_verticallocev",
                    "test_qg_verticallocev_io",
                ]

        ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
        with working_dir(self.build_directory):
            if skipped_tests:
                ctest("--timeout", "120", "-E", "|".join(skipped_tests))
            else:
                ctest("--timeout", "120")
