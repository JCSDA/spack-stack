#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR
git clone https://github.com/JCSDA/spack-stack -b develop spack-stack-build-cache-${RUNID}
