#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/$RUNID

set +x
. setup.sh
set -x

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  spack buildcache push --unsigned --force ${BUILD_CACHE} $PACKAGES_TO_INSTALL
  spack buildcache rebuild-index ${BUILD_CACHE}
done
