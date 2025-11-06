# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess


from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class AdpPreprocessors(MakefilePackage):
    """Unified, model-agnostic software system that processes atmospheric observations for the Navy's numerical weather prediction data assimilation systems"""

    homepage = "https://github.nrlmry.navy.mil/ADP/adp-preprocessors/wiki"
    #git = "https://github.nrlmry.navy.mil/ADP/adp-preprocessors.git"
    git = "https://github.nrlmry.navy.mil/climbfuji/adp-preprocessors.git"

    maintainers("climbfuji")

    #license("UNKNOWN", checked_by="github_user1")

    # Update commit once 1.2.0 is released
    version("1.2.0", commit="87e93306de9df9ff4d02bce84249976cfa2f4c97")
    version("1.1.0", commit="b2d9d4ffb472eff9ab973ef2a12f574d92c9754b")

    # MakefilePackage dependencies
    depends_on("c", type="build")
    depends_on("fortran", type="build")
    depends_on("gmake", type="build")

    depends_on("mpi")
    depends_on("fftw-api")
    depends_on("lapack")
    # Unclear what to do for GNU. Would be better to fix the build system
    # and let spack provide whatever lapack/fftw provider the user wants
    # instead of hardcoding it to MKL for Intel?
    depends_on("mkl", when="^intel-oneapi-compilers")
    depends_on("mkl", when="^intel-oneapi-compilers-classic")
    depends_on("hdf5@1.14: +fortran")
    depends_on("netcdf-fortran@4.4.4:")
    depends_on("esmf@8.5.0:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("BUILD_WITH_HDF5", "ON")
        env.set("HDF5PATH", self.spec["hdf5"].prefix)
        env.set("HDF5LIB", f"-L{self.spec['hdf5'].prefix.lib}")
        env.set("HDF5MOD", f"-I{join_path(self.spec['hdf5'].prefix, 'mod/static')}")

    def build(self, spec, prefix):
        with working_dir("src"):
            if self.compiler.name == "gcc":
                make("-f", "makefile", "spack_gcc")
            elif self.compiler.name == "intel-oneapi-compilers":
                make("-f", "makefile", "spack_oneapi")
            else:
                raise InstallError(f"Compiler {self.compiler.name} not configured")

    def install(self, spec, prefix):
        for subdir in ['bin', 'lib', 'mod']:
            copy_tree(join_path(self.stage.source_path, subdir), join_path(prefix, subdir))

    def check(self):
        # Serial tests
        for test in ["test_paths", "test_serial"]:
            test_program = which(join_path(self.stage.source_path, "src/io_tools/test/.objdir", test))
            test_program()
        # Parallel tests
        for test in ["test_parallel"]:
            mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
            test_program = join_path(self.stage.source_path, "src/io_tools/test/.objdir", test)
            if mpirun:
                mpirun("-np", "4", test_program)
            else:
                tty.info(f"Bypassing test {test} because mpirun not found")
        # Smoke test: call main executable without arguments, according to the package,
        # this prints an error message but still exits with status code zero
        tty.info("Smoke test for do_satwind_processing.exe, expect 'failed--istats = 3'")
        res = subprocess.run(join_path(self.stage.source_path, "bin", "do_satwind_processing.exe"))
        assert res.returncode == 0
