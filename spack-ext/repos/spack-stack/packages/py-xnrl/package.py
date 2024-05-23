# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXnrl(PythonPackage):
    """xNRL helps you read NRL NWP output into xarray Datasets nested within Pandas DataFrames."""

    #homepage = "https://github.nrlmry.navy.mil/Python/xnrl"
    url = "https://github.nrlmry.navy.mil/Python/xnrl/archive/refs/tags/2023.10.11.tar.gz"
    git = "https://github.nrlmry.navy.mil/Python/xnrl.git"

    maintainers("climbfuji")

    license("custom")

    version("main", branch="main")
    version("2023.10.11", sha256="beff36e3b766449b1a341735b517fbab25331e7363ac21ffc544da284432a482")
    version("2022.09.29", sha256="xxxxyyyy509f58f3fe518c12dd5a488c67123fdd66ccb0b968b34fd11e512153")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-poetry@1.6.1", type="build")

    depends_on("eccodes", type=("build", "run"))
    #depends_on("py-netcdf4@1.6.4:", type=("build", "run"))
    #depends_on("py-h5netcdf@1.2.0:", type=("build", "run"))
    #depends_on("py-numpy@1.25.2:", type=("build", "run"))
    #depends_on("py-xarray@2023.9.0:", type=("build", "run"))
    #depends_on("py-metpy@1.5.1:", type=("build", "run"))
    #depends_on("py-dask@2023.9.3: +delayed", type=("build", "run"))
    depends_on("py-netcdf4", type=("build", "run"))
    depends_on("py-h5netcdf", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-xarray", type=("build", "run"))
    depends_on("py-metpy", type=("build", "run"))
    depends_on("py-dask +delayed", type=("build", "run"))

    def url_for_version(self, version):
        if version == Version("2022.09.29"):
            url = f"https://github.com/U-S-NRL-Marine-Meteorology-Division/xnrl/archive/refs/tags/{version}.tar.gz"
        else:
            url = f"https://github.nrlmry.navy.mil/Python/xnrl/archive/refs/tags/{version}.tar.gz"
        return url.format(version)