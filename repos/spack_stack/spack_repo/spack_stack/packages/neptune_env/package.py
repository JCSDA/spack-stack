# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class NeptuneEnv(BundlePackage):
    """Development environment for NEPTUNE standalone"""

    # Fake URL
    homepage = "https://github.com/notavalidaccount/neptune"
    git = "https://github.com/notavalidaccount/neptune.git"

    maintainers("climbfuji", "areinecke")

    version("1.5.0")

    variant("espc", default=False, description="Build ESPC dependencies")
    variant("ncview", default=False, description="Build ncview")
    variant("debug", default=False, description="Build debug version of selected dependencies")
    variant("openmp", default=True, description="Build OpenMP-enabled versions of dependencies")

    depends_on("base-env", type="run")

    depends_on("blas", type="run")
    depends_on("lapack", type="run")
    if not sys.platform == "darwin":
        depends_on("numactl", type="run")

    depends_on("codee", type="run")
    depends_on("libyaml", type="run")
    depends_on("p4est", type="run")
    depends_on("w3emc", type="run")
    depends_on("ip ~openmp", type="run", when="~openmp")
    depends_on("ip +openmp", type="run", when="+openmp")
    depends_on("esmf ~debug ~openmp", type="run", when="~debug ~openmp")
    depends_on("esmf ~debug +openmp", type="run", when="~debug +openmp")
    depends_on("esmf +debug ~openmp", type="run", when="+debug ~openmp")
    depends_on("esmf +debug +openmp", type="run", when="+debug +openmp")
    depends_on("nco", type="run")
    depends_on("mct", type="run")

    with when("+espc"):
        depends_on("fftw", type="run")
        depends_on("netlib-lapack", type="run")

    with when("+ncview"):
        depends_on("ncview", type="run")

    # Basic Python dependencies that are always needed
    depends_on("py-f90nml", type="run")
    depends_on("py-python-dateutil", type="run")
    depends_on("py-pyyaml", type="run")

    # There is no need for install() since there is no code.
