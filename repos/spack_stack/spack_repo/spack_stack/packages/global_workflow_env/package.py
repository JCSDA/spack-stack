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

    # Also pulls in (transitively): python (-> sqlite), git (-> gettext),
    # parallelio+pnetcdf (-> parallel-netcdf)
    depends_on("base-env")

    # UFS deps
    # sorc/ufs_model.fd: gfs/gefs/sfs/gcafs model builds (sorc/build_ufs.sh); also
    # covers NEXUS (gefs/gcafs). Default +python pulls ufs-pyenv (py-jinja2
    # -> py-markupsafe, py-netcdf4 -> py-certifi, py-pandas -> py-pytz, py-numpy,
    # py-pyyaml, py-f90nml, py-python-dateutil, ...), the runtime python modules
    # loaded by modulefiles/gw_run.common.lua and the py-wxflow prerequisites
    depends_on("ufs-weather-model-env")
    # sorc/ufs_utils.fd (sorc/build_ufs_utils.sh); also provides, for all variants:
    # nco (-> antlr, gsl, udunits, zstd), prod-util, wgrib2 (-> g2c), bufr, sigio,
    # sfcio, nemsio, nemsiogfs, ncio, landsfcutil, wrf-io, netcdf-cxx, esmf, ip,
    # sp (^ip@:4), g2, g2tmpl, jasper, libpng, bacio, w3emc -- i.e. everything the
    # gfs_utils/UPP/GSI builds and the runtime modulefiles need from NCEPlibs
    depends_on("ufs-utils-env")

    #global workflow deps
    depends_on("py-wxflow")  # workflow framework (ush/python/pygfs, workflow/, sorc/wxflow); also GCAFS venv (versions/requirements_gcafs.txt)
    depends_on("grib-util")  # runtime: cnvgrib/grbindex/tocgrib2 (wave prdgen, AWIPS, prep scripts); pulls g2c and w3nco (also UPP/nemsio deps)
    depends_on("cdo")  # runtime: wave prep (dev/jobs/JGLOBAL_WAVE_PREP), ush/ocnice_extractvars.sh; pulls eccodes -> openjpeg

    #GCAFS deps only
    depends_on("py-mpi4py")  # FIXME not referenced anywhere in global-workflow, incl. versions/requirements_gcafs.txt -- verify

    #metplus dependencies (verification: sorc/verif-global.fd, gw_verif.* modulefiles)
    # NOTE per versions/spack.ver, met@11.1.1/metplus@5.1.0 are incompatible with verif-global
    depends_on("met", when="+metplus")  # pulls g2c, gsl, netcdf-cxx4
    depends_on("metplus", when="+metplus")

    #uwtools dependencies
    depends_on("uwtools", when="+uwtools")

    # GDASApp dependencies (sorc/gdas.cd, JEDI-based DA; sorc/build_gdas.sh)
    with when("+gdas"):
        # jedi-base-env member: py-scipy, eccodes, bufr, netcdf-cxx4,
        # hdf (-> libjpeg-turbo, the "libjpeg" runtime module), boost, atlas, ...
        depends_on("jedi-fv3-env")
        depends_on("jedi-tools-env")  # also provides py-pygithub, awscli-v2
        depends_on("ioda")  # requires netcdf-cxx (from ufs-utils-env)
        depends_on("pigz")  # loaded by sorc/gdas.cd wcoss2 modulefile; not provided by any env

    # GSI dependencies (sorc/gsi_enkf.fd, gsi_utils.fd, gsi_monitor.fd;
    # gsi_utils is also built for gdas and gcafs per sorc/build_opts.yaml)
    # provides crtm, gsi-ncdiag, bufr, ncio, nemsio, sfcio, sigio, wrf-io, lapack
    depends_on("gsi-env", when="+gsi")

    # CI dependencies (dev/ci scripts: utils/githubpr.py, driver_weekly.sh)
    depends_on("py-pygithub", when="+ci")  # NOTE was "pygithub", which is not a spack package
    depends_on("gh", when="+ci")

    # There is no need for install() since there is no code.
