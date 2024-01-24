# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediToolsEnv(BundlePackage):
    """Development environment for jedi-tools"""

    homepage = "https://github.com/JCSDA-internal/jedi-tools"
    git = "https://github.com/JCSDA-internal/jedi-tools.git"

    maintainers("climbfuji", "srherbener")

    version("1.0.0")

    variant("latex", default=False, description="Enable building LaTeX documentation with Sphinx")

    depends_on("awscli-v2", type="run")
    # Don't install aws-parallelcluster via spack, this is
    # not well maintained package with strict dependencies.
    # Use a venv on top of spack-stack instead.
    # depends_on("aws-parallelcluster", type="run")
    depends_on("py-click", type="run")
    depends_on("py-openpyxl", type="run")
    depends_on("py-pandas +excel", type="run")
    depends_on("py-pygithub", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-sphinx", type="run")
    depends_on("py-myst-parser", type="run")
    depends_on("py-sphinxcontrib-bibtex", type="run")
    depends_on("texlive", when="+latex", type="run")

    conflicts("%intel", msg="jedi-tools-env does not build with Intel")

    # There is no need for install() since there is no code.
