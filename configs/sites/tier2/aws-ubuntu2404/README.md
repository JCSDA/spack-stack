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
   --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"ubuntu2404-spack-stack-gcc-intel"},{"Key":"User","Value":$(whoami)}]}' \
   --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
   --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":false,"EnableResourceNameDnsAAAARecord":false}' \
   --count "1" 
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
* 300GB of gp3 storage as /

## Pre-requisites (For All Compilers)

### Installing Packages

```bash
# Update system software and start a tmux session.
sudo su -
apt update
apt upgrade

# Build tools
apt install -y build-essential g++-11 gcc-11 gfortran-11 make cmake automake autoconf

#Install other requirements.
apt install -y cpp-11 libgomp1 git git-lfs autopoint mysql-server libmysqlclient-dev qtbase5-dev qt5-qmake libqt5svg5-dev qt5dxcb-plugin wget curl file tcl-dev gnupg2 iproute2 locales unzip less bzip2 gettext libtree pkg-config libcurl4-openssl-dev

# Editors
apt install -y vim nano 

# Python develop.
apt install -y python3 python3-pip python3-setuptools

# Configure git credential caching and git lfs for the rocky user and root.
git config --global credential.helper 'cache --timeout=3600'
git lfs install

# Change the gcc, g++, and gfortran version to 11 and give it the highest priority
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100
update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-11 100

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

### Setup MySQL Sercer

```bash
sudo systemctl start mysqld.service
sudo systemctl enable mysqld

# Use the mysql server.
mysql -u root
exit
```

### Clone `spack-stack`

```bash
cd /opt
sudo git clone -b develop --depth 1 --recursive https://github.com/jcsda/spack-stack.git
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
spack stack create env --site linux.default --template unified-dev --name unified-env-gcc --compiler gcc
cd envs/unified-env-gcc 
spack env activate -p .
export SPACK_SYSTEM_CONFIG_PATH="$PWD/site"
spack external find --scope system \
    --exclude cmake \
    --exclude curl --exclude openssl \
    --exclude openssh --exclude python
spack external find --scope system wget
spack external find --scope system mysql
spack external find --scope system grep
spack compiler find --scope system
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
  gcc-runtime:
    buildable: false
    externals:
    - spec: gcc-runtime@11.4.0
      prefix: /usr
  qt:
    buildable: false
    externals:
    - spec: qt@5.15.3
      prefix: /usr
      version: [5.15.3]
EOF

# Continue configuration.
spack config add "packages:all:compiler:[gcc@11.4.0]"
spack config add "packages:all:providers:mpi:[openmpi@5.0.5]"
spack config add "packages:fontconfig:variants:+pic"
spack config add "packages:pixman:variants:+pic"
spack config add "packages:cairo:variants:+pic"
spack config add "packages:ewok-env:variants:+mysql"

# Concretize and install
spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d -c log.concretize
spack install --verbose --fail-fast 2>&1 | tee log.install

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
<summary><b>Intel Installation</b></summary>

#### Install Intel Compiler

```bash
sudo su -

mkdir -p /opt/intel/src
pushd /opt/intel/src

# Download Intel install assets.
wget -O cpp-compiler.sh https://registrationcenter-download.intel.com/akdlm/IRC_NAS/d85fbeee-44ec-480a-ba2f-13831bac75f7/l_dpcpp-cpp-compiler_p_2023.2.3.12_offline.sh
wget -O fortran-compiler.sh https://registrationcenter-download.intel.com/akdlm/IRC_NAS/0ceccee5-353c-4fd2-a0cc-0aecb7492f87/l_fortran-compiler_p_2023.2.3.13_offline.sh
wget -O tbb.sh https://registrationcenter-download.intel.com/akdlm/IRC_NAS/c95cd995-586b-4688-b7e8-2d4485a1b5bf/l_tbb_oneapi_p_2021.10.0.49543_offline.sh
wget -O mpi.sh https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4f5871da-0533-4f62-b563-905edfb2e9b7/l_mpi_oneapi_p_2021.10.0.49374_offline.sh
wget -O math.sh https://registrationcenter-download.intel.com/akdlm/IRC_NAS/adb8a02c-4ee7-4882-97d6-a524150da358/l_onemkl_p_2023.2.0.49497_offline.sh

# Install the Intel assets.
sh cpp-compiler.sh -a --silent --eula accept 2>&1 | tee install.cpp-compiler.log
sh fortran-compiler.sh -a --silent --eula accept | tee install.fortran-compiler.log
sh tbb.sh -a --silent --eula accept | tee install.tbb.log
sh mpi.sh -a --silent --eula accept | tee install.mpi.log
sh math.sh -a --silent --eula accept | tee install.math.log

popd
exit
```

#### Install Intel Spack-Stack Environment

```bash
sudo su -

source /opt/intel/oneapi/compiler/2023.2.3/env/vars.sh
source /opt/intel/oneapi/mpi/2021.10.0/env/vars.sh
source /opt/intel/oneapi/setvars.sh

cd /opt/spack-stack
source ./setup.sh

spack stack create env --site linux.default --template unified-dev --name unified-env-intel --compiler intel
cd envs/unified-env-intel
spack env activate -p .

export SPACK_SYSTEM_CONFIG_PATH="${PWD}/site"

spack external find --scope system --exclude bison --exclude openssl --exclude python --exclude gettext --exclude m4 --exclude cmake --exclude curl
spack external find --scope system perl
spack external find --scope system wget
spack external find --scope system texlive
spack external find --scope system mysql
spack external find --scope system grep

# No external find for pre-installed intel-oneapi-mpi,
# and no way to add object entry to list using "spack config add".
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  gcc:
    buildable: false
    externals:
    - spec: gcc@11.4.0
      prefix: /usr
  gcc-runtime:
    buildable: false
    externals:
    - spec: gcc-runtime@11.4.0
      prefix: /usr
  grep:
    buildable: False
    externals:
    - spec: grep@3.11
      prefix: /usr
  intel-oneapi-mpi:
    externals:
    - spec: intel-oneapi-mpi@2021.10.0%intel@2021.10.0 +classic-names
      prefix: /opt/intel/oneapi
EOF

# Can't find qt5 because qtpluginfo is broken,
# and no way to add object entry to list using "spack config add".
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  qt:
    buildable: false
    externals:
    - spec: qt@5.15.3
      prefix: /usr
EOF

spack compiler find --scope system

unset SPACK_SYSTEM_CONFIG_PATH

spack config add "packages:mpi:buildable:False"
spack config add "packages:all:providers:mpi:[intel-oneapi-mpi@2021.10.0]"
spack config add "packages:all:compiler:[intel@2021.10.0, gcc@11.4.0]"

# edit envs/unified-env/site/compilers.yaml and replace the following line in the **Intel** compiler section:
#     environment: {}
# -->
#     environment:
#       prepend_path:
#         LD_LIBRARY_PATH: '/opt/intel/oneapi/compiler/2023.2.3/linux/compiler/lib/intel64_lin'

spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d log.concretize
spack install --fail-fast -j 12 2>&1 | tee log.install
spack module lmod refresh
spack stack setup-meta-modules

cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/spack-stack/envs/unified-env-gcc/install/modulefiles/Core
EOF
```

</details>

## Test Installation

<details>
<summary>GCC</summary>

```bash
# Example given for building jedi-bundle
module use /opt/spack-stack/envs/unified-dev-gcc/install/modulefiles/Core
module load stack-gcc/12.3.0
module load stack-openmpi/5.0.5
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

<details>
<summary>Intel</summary>

```bash
# Example given for building jedi-bundle
module use /opt/spack-stack/envs/unified-env-intel/install/modulefiles/Core
module load stack-intel/2021.10.0
module load stack-intel-oneapi-mpi/2021.10.0
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

# (Optional) Re-source the intel environment
source /opt/intel/oneapi/setvars.sh

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
