#!/bin/bash

# Do some stuff, and exit non-zero if UFSWM cannot be successfully built and
# tested (ideally, have a discernably different error condition if there are
# numerical differences)

echo Base directory: ${RUNDIR:?}
cd ${RUNDIR}

UFSWM_BRANCH=${UFSWM_BRANCH:-develop}
UFSWM_URL=${UFSWM_URL:-"https://github.com/ufs-community/ufs-weather-model.git"}

git clone -b ${BRANCH} --single-branch --recurse-submodules ${UFSWM_URL}
cd ufs-weather-model/tests

# rt.sh will parse arguments passed to it
./rt.sh  "${@}"

rc = $?
return rc
