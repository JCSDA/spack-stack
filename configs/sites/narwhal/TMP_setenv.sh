#!/bin/bash

module unload PrgEnv-cray/8.3.2
module load PrgEnv-intel/8.1.0
module unload intel/2021.4.0
module unload cray-python/3.9.4.1

module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
module load miniconda/3.9.12
module load ecflow/5.8.4

module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-v1/envs/skylab-2.0.0-intel-2021.3.0/install/modulefiles/Core
module load stack-intel/2021.3.0
module load stack-cray-mpich/8.1.14
module load stack-python/3.9.12

module load jedi-ewok-env/1.0.0 jedi-fv3-env/1.0.0 soca-env/1.0.0 sp/2.3.3

module unload cray-libsci/21.08.1.2
module load cray-libsci/22.08.1.1
export LD_LIBRARY_PATH=/opt/cray/pe/libsci/22.08.1.1/INTEL/19.0/x86_64/lib:$LD_LIBRARY_PATH

module li

cd /p/work1/heinzell/jedi-bundle-develop-20221017/build-openmp/
