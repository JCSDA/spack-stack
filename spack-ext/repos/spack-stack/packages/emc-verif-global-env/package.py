# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EmcVerifGlobalEnv(BundlePackage):
    """Development environment for emc-verif-global"""

    homepage = "https://github.com/NOAA-EMC/EMC_verif-global"
    git = "https://github.com/NOAA-EMC/EMC_verif-global.git"

    maintainers("AlexanderRichert-NOAA")

    version("1.0.0")

    depends_on("python")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("nco")
    depends_on("prod-util")
    depends_on("grib-util")
    depends_on("py-cartopy")
    depends_on("py-numpy")
    depends_on("py-netcdf4")
    depends_on("py-matplotlib")
    depends_on("py-pandas")
    # Test grads
    # depends_on('grads')
    # Currently, wgrib2 doesn't build with oneapi,
    # but there isn't a "when not" option in spack yet
    depends_on("wgrib2", when="%apple-clang")
    depends_on("wgrib2", when="%gcc")
    depends_on("wgrib2", when="%intel")
    depends_on("python")
    depends_on("prod-util")
    depends_on("met")
    depends_on("metplus")

    # There is no need for install() since there is no code.
