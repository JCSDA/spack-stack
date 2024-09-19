#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

if [ "$KEEP_WEEKLY_BUILD_DIR" != YES ]; then
  /usr/bin/rm -rf ${RUNDIR:?}/${RUNID:?}
fi
