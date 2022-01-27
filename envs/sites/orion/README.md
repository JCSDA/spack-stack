ORION

module purge
module unuse /apps/modulefiles/core
export MODULEPATH_ROOT=$HOME/test_modulefiles
module use /home/dheinzel/test_modulefiles/core
module load intel/2020.2 impi/2020.2
module load python/3.9.2
module load contrib noaatools
module av
module li

# SPACK ENV

/work/noaa/gsd-hpcs/dheinzel/jcsda/spack-stack-20220124
source spack/share/spack/setup-env.sh
spack env activate -p -d envs_orion

# fv3-bundle

module purge
module unuse /apps/modulefiles/core
export MODULEPATH_ROOT=$HOME/test_modulefiles
module use /home/dheinzel/test_modulefiles/core
#module load intel/2020.2 impi/2020.2
#module load python/3.9.2
module load contrib noaatools
module av
module li


cd /work/noaa/gsd-hpcs/dheinzel/jcsda/fv3-bundle/fv3-bundle-spack-stack-20220120/buildscripts
module use /work/noaa/gsd-hpcs/dheinzel/jcsda/spack-stack-20220118/envs/install/modulefiles/intel/19.1.2
module use /work/noaa/gsd-hpcs/dheinzel/jcsda/spack-stack-20220118/envs/install/modulefiles/intel-mpi/2019.8.254-zr5qzq7/intel/19.1.2
module av
