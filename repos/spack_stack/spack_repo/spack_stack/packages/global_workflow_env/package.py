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

    depends_on("ufs-pyenv")
    depends_on("prod-util")
    depends_on("grib-util")
    depends_on("zlib")
    depends_on("pigz")
    depends_on("zstd")
    depends_on("gettext")
    depends_on("sqlite")
    depends_on("cmake")
    depends_on("libjpeg")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("openjpeg")
    depends_on("proj")
    depends_on("nco")
    depends_on("udunits")
    depends_on("hdf5")
    depends_on("antlr")
    depends_on("cdo")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("parallel-netcdf")
    depends_on("parallelio")
    depends_on("gsl")
    depends_on("esmf")
    depends_on("bacio")
    depends_on("py-mpi4py")
    depends_on("py-scipy")
    depends_on("py-certifi")
    depends_on("py-markupsafe")
    depends_on("py-jinja2")
    depends_on("py-pytz")
    depends_on("py-setuptools")
    depends_on("py-six")
    depends_on("py-xarray")
    depends_on("g2")
    depends_on("g2c")
    depends_on("g2tmpl")
    depends_on("w3nco")
    depends_on("w3emc")
    depends_on("sp", when="^ip@:4")
    depends_on("ip")
    depends_on("nemsio")
    depends_on("nemsiogfs")
    depends_on("ncio")
    depends_on("landsfcutil")
    depends_on("sigio")
    depends_on("bufr")
    depends_on("wgrib2")
    depends_on("met", when="+metplus")
    depends_on("metplus", when="+metplus")
    depends_on("crtm")
    depends_on("py-wxflow")
    depends_on("uwtools", when="+uwtools")
    # Check if the gdas variant is enabled
    if "+gdas" in spec:
        depends_on("nghttp2")
        depends_on("curl")
        depends_on("openssl")
        depends_on("eccodes")
        depends_on("libxt")
        depends_on("libxmu")
        depends_on("py-pybind11")
        depends_on("snappy")
        depends_on("libxpm")
        depends_on("c-blosc")
        depends_on("eckit")
        depends_on("libxaw")
        depends_on("fckit")
        depends_on("fiat")
        depends_on("fms")
        depends_on("netcdf-cxx4")
        depends_on("json")
        depends_on("py-packaging")
        depends_on("ectrans")
        depends_on("qhull")
        depends_on("atlas")
        depends_on("py-tzdata")
        depends_on("gsl-lite")
        depends_on("krb5")
        depends_on("libtirpc")
        depends_on("py-click")
        depends_on("hdf")
        depends_on("ecbuild")
        depends_on("jedi-cmake")

    if "+gsi" in spec:
        depends_on("sfcio")
        depends_on("wrfio")
        depends_on("gsi-ncdiag")

    if "+ci" in spec:
        depends_on("pytest")
        depends_on("pytest-cov")
        depends_on("codecov")
        depends_on("pygithub")
        depends_on("gh")

    # There is no need for install() since there is no code.
