#!/bin/bash

COMPILERS=${COMPILERS:-"oneapi gcc"}
TEMPLATES=${TEMPLATES:-"unified-dev"}

# module --force purge
# umask 0022

SPACK_STACK_URL=https://github.com/stiggy87/spack-stack.git
SPACK_STACK_BRANCH=feature/hdf5-weekly-build-testing

SOURCE_CACHE=./local-source
BUILD_CACHE=./local-binary

PADDED_LENGTH=0
# For AWS based testing, this is a no since spack-stack can grow large if not cleaned up.
# We would need to figure out an S3 bucket or other storage to keep a weekly build.
# Would have to clean it up after so many builds.
KEEP_WEEKLY_BUILD_DIR="NO"
REUSE_BUILD_CACHE=YES
SKIP_FETCH=NO

PACKAGES_TO_TEST="hdf5"
PACKAGES_TO_INSTALL="ewok-env global-workflow-env jedi-fv3-env"
FIND_CMD="find"
TEST_UFSWM=OFF
