# Preparing NRL ParallelWorks AWS clusters for spack-stack

## Prerequisites

### GNU 13.4.0

Download and install:
```
module purge
umask 0022

mkdir -p /project/spack-stack/gcc-13.4.0/src
cd /project/spack-stack/gcc-13.4.0/src
wget https://github.com/gcc-mirror/gcc/archive/refs/tags/releases/gcc-13.4.0.tar.gz
tar -xf gcc-13.4.0.tar.gz

cd gcc-releases-gcc-13.4.0
./contrib/download_prerequisites 2>&1 | tee log.download_prerequisites
./configure \
  --prefix=/project/spack-stack/gcc-13.4.0 \
  --disable-multilib \
  2>&1 | tee log.configure
make -j48 2>&1 | tee log.make
# Cannot run make check, because autogen is not installed
#make check 2>&1 | tee log.check
make install 2>&1 | tee log.install
```

Create modulefile `/project/spack-stack/gcc-13.4.0/modulefiles/gcc/13.4.0`:
```
mkdir -p /project/spack-stack/gcc-13.4.0/modulefiles/gcc
cat << EOF > /project/spack-stack/gcc-13.4.0/modulefiles/gcc/13.4.0
#%Module1.0

module-whatis "Provides gcc-13.4.0 for use with spack."

conflict gnu
conflict gcc

proc ModulesHelp { } {
puts stderr "Provides gcc-13.4.0 for use with spack."
}


# Set this value
set GCC_PATH "/project/spack-stack/gcc-13.4.0"

prepend-path PATH "${GCC_PATH}/bin"
prepend-path LD_LIBRARY_PATH "${GCC_PATH}/lib"
prepend-path LD_LIBRARY_PATH "${GCC_PATH}/lib64"
prepend-path LIBRARY_PATH "${GCC_PATH}/lib"
prepend-path LIBRARY_PATH "${GCC_PATH}/lib64"
prepend-path CPATH "${GCC_PATH}/include"
prepend-path CMAKE_PREFIX_PATH "${GCC_PATH}"
prepend-path PKG_CONFIG_PATH "${GCC_PATH}/usr/lib64/pkgconfig"
prepend-path MANPATH "${GCC_PATH}/share/man"
EOF
```

### OpenMPI 4.1.8

Download and install:
```
module purge
umask 0022

module use /project/spack-stack/gcc-13.4.0/modulefiles
module load gcc/13.4.0

mkdir -p /project/spack-stack/openmpi-4.1.8/gcc-13.4.0/src
cd /project/spack-stack/openmpi-4.1.8/gcc-13.4.0/src
wget https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.8.tar.gz
tar -xf openmpi-4.1.8.tar.gz

cd openmpi-4.1.8
./configure \
  --prefix=/project/spack-stack/openmpi-4.1.8/gcc-13.4.0 \
  2>&1 | tee log.configure
make -j48 2>&1 | tee log.make
make check 2>&1 | tee log.check
make install 2>&1 | tee log.install
```

Create modulefile `/project/spack-stack/openmpi-4.1.8/gcc-13.4.0/modulefiles/openmpi/4.1.8`:
```
mkdir -p /project/spack-stack/openmpi-4.1.8/gcc-13.4.0/modulefiles/openmpi
cd /project/spack-stack/openmpi-4.1.8/gcc-13.4.0/modulefiles/openmpi
cat <<EOF > /project/spack-stack/openmpi-4.1.8/gcc-13.4.0/modulefiles/openmpi/4.1.8
#%Module1.0

module-whatis "Provides openmpi-4.1.8 compiled with gcc-13.4.0 for use with spack."

conflict gnu
conflict gcc

proc ModulesHelp { } {
puts stderr "Provides openmpi-4.1.8 compiled with gcc-13.4.0 for use with spack."
}


# Set this value
set OPENMPI_PATH "/project/spack-stack/openmpi-4.1.8/gcc-13.4.0"

prepend-path PATH "${OPENMPI_PATH}/bin"
prepend-path LD_LIBRARY_PATH "${OPENMPI_PATH}/lib"
prepend-path LIBRARY_PATH "${OPENMPI_PATH}/lib"
prepend-path CPATH "${OPENMPI_PATH}/include"
prepend-path CMAKE_PREFIX_PATH "${OPENMPI_PATH}"
prepend-path MANPATH "${OPENMPI_PATH}/share/man"
EOF
```

### Intel oneAPI 2025.3.0

Download and install:
```
module purge
umask 022

mkdir -p /project/spack-stack/oneapi-2025.3.0/src
cd /project/spack-stack/oneapi-2025.3.0/src
wget https://registrationcenter-download.intel.com/akdlm/IRC_NAS/66021d90-934d-41f4-bedf-b8c00bbe98bc/intel-oneapi-hpc-toolkit-2025.3.0.381_offline.sh

sh ./intel-oneapi-hpc-toolkit-2025.3.0.381_offline.sh -a --silent --cli --eula accept
```

Select a custom installation of all components in `/project/spack-stack/oneapi-2025.3.0`. After the installation, create the modulefiles:
```
cd /project/spack-stack/oneapi-2025.3.0
./modulefiles-setup.sh --ignore-latest --output-dir=/project/spack-stack/oneapi-2025.3.0/modulefiles

# Fix non-ascii characters in modulefiles
sed -i 's/®//g' `grep -lRe '®' modulefiles`
```
