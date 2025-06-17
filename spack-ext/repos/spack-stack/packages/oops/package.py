# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Oops(CMakePackage):
    """Object Oriented Prediction System"""

    homepage = "https://github.com/JCSDA/oops"
    git = "https://github.com/JCSDA/oops.git"

    maintainers = ["climbfuji"]

    version("develop", branch="develop", no_cache=True)
    version("1.10.0.20241216", commit="58b068767ec4af2cbecfe86499b87a0d4723778f")

    variant("l95", default=True, description="Build LORENZ95 toy model")
    variant("mkl", default=False, description="Use MKL for LAPACK implementation (if available)")
    variant("openmp", default=True, description="Build oops with OpenMP support")
    variant("qg", default=True, description="Build QG toy model")
    variant('gptl', default=False, description='Use GPTL profiling library (if available)')

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
            self.define_from_variant("ENABLE_LORENZ95_MODEL", "l95"),
            self.define_from_variant("ENABLE_QG_MODEL", "qg"),
            self.define_from_variant("ENABLE_MKL", "mkl"),
            self.define_from_variant("OPENMP", "openmp"),
            self.define_from_variant("ENABLE_GPTL", "gptl"),
        ]
        return res
