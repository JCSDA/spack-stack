# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage

from spack.package import *


class JediNeptuneEnv(BundlePackage):
    """Development environment for neptune-bundle"""

    # Fake URL
    homepage = "https://github.com/JCSDA-internal/neptune-bundle"
    git = "https://github.com/JCSDA-internal/neptune-bundle.git"

    maintainers("climbfuji", "areineke")

    version("1.0.0")

    variant("adp", default=False, description="Build ADP preprocessors")

    variant("jedi", default=False, description="Build JEDI components required for JEDI-NEPTUNE")

    depends_on("jedi-base-env", type="run")
    depends_on("neptune-env", type="run")
    depends_on("neptune-python-env", type="run")

    with when("+adp"):
        depends_on("adp-preprocessors", type="run")

    with when("+jedi"):
        depends_on("oops", type="run")
        depends_on("crtm@v2.4.1-jedi.2", type="run")
        depends_on("ioda", type="run")
        depends_on("ioda-converters", type="run")
        depends_on("ropp-ufo", type="run")
        depends_on("ufo +crtm-v2 +ropp", type="run")

    # There is no need for install() since there is no code.
