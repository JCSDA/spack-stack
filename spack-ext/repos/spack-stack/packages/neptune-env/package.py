# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class NeptuneEnv(BundlePackage):
    """Development environment for NEPTUNE standalone"""

    # Fake URL
    homepage = "https://github.com/notavalidaccount/neptune"
    git = "https://github.com/notavalidaccount/neptune.git"

    maintainers("climbfuji", "areinecke")

    version("1.5.0")

    variant("espc", default=False, description="Build ESPC dependencies")

    depends_on("base-env", type="run")

    depends_on("blas", type="run")
    depends_on("lapack", type="run")
    if not sys.platform == "darwin":
        depends_on("numactl", type="run")

    depends_on("libyaml", type="run")
    depends_on("p4est", type="run")
    depends_on("w3emc", type="run")
    depends_on("sp", type="run", when="%aocc")
    depends_on("ip@5:", type="run", when="%apple-clang")
    depends_on("ip@5:", type="run", when="%gcc")
    depends_on("ip@5:", type="run", when="%intel")
    depends_on("ip@5:", type="run", when="%oneapi")
    depends_on("esmf +python", when="+python", type="run")
    depends_on("esmf ~python", when="~python", type="run")
    depends_on("nco", type="run")
    depends_on("mct", type="run")

    with when("+espc"):
        depends_on("fftw", type="build")
        depends_on("netlib-lapack", type="build")

    # Basic Python dependencies that are always needed
    depends_on("py-f90nml", type="run")
    depends_on("py-python-dateutil", type="run")

    # There is no need for install() since there is no code.
