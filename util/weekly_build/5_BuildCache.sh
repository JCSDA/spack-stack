#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/$RUNID

. setup.sh

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  spack buildcache push --unsigned --force ${BUILD_CACHE_DIR?"BUILD_CACHE_DIR must be set!"} $PACKAGES_TO_INSTALL
done
