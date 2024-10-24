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
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
  if [ "${SOURCE_CACHE::7}" == "file://" ]; then
    mirrorpath=${SOURCE_CACHE}
  else
    mirrorpath=$(spack mirror list | awk "{if (\$1==\"$SOURCE_CACHE\") print \$NF}")
  fi
  spack mirror create --dependencies --directory ${mirrorpath?"Source mirror path could not be determined. Check site's mirrors.yaml."} ${PACKAGES_TO_INSTALL:---all} 2>&1 | tee log.fetch
  # Just install the packages we're testing (+dependencies):
  spack_install_exe install $INSTALL_OPTS --test root $PACKAGES_TO_TEST
  # Install the rest of the stack as usual:
  spack_install_exe install $INSTALL_OPTS $PACKAGES_TO_INSTALL
done
