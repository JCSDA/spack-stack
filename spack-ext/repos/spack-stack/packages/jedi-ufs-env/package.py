# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediUfsEnv(BundlePackage):
    """Development environment for ufs-bundle"""

    homepage = "https://github.com/JCSDA/ufs-bundle"
    git = "https://github.com/JCSDA/ufs-bundle.git"

    maintainers("climbfuji", "mark-a-potts")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")
    depends_on("fms@2023.04+pic", type="run")

    depends_on("bacio", type="run")
    depends_on("g2", type="run")
    depends_on("g2tmpl", type="run")
    depends_on("ip", type="run")
    depends_on("nemsio", type="run")
    depends_on("sfcio", type="run")
    depends_on("sigio", type="run")
    depends_on("w3emc", type="run")
    depends_on("w3nco", type="run")
    depends_on("esmf", type="run")
    depends_on("mapl", type="run")

    # There is no need for install() since there is no code.
