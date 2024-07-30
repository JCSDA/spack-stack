#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/spack-stack-build-cache-$RUNID

. setup.sh

for compiler in $COMPILERS; do
  spack stack create env --name build-$compiler --template unified-dev --platform $PLATFORM
  cd envs/build-$compiler
  sed -i "s|- compilers: \['%.*|- compilers: ['%$compiler']|" spack.yaml
  # Check for duplicates and fail before doing the "real" concretization with test deps:
  spack concretize --fresh 2>&1 | tee log.concretize
  ${SPACK_STACK_DIR:?}/utils/show_duplicate_packages.py -d -i crtm log.concretize
  spack concretize --force --fresh --test all 2>&1 | tee log.concretize_test
done
