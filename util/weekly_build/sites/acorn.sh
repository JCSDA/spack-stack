module load gcc/11.2.0 python/3.11.7
COMPILERS=${COMPILERS:-"intel@2022.0.2.262 intel@19.1.3.304"}
BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/lfs/h1/emc/nceplibs/noscrub/spack-stack/build_cache}
function spack_install_exe {
#  set +e
#  ( /opt/pbs/bin/qsub -N spack-build-cache-$RUNID-A -j oe -A NCEPLIBS-DEV -l select=1:ncpus=6:mem=10000MB -l walltime=03:00:00 -V -Wblock=true -- $(which spack) $* ) &
#  ( /opt/pbs/bin/qsub -N spack-build-cache-$RUNID-B -j oe -A NCEPLIBS-DEV -l select=1:ncpus=6:mem=10000MB -l walltime=03:00:00 -V -Wblock=true -- $(which spack) $* ) &
#  wait
#  rc=$?
#  set -e
#  cat spack-build-cache-${RUNID}*
#  return $rc
##  cp ${SPACK_STACK_DIR:?}/util/acorn/{build.pbs,spackinstall.sh} ${SPACK_ENV}/.
##  /opt/pbs/bin/qsub -Wblock=true ${SPACK_ENV}/build.pbs
##  spack $* | tee -a log.install 2>&1
  shift 1
  ${SPACK_STACK_DIR}/util/parallel_install.sh 3 4 $*
}
PACKAGES_TO_TEST="libpng libaec jasper w3emc g2c"
PACKAGES_TO_INSTALL="ufs-weather-model-env global-workflow-env gsi-env madis"
function alert_cmd {
  module purge # annoying libstdc++ issue
  mail -s 'spack-stack weekly build failure' alexander.richert@noaa.gov  < <(echo "Weekly spack-stack build failed in $1. Run ID: $RUNID")
}
TEST_UFSWM=ON
