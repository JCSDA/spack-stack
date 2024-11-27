#!/bin/bash

# Do some stuff, and exit non-zero if UFSWM cannot be successfully built and
# tested (ideally, have a discernably different error condition if there are
# numerical differences)

cd ${RUNDIR}

# The following need to be cleaned up for proper variable substitution; this is a one-off test
BRANCH=spack-stack-automation

git clone -b ${BRANCH} --single-branch --recurse-submodules https://github.com/rickgrubin-noaa/ufs-weather-model.git
cd ufs-weather-model/tests

# -r ==> rocoto ; not strictly necessary, can run without
./rt.sh -a epic -k -r -n "control_c48 intel"

rc = $?
return rc

