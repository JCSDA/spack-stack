if [ ! -z $SPACK_STACK_DIR ]; then
  . ${SPACK_STACK_DIR}/configs/sites/tier1/wcoss2/setup.sh
fi

COMPILERS=${COMPILERS:-"oneapi-2024.2.1 intel-19.1.3.304"}
TEMPLATES=${TEMPLATES:-"unified-dev"}
function spack_install_wrapper {
  logfile=$1
  shift 2
  spack fetch --missing --no-checksum ${PACKAGES_TO_INSTALL} &> log.fetch
  if [[ $(spack spec ${PACKAGES_TO_INSTALL} | grep -Pc '(?<=[\s\^])go(?=@)') -gt 0 ]]; then
    if [ "$REUSE_BUILD_CACHE" == YES ]; then cache_flag="--no-check-signature"; else cache_flag="--no-cache"; fi
    /opt/pbs/bin/qsub -N spack-build-cache-$RUNID -j oe -A NCEPLIBS-DEV -l "select=1:ncpus=8:mem=20GB,walltime=00:45:00" -q dev -V -Wblock=true -- $(which spack) install $cache_flag go
    ${SPACK_SPACK_DIR}/util/fetch_go_deps.py
    chmod u+rX ${GOMODCACHE}/cache -R
  fi
  spack config add 'config:build_stage:$tempdir/$user/spack-stage'
  if [[ " $* " =~ "-env " || -z $PACKAGES_TO_TEST ]]; then # for the "real" install step
    walltime=${INSTALL_WALLTIME:-03:30:00}
  else # when running test step
    walltime=${TEST_WALLTIME:-01:00:00}
  fi
  if [ "$SINGLE_NODE" == YES ]; then
    spack config add 'config:locks:false'
    /opt/pbs/bin/qsub -N spack-build-cache-$RUNID -j oe -A NCEPLIBS-DEV -l "select=1:ncpus=8:mem=20GB,walltime=$walltime" -q dev -V -Wblock=true -- ${SPACK_STACK_DIR}/util/parallel_install.sh 1 8 $*
  else
    /opt/pbs/bin/qsub -N spack-build-cache-$RUNID -j oe -A NCEPLIBS-DEV -l "select=1:ncpus=18:mem=30GB,walltime=$walltime" -q dev -V -Wblock=true -- ${SPACK_STACK_DIR}/util/parallel_install.sh 3 6 $*
  fi
  return $?
}
function alert_cmd {
  module purge # annoying libstdc++ issue
  mail -s 'spack-stack weekly build failure' alexander.richert@noaa.gov  < <(echo "Weekly spack-stack build failed in $1. Run ID: $RUNID")
}
PACKAGES_TO_TEST=${PACKAGES_TO_TEST:-"libpng libaec jasper w3emc g2c netcdf-c netcdf-fortran bufr g2 bacio ip g2tmpl nemsio sigio ncio"}
PACKAGES_TO_INSTALL=${PACKAGES_TO_INSTALL:-"ufs-weather-model-env global-workflow-env gsi-env madis"}
PADDED_LENGTH=140
TEST_UFSWM=OFF
BATCHACCOUNT=NCEPLIBS-DEV
FIND_CMD="find"
SKIP_FETCH=YES
