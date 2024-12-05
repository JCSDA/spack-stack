
COMPILERS=${COMPILERS:-"intel"}
TEMPLATES=${TEMPLATES:-"unified-dev"}

function alert_cmd {
  mail -s 'spack-stack weekly build failure' richard.grubin@noaa.gov < <(echo "Weekly spack-stack build failed in $1. Run ID: $RUNID")
}

module --force purge
umask 0022

SPACK_STACK_URL=https://github.com/JCSDA/spack-stack.git
SPACK_STACK_BRANCH=develop

KEEP_WEEKLY_BUILD_DIR="YES"
PADDED_LENGTH=200

# package test / install settings (future use)
# PACKAGES_TO_TEST="libpng libaec jasper w3emc g2c"
# PACKAGES_TO_INSTALL="ufs-weather-model-env"

TEST_UFSWM=ON
UFSWM_BRANCH=develop
UFSWM_URL="https://github.com/ufs-community/ufs-weather-model.git"

# rt.sh parameters / arguments
BATCHACCOUNT=epic
RT_ARGS="-k -r"
