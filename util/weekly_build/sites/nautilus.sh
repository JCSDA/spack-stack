COMPILERS=${COMPILERS:-"intel oneapi gcc"}
#TEMPLATES=${TEMPLATES:-"neptune-dev unified-dev"}
TEMPLATES=${TEMPLATES:-"neptune-dev"}
module purge
umask 0022

SPACK_STACK_URL=https://github.nrlmry.navy.mil/JCSDA/spack-stack
SPACK_STACK_BRANCH=feature/weekly_build_nautilus
KEEP_WEEKLY_BUILD_DIR="YES"

