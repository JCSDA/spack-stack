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

    depends_on("base-env")

    #UFS deps
    depends_on("ufs-weather-model-env")
    depends_on("ufs-utils-env")
    depends_on("ufs-pyenv")

    #global workflow deps
    depends_on("py-wxflow")
    depends_on("py-scipy")
    depends_on("py-certifi")
    depends_on("py-markupsafe")
    depends_on("py-jinja2")
    depends_on("py-pytz")
    depends_on("parallel-netcdf")
    depends_on("netcdf-cxx")
    depends_on("grib-util")
    depends_on("sigio")
    depends_on("wgrib2")
    depends_on("nco")
    depends_on("prod-util")
    depends_on("antlr")
    depends_on("pigz")
    depends_on("zstd")
    depends_on("gettext")
    depends_on("libjpeg")
    depends_on("openjpeg")
    depends_on("w3nco")
    depends_on("cdo")
    depends_on("gsl")

    #rocoto deps
    depends_on("sqlite")

    #GCAFS deps only
    depends_on("py-mpi4py")

    #GFS-utils deps only
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

    #metplus dependencies
    depends_on("met", when="+metplus")
    depends_on("metplus", when="+metplus")

    #uwtools dependencies
    depends_on("uwtools", when="+uwtools")

    # GDASApp dependencies
    with when("+gdas"):
        depends_on("jedi-fv3-env", when="+gdas")
        depends_on("jedi-tools-env", when="+gdas")
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
