#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -e

cd $RUNDIR
git clone --recurse-submodules https://github.com/JCSDA/spack-stack -b develop spack-stack-build-cache-${RUNID}
