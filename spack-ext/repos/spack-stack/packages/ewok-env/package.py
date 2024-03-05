# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EwokEnv(BundlePackage):
    """Development environment for ewok"""

    # DH* TODO UPDATE FROM INTERNAL TO PUBLIC
    homepage = "https://github.com/JCSDA-internal/ewok"
    git = "https://github.com/JCSDA-internal/ewok.git"

    maintainers("climbfuji", "ericlingerfelt")

    version("1.0.0")

    # Variants for workflow engines
    variant("ecflow", default=True, description="Use ecflow workflow engine")
    variant("cylc", default=False, description="Use cylc workflow engine")

    # Variant for MySQL (JEDI-Skylab/R2D2 localhost mode)
    variant("mysql", default=False, description="Provide option to use local MySQL server")

    # Variants defining repositories that are not yet publicly available
    variant("solo", default=False, description="Build solo (general tools for Python programmers)")
    variant(
        "r2d2",
        default=False,
        description="Build R2D2 (Research Repository for Data and Diagnostics)",
    )
    variant(
        "ewok",
        default=False,
        description="Build EWOK (Experiments and Workflows Orchestration Kit)",
    )

    depends_on("jedi-base-env", type="run")
    depends_on("awscli-v2", type="run")
    depends_on("py-boto3", type="run")
    depends_on("py-cartopy", type="run")
    depends_on("py-gitpython", type="run")
    depends_on("py-globus-cli", type="run")
    depends_on("py-jinja2", type="run")
    depends_on("py-ruamel-yaml", type="run")
    depends_on("py-ruamel-yaml-clib", type="run")

    # Workflow engines
    with when("+ecflow"):
        depends_on("ecflow", type="run")
    with when("+cylc"):
        depends_on("py-cylc-flow", type="run")
        depends_on("py-cylc-rose", type="run")
        depends_on("py-cylc-uiserver", type="run")

    # MySQL server for JEDI-Skylab/R2D2 localhost mode
    depends_on("mysql", when="+mysql", type="run")

    # MySQL Python API
    # Comment out for now until build problems are solved
    # https://github.com/jcsda/spack-stack/issues/522
    # depends_on("py-mysql-connector-python", type="run")

    depends_on("solo", when="+solo", type="run")
    depends_on("r2d2", when="+r2d2", type="run")
    depends_on("ewok", when="+ewok", type="run")

    # There is no need for install() since there is no code.
