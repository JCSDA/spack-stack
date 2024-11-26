#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/${RUNID}

set +x
. setup.sh
set -x

if [ "$REUSE_BUILD_CACHE" == YES ]; then
  cache_flag="--no-check-signature"
else
  cache_flag="--no-cache"
fi

INSTALL_OPTS="--show-log-on-error --fail-fast $cache_flag $INSTALL_OPTS"

for compiler in $COMPILERS; do
  for template in $TEMPLATES; do
    envname=build-$template-${compiler/@/-}
    envdir=$RUNDIR/$RUNID/envs/$envname
    echo "Building environment $envname in $envdir"
    cd $envdir
    spack env activate .
    if [ "${SOURCE_CACHE::7}" == "file://" ]; then
      mirrorpath=${SOURCE_CACHE}
    else
      mirrorpath=$(spack mirror list | awk "{if (\$1==\"$SOURCE_CACHE\") print \$NF}")
    fi
    mirrorpath=${mirrorpath#file://}
    spack_wrapper log.fetch mirror create --dependencies \
        --directory ${mirrorpath?"Source mirror path could not be determined. Check site's mirrors.yaml."} \
        ${PACKAGES_TO_INSTALL:---all}
    # Just install the packages we're testing (+dependencies):
    if [[ ! -z "${PACKAGES_TO_TEST}" ]]; then
      spack_install_wrapper log.install-and-test install $INSTALL_OPTS --test root $PACKAGES_TO_TEST
    fi
    # Install the rest of the stack as usual:
    spack_install_wrapper log.install install $INSTALL_OPTS $PACKAGES_TO_INSTALL
  done
done
