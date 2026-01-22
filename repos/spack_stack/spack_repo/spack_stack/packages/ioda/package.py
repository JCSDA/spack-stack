# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Ioda(CMakePackage):
    """Interface for Observation Data Access"""

    homepage = "https://github.com/JCSDA/ioda"
    git = "https://github.com/JCSDA/ioda.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    version("2.9.0.20260120", commit="6e76616001067384f7d0ca4341ad78e81527af8b")

    patch("ioda_cmake_import.patch", when="@2.9.0.20260120")

    variant("doc", default=False, description="Build IODA documentation")
    # Let's always assume IODA_BUILD_LANGUAGE_FORTRAN=on.
    # variant('fortran', default=True, description='Build the ioda Fortran interface')
    variant("odc", default=True, description="Build ODC bindings")
    # ioda has no explicit OpenMP calls, but header files from Eigen and oops do use openmp.
    variant("openmp", default=True, description="Build with OpenMP support")
    # Let's always BUILD_PYTHON_BINDINGS.
    # variant('python', default=True, description='Build the ioda Python interface')

    generator("make")

    # Project doesn't list "c" as a dependency in CMakeLists.txt, but cmake step fails w/o it
    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("fortran", type=("build"))

    depends_on("boost@1.64.0:")
    depends_on("bufr")
    depends_on("bufr@12.0.1:", when="@2.9:")
    # This is optional, and it needs netcdf-cxx - which versions?
    depends_on("bufr-query@0.0.4:", when="@2.9:")
    depends_on("cmake", type=("build"))
    depends_on("cmake@3.14:", type=("build"), when="@2.9:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@2.9:")
    depends_on("eckit")
    depends_on("eckit@1.23.0:", when="@2.9:")
    depends_on("eigen")
    depends_on("fckit")
    depends_on("fckit@0.10.1:", when="@2.9:")
    depends_on("gsl-lite")
    depends_on("hdf5@1.12.0: +mpi")
    depends_on("hdf5@1.14.0: +mpi", when="@2.9:")
    depends_on("jedi-cmake", type=("build"))
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "link", "run"))
    depends_on("mpi")
    depends_on("nccmp")
    # netcdf-cxx needed for bufr-query, but which version?
    depends_on("netcdf-cxx", when="@2.9:")
    depends_on("odc", when="+odc")
    depends_on("odc@1.4.6:", when="@2.9: +odc")
    depends_on("oops+openmp", when="+openmp")
    depends_on("oops~openmp", when="~openmp")
    depends_on("oops@1.10", when="@2.9:")
    depends_on("python")
    depends_on("python@3.9:3.11", when="@2.9:")
    depends_on("py-pybind11")
    depends_on("py-pycodestyle")
    depends_on("udunits")
    depends_on("udunits@2.2.0:", when="@2.9:")

    def cmake_args(self):
        res = [
            self.define_from_variant("ENABLE_IODA_DOC", "doc"),
        ]
        return res
