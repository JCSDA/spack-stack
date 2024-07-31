#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/spack-stack-build-cache-${RUNID}

. setup.sh

installopts="--show-log-on-error"

for compiler in $COMPILERS; do
  cd envs/build-$compiler
  spack env activate .
  # Just install the packages we're testing (+dependencies):
  spack install $installopts --test root $PACKAGESTOTEST 2>&1 | tee log.install_withtesting
  # Install the rest of the stack as usual:
  spack install $installopts 2>&1 | tee log.install
done
