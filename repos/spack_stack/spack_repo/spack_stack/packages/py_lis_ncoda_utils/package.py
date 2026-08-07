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
    #version("2024.05.23", sha256="73611e72f4a192c9b93039381fdd085c7f1fe09fbdff4bdeb285f744ad2fb05d")

    depends_on("python@3.11:", type=("build", "run"))
    depends_on("fortran", type="build")
    
    depends_on("py-scikit-build-core", type="build")
    depends_on("py-numpy", type=("build", "run"))
    
    depends_on("py-cfgrib", type="run")
    depends_on("py-h5py", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-xarray", type="run")
