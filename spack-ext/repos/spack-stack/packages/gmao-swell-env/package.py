# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GmaoSwellEnv(BundlePackage):
    """Development environment for swell"""

    homepage = "https://geos-esm.github.io/swell/"
    git = "https://github.com/GEOS-ESM/swell"

    maintainers("climbfuji", "danholdaway", "mathomp4")

    # Current version
    version("1.0.0")

    # Main JEDI modules
    depends_on("jedi-base-env", type="run")

    # Add CRTM 2.4.0
    depends_on("crtm@v2.4-jedi.2", type="run")

    # Additional dependencies for JEDI used by swell
    depends_on("fms@2023.04+pic", type="run")
    depends_on("nco", type="run")

    # GEOS
    # depends_on("geos-dev-env", type="run")  # We should have the modules needed to build GEOSgcm

    # Python packages for swell, eva, and other utilities
    depends_on("py-boto3", type="run")
    depends_on("py-cartopy", type="run")
    depends_on("py-click", type="run")
    depends_on("py-contourpy", type="run")
    depends_on("py-gitpython", type="run")
    depends_on("py-jinja2", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-pip", type="run")
    depends_on("py-pkgconfig", type="run")
    depends_on("py-requests", type="run")
    depends_on("py-urllib3", type="run")
    depends_on("py-wheel", type="run")
    depends_on("py-setuptools", type="run")

    # Different versions than other bundles
    depends_on("py-pycodestyle@2.10:", type="run")
    depends_on("py-pyyaml@6:", type="run")

    # Future dependencies needed
    # depends_on("py-bokeh", type="run")
    # depends_on("py-cylc-flow", type="run")
    # depends_on("py-cylc-uiserver", type="run")
    # depends_on("py-flake8", type="run")
    # depends_on("py-hvplot", type="run")
    # depends_on("py-holoviews", type="run")
    # depends_on("py-isodate", type="run")
    # depends_on("py-questionary", type="run")
    # depends_on("py-scikit-learn", type="run")
    # depends_on("py-seaborn", type="run")

    conflicts(
        "%gcc platform=darwin",
        msg="gmao-swell-env does " + "not build with gcc (11?) on macOS (12), use apple-clang",
    )

    # There is no need for install() since there is no code.
