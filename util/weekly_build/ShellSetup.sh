echo Run ID: ${1?"First arg: Unique run ID"}
echo Run directory: ${2?"Second arg: base directory for build"}
echo Platform name: ${3?"Third arg: platform name ('hera', 'hercules', etc.)"}

export RUNID=$1
export RUNDIR=$2
export PLATFORM=$3

if [ ${RUNDIR::1} != "/" ]; then
  echo "FATAL ERROR: Directory should be an absolute path!"
  exit 1
fi

export COMPILERS=intel

export PACKAGES_TO_TEST="libpng libaec jasper scotch w3emc g2 g2c"

case $PLATFORM in
  hercules)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/work/noaa/epic/role-epic/spack-stack/hercules/build_cache}
    ;;
  orion)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/work/noaa/epic/role-epic/spack-stack/orion/build_cache}
    ;;
  discover16)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/gpfsm/dswdev/jcsda/spack-stack/scu16/build_cache}
    ;;
  discover17)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/gpfsm/dswdev/jcsda/spack-stack/scu17/build_cache}
    ;;
  derecho)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/glade/work/epicufsrt/contrib/spack-stack/derecho/build_cache}
    ;;
  acorn)
    COMPILERS="intel@19 intel@2022"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/lfs/h1/emc/nceplibs/noscrub/spack-stack/build_cache}
    TEST_UFSWM=ON
    SCHEDULER_CMD="qsub -N spack-build-cache-$RUNID -A NCEPLIBS-DEV -l nodes=1:ppn=6 -l walltime=03:00:00 -V -Wblock=true --"
    PACKAGES_TO_INSTALL=" ufs-weather-model-env global-workflow-env upp-env"
    INSTALL_OPTS="-j6"
    ;;
  gaea)
    COMPILERS="intel"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/ncrc/proj/epic/spack-stack/build_cache}
    ;;
  hera)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/scratch1/NCEPDEV/nems/role.epic/spack-stack/build_cache}
    ;;
  jet)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/build_cache}
    ;;
  narwhal)
    COMPILERS="intel gcc"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/p/app/projects/NEPTUNE/spack-stack/build_cache}
    ;;
  nautilus)
    COMPILERS="intel"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/p/app/projects/NEPTUNE/spack-stack/build_cache}
    ;;
  s4)
    COMPILERS="intel"
    BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/data/prod/jedi/spack-stack/build_cache}
    ;;
  linux.default)
    COMPILERS="gcc"
esac

echo "Build cache target directory: ${BUILD_CACHE_DIR?'BUILD_CACHE_DIR must be set!'}"
