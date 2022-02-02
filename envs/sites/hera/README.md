# Orion
## General instructions for getting the module environment right/fixed
```
module purge
module unuse /apps/modulefiles/core
export MODULEPATH_ROOT=$HOME/test_modulefiles
module use /home/dheinzel/test_modulefiles/core
```

## Building your own spack stack
```
git clone -b jcsda_emc_spack_stack --recursive https://github.com/climbfuji/spack-stack
cd spack-stack
export SPACK_BASE_DIR=$PWD
module load python/3.9.2
source spack/share/spack/setup-env.sh
rsync -av envs/ envs_orion/
vi envs_orion/spack.yaml
# comment out the "please_configure_your_site" site config and activate the hera site config
spack env activate -p -d envs_orion
spack install -v fv3-bundle-env 2>&1 | tee spack.install.fv3-bundle-env.log
```
... work in progress ... ufs-bundle-env and then metamodules





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
