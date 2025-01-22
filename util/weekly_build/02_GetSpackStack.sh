#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR
if [ -d $RUNID ]; then
  cd $RUNID
  git pull
else
  git clone --depth 1 --recurse-submodules --shallow-submodules ${SPACK_STACK_URL:-https://github.com/JCSDA/spack-stack} -b ${SPACK_STACK_BRANCH:-develop} $RUNID
fi
