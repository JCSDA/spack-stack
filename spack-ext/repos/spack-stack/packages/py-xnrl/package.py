# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXnrl(PythonPackage):
    """xNRL helps you read NRL NWP output into xarray Datasets nested within Pandas DataFrames."""

    #homepage = "https://github.nrlmry.navy.mil/Python/xnrl"
    url = "https://github.nrlmry.navy.mil/Python/xnrl/archive/refs/tags/2024.05.23.tar.gz"
    git = "https://github.nrlmry.navy.mil/Python/xnrl.git"

    maintainers("climbfuji")

    license("custom")

    version("main", branch="main")
    version("2024.05.23", sha256="73611e72f4a192c9b93039381fdd085c7f1fe09fbdff4bdeb285f744ad2fb05d")

    variant("numba", default=False, description="Build packages that require py-numba")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-poetry", type="build")

    depends_on("py-metpy", type=("build", "run"))
    # Note: if the +delayed option is removed, also
    # need to remove it from gmao-swell-env.
    depends_on("py-dask +delayed", type=("build", "run"))
    depends_on("py-h5netcdf", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    depends_on("py-ecmwflibs", type=("build", "run"))
    depends_on("eccodes", type=("build", "run"))
    depends_on("py-cfgrib", type=("build", "run"))
    depends_on("py-cf-xarray", type=("build", "run"))
    # Does not exist in spack, and is deprecated - ignore
    #depends_on("py-pygrib", type=("build", "run"))
    depends_on("py-cartopy", type=("build", "run"))
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    # Turn off performance variant to avoid py-numba and llvm compiler dependency
    depends_on("py-pandas ~performance", type=("build", "run"), when="~numba")
    depends_on("py-pandas +performance", type=("build", "run"), when="+numba")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-xesmf", type=("build", "run"), when="+numba")
    depends_on("py-xskillscore", type=("build", "run"), when="+numba")
