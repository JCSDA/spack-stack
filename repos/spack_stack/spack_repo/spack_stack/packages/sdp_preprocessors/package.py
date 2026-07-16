# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess


from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class SdpPreprocessors(MakefilePackage):
    """Satellite data processor focusing on satellite radiances and GNSS RO."""

    homepage = "https://github.nrlmry.navy.mil/NAVGEM/sdp/wiki"
    git = "https://github.nrlmry.navy.mil/NAVGEM/sdp.git"

    maintainers("climbfuji")

    #license("UNKNOWN", checked_by="github_user1")

    version("main", branch="main")
    # This is branch bugfix/spack_take2 as of 2027/07/16
    version("0.1.0", commit="375d2a8971ada8f2823c1cfd818e4ae4099830b8")

    # MakefilePackage dependencies
    depends_on("c", type="build")
    depends_on("fortran", type="build")
    depends_on("gmake", type="build")

    depends_on("mpi")
    depends_on("fftw-api")
    depends_on("lapack")
    depends_on("hdf5@1.14: +fortran")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran@4.4.4:")
    depends_on("esmf@8.5.0:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("HDF5_HOME", self.spec["hdf5"].prefix)
        env.set("HDF5LIB", self.spec["hdf5"].prefix.lib)
        env.set("NETCDFC_HOME", self.spec["netcdf-c"].prefix)
        env.set("NETCDFFORTRAN_HOME", self.spec["netcdf-fortran"].prefix)
        env.set("ZLIB_LIBDIR", self.spec["zlib-api"].prefix.lib)
        # Build with only one thread to avoid race conditions
        env.set("MAKE_PROCS", str(1))

    def build(self, spec, prefix):
        with working_dir("src"):
            if self.compiler.name == "gcc":
                make("-f", "Make_ar", "spack_gcc")
            elif self.compiler.name == "intel-oneapi-compilers":
                make("-f", "Make_ar", "spack_oneapi")
            else:
                raise InstallError(f"Compiler {self.compiler.name} not configured")

    def install(self, spec, prefix):
        # "Install" in build tree, then copy over
        with working_dir("src"):
            make("-f", "Make_ar", "install")
        for subdir in ['bin', 'etc', 'lib', 'mod']:
            copy_tree(join_path(self.stage.source_path, subdir), join_path(prefix, subdir))

    # DH* 20260529 todo: configure tests
    #def check(self):
    #    with working_dir("src/script"):
    #        pass
    #    # Serial tests
    #    for test in ["test_paths", "test_serial"]:
    #        test_program = which(join_path(self.stage.source_path, "src/io_tools/test/.objdir", test))
    #        test_program()
    #    # Parallel tests
    #    for test in ["test_parallel"]:
    #        mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
    #        test_program = join_path(self.stage.source_path, "src/io_tools/test/.objdir", test)
    #        if mpirun:
    #            mpirun("-np", "4", test_program)
    #        else:
    #            tty.info(f"Bypassing test {test} because mpirun not found")
    #    # Smoke test: call main executable without arguments, according to the package,
    #    # this prints an error message but still exits with status code zero
    #    tty.info("Smoke test for do_satwind_processing.exe, expect 'failed--istats = 3'")
    #    res = subprocess.run(join_path(self.stage.source_path, "bin", "do_satwind_processing.exe"))
    #    assert res.returncode == 0
    # *DH
