#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR/$RUNID

set +x
. setup.sh
set -x

for compiler in $COMPILERS; do
  rm -rf $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack stack create env --name build-${compiler/@/-} --template unified-dev --site $PLATFORM --compiler $compiler
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  # Check for duplicates and fail before doing the "real" concretization with test deps:
  spack concretize --fresh 2>&1 | tee log.concretize
  ${SPACK_STACK_DIR:?}/util/show_duplicate_packages.py log.concretize -d -i crtm -i esmf
  spack concretize --force --fresh --test all 2>&1 | tee log.concretize_test
done
