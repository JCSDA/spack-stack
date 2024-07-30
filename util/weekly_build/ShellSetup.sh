echo Run ID: ${1?"First arg: Unique run ID"}
echo Base directory: ${2?"Second arg: base directory for build"}
echo Platform name: ${3?"Third arg: platform name ('hera', 'hercules', etc.)"}

export RUNID=$1
export BASEDIR=$2
export PLATFORM=$3

if [ ${BASEDIR::1} != "/" ]; then
  echo "FATAL ERROR: Directory should be an absolute path!"
  exit 1
fi

export COMPILERS=intel

export PACKAGESTOTEST="libpng libaec jasper scotch w3emc bacio g2 g2c"
