#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

if [ "$TEST_UFSWM" == ON ]; then
  ./apptests/test_ufswm.sh
fi
