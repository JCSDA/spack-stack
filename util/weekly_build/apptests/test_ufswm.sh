#!/bin/bash

# Do some stuff, and exit non-zero if UFSWM cannot be successfully built and
# tested (ideally, have a discernably different error condition if there are
# numerical differences)

echo "Current directory, in which ufs-weather-model will be cloned: $PWD"

UFSWM_BRANCH=${UFSWM_BRANCH:-develop}
UFSWM_URL=${UFSWM_URL:-"https://github.com/ufs-community/ufs-weather-model.git"}

if [ ! -d ufs-weather-model ]; then
  git clone --recurse-submodules --single-branch --depth 1 --shallow-submodules ${UFSWM_URL} -b ${UFSWM_BRANCH}
fi
cd ufs-weather-model/tests

# rt.sh will parse arguments passed to it
./rt.sh $RT_ARGS -a ${BATCHACCOUNT:?} -n 'control_c48 intel'

rc = $?
return rc
