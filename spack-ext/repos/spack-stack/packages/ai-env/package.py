# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AiEnv(BundlePackage):
    """Development environment for AI/ML applications"""

    # DH* TODO UPDATE FROM INTERNAL TO PUBLIC
    homepage = "https://github.com/JCSDA/spack-stack"
    git = "https://github.comJCSDA/spack-stack.git"

    maintainers("climbfuji", "srherbener")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")
    depends_on("py-torch +internal-protobuf", type="run")

    # There is no need for install() since there is no code.
