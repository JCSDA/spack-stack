# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyLisNcodaUtils(PythonPackage):
    """Utility to convert LIS and NCODA files for NEPTUNE."""

    homepage = "https://github.nrlmry.navy.mil/neptune/lis-ncoda-utils"
    url = "https://github.nrlmry.navy.mil/neptune/lis-ncoda-utils/archive/refs/tags/2.0.0.tar.gz"
    git = "https://github.nrlmry.navy.mil/neptune/lis-ncoda-utils.git"

    maintainers("climbfuji")

    license("custom")

    version("develop", branch="develop")
    version("2.0.0", commit="85cb17c70705e88d15c5ff191b177090a5136052")

    depends_on("python@3.11:", type=("build", "run"))
    depends_on("fortran", type="build")

    depends_on("cmake@3.15:", type="build")    
    depends_on("py-scikit-build-core", type="build")
    depends_on("py-numpy", type=("build", "run"))
    
    depends_on("py-cfgrib", type="run")
    depends_on("py-h5py", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-xarray", type="run")
