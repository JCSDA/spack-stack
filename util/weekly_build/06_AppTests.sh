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
  spack module lmod refresh -y
  spack stack setup-meta-modules
done

# TODO: test against all compilers
# For now, only Intel (see apptests/test_ufswm.sh)
if [ "$TEST_UFSWM" == ON ]; then
  ./apptests/test_ufswm.sh
fi
