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
        depends_on("oops@1.10.0.20250827", type="run")
        depends_on("crtm@3.1.3", type="run")
        depends_on("ioda@2.9.0.20250826", type="run")
        depends_on("ioda-converters@0.0.1.20250830", type="run")
        depends_on("ropp-ufo@11.0.20251022", type="run")
        depends_on("ufo@1.10.0.20250821 +ropp", type="run")
