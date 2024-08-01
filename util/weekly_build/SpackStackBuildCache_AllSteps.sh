#!/bin/bash

set -ex

cd $(dirname $0)

. ShellSetup.sh $*

trap "ERROR" ERR

function ERROR { alert_cmd ; exit 1;}

export SETUPDONE=YES

./1_DirectorySetup.sh $*
./2_GetSpackStackDevelop.sh $*
./3_SetupUnifiedEnv.sh $*
./4_SpackInstall.sh $*
./5_BuildCache.sh $*
./6_AppTests.sh $*
./7_Cleanup.sh $*
