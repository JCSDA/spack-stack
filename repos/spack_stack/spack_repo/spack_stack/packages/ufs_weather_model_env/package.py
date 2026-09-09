# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class UfsWeatherModelEnv(BundlePackage):
    """Development environment for ufs-weather-model"""

    homepage = "https://github.com/ufs-community/ufs-weather-model"
    git = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers("AlexanderRichert-NOAA", "climbfuji")

    version("1.0.0")

    variant(
        "debug",
        default=False,
        description="Build a debug version of certain dependencies (ESMF, MAPL)",
    )
    variant("python", default=True, description="Include extra Python packages")
    variant("ncutils", default=True, description="Include extra NetCDF utilities (cprnc and nccmp)")
    variant("kokkos", default=False, description="Enable kokkos and kokkos-kernels")
    variant("arborx", default=False, description="Enable arborx")

    depends_on("cmake", type="run")
    depends_on("python", type="run")

    depends_on("bacio", type="run")
    depends_on("crtm", type="run")
    depends_on("esmf~debug", type="run", when="~debug")
    depends_on("esmf+debug", type="run", when="+debug")
    depends_on("fms +gfs_phys constants=GFS", type="run")
    depends_on("g2", type="run")
    depends_on("g2tmpl", type="run")
    depends_on("gftl-shared", type="run")
    depends_on("hdf5", type="run")
    depends_on("ip", type="run")
    depends_on("jasper", type="run")
    depends_on("libpng", type="run")
    depends_on("mapl~debug", type="run", when="~debug")
    depends_on("mapl+debug", type="run", when="+debug")
    depends_on("netcdf-c", type="run")
    depends_on("netcdf-fortran", type="run")
    depends_on("parallelio", type="run")
    depends_on("scotch", type="run")
    depends_on("sp", type="run", when="^ip@:4")
    depends_on("w3emc", type="run")
    depends_on("zlib-api", type="run")

    depends_on("ufs-pyenv", type="run", when="+python")
    depends_on("cprnc", type="run", when="+ncutils")
    depends_on("nccmp", type="run", when="+ncutils")

    # https://github.com/JCSDA/spack-stack/issues/2081
    # kokkos for UFS-WM atmospheric composition modeling components (CATChem & CECE)
    # default to +openmp and +serial for both packages
    # kokkos and kokkos-kernels are spec'd in common/packages.yaml and <site>/packages.yaml
    with when("+kokkos"):
        depends_on("kokkos", type="run")
        depends_on("kokkos-kernels", type="run")

    with when("+arborx"):
        depends_on("arborx", type="run")
        requires("+kokkos", msg="Arborx requires +kokkos")

    # There is no need for install() since there is no code.
