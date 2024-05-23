# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediNeptuneEnv(BundlePackage):
    """Development environment for neptune-bundle"""

    # Fake URL
    homepage = "https://github.com/JCSDA-internal/neptune-bundle"
    git = "https://github.com/JCSDA-internal/neptune-bundle.git"

    maintainers("climbfuji", "areineke")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")
    depends_on("neptune-env", type="run")

    # There is no need for install() since there is no code.
