## spack-stack AMI (Ubuntu 24.04)

This document is to go over the the running and usage of this specific AMI for Ubuntu 24.04 LTS. This image has two environments: gnu (gcc-12.3), and intel (intel@2021.10.0). You can use either one of these environments for development purposes.

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
sudo git clone -b release/2.0 --depth 1 --recursive https://github.com/jcsda/spack-stack.git
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
sed -i "s/- '%gcc'/- '%gcc_toolchain'/" ./common/packages.yaml
spack stack create env --site linux.default --template unified-dev --name unified-gcc --compiler gcc
cd envs/unified-gcc
spack env activate -p .
unset SPACK_DISABLE_LOCAL_CONFIG
export SPACK_SYSTEM_CONFIG_PATH="$(pwd)/site"
spack external find --scope system \
    --exclude cmake \
    --exclude curl --exclude openssl \
    --exclude openssh --exclude python
spack external find --scope system wget
spack external find --scope system grep
spack compiler find --scope system
export SPACK_DISABLE_LOCAL_CONFIG=true
unset SPACK_SYSTEM_CONFIG_PATH
# ACTION: Edit the site/compilers.yaml with the following.
#   1) Delete or comment gcc-13 refs and preserve only gcc-12
#   2) Delete or comment clang refs.
# ACTION: Edit the site/packages.yaml and add these packages
# If not present.
cat << 'EOF' >> $PWD/site/packages.yaml
  gcc:
    buildable: false
    externals:
    - spec: gcc@11.4.0
      prefix: /usr
  qt:
    buildable: false
    externals:
    - spec: qt@5.15.3
      prefix: /usr
      version: [5.15.3]
EOF

# Continue configuration.
spack config add "packages:all:prefer:['%gcc']"
spack config add "packages:all:providers:mpi:[openmpi@5.0.8]"
spack config add "packages:fontconfig:variants:+pic"
spack config add "packages:pixman:variants:+pic"
spack config add "packages:cairo:variants:+pic"
spack config add "packages:met:variants:+python +grib2 +graphics +lidar2nc +modis"

# Concretize and install
spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i fms -i crtm -i crtm-fix -i esmf -i mapl -i py-cython
spack install --fail-fast -j 14 2>&1 | tee log.install

# Install modules
spack module lmod refresh
spack stack setup-meta-modules

# Add a number of default module locations to the lmod startup script.
cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/spack-stack/envs/unified-env-gcc/install/modulefiles/Core
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
apt install intel-oneapi-compiler-dpcpp-cpp-2025.3 intel-oneapi-compiler-fortran-2025.3 intel-oneapi-mpi-devel-2021.17 intel-oneapi-tbb-devel-2022.3 intel-oneapi-mkl-devel-2025.3 -y

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

# Create combined module file.
mkdir /opt/intel/oneapi/modulefiles/intel-oneapi-full-env/
cat << 'EOF' >> /opt/intel/oneapi/modulefiles/intel-oneapi-full-env/2025.3.0
#%Module1.0
##
## intel-oneapi-full-env/2025.3.0
## Intel oneAPI full module environment

proc ModulesHelp { } {
    puts stderr "intel-oneapi-full-env defines the entire module set used for spack-stack intel builds"
}
module-whatis "intel-oneapi-full-env defines the entire module set used for spack-stack intel builds"
module load umf/1.0.2
module load tbb/2022.3
module load compiler-rt/2025.3.0
module load compiler/2025.3.0
module load mkl/2025.3
module load compiler-intel-llvm/2025.3.0
EOF
```

#### Install Intel OneAPI Spack-Stack Environment

```bash
sudo su -

module load intel-oneapi-full-env/2025.3.0
export FC=ifx
export CXX=icpx
export CC=icx

cd /opt/spack-stack
source ./setup.sh

spack stack create env --site linux.default --template unified-dev --name unified-oneapi --compiler oneapi
cd envs/unified-oneapi
spack env activate -p .


# Before finding packages you need to go into ./common/packages.yaml
# and comment out gmake requirements to prevent gmake from being
# over-constrained.
#   pico ./common/packages.yaml
# Near the top of the file find and comment out these three lines.
#  gmake:
#    require:
#    - '%gcc'


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
  intel-oneapi-mkl:
    buildable: false
    externals:
    - spec: intel-oneapi-mkl@2025.3
      prefix: /opt/intel/oneapi
      modules:
      - mkl/2025.3
  intel-oneapi-mpi:
    buildable: false
    externals:
    - spec: intel-oneapi-mpi@2021.17
      prefix: /opt/intel/oneapi
      modules:
      - mpi/2021.17
  intel-oneapi-tbb:
    buildable: false
    externals:
    - spec: intel-oneapi-tbb@2022.3
      prefix: /opt/intel/oneapi
      modules:
      - tbb/2022.3
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
#     - spec: intel-oneapi-compilers@2025.3.0
#       prefix: /opt/intel/oneapi
#       modules:
#       - umf/1.0.2
#       - tbb/2022.3
#       - compiler-rt/2025.3.0
#       - compiler/2025.3.0
#       extra_attributes:
#         compilers:
#           c: /opt/intel/oneapi/compiler/2025.3/bin/icx
#           fortran: /opt/intel/oneapi/compiler/2025.3/bin/ifx
#           cxx: /opt/intel/oneapi/compiler/2025.3/bin/icpx
#   gcc:
#     buildable: false
#     externals:
#     - spec: gcc@13.3.0 languages:='c,c++,fortran'
#       ....

export SPACK_DISABLE_LOCAL_CONFIG=true
unset SPACK_SYSTEM_CONFIG_PATH

# Edit the spack.yaml to include these clauses.
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
        mpi: [intel-oneapi-mpi@2021.17]
    met:
      variants: +python +grib2 +graphics +lidar2nc +modis
    mpi:
      buildable: false
      require:
      - intel-oneapi-mpi@2021.17
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

spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py
spack install --fail-fast -j 12 2>&1 | tee log.install
spack module lmod refresh
spack stack setup-meta-modules

cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/spack-stack/envs/unified-env-oneapi/install/modulefiles/Core
EOF
```

</details>

## Test Installation

<details>
<summary>GCC</summary>

```bash
# Example given for building jedi-bundle
module use /opt/spack-stack/envs/unified-dev-gcc/install/modulefiles/Core
module load stack-gcc/11.4.0
module load stack-openmpi/5.0.5
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
module use /opt/spack-stack/envs/unified-env-oneapi/install/modulefiles/Core
module load stack-intel-oneapi-compilers/2025.3.0
module load stack-intel-oneapi-mpi/2021.17
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
make -j10
ctest
```

</details>

The installation and configuration is now complete for the instance.
