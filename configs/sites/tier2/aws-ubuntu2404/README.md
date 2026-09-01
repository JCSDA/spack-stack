## spack-stack AMI (Ubuntu 24.04)

This document is to go over the the running and usage of this specific AMI for Ubuntu 24.04 LTS. This image has two environments: gnu (gcc-13.3.0), and intel (intel-oneapi 2026.1.1). You can use either one of these environments for development purposes.

### Using the Snapshot

Here is an example `aws cli` command-line to run a pre-built snapshot with your designated key-pair.

```bash
aws ec2 run-instances \
   --image-id "ami-0ea3c35c5c3284d82" --instance-type "m6i.4xlarge" \
   --key-name YOUR-KEYPAIR \
   --block-device-mappings '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"Iops":3000,"SnapshotId":"snap-05fb00e35af5550e7","VolumeSize":150,"VolumeType":"gp3","Throughput":125}}' \
   --network-interfaces '{"SubnetId":"subnet-072fb62ff85b32a7a","AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-0091fa8e748fbe355"]}' \
   --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"ubuntu2404-spack-stack-1.9-gcc-oneapi"}]}' \
   --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
   --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":false,"EnableResourceNameDnsAAAARecord":false}' \
   --count 1
```

## Using this Site Config

JCSDA publishes a fully configured and built installation of spack stack derived
from this config as an AWS Snapshot. The easiest way to use this
configuration of spack stack is to launch a VM using that AMI. The instructions
below are included for maintainance of the history of this site config and
their possible relevance to debugging issues should they arise.

### Base Instance

This AMI was built on an instance with these properties:

* AMI Name: ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-20240927
* AMI ID: ami-0ea3c35c5c3284d82
* Instance m6i.4xlarge  (uses Intel Xeon processor)
* 150GB of gp3 storage as /

## Pre-requisites (For All Compilers)

### Installing Packages

```bash
# Update system software and start a tmux session.
sudo su -
apt update
apt upgrade -y

# Build tools
apt install -y build-essential g++-13 gcc-13 gfortran-13 make cmake automake autoconf apt-utils

#Install other requirements.
apt install -y cpp-13 libgomp1 git git-lfs autopoint mysql-server libmysqlclient-dev qtbase5-dev qt5-qmake libqt5svg5-dev qt5dxcb-plugin wget curl file tcl-dev gnupg2 iproute2 locales unzip less bzip2 gettext libtree pkg-config libcurl4-openssl-dev mysql-server libtool flex llvm-14

# Set llvm config.
update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-14 10

# Editors
apt install -y vim nano

# Python develop.
apt install -y python3 python3-pip python3-setuptools

# Configure git credential caching and git lfs for the rocky user and root.
git config --global credential.helper 'cache --timeout=3600'
git lfs install
# Change the gcc, g++, and gfortran version to 13 and give it the highest priority
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100
update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-13 100

exit # Exit root access
```

**Important**: Running the `update-alternatives` changes defaults, and if you need to use a different version of gcc/g++/gfortran you can run: `update-alternatives --config [gcc|g++|gfortran]` and select the version you want that is installed.

### Install Lmod

```bash
# Install lua/lmod manually because apt only has older versions
# that are not compatible with the modern lua modules spack produces
# https://lmod.readthedocs.io/en/latest/030_installing.html#install-lua-x-y-z-tar-gz
sudo su -
mkdir -p /opt/lua/5.1.4.9/src && cd $_
wget https://sourceforge.net/projects/lmod/files/lua-5.1.4.9.tar.bz2
tar -xvf lua-5.1.4.9.tar.bz2
cd lua-5.1.4.9
./configure --prefix=/opt/lua/5.1.4.9 2>&1 | tee log.config
make VERBOSE=1 2>&1 | tee log.make
make install 2>&1 | tee log.install

cat << 'EOF' >> /etc/profile.d/02-lua.sh
# Set environment variables for lua
export PATH="/opt/lua/5.1.4.9/bin:$PATH"
export LD_LIBRARY_PATH="/opt/lua/5.1.4.9/lib:$LD_LIBRARY_PATH"
export CPATH="/opt/lua/5.1.4.9/include:$CPATH"
export MANPATH="/opt/lua/5.1.4.9/man:$MANPATH"
EOF

source /etc/profile.d/02-lua.sh
mkdir -p /opt/lmod/8.7/src
cd /opt/lmod/8.7/src
wget https://sourceforge.net/projects/lmod/files/Lmod-8.7.tar.bz2
tar -xvf Lmod-8.7.tar.bz2
cd Lmod-8.7
# Note the weird prefix, lmod installs in PREFIX/lmod/X.Y automatically
./configure --prefix=/opt/ \
            --with-lmodConfigDir=/opt/lmod/8.7/config \
            2>&1 | tee log.config
make install 2>&1 | tee log.install
ln -sf /opt/lmod/lmod/init/profile /etc/profile.d/z00_lmod.sh
ln -sf /opt/lmod/lmod/init/cshrc /etc/profile.d/z00_lmod.csh
ln -sf /opt/lmod/lmod/init/profile.fish /etc/profile.d/z00_lmod.fish

# Log out completely, ssh back into the instance and check if lua modules work
exit
exit
```

### Clone `spack-stack`

```bash
cd /opt
sudo git clone -b release/2.1 --depth 1 --recursive https://github.com/jcsda/spack-stack.git
```

## Install Spack-Stack Steps by Compiler

<details>
<summary><b>GCC Installation</b></summary>

```bash
sudo su -

cd /opt/spack-stack
source setup.sh
# Swap default module type for default linux.
sed -i 's/tcl/lmod/g' configs/sites/tier2/linux.default/modules.yaml
spack stack create env --site linux.default --template unified-dev --name unified-gcc --compiler gcc
cd envs/unified-gcc
spack env activate -p .
unset SPACK_DISABLE_LOCAL_CONFIG
export SPACK_SYSTEM_CONFIG_PATH="$(pwd)/site"
spack external find --scope system \
    --exclude cmake \
    --exclude curl --exclude openssl \
    --exclude openssh --exclude python
spack compiler find --scope system
export SPACK_DISABLE_LOCAL_CONFIG=true
unset SPACK_SYSTEM_CONFIG_PATH
# ACTION: Edit the generated compiler config (site/compilers.yaml and/or the
# compiler entries in site/packages.yaml) with the following.
#   1) Keep a single gcc@13.3.0 spec (the system compiler installed above);
#      delete any empty or duplicate gcc specs. Redundant/empty specs cause
#      cryptic build errors later.
#   2) Delete or comment clang/llvm refs.

# Continue configuration.
spack config add "packages:all:prefer:['%gcc']"
spack config add "packages:all:providers:mpi:[openmpi@5.0.8]"
spack config add "packages:fontconfig:variants:+pic"
spack config add "packages:pixman:variants:+pic"
spack config add "packages:cairo:variants:+pic"
spack config add "packages:met:variants:+python +grib2 +graphics +lidar2nc +modis"
spack config add "packages:ewok-env:require:[+ecflow]"
# Pin py-netcdf4
spack config add "packages:py-netcdf4:require:[\"@1.7.2\"]"

# Concretize and install
spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i fms -i crtm -i crtm-fix -i esmf -i mapl -i py-cython
spack install --fail-fast -j 14 2>&1 | tee log.install

# Install modules
spack module lmod refresh
spack stack setup-meta-modules

# Add a number of default module locations to the lmod startup script.
cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/spack-stack/envs/unified-gcc/install/modulefiles/Core
EOF
```

</details>

<details>
<summary><b>Intel OneAPI Installation</b></summary>

#### Install Intel OneAPI Compiler

```bash
sudo su -

wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list
apt update
apt install intel-oneapi-compiler-dpcpp-cpp-2026.1 intel-oneapi-compiler-fortran-2026.1 intel-oneapi-mpi-devel-2021.18 intel-oneapi-tbb-devel-2023.1 intel-oneapi-mkl-devel-2026.1 -y

exit
```

#### Setup OneAPI Modules

```bash
sudo su -
# Create all modulefiles.
/opt/intel/oneapi/modulefiles-setup.sh --output-dir=/opt/intel/oneapi/modulefiles
module use /opt/intel/oneapi/modulefiles

# Add the oneapi module files to lmod init (confirm that this file does not exist)
cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/intel/oneapi/modulefiles
EOF

# Create combined module file. Note that the compiler modulefile has a "tcm"
# prerequisite; omitting it fails the load with "Cannot load module
# compiler/2026.1.1. At least one of these module(s) must be loaded: tcm".
mkdir /opt/intel/oneapi/modulefiles/intel-oneapi-full-env/
cat << 'EOF' >> /opt/intel/oneapi/modulefiles/intel-oneapi-full-env/2026.1.1
#%Module1.0
##
## intel-oneapi-full-env/2026.1.1
## Intel oneAPI full module environment

proc ModulesHelp { } {
    puts stderr "intel-oneapi-full-env defines the entire module set used for spack-stack intel builds"
}
module-whatis "intel-oneapi-full-env defines the entire module set used for spack-stack intel builds"
module load umf/1.1.0
module load tcm/1.5
module load tbb/2023.1
module load compiler-rt/2026.1.1
module load compiler/2026.1.1
module load mkl/2026.1
module load compiler-intel-llvm/2026.1.1
EOF
```

#### Install Intel OneAPI Spack-Stack Environment

The steps below are how this site config was generated. Note that the oneAPI
modules must **not** be loaded during `spack install` -- see "The module-load
trap" at the end of this section.

```bash
sudo su -

module load intel-oneapi-full-env/2026.1.1
export FC=ifx
export CXX=icpx
export CC=icx

cd /opt/spack-stack
source ./setup.sh

spack stack create env --site linux.default --template unified-dev --name unified-oneapi --compiler oneapi
cd envs/unified-oneapi
spack env activate -p .


# Find external packages for the site config.
unset SPACK_DISABLE_LOCAL_CONFIG
export SPACK_SYSTEM_CONFIG_PATH="$(pwd)/site"
spack external find --scope system --exclude bison --exclude openssl --exclude python --exclude gettext --exclude m4 --exclude cmake --exclude curl
spack external find --scope system wget
spack external find --scope system grep

# Here we are doing some manual configuration to address the
# following tricky situations
# - External find doesn't work well for pre-installed intel-oneapi-mpi
#   and we are using an external module load for this.
# - Disable "buildable" on all intel modules.
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  intel-oneapi-runtime:
    buildable: false
    externals:
    - spec: intel-oneapi-runtime@2026.1.1
      prefix: /opt/intel/oneapi
      modules:
      - compiler-rt/2026.1.1
  intel-oneapi-mkl:
    buildable: false
    externals:
    # No "modules:" here on purpose - see "The module-load trap" below.
    - spec: intel-oneapi-mkl@2026.1
      prefix: /opt/intel/oneapi
  intel-oneapi-mpi:
    buildable: false
    externals:
    - spec: intel-oneapi-mpi@2021.18
      prefix: /opt/intel/oneapi
      modules:
      - mpi/2021.18
  intel-oneapi-tbb:
    buildable: false
    externals:
    - spec: intel-oneapi-tbb@2023.1
      prefix: /opt/intel/oneapi
      modules:
      - tbb/2023.1
EOF

spack compiler find --scope system

# Edit site/packages.yaml
pico ${PWD}/site/packages.yaml
# Your intel compiler should look something like this below
# and any non-preferred GCC toolchains should be removed. Note
# that GCC should reference languages c, c++, but not fortran.
#
# NOTE! watch out for redundant empty gcc specs which will cause
# unintelligible build errors later. There should only be one spec
# under "externals:".
#
#   intel-oneapi-compilers:
#     buildable: false
#     externals:
#     - spec: intel-oneapi-compilers@2026.1.1
#       prefix: /opt/intel/oneapi
#       modules:
#       - umf/1.1.0
#       - tcm/1.5
#       - tbb/2023.1
#       - compiler-rt/2026.1.1
#       - compiler/2026.1.1
#       extra_attributes:
#         compilers:
#           c: /opt/intel/oneapi/compiler/2026.1/bin/icx
#           fortran: /opt/intel/oneapi/compiler/2026.1/bin/ifx
#           cxx: /opt/intel/oneapi/compiler/2026.1/bin/icpx
#   gcc:
#     buildable: false
#     externals:
#     - spec: gcc@13.3.0 languages:='c,c++,fortran'
#       ....

# Edit the spack.yaml to include these clauses. Note this must happen before
# SPACK_SYSTEM_CONFIG_PATH is unset, or it writes to /packages.yaml.
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
    all:
      prefer:
      - '%oneapi'
      conflict:
      - '%c=oneapi %fortran=gcc'
      - '%c,cxx=oneapi %fortran=gcc'
      - '%c=gcc %fortran=oneapi'
      - '%c,cxx=gcc %fortran=oneapi'
      - '%fortran=oneapi %c=gcc'
      - '%fortran=oneapi %c,cxx=gcc'
      - '%fortran=gcc %c,cxx=oneapi'
      - '%fortran=gcc %c=oneapi'
      providers:
        mpi: [intel-oneapi-mpi@2021.18]
    met:
      variants: +python +grib2 +graphics +lidar2nc +modis
    openmpi:
      buildable: false
    mpich:
      buildable: false
    py-scipy:
      require:
      #- '%c,cxx,fortran=gcc'
      - 'cxxflags="-O1"'
    jedi-base-env:
      require:
      - ~bufrquery
      - +fftw
      - +hdf4
    py-pyyaml:
      require:
      - +libyaml
EOF

export SPACK_DISABLE_LOCAL_CONFIG=true
unset SPACK_SYSTEM_CONFIG_PATH

# Purge the oneAPI modules before installing - see the trap below.
module purge

spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py
spack install --fail-fast -j 12 2>&1 | tee log.install
spack module lmod refresh && \
spack stack setup-meta-modules

cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/spack-stack/envs/unified-oneapi/install/modulefiles/Core
EOF
```

#### The module-load trap

Spack loads an external's `modules:` itself and treats a load that does not change
`LOADEDMODULES` as a failure. So any oneAPI module already loaded in your shell
makes `spack install` die with a misleading `ModuleLoadError` partway through.
Purge before installing, and let spack do the loading.

For the same reason no two externals may list the same module. That is why
`intel-oneapi-mkl` above has no `modules:`: it would load before the compilers
entry and miss its `tbb`/`compiler-rt` prereqs, but listing those on mkl collides
with the compilers entry. It needs neither -- the recipe sets `MKLROOT` from
`prefix`.

</details>

## Test Installation

<details>
<summary>GCC</summary>

```bash
# Example given for building jedi-bundle
module use /opt/spack-stack/envs/unified-gcc/install/modulefiles/Core
module load stack-gcc/13.3.0
module load stack-openmpi/5.0.8
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

mkdir ~/jedi
cd ~/jedi
git clone https://github.com/JCSDA-internal/jedi-bundle.git
cd jedi-bundle
mkdir build && cd build
ecbuild ../
make update
make -j10
ctest
```

</details>

<details>
<summary>Intel OneAPI</summary>

```bash
# Build jedi-bundle with oneapi
module use /opt/spack-stack/envs/unified-oneapi/install/modulefiles/Core
module load stack-intel-oneapi-compilers/2026.1.1
module load stack-intel-oneapi-mpi/2021.18
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

mkdir /opt/jedi
cd /opt/jedi
git clone https://github.com/JCSDA-internal/jedi-bundle.git
cd jedi-bundle
mkdir build && cd build
ecbuild ../
make update
make -j10 2>&1 | tee log.make
ctest
```

</details>

The installation and configuration is now complete for the instance.
