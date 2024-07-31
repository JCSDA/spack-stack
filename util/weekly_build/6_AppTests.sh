#!/bin/bash

set -e

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

if [ "$TEST_UFSWM" == ON ]; then
  ./apptests/test_ufswm.sh
fi
