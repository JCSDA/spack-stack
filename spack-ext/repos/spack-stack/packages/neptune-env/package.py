# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class NeptuneEnv(BundlePackage):
    """Development environment for neptune standalone"""

    # Fake URL
    homepage = "https://github.com/notavalidaccount/neptune"
    git = "https://github.com/notavalidaccount/neptune.git"

    maintainers("climbfuji", "areinecke")

    version("1.4.0")

    variant("python", default=True, description="Build Python dependencies")
    variant("espc", default=True, description="Build ESPC dependencies")
    variant("xnrl", default=True, description="Build XNRL and its extra Python dependencies")

    depends_on("base-env", type="run")

    depends_on("blas", type="run")
    depends_on("lapack", type="run")
    if not sys.platform == "darwin":
        depends_on("numactl", type="run")

    depends_on("libyaml", type="run")
    depends_on("p4est", type="run")
    depends_on("w3emc", type="run")
    depends_on("w3nco", type="run")
    depends_on("ip@5:", type="run")
    depends_on("esmf", type="run")
    depends_on("nco", type="run")
    depends_on("mct", type="run")

    conflicts("+xnrl", when="~python", msg="Variant xnrl requires variant python")

    with when("+espc"):
        depends_on("fftw", type="build")
        depends_on("netlib-lapack", type="build")

    with when("+python"):
        depends_on("py-f90nml", type="run")
        depends_on("py-h5py", type="run")
        depends_on("py-netcdf4", type="run")
        depends_on("py-pandas", type="run")
        depends_on("py-pycodestyle", type="run")
        depends_on("py-pybind11", type="run")
        depends_on("py-pyhdf", type="run")
        depends_on("py-python-dateutil", type="run")
        depends_on("py-pyyaml", type="run")
        depends_on("py-scipy", type="run")
        depends_on("py-xarray", type="run")
        depends_on("py-pytest", type="run")
        depends_on("py-fortranformat", type="run")

    with when("+xnrl"):
        depends_on("py-xnrl", type="run")

    # There is no need for install() since there is no code.
