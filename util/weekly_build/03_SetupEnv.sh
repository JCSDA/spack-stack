#!/bin/bash

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

set -ex

cd $RUNDIR/$RUNID

set +x
. setup.sh
set -x

for compiler in $COMPILERS; do
  for template in $TEMPLATES; do
    [[ ${compiler} == *"@="* ]] && envname=build-$template-${compiler/@=/-} || envname=build-$template-${compiler/@/-}
    envdir=$RUNDIR/$RUNID/envs/$envname
    echo "Setting up environment $envname in $envdir"
    if [ ! -d $envdir ]; then
      spack stack create env --name $envname --template $template --site $PLATFORM --compiler $compiler
    fi
    cd $envdir
    spack env activate .
    spack config add "config:install_tree:padded_length:${PADDED_LENGTH:-200}"
    # Check for duplicates and fail before doing the "real" concretization:
    spack_wrapper log.concretize concretize --fresh
    ${SPACK_STACK_DIR:?}/util/show_duplicate_packages.py -i crtm-fix -i crtm -i esmf -i mapl -i neptune-env
#   The following is not working at the moment, for seemingly a couple reasons. Therefore packages with test-only deps cannot be tested.
#    spack concretize --force --fresh --test all | tee log.concretize_test
  done
done
