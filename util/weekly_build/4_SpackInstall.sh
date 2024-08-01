#!/bin/bash

set -e

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/${RUNID}

. setup.sh

INSTALL_OPTS="--show-log-on-error $INSTALL_OPTS"

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  spack fetch
  # Just install the packages we're testing (+dependencies):
  $SCHEDULER_CMD $(which spack) install $INSTALL_OPTS --test root $PACKAGES_TO_TEST 2>&1 | tee log.install_withtesting
  # Install the rest of the stack as usual:
  $SCHEDULER_CMD $(which spack) install $INSTALL_OPTS $PACKAGES_TO_INSTALL 2>&1 | tee log.install
done
