#!/bin/bash

set -ex

if [ -z $SETUPDONE ]; then . ShellSetup.sh $* ; fi

cd $RUNDIR/${RUNID}

set +x
. setup.sh
set -x

<<<<<<< HEAD
INSTALL_OPTS="--show-log-on-error --fail-fast --no-cache $INSTALL_OPTS"
=======
if [ "$REUSE_BUILD_CACHE" == YES ]; then
  cache_flag="--no-check-signature"
else
  cache_flag="--no-cache"
fi

INSTALL_OPTS="--show-log-on-error --fail-fast $cache_flag $INSTALL_OPTS"
>>>>>>> 5068f19444eaa1564c66a6e9ff751bf7fac16be6

for compiler in $COMPILERS; do
  cd $RUNDIR/$RUNID/envs/build-${compiler/@/-}
  spack env activate .
<<<<<<< HEAD
  #spack fetch # 2>&1 | tee log.fetch
  #if [ -z "$PACKAGES_TO_INSTALL" ]; then
  #  spack fetch --missing # 2>&1 | tee log.fetch
  #else
  #  spack fetch --missing --dependencies $PACKAGES_TO_INSTALL # 2>&1 | tee log.fetch
  #fi
  # Just install the packages we're testing (+dependencies):
  spack_install_exe install $INSTALL_OPTS --test root $PACKAGES_TO_TEST # 2>&1 | tee log.test.install
  # Install the rest of the stack as usual:
  spack_install_exe install $INSTALL_OPTS $PACKAGES_TO_INSTALL # 2>&1 | tee log.install
=======
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
>>>>>>> 5068f19444eaa1564c66a6e9ff751bf7fac16be6
done
