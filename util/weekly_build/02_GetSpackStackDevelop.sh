#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR
if [ -d $RUNID ]; then
  cd $RUNID
  git pull
else
  #git clone --recurse-submodules https://github.com/AlexanderRichert-NOAA/spack-stack -b weekly_build $RUNID
  git clone --recurse-submodules https://github.nrlmry.navy.mil/JCSDA/spack-stack -b feature/weekly_build_nautilus $RUNID
fi
