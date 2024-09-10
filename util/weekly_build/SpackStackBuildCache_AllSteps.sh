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

trap_and_run ./1_DirectorySetup.sh $*
trap_and_run ./2_GetSpackStackDevelop.sh $*
trap_and_run ./3_SetupUnifiedEnv.sh $*
trap_and_run ./4_SpackInstall.sh $*
trap_and_run ./5_BuildCache.sh $*
trap_and_run ./6_AppTests.sh $*
trap_and_run ./7_Cleanup.sh $*
