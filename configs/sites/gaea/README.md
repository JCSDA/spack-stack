# Gaea
## General instructions/prerequisites

### One-off: install qt5
The default `qt5` in `/usr` is incomplete and thus insufficient for building `ecflow`. Because installing `qt5` is complex and has a lot of OS (X11) dependencies, we install it outside of spack with the default OS compiler and then point to it in Gaea's `packages.yaml`. Steps to install `qt5`:
```
module unload intel cray-mpich cray-python darshan
module load cray-python/3.7.3.2
cd /lustre/f2/pdata/esrl/gsd/spack-stack
mkdir -p qt-5.15.3/src
cd qt-5.15.3/src
git clone git://code.qt.io/qt/qt5.git
cd qt5/
git fetch --tags
git checkout v5.15.3-lts-lgpl
perl init-repository
git submodule update --init --recursive
cd ..
mkdir qt5-build
cd qt5-build/
../qt5/configure -opensource -nomake examples -nomake tests -prefix /lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.3 -skip qtdocgallery 2>&1 | tee log.configure
gmake -j4 2>&1 | tee log.gmake
gmake install 2>&1 | tee log.install
```

### Set up the user environment for working with spack/building new software environments
```
module unload intel
module unload cray-mpich
module unload cray-python
module unload darshan
module load cray-python/3.7.3.2
```

### Known issues
1. Random "permission denied" errors during the spack install phase
If random errors during the spack install phase occur related to "permission denied" when building packages, edit `envs/env_name/config.yaml` and comment out the lines `build_stage` and `test_stage`.
