# Copyright 2013-2026 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class GeosGcmEnv(BundlePackage):
    """Development environment for GEOS-GCM"""

    homepage = "https://gmao.gsfc.nasa.gov/GEOS_systems"
    git = "https://github.com/GEOS-ESM/GEOSgcm"

    maintainers("climbfuji", "mathomp4", "Dooruk")

    # Current version
    version("12.1.0")
    version("11.10.0", preferred=True)

    variant("debug", default=False, description="Build debug version of selected dependencies")
    variant("fms", default=True, description="Build FMS as part of the environment")
    variant("cdo", default=True, description="Build CDO as part of the environment")
    variant("grads", default=False, description="Build GrADS as part of the environment")

    depends_on("base-env", type="run")

    depends_on("blas", type="run")
    depends_on("lapack", type="run")

    depends_on("mepo", type="run")
    depends_on("esmf ~debug", type="run", when="~debug")
    depends_on("esmf +debug", type="run", when="+debug")

    depends_on(
        "fms@2024.03 precision=32,64 ~gfs_phys +openmp +pic constants=GEOS +deprecated_io +yaml build_type=Release", #noqa: E501
        type="run",
        when="@11.10:12.0 +fms",
    )

    depends_on(
        "fms@2026.01.01 precision=mixed ~gfs_phys +openmp +pic constants=GEOS +yaml build_type=Release", #noqa: E501
        type="run",
        when="@12.1: +fms",
    )

    # mapl is built as part of GEOS, don't load;
    # needs external gftl-shared/fargparse/pflogger
    # depends_on("mapl", type="run")
    depends_on("gftl-shared", type="run")
    depends_on("fargparse", type="run")
    depends_on("pflogger", type="run")
    depends_on("pfunit", type="run")
    #
    depends_on("py-numpy", type="run")
    depends_on("py-pyyaml", type="run")
    depends_on("py-ruamel-yaml", type="run")
    depends_on("udunits", type="run")

    # Needed for f2py
    depends_on("meson", type="run")
    depends_on("ninja", type="run")

    depends_on("perl", type="run")

    depends_on("py-cmocean", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-xarray", type="run")
    depends_on("py-cartopy", type="run")

    depends_on("nco", type="run")
    depends_on("nccmp", type="run")
    depends_on("cdo", type="run", when="+cdo")

    depends_on("grads", type="run", when="+grads")

    # There is no need for install() since there is no code.
