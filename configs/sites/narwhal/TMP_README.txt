module unload PrgEnv-cray/8.3.2
module load PrgEnv-intel/8.1.0
module unload intel/2021.4.0
module unload cray-python/3.9.4.1

module li

Currently Loaded Modulefiles:
  1) intel/2021.3.0           5) craype-network-ofi       9) cray-libsci/21.08.1.2   13) PrgEnv-intel/8.1.0
  2) craype/2.7.10            6) cray-dsmml/0.2.1        10) cray-pals/1.1.5
  3) craype-x86-rome          7) perftools-base/21.09.0  11) bct-env/0.1
  4) libfabric/1.11.0.4.125   8) cray-mpich/8.1.14       12) mpscp/1.3a



mkdir -p /p/work1/heinzell/git-lfs-2.10.0/src
# On Cheyenne
wget https://download.opensuse.org/repositories/openSUSE:/Leap:/15.2/standard/x86_64/git-lfs-2.10.0-lp152.1.2.x86_64.rpm
# Copy over from Cheyenne
.... follow instructions in read the docs, install in /p/work1/heinzell/git-lfs-2.10.0

install own miniconda

install qt5 with module

ecflow ...
module load gcc/10.3.0
miniconda/3.9.12

remove the following from ecFlow-5.8.4-Source/build_scripts/boost_build.sh
       if [ "$PE_ENV" = INTEL ] ; then
          tool=intel
       fi
       if [ "$PE_ENV" = CRAY ] ; then
          tool=cray
       fi
       
CC=gcc CXX=g++ FC=gfortran cmake .. -DCMAKE_INSTALL_PREFIX=/p/work1/heinzell/ecflow-5.8.4 2>&1 | tee log.cmake





module use /p/work1/heinzell/modulefiles
module load miniconda/3.9.12
module load ecflow/5.8.4


cd /p/work1/heinzell/spack-stack





heinzell@x1006c1s6b1n0:/p/work1/heinzell/miniconda-3.9.12/lib> ls -l libtinfow*
-rw-rw-r-- 1 heinzell 4635GYFM 496544 Sep 15 16:01 libtinfow.a
lrwxrwxrwx 1 heinzell 4635GYFM     16 Sep 15 16:01 libtinfow.so -> libtinfow.so.6.3
lrwxrwxrwx 1 heinzell 4635GYFM     16 Sep 15 16:01 libtinfow.so.6 -> libtinfow.so.6.3
lrwxrwxrwx 1 heinzell 4635GYFM     20 Sep 15 16:05 libtinfow.so.6.3 -> /lib64/libtinfo.so.6
-rwxrwxr-x 1 heinzell 4635GYFM 287736 Sep 15 16:01 libtinfow.so.6.3.conda.original







module use /p/work1/heinzell/spack-stack/envs/skylab-dev-intel-2021.3.0/install/modulefiles/Core
module load stack-intel/2021.3.0
module load stack-cray-mpich/8.1.14
module load stack-python/3.9.12
module available

module load jedi-ewok-env/1.0.0 jedi-fv3-env/1.0.0 soca-env/1.0.0
# NOT YET
#module load crtm/


module unload PrgEnv-cray/8.3.2
module load PrgEnv-intel/8.1.0
module unload intel/2021.4.0
module unload cray-python/3.9.4.1
module use /p/work1/heinzell/modulefiles
module load miniconda/3.9.12
module use /p/work1/heinzell/spack-stack/envs/skylab-dev-intel-2021.3.0/install/modulefiles/Core
module load stack-intel/2021.3.0
module load stack-cray-mpich/8.1.14
module load stack-python/3.9.12
module load jedi-ewok-env/1.0.0 jedi-fv3-env/1.0.0 soca-env/1.0.0
### module load crtm/v2.3-jedi.4
