#!/bin/bash

echo "build host: $(hostname)"

set -exa

cd $(dirname $0)

. ShellSetup.sh $*
export SETUPDONE=YES

function trap_and_run {
  trap ERROR ERR
  scriptname=$1
  function ERROR { alert_cmd $scriptname ; exit 1;}
  $*
}

trap_and_run ./01_DirectorySetup.sh $*
trap_and_run ./02_GetSpackStack.sh $*
trap_and_run ./03_SetupUnifiedEnv.sh $*
trap_and_run ./04_SpackInstall.sh $*
trap_and_run ./05_BuildCache.sh $*
trap_and_run ./06_AppTests.sh $*
trap_and_run ./07_Cleanup.sh $*
