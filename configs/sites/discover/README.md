# Discover

## General instructions/prerequisites
```
module purge
```

### One-off: prepare miniconda python3 environment
See instructions in miniconda/README.md. Don't forget to log off and back on to forget about the conda environment.

### One-off: install qt5
The default `qt5` in `/usr` is incomplete and thus insufficient for building `ecflow`. Because installing `qt5` is complex and has a lot of OS (X11) dependencies, we install it outside of spack with GCC and then point to it in Discover's `packages.yaml`. Steps to install `qt5`:
```
module purge
module use /discover/swdev/jcsda/spack-stack/modulefiles
module load miniconda/3.9.7
module load comp/gcc/10.1.0

cd /gpfsm/dswdev/jcsda/spack-stack/
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
../qt5/configure -opensource -nomake examples -nomake tests -prefix /discover/swdev/jcsda/spack-stack/qt-5.15.3 -skip qtdocgallery -skip qtwebengine 2>&1 | tee log.configure
gmake -j4 2>&1 | tee log.gmake
gmake install 2>&1 | tee log.install
```

### Set up the user environment for working with spack/building new software environments
This needs to be done every time before installing packages with spack or before using spack-provided modules!
```
module use /discover/swdev/jcsda/spack-stack/modulefiles
module load miniconda/3.9.7
```
