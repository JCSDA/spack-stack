module load gcc/11.2.0 python/3.8.6
COMPILERS=${COMPILERS:-"intel@2022.2.0.262 intel@19.1.3.304"}
TEMPLATES=${TEMPLATES:-"unified-dev"}
function spack_install_wrapper {
  logfile=$1
  shift 2
  spack fetch --missing ${PACKAGES_TO_INSTALL} &> log.fetch
  if [[ " $* " =~ " global-workflow-env " ]]; then
    spack config add "config:build_stage:${SPACK_ENV:?}/stage"
    spack install $INSTALL_OPTS gh
  fi
  spack config add 'config:build_stage:$tempdir/$user/spack-stage'
  if [[ " $* " =~ "-env " ]]; then # for the "real" install step
    walltime=03:30:00
  else # when running test step
    walltime=01:00:00
  fi
  /opt/pbs/bin/qsub -N spack-build-cache-$RUNID -j oe -A NCEPLIBS-DEV -l "select=1:ncpus=12:mem=24GB,walltime=$walltime" -q dev -V -Wblock=true -- ${SPACK_STACK_DIR}/util/parallel_install.sh 2 6 $*
  return $?
}
function alert_cmd {
  module purge # annoying libstdc++ issue
  mail -s 'spack-stack weekly build failure' alexander.richert@noaa.gov  < <(echo "Weekly spack-stack build failed in $1. Run ID: $RUNID")
}
PACKAGES_TO_TEST="libpng libaec jasper w3emc g2c netcdf-c netcdf-fortran"
PACKAGES_TO_INSTALL="ufs-weather-model-env global-workflow-env gsi-env madis"
PADDED_LENGTH=140
TEST_UFSWM=OFF
BATCHACCOUNT=NCEPLIBS-DEV
FIND_CMD="find"
SKIP_FETCH=YES
