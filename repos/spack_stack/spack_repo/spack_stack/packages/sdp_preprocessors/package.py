# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess
from pathlib import Path


from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class SdpPreprocessors(MakefilePackage):
    """Satellite data processor focusing on satellite radiances and GNSS RO."""

    homepage = "https://github.nrlmry.navy.mil/NAVGEM/sdp/wiki"
    git = "https://github.nrlmry.navy.mil/NAVGEM/sdp.git"

    maintainers("climbfuji")

    license("custom", checked_by="climbfuji")

    version("main", branch="main")
    version("0.1.0", commit="eb2965331779a1962c0c31e382827f00e3db6de8")

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
        # Check for expected files, since errors from make aren't caught reliably.
        expected_executables = [
            "amsua_nogaps.exe",
            "amsub_mhs_nogaps.exe",
            "aqua_nogaps.exe",
            "atms_nogaps.exe",
            "atovin.exe",
            "cris_nogaps.exe",
            "geo_asr_nogaps.exe",
            "geo_csr_nogaps.exe",
            "gnss_gb_nogaps.exe",
            "gps_nogaps.exe",
            "iasi_nogaps.exe",
            "mwi_nogaps.exe",
            "omps_nogaps.exe",
            "radiance_prep.exe",
            "ssmis_nogaps.exe",
            "ssmis_uas_nogaps.exe",
        ]
        for exe in expected_executables:
            p = Path(join_path(self.stage.source_path, "bin", exe))
            if not p.exists():
                raise InstallError(f"Expected executable {exe} not found.")
        # Copy relevant directories over to final location
        for subdir in ['bin', 'etc', 'lib', 'mod']:
            copy_tree(join_path(self.stage.source_path, subdir), join_path(prefix, subdir))

    def check(self):
        with working_dir("src/script"):
            res = subprocess.run("./run_all_test.sh")
            assert res.returncode == 0
