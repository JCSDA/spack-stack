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

    # UFS deps
    # sorc/ufs_model.fd: gfs/gefs/sfs/gcafs model builds (sorc/build_ufs.sh); also
    # covers NEXUS (gefs/gcafs), whose modulefiles only load a subset of these libs
    depends_on("ufs-weather-model-env")
    # sorc/ufs_utils.fd (sorc/build_ufs_utils.sh); note this env also provides, for all
    # variants: nco, prod-util, wgrib2, bufr, sigio, sfcio, nemsio, nemsiogfs, ncio,
    # landsfcutil, wrf-io, netcdf-cxx
    depends_on("ufs-utils-env")
    # py-netcdf4/numpy/pandas/pyyaml/f90nml/dateutil/jinja2 loaded at runtime
    # (modulefiles/gw_run.common.lua, versions/spack.ver)
    depends_on("ufs-pyenv")

    #global workflow deps
    depends_on("py-wxflow")  # workflow framework (ush/python/pygfs, workflow/, sorc/wxflow); also GCAFS venv (versions/requirements_gcafs.txt)
    depends_on("py-scipy")  # GDASApp/EVA (sorc/gdas.cd modulefiles; member of jedi-base-env); no direct workflow import found
    depends_on("py-certifi")  # GCAFS venv (versions/requirements_gcafs.txt); also py-requests/py-netcdf4 dep
    depends_on("py-markupsafe")  # py-jinja2 dep; GCAFS venv
    depends_on("py-jinja2")  # parm template rendering via wxflow; runtime module (gw_run.common.lua, gw_setup.*); GDASApp; GCAFS venv
    depends_on("py-pytz")  # py-pandas dep; no direct workflow use found
    depends_on("parallel-netcdf")  # UFS model PnetCDF I/O; GDASApp modulefiles
    depends_on("netcdf-cxx")  # ioda dep (GDASApp); no direct workflow use found
    depends_on("grib-util")  # runtime: cnvgrib/grbindex/tocgrib2 (wave prdgen, AWIPS, prep scripts); gw_run.common.lua
    depends_on("sigio")  # build: gfs_utils and GSI (spectral sigma I/O); also in ufs-utils-env/gsi-env
    depends_on("wgrib2")  # runtime: product/stat scripts in ush and scripts; build: gfs_utils
    depends_on("nco")  # runtime: ncks etc. (ush/ocnice_extractvars.sh, ush/wave_prnc_cur.sh); GDASApp modulefiles
    depends_on("prod-util")  # runtime: ndate/setpdy, UTILROOT (gw_run.common.lua); GSI build modulefiles
    depends_on("antlr")  # nco dep; no direct workflow use found
    depends_on("pigz")  # GDASApp wcoss2 modulefile only; candidate for +gdas
    depends_on("zstd")  # netcdf compression for UFS model output (UFSATM io); nco dep; wcoss2 modulefiles (ufs/gdas/nexus)
    depends_on("gettext")  # GDASApp modulefiles only; candidate for +gdas
    depends_on("libjpeg")  # wcoss2 runtime graphics (gempak/imagemagick, gw_run.wcoss2.lua); GDASApp modulefiles
    depends_on("openjpeg")  # GRIB2 JPEG2000 codec for wgrib2 and eccodes (GDASApp)
    depends_on("w3nco")  # grib-util/nemsio/UPP dep; find_package in sorc/CMakeLists.txt (workflow_utils)
    depends_on("cdo")  # runtime: wave prep (dev/jobs/JGLOBAL_WAVE_PREP), ush/ocnice_extractvars.sh; gw_run.common.lua
    depends_on("gsl")  # nco and MET dep; runtime module (gw_run.wcoss2.lua)

    #rocoto deps (workflow manager, loaded by gw_setup.* modulefiles)
    depends_on("sqlite")

    #GCAFS deps only
    depends_on("py-mpi4py")  # FIXME not referenced anywhere in global-workflow, incl. versions/requirements_gcafs.txt -- verify

    # grib/product-processing libs: gfs_utils and UPP builds, which are built for every
    # system ("common" in sorc/build_opts.yaml); most also UFS deps via the envs above
    depends_on("ip")  # gfs_utils, GSI, UPP, grib-util, wgrib2 #ufs
    depends_on("sp", when="^ip@:4")  # legacy companion to ip@:4; GSI, UPP, grib-util #ufs
    depends_on("jasper")  # GRIB2 JPEG2000 codec (g2, grib-util); NEXUS #ufs
    depends_on("libpng")  # GRIB2 PNG codec (g2, wgrib2); gfs_utils build; NEXUS #ufs
    depends_on("bacio")  # NCEP binary I/O, used by gfs_utils/GSI/UPP and NCEP libs; NEXUS #ufs
    depends_on("esmf")  # UFS model, GDASApp, UFS_UTILS, NEXUS; runtime module (gw_run.common.lua) #ufs
    depends_on("g2")  # gfs_utils build, grib-util, UPP #ufs
    depends_on("g2tmpl")  # UPP GRIB2 templates; runtime module (gw_run.common.lua) #ufs
    depends_on("g2c")  # wgrib2, grib-util, and MET dep
    depends_on("w3emc")  # gfs_utils, GSI, gsi_monitor, UPP, grib-util #ufs

    #metplus dependencies (verification: sorc/verif-global.fd, gw_verif.* modulefiles)
    # NOTE per versions/spack.ver, met@11.1.1/metplus@5.1.0 are incompatible with verif-global
    depends_on("met", when="+metplus")
    depends_on("metplus", when="+metplus")

    #uwtools dependencies
    depends_on("uwtools", when="+uwtools")

    # GDASApp dependencies (sorc/gdas.cd, JEDI-based DA; sorc/build_gdas.sh)
    with when("+gdas"):
        depends_on("jedi-fv3-env")
        depends_on("jedi-tools-env")
        depends_on("ioda")  # requires netcdf-cxx
        # The NCEP I/O formats below are also unconditional gfs_utils build deps
        # (gfs_utils.fd/modulefiles/gfsutils_common.lua); covered for all variants
        # by ufs-utils-env
        depends_on("wrf-io")
        depends_on("nemsio")
        depends_on("nemsiogfs")
        depends_on("ncio")
        depends_on("landsfcutil")
        depends_on("sfcio")

    # GSI dependencies (sorc/gsi_enkf.fd, gsi_utils.fd, gsi_monitor.fd;
    # gsi_utils is also built for gdas and gcafs per sorc/build_opts.yaml)
    with when("+gsi"):
        depends_on("gsi-env")
        depends_on("bufr")  # also unconditional gfs_utils build dep (gfs_bufr, tocsbufr); covered by ufs-utils-env
        # same note as +gdas: also unconditional gfs_utils build deps, covered by ufs-utils-env
        depends_on("wrf-io")
        depends_on("nemsio")
        depends_on("nemsiogfs")
        depends_on("ncio")
        depends_on("landsfcutil")
        depends_on("sfcio")

    # CI dependencies (dev/ci scripts: utils/githubpr.py, driver_weekly.sh)
    depends_on("pygithub", when="+ci")
    depends_on("gh", when="+ci")

    # There is no need for install() since there is no code.
