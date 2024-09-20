#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

echo Base directory: ${RUNDIR:?}

mkdir -p $RUNDIR
