#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR
if [ ! -d $RUNID ]; then
  git clone --recurse-submodules https://github.com/JCSDA/spack-stack -b develop $RUNID
fi
