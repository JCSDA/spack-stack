#!/bin/bash
# This script is run by build.pbs as a pseudo-MPI task.

hostname
umask 002
module reset
cd $PBS_O_WORKDIR
. ../../setup.sh
spack env activate .
printenv &> output/env.${PBS_JOBID}.${PMI_RANK}
mkdir -p $TMPDIR

# Loading these modules to avoid ESMF issue:
module load PrgEnv-gnu
module load gcc/11.2.0
module load craype
module load cray-mpich

# Run installation:
SPACK_DISABLE_LOCAL_CONFIG=true SPACK_USER_CONFIG_PATH=/dev/null LC_ALL=en_US.UTF-8 spack install --no-cache -j8 &> output/log.${PBS_JOBID}.${PMI_RANK}

exit 0
