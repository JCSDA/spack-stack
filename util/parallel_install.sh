#!/usr/bin/bash

# This script launches backgrounded instances of the 'spack install' command
# for an active Spack environment ($SPACK_ENV must be set). The first two
# arguments are required, specifying the number of instances and number of
# threads per instance, respectively. Remaining arguments are passed to the
# 'spack install' command. It is strongly recommended to only run this utility
# in a concretized environment. The script can be sourced so that the
# backgrounded jobs are associated with the current shell environment (strongly
# recommended when running inside a 'screen' or 'tmux' session).
#
# NOTE: If you are installing on a shared system (i.e., an HPC platform),
# especially if not running through a job scheduler with specified resources,
# be respectful of system resources and usage policies.
#
# *Depending on available resources*, for building the entire spack-stack
# unified environment, 2-4 instances with 4-8 cores each is generally
# reasonable. Six or more instances is generally overkill, as is more than 8
# cores per package build.
#
# Example usage:
#
#  % ../../utils/parallel_install.sh 2 6
# -or-
#  % . utils/parallel_install.sh 4 4 --fail-fast --verbose esmf

argtext="Run as '$0 N M', where N=# of instances, M=# of threads per instance"
n_instances=${1?"$argtext"}
n_threads=${2?"$argtext"}
shift 2

if [[ ! " $(seq -s ' ' 10) " =~ " $n_instances " ]]; then echo "Invalid number of instances" ; exit 1; fi
if [[ ! " $(seq -s ' ' 64) " =~ " $n_threads " ]]; then echo "Invalid number of threads" ; exit 1; fi

echo "Installing with $n_instances instances and ${n_threads} threads in environment '${SPACK_ENV?"SPACK_ENV not set!"}'"

for i in $(seq $n_instances); do
  cmd="spack install -j $n_threads $*"
  echo $cmd | tee ${SPACK_ENV}/log.install.proc${i}
  $cmd &>> ${SPACK_ENV}/log.install.proc${i} &
done

# If running as executable:
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    wait
fi
