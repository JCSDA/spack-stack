#COMPILERS=${COMPILERS:-"intel oneapi gcc"}
#TEMPLATES=${TEMPLATES:-"neptune-dev unified-dev"}
set -e
if [[ -z ${COMPILERS} || ${#COMPILERS[@]} -ne 1 ]]; then
  echo "ERROR, COMPILERS (can only be one) not set/invalid!"
  exit 1
fi
if [[ -z ${TEMPLATES} || ${#TEMPLATES[@]} -ne 1 ]]; then
 echo "ERROR, TEMPLATES (can only be one) not set/invalid!"
 exit 1
fi
set +e

module purge
umask 0022

SPACK_STACK_URL=https://github.nrlmry.navy.mil/JCSDA/spack-stack
SPACK_STACK_BRANCH=ci
KEEP_WEEKLY_BUILD_DIR="YES"
FIND_CMD="lfs find"
