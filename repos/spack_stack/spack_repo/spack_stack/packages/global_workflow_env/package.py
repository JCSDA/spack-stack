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
    variant("ci", default=False, description="Build for automated CI testing")

    depends_on("base-env")
    depends_on("ufs-pyenv")
    depends_on("prod-util")
    depends_on("grib-util")
    depends_on("pigz")
    depends_on("zstd")
    depends_on("gettext")
    depends_on("sqlite")
    depends_on("libjpeg")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("openjpeg")
    depends_on("proj")
    depends_on("nco")
    depends_on("udunits")
    depends_on("antlr")
    depends_on("cdo")
    depends_on("parallel-netcdf")
    depends_on("gsl")
    depends_on("esmf")
    depends_on("py-mpi4py")
    depends_on("py-scipy")
    depends_on("py-certifi")
    depends_on("py-markupsafe")
    depends_on("py-jinja2")
    depends_on("py-pytz")
    depends_on("py-six")
    depends_on("py-xarray")
    depends_on("g2c")
    depends_on("w3nco")
    depends_on("nemsio")
    depends_on("nemsiogfs")
    depends_on("ncio")
    depends_on("landsfcutil")
    depends_on("sigio")
    depends_on("bufr")
    depends_on("wgrib2")
    depends_on("met", when="+metplus")
    depends_on("metplus", when="+metplus")
    depends_on("py-wxflow")
    depends_on("uwtools", when="+uwtools")
    depends_on("upp-env")
    depends_on("ufs-util-env")

    depends_on("ufs-weather-model-env")

    if "+gdas" in spec:
        depends_on("jedi-fv3-env")
        depends_on("jedi-tools-env")
        depends_on("jedi-um-env")
        depends_on("ioda")
        depends_on("nghttp2")
        depends_on("py-tzdata")
        depends_on("krb5")

    depends_on("gsi-env", when="+gsi")

    if "+ci" in spec:
        depends_on("codecov")
        depends_on("pygithub")
        depends_on("gh")

    # There is no need for install() since there is no code.
