# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediGeosEnv(BundlePackage):
    """Development environment for JEDI-GEOS"""

    homepage = "https://github.com/JCSDA/jedi-bundle"
    git = "https://github.com/JCSDA/jedi-bundle.git"

    maintainers("climbfuji", "srherbener")

    version("1.0.0")

    depends_on("jedi-base-env", type="run")
    #depends_on("blas", type="run")
    depends_on("mepo", type="run")
    depends_on("esmf", type="run")
    # mapl is built as part of GEOS, don't load;
    # needs external gftl-shared/fargparse/pflogger
    # depends_on("mapl", type="run")
    depends_on("gftl-shared", type="run")
    depends_on("fargparse", type="run")
    depends_on("pflogger", type="run")
    #
    depends_on("py-numpy", type="run")

    # There is no need for install() since there is no code.
