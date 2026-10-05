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
    variant("uwtools", default=True, description="Build uwtools")
    variant("metplus", default=True, description="Build METplus to support verifiation")
    variant("gdas", default=True, description="Build for GDASApp DA support")
    variant("gsi", default=True, description="Build for GSI DA support")
    variant("ci", default=True, description="Build for automated CI testing")

    # Core: python, cmake, git, hdf5, netcdf-c, netcdf-fortran
    depends_on("base-env")

    # UFS deps
    depends_on("ufs-weather-model-env")
    depends_on("ufs-utils-env")

    # global workflow deps
    depends_on("py-wxflow")
    depends_on("py-jinja2")
    depends_on("py-pyyaml")
    depends_on("py-numpy")
    depends_on("py-netcdf4")
    depends_on("py-xarray")
    depends_on("py-pandas")
    depends_on("py-python-dateutil")
    depends_on("py-f90nml")
    depends_on("wgrib2")
    depends_on("nco")
    depends_on("cdo")
    depends_on("grib-util")
    depends_on("prod-util")
    depends_on("esmf")
    depends_on("sp")
    depends_on("g2tmpl")
    depends_on("crtm")
    depends_on("gsi-ncdiag")
    depends_on("bufr")
    depends_on("jasper")
    depends_on("libpng")

    #metplus dependencies
    depends_on("met", when="+metplus")
    depends_on("metplus", when="+metplus")
    depends_on("imagemagick", when="+metplus")

    #uwtools dependencies
    depends_on("uwtools", when="+uwtools")

    # GDASApp dependencies
    with when("+gdas"):
        depends_on("jedi-fv3-env")
        depends_on("jedi-tools-env")
        depends_on("ioda")
        depends_on("pigz")

    # GSI dependencies
    depends_on("gsi-env", when="+gsi")

    # CI dependencies
    depends_on("py-pygithub", when="+ci")
    depends_on("gh", when="+ci")

    # There is no need for install() since there is no code.
