# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ufo(CMakePackage):
    """Unified Forward Operator"""

    homepage = "https://github.com/JCSDA/ufo"
    git = "https://github.com/JCSDA/ufo.git"

    maintainers = ["climbfuji"]

    version("develop", branch="develop", no_cache=True)
    version("1.10.0.20241217", commit="49ddba60c484bc5b8bac81b660e3b1b0905cd314")

    variant("crtm-v2", default=True, description="Build CRTM v2 operator")
    variant("crtm-v3", default=False, description="Build CRTM v3 operator")
    # JCSDA-internal repository needed.
    variant("geos-aero", default=False, description="Build GEOS-AERO AOD operator")
    variant("gsw", default=True, description="Build marine observation operators")
    # JCSDA-internal repository is public, but there is no "release" of the code yet.
    variant(
        "oasim", default=False, description="Build with Ocean Atmosphere Spectral Irradiance Model"
    )
    # NRL-internal repository needed.
    variant("ropp", default=False, description="Build ROPP operator")
    # JCSDA-internal repository needed.
    variant("rttov", default=False, description="Build RTTOV operator")

    conflicts("+crtm-v2 +crtm-v3", msg="UFO: choose either CRTM v2 or v3, not both.")

    conflicts("+geos-aero", msg="UFO: GEOS-AERO to be implemented.")
    conflicts("+oasim", msg="UFO: OASIM to be implemented.")
    conflicts("+rttov", msg="UFO: RTTOV to be implemented.")

    depends_on("boost")
    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@1.10:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@1.10:")
    depends_on("eckit")
    depends_on("eckit@1.24.4:", when="@1.10:")
    depends_on("eigen")
    depends_on("fckit")
    depends_on("fckit@0.11.0:", when="@1.10:")
    depends_on("gsl-lite")
    depends_on("ioda")
    # DH* TODO
    depends_on("ioda@2.9", when="@1.10:")
    depends_on("jedi-cmake", type=("build"))
    depends_on("mpi")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")
    depends_on("oops")
    depends_on("oops@1.10", when="@1.10")

    depends_on("crtm@v2", when="+crtm-v2")
    # DH* TODO UPDATE
    depends_on("crtm@=v2.4.1-jedi", when="@1.10 +crtm-v2")
    #depends_on("crtm@=v2.4.1-jedi.2", when="@1.10 +crtm-v2")
    # *DH

    depends_on("crtm@3", when="+crtm-v3")
    # DH* TODO UPDATE
    depends_on("crtm@=3.1.1.2", when="@1.10 +crtm-v3")
    #depends_on("crtm@=3.1.2", when="@1.10 +crtm-v3")
    # *DH

    # depends_on('geos-aero', when='+geos-aero')
    # depends_on('geos-aero@0.0.0', when='@1.7.0 +geos-aero')

    # depends_on('oasim', when='+oasim')
    # depends_on('oasim@0.0.0', when='@1.7.0 +oasim')

    depends_on("gsw", when="+gsw")
    depends_on("gsw@3.0.7", when="@1.7: +gsw")

    depends_on('ropp-ufo', when='+ropp')
    depends_on('ropp-ufo@11.0', when='@1.10 +ropp')

    # depends_on('rttov', when='+rttov')
    # depends_on('rttov@12.1.0', when='@1.7.0 +rttov')
