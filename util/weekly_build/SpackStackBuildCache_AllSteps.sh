#!/bin/bash

set -e

. ShellSetup.sh $*

trap "ERROR" ERR

function ERROR {
  eval "$ALERT_CMD"
  exit 1
}

export SETUPDONE=YES

./1_DirectorySetup.sh $*
./2_GetSpackStackDevelop.sh $*
./3_SetupUnifiedEnv.sh $*
./4_SpackInstall.sh $*
./5_BuildCache.sh $*
./6_AppTests.sh $*
./7_Cleanup.sh $*
