#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

if [ "$KEEP_WEEKLY_BUILD_DIR" != YES ]; then
  /usr/bin/rm -rf ${RUNDIR:?}/${RUNID:?}
else
  ${FIND_CMD} ${RUNDIR:?}/${RUNID:?} -type f -print0 | xargs -0 touch
fi
