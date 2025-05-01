#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR
if [ -d $RUNID ]; then
  cd $RUNID
  git pull
else
  git clone --depth 1 --recurse-submodules --shallow-submodules ${SPACK_STACK_URL:-https://github.com/JCSDA/spack-stack} -b ${SPACK_STACK_BRANCH:-develop} $RUNID
#  export SPACK_STACK_BRANCH=fix_hercules_orion_intel_config
#  git clone --depth 1 --recurse-submodules --shallow-submodules https://github.com/rickgrubin-noaa/spack-stack -b multiple_ufs_tests $RUNID
fi
