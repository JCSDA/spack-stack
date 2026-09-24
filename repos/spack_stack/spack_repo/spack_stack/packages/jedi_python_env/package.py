# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class JediPythonEnv(BundlePackage):
    """Python dependencies for JEDI applications, on top of jedi-base-env"""

    homepage = "https://github.com/jcsda/spack-stack"
    git = "https://github.com/jcsda/spack-stack.git"

    maintainers("climbfuji", "srherbener")

    version("1.0.0")

    # Mirrors the jedi-base-env variant so py-pyhdf tracks the hdf4 library
    variant("hdf4", default=True, description="Build hdf4 library and python hdf module")
    variant("bufrquery", default=True, description="Build bufr-query library")

    depends_on("jedi-base-env", type="run")
    depends_on("jedi-base-env +hdf4", when="+hdf4", type="run")
    depends_on("jedi-base-env ~hdf4", when="~hdf4", type="run")

    # bufr is built +python in configs/common/packages.yaml, so it carries a
    # py-numpy run dependency; bufr-query is its python-bindings companion.
    depends_on("bufr", type="run")
    depends_on("bufr-query", when="+bufrquery", type="run")

    # Python packages
    depends_on("py-eccodes", type="run")
    depends_on("py-f90nml", type="run")
    depends_on("py-h5py", type="run")
    depends_on("py-netcdf4", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-pycodestyle", type="run")
    depends_on("py-pyhdf", when="+hdf4", type="run")
    depends_on("py-python-dateutil", type="run")
    depends_on("py-pyyaml", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-xarray", type="run")

    # There is no need for install() since there is no code.
