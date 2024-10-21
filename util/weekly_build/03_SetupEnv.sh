#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR/$RUNID

set +x
. setup.sh
set -x

for compiler in $COMPILERS; do
  for template in $TEMPLATES; do
    echo "Setting up environment build-${compiler/@/-} using template $template"
    rm -rf $RUNDIR/$RUNID/envs/build-${compiler/@/-}
    spack stack create env --name build-${template}-${compiler/@/-} --template $template --site $PLATFORM --compiler $compiler
    cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
    spack env activate .
    spack config add "config:install_tree:padded_length:${PADDED_LENGTH:-200}"
    # Check for duplicates and fail before doing the "real" concretization:
    spack concretize --fresh 2>&1 | tee log.concretize
    ${SPACK_STACK_DIR:?}/util/show_duplicate_packages.py log.concretize -d -i crtm -i esmf
    spack concretize --fresh --force
#   The following is not working at the moment, for seemingly a couple reasons. Therefore packages with test-only deps cannot be tested.
#    spack concretize --force --fresh --test all 2>&1 | tee log.concretize_test
    # Get path to local-source mirror from spack site config
    SOURCE_MIRROR=`spack mirror list | grep local-source`
    SOURCE_MIRROR=${SOURCE_MIRROR/local-source \[sb\] file:\/\//}
    # Download all source codes needed to build the environment
    spack mirror create -a -d ${SOURCE_MIRROR}
  done
done
