# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class NeptunePythonEnv(BundlePackage):
    """Development environment for NEPTUNE standalone with all Python dependencies"""

    # Fake URL
    homepage = "https://github.com/notavalidaccount/neptune"
    git = "https://github.com/notavalidaccount/neptune.git"

    maintainers("climbfuji", "areinecke")

    version("1.5.0")

    variant("gittools", default=False, description="Build additional tools for Git/GitHub")
    variant("lis-ncoda-utils", default=False, description="Build LIS/NCODA utilities")

    depends_on("neptune-env", type="run")
    # Enable the Python variant for ESMF
    depends_on("esmf +python", type="run")

    depends_on("py-arch", type="run")
    depends_on("py-cartopy", type="run")
    depends_on("py-cfgrib", type="run")
    depends_on("py-h5py", type="run")
    depends_on("py-imageio", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pycodestyle", type="run")
    depends_on("py-pybind11", type="run")
    depends_on("py-pyhdf", type="run")
    depends_on("py-regionmask", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-xarray", type="run")
    depends_on("py-pytest", type="run")
    depends_on("py-fortranformat", type="run")

    depends_on("met", type="run")
    depends_on("metplus", type="run")

    with when("+gittools"):
        depends_on("gh", type="run")
        depends_on("py-pygithub", type="run")

    with when("+lis-ncoda-utils"):
        depends_on("py-lis-ncoda-utils", type="run")

    # There is no need for install() since there is no code.
