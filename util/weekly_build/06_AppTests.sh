#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/$RUNID

set +x
. setup.sh
set -x

for compiler in $COMPILERS; do
  for template in $TEMPLATES; do
    envname=build-$template-${compiler/@/-}
    envdir=$RUNDIR/$RUNID/envs/$envname
    cd $envdir
    spack env activate .
    spack module lmod refresh -y
    spack stack setup-meta-modules
  done
done

if [ "$TEST_UFSWM" == ON ]; then
  . $(dirname $0)/apptests/test_ufswm.sh
fi
