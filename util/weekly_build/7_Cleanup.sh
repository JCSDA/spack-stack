#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

/usr/bin/rm -rf ${RUNDIR:?}/${RUNID:?}
