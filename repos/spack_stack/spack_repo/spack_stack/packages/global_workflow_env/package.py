# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class GlobalWorkflowEnv(BundlePackage):
    """Development environment for NOAA's Global Workflow"""

    homepage = "https://github.com/NOAA-EMC/global-workflow"
    git = "https://github.com/NOAA-EMC/global-workflow.git"

    maintainers("AlexanderRichert-NOAA")

    version("1.0.0")
    variant("uwtools", default=False, description="Build uwtools")
    variant("metplus", default=True, description="Build METplus to support verifiation")
    variant("gdas", default=True, description="Build for GDASApp DA support")
    variant("gsi", default=True, description="Build for GSI DA support")
    variant("ci", default=True, description="Build for automated CI testing")

    '''
    variant("python", default=True, description="Include extra Python packages")
    variant("ncutils", default=True, description="Include extra NetCDF utilities (cprnc and nccmp)")

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
    '''
    depends_on("base-env")
    depends_on("ufs-weather-model-env")
    depends_on("ufs-pyenv")
    depends_on("parallel-netcdf")
    depends_on("netcdf-c") #ufs, base-env
    depends_on("netcdf-fortran") #ufs, base-env
    depends_on("netcdf-cxx")
    depends_on("nccmp")

    depends_on("py-wxflow")
    depends_on("py-mpi4py")
    depends_on("py-scipy")
    depends_on("py-certifi")
    depends_on("py-markupsafe")
    depends_on("py-jinja2")
    depends_on("py-pytz")

    depends_on("grib-util")
    depends_on("sigio")
    depends_on("wgrib2")

    depends_on("nco")
    depends_on("prod-util")

    depends_on("antlr")
    depends_on("pigz")
    depends_on("zstd")
    depends_on("gettext")
    depends_on("sqlite")
    depends_on("libjpeg")
    depends_on("openjpeg")

    depends_on("w3nco")

    depends_on("cdo")
    depends_on("gsl")

    depends_on("ip") #ufs
    depends_on("sp", when="^ip@:4") #ufs
    depends_on("jasper") #ufs
    depends_on("libpng") #ufs
    depends_on("bacio") #ufs
    depends_on("esmf") #ufs
    depends_on("g2") #ufs
    depends_on("g2tmpl") #ufs
    depends_on("g2c")
    depends_on("w3emc") #ufs

    depends_on("met", when="+metplus")
    depends_on("metplus", when="+metplus")
    depends_on("uwtools", when="+uwtools")

    # GDASApp dependencies
    with when("+gdas"):
        depends_on("jedi-fv3-env", when="+gdas")
        depends_on("jedi-tools-env", when="+gdas")
        depends_on("jedi-um-env", when="+gdas")
        depends_on("ioda", when="+gdas")
        depends_on("wrf-io")
        depends_on("nemsio")
        depends_on("nemsiogfs")
        depends_on("ncio")
        depends_on("landsfcutil")
        depends_on("sfcio")

    # GSI dependencies
    with when("+gsi"):
        depends_on("gsi-env")
        depends_on("bufr")
        depends_on("wrf-io")
        depends_on("nemsio")
        depends_on("nemsiogfs")
        depends_on("ncio")
        depends_on("landsfcutil")
        depends_on("sfcio")

    # CI dependencies
    depends_on("pygithub", when="+ci")
    depends_on("gh", when="+ci")

    # There is no need for install() since there is no code.
