# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class JediMetalEnv(BundlePackage):
    """Minimum  development environment for macos tahoe"""

    homepage = "https://github.com/jcsda/spack-stack"
    git = "https://github.com/jcsda/spack-stack.git"

    maintainers("nobody")

    version("1.0.0")

    variant("fftw", default=True, description="Build fftw")
    variant("hdf4", default=True, description="Build hdf4 library and python hdf module")

#    depends_on("base-env", type="run") ########################################
    # Basic utilities
    if sys.platform == "darwin":
        depends_on("libbacktrace", type="run")

    # I/O
    depends_on("zlib-api", type="run")
    depends_on("hdf5", type="run")
    depends_on("netcdf-c", type="run")
    depends_on("netcdf-fortran", type="run")
    depends_on("parallelio", type="run")
    depends_on("nccmp", type="run")

    depends_on("bison", type="run")
    depends_on("boost", type="run")
    depends_on("ecbuild", type="run")
    depends_on("ectrans", type="run")
    depends_on("eckit", type="run")
    depends_on("ecmwf-atlas", type="run")
    depends_on("eigen", type="run")
    depends_on("fckit", type="run")
    depends_on("fftw-api", when="+fftw", type="run")
    depends_on("flex", type="run")
    depends_on("gsl-lite", type="run")
    depends_on("hdf", when="+hdf4", type="run")
    depends_on("jedi-cmake", type="run")
    depends_on("netcdf-cxx4", type="run")
    depends_on("ncview", type="run")
    depends_on("udunits", type="run")

    depends_on("parallel-netcdf", type="run")
    depends_on("parallelio +pnetcdf", type="run")
    depends_on("metis", type="run")
    depends_on("jasper", type="run")

#   depends_on("ecflow", type="run")

    # There is no need for install() since there is no code.
