#!/bin/bash

# Do some stuff, and exit non-zero if UFSWM cannot be successfully built and
# tested (ideally, have a discernably different error condition if there are
# numerical differences)

echo Base directory: ${RUNDIR:?}
cd ${RUNDIR}

UFSWM_BRANCH=${UFSWM_BRANCH:-develop}
UFSWM_URL=${UFSWM_URL:-"https://github.com/ufs-community/ufs-weather-model.git"}

git clone --single-branch --recurse-submodules ${UFSWM_URL} -b ${UFSWM_BRANCH}
cd ufs-weather-model/tests

# rt.sh will parse arguments passed to it
RT_ARGS=${RT_ARGS:-"-a ${BATCHACCOUNT:?} -n 'control_c48 intel'"}
./rt.sh $RT_ARGS

rc = $?
return rc
