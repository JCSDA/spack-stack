#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/${RUNID}

set +x
. setup.sh
set -x

INSTALL_OPTS="--show-log-on-error $INSTALL_OPTS"

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  spack fetch
  # Just install the packages we're testing (+dependencies):
  scheduler_cmd $(which spack) install $INSTALL_OPTS --test root $PACKAGES_TO_TEST
  # Install the rest of the stack as usual:
  scheduler_cmd $(which spack) install $INSTALL_OPTS $PACKAGES_TO_INSTALL
done
