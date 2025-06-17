# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class FalconEnv(BundlePackage):
    """Development environment for NEPTUNE-JEDI (FALCON)"""

    # Fake URL
    homepage = "https://github.nrlmry.navy.mil/falcon/neptune-bundle"
    git = "https://github.nrlmry.navy.mil/falcon/neptune-bundle.git"

    maintainers("climbfuji", "sking112")

    version("1.0.0")

    variant("jedi", default=False, description="Build JEDI components")

    depends_on("neptune-env", type="run")
    depends_on("neptune-python-env", type="run")

    depends_on("bison", type="run")
    depends_on("blas", type="run")
    depends_on("boost", type="run")
    depends_on("bufr", type="run")
    depends_on("bufr-query", type="run")
    depends_on("ecbuild", type="run")
    depends_on("eccodes", type="run")
    depends_on("eckit", type="run")
    depends_on("ecmwf-atlas", type="run")
    depends_on("eigen", type="run")
    depends_on("fckit", type="run")
    depends_on("fftw-api", type="run")
    depends_on("flex", type="run")
    depends_on("git-lfs", type="run")
    #depends_on("gsibec", type="run")
    depends_on("gsl-lite", type="run")
    #depends_on("hdf", when="+hdf4", type="run")
    depends_on("jedi-cmake", type="run")
    depends_on("netcdf-cxx", type="run")
    depends_on("nccmp", type="run")
    depends_on("ncview", type="run")
    depends_on("nlohmann-json", type="run")
    depends_on("nlohmann-json-schema-validator", type="run")
    depends_on("odc", type="run")
    #depends_on("sp", type="run", when="^ip@:4")
    depends_on("udunits", type="run")

    with when("+jedi"):
        depends_on("oops", type="run")
        depends_on("crtm", type="run")
        depends_on("ioda", type="run")
        depends_on("ropp-ufo", type="run")
        depends_on("ufo", type="run")

    # There is no need for install() since there is no code.
