# Cheyenne
## General instructions for getting the module environment right/fixed
```
module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
export MODULEPATH_ROOT=/glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules
module use /glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules/compilers
```

## Building your own spack stack
```
git clone -b jcsda_emc_spack_stack --recursive https://github.com/climbfuji/spack-stack
cd spack-stack
export SPACK_BASE_DIR=$PWD
module load python/3.7.9
source spack/share/spack/setup-env.sh
rsync -av envs/ envs_cheyenne/
vi envs_cheyenne/spack.yaml
# comment out the "please_configure_your_site" site config and activate the cheyenne site config
spack env activate -p -d envs_cheyenne
spack install -v fv3-bundle-env 2>&1 | tee spack.install.fv3-bundle-env.log
spack install -v ufs-bundle-env 2>&1 | tee spack.install.ufs-bundle-env.log
spack module lmod refresh
./meta_modules/setup_meta_modules.py
```

## Using spack stack
### In general
```
module use SPACK_BASE_DIR/envs_cheyenne/install/modulefiles/Core
module load stack-intel/2020.1.217
module load stack-intel-mpi/2019.7.217
module load stack-python/3.7.9
module li
module av
```

### Build fv3-bundle
```
git clone -b fv3_bundle_jedi_spack_stack --recursive https://github.com/climbfuji/fv3-bundle
cd fv3-bundle/buildscripts
./build_cheyenne.sh 2>&1 | tee build_cheyenne.log
```

### Build ufs-weather-model
```
git clone -b ufs-weather-model-spack-stack --recursive https://github.com/climbfuji/ufs-weather-model
cd ufs-weather-model/tests
./compile.sh cheyenne.intel '-DAPP=ATM -DCCPP_SUITES=FV3_GFS_v16,FV3_RAP' '' NO NO 2>&1 | tee compile.log
```
