#!/bin/bash

set -e

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/spack-stack-build-cache-${RUNID}

. setup.sh

for compiler in $COMPILERS; do
  cd envs/build-$compiler
  spack env activate .
  spack buildcache push --unsigned --force ${BUILD_CACHE_DIR?"BUILD_CACHE_DIR must be set!"}
done
