# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *


class Ioda(CMakePackage):
    """Interface for Observation Data Access"""

    homepage = "https://github.com/JCSDA/ioda"
    git = "https://github.com/JCSDA/ioda.git"

    maintainers("climbfuji")

    version("develop", branch="develop", no_cache=True)
    version("2.9.0.20250826", commit="6e76616001067384f7d0ca4341ad78e81527af8b")

    patch("ioda_cmake_import.patch", when="@2.9.0.20250826")

    variant("doc", default=False, description="Build IODA documentation")
    # Let's always assume IODA_BUILD_LANGUAGE_FORTRAN=on.
    # variant('fortran', default=True, description='Build the ioda Fortran interface')
    variant("odc", default=True, description="Build ODC bindings")
    # ioda has no explicit OpenMP calls, but header files from Eigen and oops do use openmp.
    variant("openmp", default=True, description="Build with OpenMP support")
    # Let's always BUILD_PYTHON_BINDINGS.
    # variant('python', default=True, description='Build the ioda Python interface')

    generator("make")

    # Project doesn't list "c" as a dependency in CMakeLists.txt, but cmake step fails w/o it
    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("fortran", type=("build"))

    depends_on("boost@1.64.0:")
    depends_on("bufr")
    depends_on("bufr@12.0.1:", when="@2.9:")
    # This is optional, and it needs netcdf-cxx - which versions?
    depends_on("bufr-query@0.0.4:", when="@2.9:")
    depends_on("cmake", type=("build"))
    depends_on("cmake@3.14:", type=("build"), when="@2.9:")
    depends_on("ecbuild", type=("build"))
    depends_on("ecbuild@3.3.2:", type=("build"), when="@2.9:")
    depends_on("eckit")
    depends_on("eckit@1.23.0:", when="@2.9:")
    depends_on("eigen")
    depends_on("fckit")
    depends_on("fckit@0.10.1:", when="@2.9:")
    depends_on("gsl-lite")
    depends_on("hdf5@1.12.0: +mpi")
    depends_on("hdf5@1.14.0: +mpi", when="@2.9:")
    depends_on("jedi-cmake", type=("build"))
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "link", "run"))
    depends_on("mpi")
    depends_on("nccmp")
    # netcdf-cxx needed for bufr-query, but which version?
    depends_on("netcdf-cxx", when="@2.9:")
    depends_on("odc", when="+odc")
    depends_on("odc@1.4.6:", when="@2.9: +odc")
    depends_on("oops+openmp", when="+openmp")
    depends_on("oops~openmp", when="~openmp")
    depends_on("oops@1.10", when="@2.9:")
    depends_on("python")
    depends_on("python@3.9:3.11", when="@2.9:")
    depends_on("py-pybind11")
    depends_on("py-pycodestyle")
    depends_on("udunits")
    depends_on("udunits@2.2.0:", when="@2.9:")

    def cmake_args(self):
        res = [
            self.define_from_variant("ENABLE_IODA_DOC", "doc"),
        ]
        return res

    def check(self):
        skipped_tests = None
        with when("@2.9.0.20250826"):
            skipped_tests = [
                "test_ioda_distribution_masterandreplica_mpi",
                "test_ioda_distribution_build_round_robin_mpi",
                "test_ioda_distribution_masterandreplica_io_pool",
                "test_ioda_distribution_timewindow",
                "test_ioda_oops_obsspace",
                "test_ioda_obsspace",
                "test_ioda_obsspace_reader_pool",
                "test_ioda_obsspace_out_odc",
                "iodatest_obsspace_out_odc_readbackin",
                "test_ioda_writer_scatwindchosen",
                "test_ioda_sort",
                "test_ioda_extendedobsspace",
                "test_ioda_extendedobsspace_MPI",
                "test_ioda_obsvector_missing_locs",
                "test_ioda_obsdatavector",
                "test_ioda_oops_obserrorcovariance",
                "test_ioda_reader_load_netcdf",
                "test_ioda_oops_departuresensemble",
                "test_ioda_time_io",
                "test_ioda_time_io_cmp_sondes",
                "test_ioda_time_io_cmp_amsua_n19",
                "test_ioda_time_io_cmp_gnssro",
                "test_ioda_time_io_reader_pool",
                "test_ioda_time_io_cmp_sondes_reader_pool",
                "test_ioda_time_io_cmp_amsua_n19_reader_pool",
                "test_ioda_time_io_cmp_gnssro_reader_pool",
                "test_ioda_time_io_reader_pool_ext_file_prep",
                "test_ioda_time_io_cmp_sondes_reader_pool_ext_file_prep",
                "test_ioda_time_io_cmp_amsua_n19_reader_pool_ext_file_prep",
                "test_ioda_time_io_cmp_gnssro_reader_pool_ext_file_prep",
                "test_ioda_time_io_cmp_windborne_reader_pool_ext_file_prep",
                "test_ioda_time_io_reader_pool_ext_file_prep_mpi7",
                "test_ioda_time_io_cmp_sondes_reader_pool_ext_file_prep_mpi7",
                "test_ioda_time_io_cmp_amsua_n19_reader_pool_ext_file_prep_mpi7",
                "test_ioda_time_io_cmp_gnssro_reader_pool_ext_file_prep_mpi7",
                "test_ioda_time_io_cmp_windborne_reader_pool_ext_file_prep_mpi7",
                "test_ioda_build_amsua_n19_file_set",
                "test_ioda_build_windborne_file_set",
                "test_ioda_build_amsua_n19_file_set_mpi7",
                "test_ioda_build_windborne_file_set_mpi7",
                "test_ioda_filter_obs_single_file_input_twfilt",
                "test_ioda_filter_obs_multi_file_input_twfilt",
                "test_ioda_filter_obs_single_file_input_twfilt_rtfilt",
                "test_ioda_filter_obs_multi_file_input_twfilt_rtfilt",
                "test_ioda_filter_obs_single_file_input_twfilt_rtfiltwindow",
                "test_ioda_filter_obs_multi_file_input_twfilt_rtfiltwindow",
                "test_ioda_filter_obs_amsua",
                "test_ioda_filter_obs_cmp_single_file_input_twfilt",
                "test_ioda_filter_obs_cmp_multi_file_input_twfilt",
                "test_ioda_filter_obs_cmp_single_file_input_twfilt_rtfilt",
                "test_ioda_filter_obs_cmp_multi_file_input_twfilt_rtfilt",
                "test_ioda_filter_obs_cmp_single_file_input_twfilt_rtfiltwindow",
                "test_ioda_filter_obs_cmp_multi_file_input_twfilt_rtfiltwindow",
                "test_ioda_filter_obs_cmp_sondes",
                "test_ioda_filter_obs_cmp_amsua",
                "test_ioda_time_io_multiple_input_files",
                "test_ioda_time_io_multiple_input_files_mpi_2",
                "test_ioda_time_io_multiple_input_files_mpi_4",
                "test_ioda_time_io_multiple_input_files_amsua_cmp",
                "test_ioda_time_io_multiple_input_files_amsua_mpi_2_cmp",
                "test_ioda_time_io_multiple_input_files_amsua_mpi_4_cmp",
                "test_ioda_time_io_multiple_input_files_sondes_cmp",
                "test_ioda_time_io_multiple_input_files_sondes_mpi_2_cmp",
                "test_ioda_time_io_multiple_input_files_sondes_mpi_4_cmp",
                "test_ioda_time_io_multiple_input_files_gnssro_cmp",
                "test_ioda_time_io_multiple_input_files_gnssro_mpi_2_cmp",
                "test_ioda_time_io_multiple_input_files_gnssro_mpi_4_cmp",
                "test_ioda-convert_aircraft_odc",
                "test_ioda-convert_aircraft_mixed_odc",
                "test_ioda-convert_surface_odc",
                "test_ioda-convert_surface_tcbogus_odc",
                "test_ioda-convert_ascatsm_odc",
                "test_ioda-convert_gnssro_profile_333_odc",
                "test_ioda-convert_gnssro_profile_100_odc",
                "test_ioda-convert_mtgirs_odc",
                "test_ioda-convert_fciasr_odc",
                "test_ioda-convert_fciclr_odc",
                "test_ioda-convert_seviriasr_odc",
                "test_ioda-convert_seviriclr_odc",
                "test_ioda-convert_geocloud_odc",
                "test_ioda-convert_oceancolour_odc",
                "test_ioda-convert_radar_doppler_wind_odc",
                "test_ioda-convert_radar_reflectivity_odc",
                "test_ioda-convert_stationsnow_statid_odc",
                "test_ioda-convert_iasi_read_channels_from_yaml_odc",
                "test_ioda_bufr_mhs",
                "test_ioda_bufr_python_encoder",
                "test_ioda_bufr_python_parallel",
                "test_ioda_pyiodautils_file_merge",
                "test_ioda_pyiodautils_file_merge_cmp",
            ]

        ctest = Executable(self.spec["cmake"].prefix.bin.ctest)
        with working_dir(self.build_directory):
            if skipped_tests:
                ctest("-E", "|".join(skipped_tests))
                #ctest("--timeout", "120", "--verbose", "-E", "|".join(skipped_tests))
            else:
                #ctest("--timeout", "120", "--verbose")
                ctest()
