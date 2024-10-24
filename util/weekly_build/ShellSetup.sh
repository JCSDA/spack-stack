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

. $(dirname $0)/sites/${PLATFORM}.sh

SOURCE_CACHE=${SOURCE_CACHE:-local-source}
BUILD_CACHE=${BUILD_CACHE:-local-binary}

echo "Source cache mirror name/directory: ${SOURCE_CACHE}"
echo "Build cache mirror name/directory: ${BUILD_CACHE}"
