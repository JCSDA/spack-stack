module unload PrgEnv-cray/8.1.0
module load PrgEnv-intel/8.1.0

module li

Currently Loaded Modulefiles:
  1) intel/2021.3.0           5) craype-network-ofi       9) cray-libsci/21.08.1.2   13) PrgEnv-intel/8.1.0
  2) craype/2.7.10            6) cray-dsmml/0.2.1        10) cray-pals/1.1.5
  3) craype-x86-rome          7) perftools-base/21.09.0  11) bct-env/0.1
  4) libfabric/1.11.0.4.125   8) cray-mpich/8.1.9        12) mpscp/1.3a

module load cray-python/3.9.4.1




mkdir -p /p/work1/heinzell/git-lfs-2.10.0/src
# On Cheyenne
wget https://download.opensuse.org/repositories/openSUSE:/Leap:/15.2/standard/x86_64/git-lfs-2.10.0-lp152.1.2.x86_64.rpm
# Copy over from Cheyenne
.... follow instructions in read the docs, install in /p/work1/heinzell/git-lfs-2.10.0

module use /p/work1/heinzell/modulefiles
module load git-lfs/2.10.0
