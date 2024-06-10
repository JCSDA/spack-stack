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
    #version("2023.10.11", sha256="beff36e3b766449b1a341735b517fbab25331e7363ac21ffc544da284432a482")
    #version("2022.09.29", sha256="xxxxyyyy509f58f3fe518c12dd5a488c67123fdd66ccb0b968b34fd11e512153")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    #depends_on("py-poetry@1.6.1", type="build")
    depends_on("py-poetry", type="build")

    #depends_on("eccodes", type=("build", "run"))
    #depends_on("py-netcdf4@1.6.4:", type=("build", "run"))
    #depends_on("py-h5netcdf@1.2.0:", type=("build", "run"))
    #depends_on("py-numpy@1.25.2:", type=("build", "run"))
    #depends_on("py-xarray@2023.9.0:", type=("build", "run"))
    #depends_on("py-metpy@1.5.1:", type=("build", "run"))
    #depends_on("py-dask@2023.9.3: +delayed", type=("build", "run"))
    #depends_on("py-netcdf4", type=("build", "run"))
    #depends_on("py-h5netcdf", type=("build", "run"))
    #depends_on("py-numpy", type=("build", "run"))
    #depends_on("py-xarray", type=("build", "run"))
    #depends_on("py-metpy", type=("build", "run"))
    #depends_on("py-dask +delayed", type=("build", "run"))

    #depends_on("py-metpy@1.4.1:", type=("build", "run"))
    depends_on("py-metpy", type=("build", "run"))
    #depends_on("py-dask@2023.3.2: +delayed", type=("build", "run"))
    depends_on("py-dask +delayed", type=("build", "run"))
    #depends_on("py-h5netcdf@1.1.0:", type=("build", "run"))
    depends_on("py-h5netcdf", type=("build", "run"))
    #depends_on("py-netcdf4@1.6.3:", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    #depends_on("py-numpy@1.24.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    #depends_on("py-tqdm@4.65.0:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    #depends_on("py-xarray@2023.3.0:", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    #depends_on("py-ecmwflibs@:0.5.3", type=("build", "run"))
    depends_on("py-ecmwflibs", type=("build", "run"))
    #depends_on("eccodes@1.6.1:", type=("build", "run"))
    depends_on("eccodes", type=("build", "run"))
    #depends_on("py-cfgrib@0.9.10.4", type=("build", "run"))
    depends_on("py-cfgrib", type=("build", "run"))
    #depends_on("py-cf-xarray@0.8.4:", type=("build", "run"))
    depends_on("py-cf-xarray", type=("build", "run"))
    # does not exist, deprecated:
    #depends_on("py-pygrib@2.1.4:", type=("build", "run"))
    #depends_on("py-cartopy@0.22.0:", type=("build", "run"))
    depends_on("py-cartopy", type=("build", "run"))
    #depends_on("py-cftime@1.6.3:", type=("build", "run"))
    depends_on("py-cftime", type=("build", "run"))
    #depends_on("py-h5py@3.11.0:", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    # stdlib:
    #depends_on("importlib@1.0.4:", type=("build", "run"))
    #depends_on("py-matplotlib@3.9.0:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    #depends_on("py-pandas@2.2.2:", type=("build", "run"))
    ### Turn off performance variant to avoid py-numba and llvm compiler dependency
    depends_on("py-pandas ~performance", type=("build", "run"))
    #depends_on("py-pandas", type=("build", "run"))
    #depends_on("py-scipy@1.13.1:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    # TRY WITHOUT xESMF
    #depends_on("py-xesmf@0.8.5:", type=("build", "run"))
    ### depends_on("py-xesmf", type=("build", "run"))
    # TRY WITHOUT BECAUSE OF NUMBA
    #depends_on("py-xskillscore@0.0.26:", type=("build", "run"))
    #depends_on("py-xskillscore", type=("build", "run"))

    #def url_for_version(self, version):
    #    if version == Version("2022.09.29"):
    #        url = f"https://github.com/U-S-NRL-Marine-Meteorology-Division/xnrl/archive/refs/tags/{version}.tar.gz"
    #    else:
    #        url = f"https://github.nrlmry.navy.mil/Python/xnrl/archive/refs/tags/{version}.tar.gz"
    #    return url.format(version)
