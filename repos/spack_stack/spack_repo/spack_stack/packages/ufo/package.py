# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Ufo(CMakePackage):
    """Unified Forward Operator"""

    homepage = "https://github.com/JCSDA/ufo"
    git = "https://github.com/JCSDA/ufo.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    version("1.10.0.20260331", commit="0fa9567eb6d0b3ce079001b98f44f3f0853ee821")
    version("1.10.0.20250821", commit="1ca49e253caa6d6a507f41ffa6875e0db7cc0751")

    patch(
        "https://github.com/jcsda/ufo/commit/ce4cbf8d9dbfd11ac5f2d4add61aa1c1bbc075fc.patch?full_index=1",
        sha256="b12aa105e8058409e5897fcc1d18054f4aef7fdb444bbb0341c1af6e0025197b",
        when="@1.10.0.20250821",
    )

    patch("ufo_crtm_testfiles.patch", when="@1.10:")

    # JCSDA-internal repository needed.
    variant("geos-aero", default=False, description="Build GEOS-AERO AOD operator")
    # Package gsw not yet available in spack
    variant("gsw", default=False, description="Build marine observation operators")
    # JCSDA-internal repository is public, but there is no "release" of the code yet.
    variant(
        "oasim", default=False, description="Build with Ocean Atmosphere Spectral Irradiance Model"
    )
    # NRL-internal repository needed.
    variant("ropp", default=False, description="Build ROPP operator")
    # JCSDA-internal repository needed.
    variant("rttov", default=False, description="Build RTTOV operator")

    conflicts("+geos-aero", msg="UFO: GEOS-AERO to be implemented.")
    conflicts("+gsw", msg="UFO: GSW to be implemented.")
    conflicts("+oasim", msg="UFO: OASIM to be implemented.")
    conflicts("+rttov", msg="UFO: RTTOV to be implemented.")

    # Project doesn't list "c" as a dependency in CMakeLists.txt, but cmake step fails w/o it
    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("fortran", type=("build"))

    depends_on("boost")
    # Leaky inherited dependency from ioda in version 1.10.0.20260331
    depends_on("bufr@12.0.1:", when="@1.10.0.20260331")
    depends_on("bufr-query@0.0.4:", when="@1.10.0.20260331")
    #
    depends_on("cmake", type=("build"))
    depends_on("cmake@3.12:", type=("build"), when="@1.10:")
    depends_on("crtm@3")
    depends_on("crtm@=3.1.3", when="@1.10")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@1.10:")
    depends_on("eckit")
    depends_on("eckit@1.24.4:", when="@1.10:")
    depends_on("eigen")
    depends_on("fckit")
    depends_on("fckit@0.11.0:", when="@1.10:")
    depends_on("gsl-lite")
    depends_on("ioda")
    depends_on("ioda@2.9.0.20260326", when="@1.10.0.20260331")
    depends_on("ioda@2.9.0.20250826", when="@1.10.0.20250821")
    depends_on("jedi-cmake", type=("build"))
    depends_on("mpi")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")
    depends_on("oops")
    depends_on("oops@1.10.0.20260331", when="@1.10.0.20260331")
    depends_on("oops@1.10.0.20250827", when="@1.10.0.20250821")
    depends_on("ufo-data@2.9.0.20260326", type=("build", "test"), when="@1.10.0.20260331")
    depends_on("ufo-data@2.9.0.20250821", type=("build", "test"), when="@1.10.0.20250821")

    # depends_on('geos-aero', when='+geos-aero')
    # depends_on('geos-aero@0.0.0', when='@1.7.0 +geos-aero')

    # depends_on('oasim', when='+oasim')
    # depends_on('oasim@0.0.0', when='@1.7.0 +oasim')

    # depends_on("gsw", when="+gsw")
    # depends_on("gsw@3.0.7", when="@1.7: +gsw")

    depends_on('ropp-ufo', when='+ropp')
    depends_on('ropp-ufo@11.0', when='@1.10 +ropp')

    # depends_on('rttov', when='+rttov')
    # depends_on('rttov@12.1.0', when='@1.7.0 +rttov')

    def cmake_args(self):
        res = [
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return res

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        """This needs to be set at build time, not at test time,
        to prevent UFO from downloading test data from S4"""
        env.set("UFO_TESTFILES", self.spec["ufo-data"].prefix)
        if self.spec["crtm"].satisfies("+fix"):
            env.set("UFO_CRTM_TESTFILES", join_path(self.spec['crtm-fix'].prefix, "fix"))

    def check(self):
        skipped_tests = None
        with when("@1.10.0.20250821"):
            skipped_tests = []
            if self.spec.satisfies("%oneapi"):
                skipped_tests += [
                    "ufo_test_tier1_test_ufo_obserrorcrossvarcorr",
                    "ufo_test_tier1_test_ufo_obserrorwithingroupcorr",
                    "ufo_test_tier1_test_ufo_obserrordiagonal",
                    "ufo_test_tier1_test_ufo_gnssrobendmetoffice_qc",
                    "ufo_test_tier1_test_ufo_gnssrobendmetoffice_qc_profile",
                    "ufo_test_tier1_test_ufo_gnssrobendmetoffice_obserror",
                    "ufo_test_tier1_test_ufo_gnssrorefmetoffice_qc",
                    "ufo_test_tier1_test_ufo_gnssrobndnbam_qc",
                    "ufo_test_tier1_test_ufo_gnssro_obs_error",
                    "ufo_test_tier1_test_ufo_gnssro_super_refraction_check",
                    "ufo_test_tier1_test_ufo_qc_modelbestfitpressure",
                    "ufo_test_tier1_test_ufo_satwind_inversion_correction",
                    "ufo_test_tier1_test_ufo_amsua_allsky_gfs_gsi_qc",
                    "ufo_test_tier1_test_ufo_cris_qc",
                    "ufo_test_tier1_test_ufo_cris_qc_land",
                    "ufo_test_tier1_test_ufo_qc_flags_true",
                    "ufo_test_tier1_test_ufo_function_averagetemperaturebelow",
                    "ufo_test_tier1_test_ufo_function_assignvalueequalchannels",
                    "ufo_test_tier1_test_ufo_fov_amsua",
                    "ufo_test_tier1_test_ufo_sample_and_reduce_over_fov",
                    "ufo_test_tier1_test_ufo_opr_gnssrorefmetoffice",
                    "ufo_test_tier1_test_ufo_linopr_gnssrorefmetoffice",
                    "ufo_test_tier1_test_ufo_opr_gnssrobendmetoffice",
                    "ufo_test_tier1_test_ufo_linopr_gnssrobendmetoffice",
                    "ufo_test_tier1_test_ufo_opr_gnssrobendmetoffice_nopseudo",
                    "ufo_test_tier1_test_ufo_linopr_gnssrobendmetoffice_nopseudo",
                    "ufo_test_tier1_test_ufo_opr_gnssrobendmetoffice_profile",
                    "ufo_test_tier1_test_ufo_opr_gnssrobendmetoffice_nosupercheck",
                    "ufo_test_tier1_test_ufo_linopr_gnssrobendmetoffice_nosupercheck",
                    "ufo_test_tier1_test_ufo_opr_groundgnssmetoffice",
                    "ufo_test_tier1_test_ufo_linopr_groundgnssmetoffice",
                    "ufo_test_tier1_test_ufo_opr_logarithm",
                    "ufo_test_tier1_test_ufo_linopr_logarithm",
                    "ufo_test_tier1_test_ufo_opr_radialvelocity",
                    "ufo_test_tier1_test_ufo_opr_satwind_metoffice",
                    "ufo_test_tier1_test_ufo_opr_seaicefrac",
                    "ufo_test_tier1_test_ufo_linopr_seaicefrac",
                    "ufo_test_tier1_test_ufo_opr_sfcpcorrected",
                    "ufo_test_tier1_test_ufo_opr_abi_ahi_crtm",
                    "ufo_test_tier1_test_ufo_linopr_abi_ahi_crtm",
                    "ufo_test_tier1_test_ufo_opr_airs_crtm",
                    "ufo_test_tier1_test_ufo_linopr_airs_crtm",
                    "ufo_test_tier1_test_ufo_opr_crtm_vis_albedo",
                    "ufo_test_tier1_test_ufo_opr_cris_crtm",
                    "ufo_test_tier1_test_ufo_linopr_cris_crtm",
                    "ufo_test_tier1_test_ufo_opr_cris_crtm_co2_options",
                    "ufo_test_tier1_test_ufo_linopr_cris_crtm_co2_options",
                    "ufo_test_tier1_test_ufo_opr_hirs4_crtm",
                    "ufo_test_tier1_test_ufo_linopr_hirs4_crtm",
                    "ufo_test_tier1_test_ufo_opr_iasi_crtm",
                    "ufo_test_tier1_test_ufo_opr_seviri_crtm",
                    "ufo_test_tier1_test_ufo_linopr_seviri_crtm",
                    "ufo_test_tier1_test_ufo_opr_sndrd1-4_crtm",
                    "ufo_test_tier1_test_ufo_linopr_sndrd1-4_crtm",
                    "ufo_test_tier1_test_ufo_obsdiag_crtm_airs_optics",
                    # Added for oneapi@2024.2.1 2026/04/01
                    "ufo_test_tier1_instrument_sonde_geos_qc",
                    "ufo_test_tier1_instrument_sfcLand_geos_qc",
                    "ufo_test_tier1_instrument_sfcMarine_geos_qc",
                    "ufo_test_tier1_test_ufo_opr_sfccorrected_pressure",
                ]
        with when("@1.10.0.20260331"):
            skipped_tests = []
            if self.spec.satisfies("%gcc"):
                skipped_tests += [
                    "ufo_instrument_amsua_n18_gfs_HofX_bc",
                    "ufo_obserrordiffusion",
                ]
            if self.spec.satisfies("%oneapi"):
                skipped_tests += [
                    "ufo_instrument_airs_aqua_gfs_HofX",
                    "ufo_instrument_airs_aqua_gfs_HofX_bc",
                    "ufo_instrument_airs_aqua_gfs_HofX_qc",
                    "ufo_instrument_airs_aqua_gfs_HofX_qc_obin",
                    "ufo_instrument_amsua_n18_gfs_HofX_bc",
                    "ufo_instrument_avhrr_metop-a_gfs_HofX",
                    "ufo_instrument_avhrr_n18_gfs_HofX",
                    "ufo_instrument_avhrr_metop-a_gfs_HofX_bc",
                    "ufo_instrument_avhrr_n18_gfs_HofX_bc",
                    "ufo_instrument_avhrr_metop-a_gfs_HofX_qc",
                    "ufo_instrument_avhrr_n18_gfs_HofX_qc",
                    "ufo_instrument_cris-fsr_n20_gfs_HofX",
                    "ufo_instrument_cris-fsr_npp_gfs_HofX",
                    "ufo_instrument_cris-fsr_n20_gfs_HofX_bc",
                    "ufo_instrument_cris-fsr_npp_gfs_HofX_bc",
                    "ufo_instrument_cris-fsr_n20_geos_HofX_qc",
                    "ufo_instrument_cris-fsr_n20_gfs_HofX_qc",
                    "ufo_instrument_cris-fsr_npp_gfs_HofX_qc",
                    "ufo_instrument_iasi_metop-a_gfs_HofX",
                    "ufo_instrument_iasi_metop-b_gfs_HofX",
                    "ufo_instrument_iasi_metop-a_gfs_HofX_bc",
                    "ufo_instrument_iasi_metop-b_gfs_HofX_bc",
                    "ufo_instrument_iasi_metop-a_gfs_HofX_qc",
                    "ufo_instrument_iasi_metop-b_gfs_HofX_qc",
                    "ufo_instrument_seviri_m11_gfs_HofX",
                    "ufo_instrument_seviri_m11_gfs_HofX_bc",
                    "ufo_instrument_seviri_m11_gfs_HofX_qc",
                    "ufo_instrument_abi_g16_gfs_HofX",
                    "ufo_instrument_abi_g16_gfs_HofX_bc",
                    "ufo_obserrorcrossvarcorr",
                    "ufo_obserrorwithingroupcorr",
                    "ufo_obserrordiagonal",
                    "ufo_obserrordiagonal_inv_gamma",
                    "ufo_gnssrobendmetoffice_qc",
                    "ufo_gnssrobendmetoffice_obserror",
                    "ufo_gnssro_super_refraction_check",
                    "ufo_airs_qc_filters",
                    "ufo_cris_qc",
                    "ufo_cris_qc_filters",
                    "ufo_cris_qc_land",
                    "ufo_iasi_qc_filters",
                    "ufo_qc_flags_true",
                    "ufo_opr_gnssrorefmetoffice",
                    "ufo_opr_gnssrorefmetoffice_refractivity_changes",
                    "ufo_opr_gnssrobendmetoffice",
                    "ufo_linopr_gnssrobendmetoffice",
                    "ufo_opr_gnssrobendmetoffice_nopseudo",
                    "ufo_linopr_gnssrobendmetoffice_nopseudo",
                    "ufo_opr_gnssrobendmetoffice_profile",
                    "ufo_opr_gnssrobendmetoffice_nosupercheck",
                    "ufo_linopr_gnssrobendmetoffice_nosupercheck",
                    "ufo_opr_gnssrobendmetoffice_refractivity_changes",
                    "ufo_linopr_gnssrobendmetoffice_refractivity_changes",
                    "ufo_opr_abi_ahi_crtm",
                    "ufo_linopr_abi_ahi_crtm",
                    "ufo_opr_airs_crtm",
                    "ufo_linopr_airs_crtm",
                    "ufo_opr_crtm_vis_albedo",
                    "ufo_opr_cris_crtm",
                    "ufo_linopr_cris_crtm",
                    "ufo_opr_cris_crtm_co2_options",
                    "ufo_linopr_cris_crtm_co2_options",
                    "ufo_opr_hirs4_crtm",
                    "ufo_linopr_hirs4_crtm",
                    "ufo_opr_iasi_crtm",
                    "ufo_iasi_crtmreconrad_linop_check",
                    "ufo_iasi_crtmreconrad_linop_tlad_check",
                    "ufo_linopr_iasi_crtm",
                    "ufo_opr_seviri_crtm",
                    "ufo_linopr_seviri_crtm",
                    "ufo_opr_sndrd1-4_crtm",
                    "ufo_linopr_sndrd1-4_crtm",
                    "ufo_obsdiag_crtm_airs_jacobian",
                    "ufo_obsdiag_crtm_airs_optics",
                    "ufo_obsdiag_crtm_cris_jacobian",
                    "ufo_obsdiag_crtm_cris_optics",
                    "ufo_obsdiag_crtm_iasi_jacobian",
                    "ufo_obsdiag_crtm_iasi_optics",
                ]

        ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
        with working_dir(self.build_directory):
            if skipped_tests:
                ctest("--timeout", "120", "-E", "|".join(skipped_tests))
            else:
                ctest("--timeout", "120")
