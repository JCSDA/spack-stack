COMPILERS=${COMPILERS:-"intel oneapi gcc"}
module purge
umask 0022
SPACK_STACK_URL=https://github.nrlmry.navy.mil/JCSDA/spack-stack
SPACK_STACK_BRANCH=feature/weekly_build_nautilus
### NEEDED ? BUILD_CACHE_DIR=${BUILD_CACHE_DIR:-/p/app/projects/NEPTUNE/spack-stack/build-cache}