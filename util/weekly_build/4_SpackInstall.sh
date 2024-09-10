#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/${RUNID}

set +x
. setup.sh
set -x

INSTALL_OPTS="--show-log-on-error --fail-fast $INSTALL_OPTS"

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  if [ -z $PACKAGES_TO_INSTALL ]; then
    spack fetch 2>&1 | tee log.fetch
  else
    spack fetch --dependencies $PACKAGES_TO_INSTALL 2>&1 | tee log.fetch
  fi
  # Just install the packages we're testing (+dependencies):
  spack_install_exe install $INSTALL_OPTS --test root $PACKAGES_TO_TEST 2>&1 | tee log.test.install
  # Install the rest of the stack as usual:
  spack_install_exe install $INSTALL_OPTS $PACKAGES_TO_INSTALL 2>&1 | tee log.install
done
