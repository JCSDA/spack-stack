# Gaea
## General instructions for getting the module environment right/fixed
```
source /lustre/f2/pdata/esrl/gsd/contrib/lua-5.1.4.9/init/init_lmod.sh
```

## Building your own spack stack
```
git clone -b jcsda_emc_spack_stack --recursive https://github.com/climbfuji/spack-stack
cd spack-stack
export SPACK_BASE_DIR=$PWD
module load cray-python/3.7.3.2
source spack/share/spack/setup-env.sh
rsync -av envs/ envs_cheyenne/
vi envs_cheyenne/spack.yaml
# comment out the "please_configure_your_site" site config and activate the gaea site config
spack env activate -p -d envs_gaea
spack install -v fv3-bundle-env 2>&1 | tee spack.install.fv3-bundle-env.log
spack install -v ufs-bundle-env 2>&1 | tee spack.install.ufs-bundle-env.log
spack module lmod refresh
./meta_modules/setup_meta_modules.py
```

## Using spack stack
### In general
```
module use SPACK_BASE_DIR/envs_gaea/install/modulefiles/Core
module load stack-intel/2021.3.0
module load stack-intel-cray-mpich/7.7.11
module load stack-python/3.7.3.2
module li
module av
```

### Build fv3-bundle
```
git clone -b fv3_bundle_jedi_spack_stack --recursive https://github.com/climbfuji/fv3-bundle
cd fv3-bundle/buildscripts
./build_gaea.sh 2>&1 | tee build_gaea.log
```

### Build ufs-weather-model
```
git clone -b ufs-weather-model-spack-stack --recursive https://github.com/climbfuji/ufs-weather-model
cd ufs-weather-model/tests
./compile.sh gaea.intel '-DAPP=ATM -DCCPP_SUITES=FV3_GFS_v16,FV3_RAP' '' NO NO 2>&1 | tee compile.log
```
