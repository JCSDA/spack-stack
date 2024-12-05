#!/bin/bash

set -ex

cd $RUNDIR/$RUNID

set +x
. setup.sh
set -x

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  spack module lmod refresh -y
  spack stack setup-meta-modules
done

if [ "$TEST_UFSWM" == ON ]; then
  ./apptests/test_ufswm.sh
fi
