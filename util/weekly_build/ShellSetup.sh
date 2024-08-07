echo Run ID: ${1?"First arg: Unique run ID"}
echo Run directory: ${2?"Second arg: base directory for build"}
echo Platform name: ${3?"Third arg: platform name ('hera', 'hercules', etc.)"}

RUNID=$1
RUNDIR=$2
PLATFORM=$3

if [ ${RUNDIR::1} != "/" ]; then
  echo "FATAL ERROR: Directory should be an absolute path!"
  exit 1
fi

PACKAGES_TO_TEST=${PACKAGES_TO_TEST:-"libpng libaec jasper scotch w3emc g2 g2c"}

function alert_cmd {
  echo "Your run failed in $1. This is a placeholder alerting function. 'alert_cmd' should be defined for each system."
}

function spack_install_exe {
  spack $* | tee -a log.install 2>&1
}

case $PLATFORM in
  hercules)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/work/noaa/epic/role-epic/spack-stack/hercules/build_cache}
    ;;
  orion)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/work/noaa/epic/role-epic/spack-stack/orion/build_cache}
    ;;
  discover16)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/gpfsm/dswdev/jcsda/spack-stack/scu16/build_cache}
    ;;
  discover17)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/gpfsm/dswdev/jcsda/spack-stack/scu17/build_cache}
    ;;
  derecho)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/glade/work/epicufsrt/contrib/spack-stack/derecho/build_cache}
    ;;
  acorn)
    COMPILERS=${COMPILERS:-"intel@2022"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/lfs/h1/emc/nceplibs/noscrub/spack-stack/build_cache}
    function spack_install_exe {
      set +e
      ( qsub -N spack-build-cache-$RUNID-A -j oe -A NCEPLIBS-DEV -l select=1:ncpus=6:mem=10000MB -l walltime=03:00:00 -V -Wblock=true -- $(which spack) $* ) &
      ( qsub -N spack-build-cache-$RUNID-B -j oe -A NCEPLIBS-DEV -l select=1:ncpus=6:mem=10000MB -l walltime=03:00:00 -V -Wblock=true -- $(which spack) $* ) &
      wait
      rc=$?
      set -e
      cat spack-build-cache-${RUNID}*
      return $rc
    }
    PACKAGES_TO_TEST="libpng libaec jasper w3emc g2c"
    PACKAGES_TO_INSTALL="ufs-weather-model-env global-workflow-env upp-env"
    INSTALL_OPTS="-j6"
    function alert_cmd {
      mail -s 'spack-stack weekly build failure' alexander.richert@noaa.gov  < <(echo "Weekly spack-stack build failed in $1. Run ID: $RUNID")
    }
    TEST_UFSWM=ON
    ;;
  gaea)
    COMPILERS=${COMPILERS:-"intel"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/ncrc/proj/epic/spack-stack/build_cache}
    ;;
  hera)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/scratch1/NCEPDEV/nems/role.epic/spack-stack/build_cache}
    ;;
  jet)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/build_cache}
    ;;
  narwhal)
    COMPILERS=${COMPILERS:-"intel gcc"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/p/app/projects/NEPTUNE/spack-stack/build_cache}
    ;;
  nautilus)
    COMPILERS=${COMPILERS:-"intel"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/p/app/projects/NEPTUNE/spack-stack/build_cache}
    ;;
  s4)
    COMPILERS=${COMPILERS:-"intel"}
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/data/prod/jedi/spack-stack/build_cache}
    ;;
  linux.default)
    COMPILERS=${COMPILERS:-"gcc"}

esac

echo "Build cache target directory: ${BUILD_CACHE_DIR?'BUILD_CACHE_DIR must be set!'}"
