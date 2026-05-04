# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class DevUtilsEnv(BundlePackage):
    """Commonly used development utilities"""

    homepage = "https://github.com/jcsda/spack-stack"
    git = "https://github.com/jcsda/spack-stack.git"

    maintainers("climbfuji", "AlexanderRichert-NOAA")

    version("1.0.0")

    variant("scalasca", default=False, description="Build Scalasca/Cube")

    depends_on("base-env", type="run")

    # I/O

    # Python
    depends_on("py-pydantic +dotenv", type="run")
    depends_on("py-pydantic-settings", type="run")

    # Scalasca/ScoreP
    depends_on("scalasca", when="+scalasca", type="run")
    depends_on("cube +gui", when="+scalasca", type="run")
  
    # Miscellaneous
    depends_on("cloc", type="run")
    depends_on("rank-run", type="run")

    # There is no need for install() since there is no code.
