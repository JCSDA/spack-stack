# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NeptuneEnv(BundlePackage):
    """Development environment for neptune standalone"""

    # Fake URL
    homepage = "https://github.com/notavalidaccount/neptune"
    git = "https://github.com/notavalidaccount/neptune.git"

    maintainers("climbfuji", "areineke")

    version("1.0.0")

    depends_on("base-env", type="run")

    depends_on("mkl", type="run")
    depends_on("numactl", type="run")

    depends_on("libyaml", type="run")
    depends_on("p4est", type="run")
    depends_on("w3emc", type="run")
    depends_on("w3nco", type="run")
    depends_on("ip@5:", type="run")
    depends_on("esmf", type="run")
    depends_on("nco", type="run")
    depends_on("mct", type="run")

    # Required by ESPC, not used by JEDI
    depends_on("fftw", type="build")
    depends_on("netlib-lapack", type="build")

    # There is no need for install() since there is no code.
