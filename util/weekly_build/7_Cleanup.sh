#!/bin/bash

set -e

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

/usr/bin/rm -rf ${RUNDIR:?}/${RUNID:?}
