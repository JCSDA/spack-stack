#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR
if [ -d $RUNID ]; then
  cd $RUNID
  git pull
else
  git clone --recurse-submodules https://github.com/AlexanderRichert-NOAA/spack-stack -b weekly_build $RUNID
fi
