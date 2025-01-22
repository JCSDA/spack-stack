## spack-stack AMI (Rocky8)

This document is to go over the the running and usage of this specific AMI for Rocky8. This image has two environments: gnu (gcc-11.2), and intel (intel@2021.10.0). You can use either one of these environments for development purposes.

### Using the AMI

Here is an example `aws cli` command-line to run this AMI with your designated key-pair.

```bash
aws ec2 run-instances \
   --image-id "ami-02391db2758465a87" --instance-type "m6i.4xlarge" \
   --key-name YOUR-KEYPAIR \
   --block-device-mappings '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"Iops":3000,"SnapshotId":"snap-05fb00e35af5550e7","VolumeSize":150,"VolumeType":"gp3","Throughput":125}}' \
   --network-interfaces '{"SubnetId":"subnet-00575f6b8ccc2005d","AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-0436b207bc220df08"]}' \
   --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"rocky8-spack-stack-gcc-intel"},{"Key":"User","Value":$(whoami)}]}' \
   --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
   --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":false,"EnableResourceNameDnsAAAARecord":false}' \
   --count "1" 
```

## Using this Site Config

JCSDA publishes a fully configured and built installation of spack stack derived
from this config as an Amazon Machine Images (AMI). The easiest way to use this
configuration of spack stack is to launch a VM using that AMI. The instructions
below are included for maintainance of the history of this site config and
their possible relevance to debugging issues should they arise.

### Base Instance

This AMI was built on an instance with these properties:

* AMI Name: Rocky-8-EC2-Base-8.9-20231119.0.x86_64-d6577ceb-8ea8-4e0e-84c6-f098fc302e82
* AMI ID: ami-02391db2758465a87
* Instance m6i.4xlarge  (uses Intel Xeon processor)
* 300GB of gp3 storage as /

## Pre-requisites (For All Compilers)

<details>
<summary>Tmux Usage</summary>

### Tmux

Rocky 8 doesn't have screen so here's a guide to tmux.

```bash
# Start a session
tmux new -s my-session-name

# Detach from a session
ctr-b d

# list sessions
tmux ls

# Attach to existing session
tmux attach -t my-session-name
```

More information on how to use `tmux`: <https://tmuxcheatsheet.com/>

</details>

### Installing Packages

```bash
# Update system software and start a tmux session.
sudo dnf -y update
sudo dnf -y install tmux
tmux new -s setup
sudo su -

# Compilers
dnf install gcc-toolset-11-gcc-c++ \
        gcc-toolset-11-gcc-gfortran \
        gcc-toolset-11-gdb

#Install other requirements.
dnf install binutils-devel \
        m4 \
        wget \
        git \
        git-lfs \
        bash-completion \
        bzip2 bzip2-devel \
        libcurl libcurl-devel \
        unzip \
        patch \
        automake \
        xorg-x11-xauth \
        xterm \
        perl-IPC-Cmd \
        pearl-core \
        gettext-devel \
        texlive \
        tcl-devel \
        nano \
        vim \
        bison \
        qt5-qtbase \
        qt5-qtbase-devel \
        qt5-qtsvg \
        qt5-qtsvg-devel \
        autoconf2.7x \
        libxml2 libxml2-devel

# Python develop.
dnf install python3-devel

# Enable gcc toolset. This is needed for later builds. Once lmod is installed
# this will be configured as a pass-through module.
scl enable gcc-toolset-11 bash

# Configure git credential caching and git lfs for the rocky user and root.
git config --global credential.helper 'cache --timeout=3600'
git lfs install

# Configure x11 forwarding.
echo "X11Forwarding yes" >> /etc/ssh/sshd_config
service sshd restart
```

### Install MySQL Community Server

```bash
dnf config-manager --set-enabled crb

dnf install mysql-server mysql-devel
sudo systemctl start mysqld.service
sudo systemctl enable mysqld

# Use the mysql server.
mysql -u root
exit
```

### Install Lmod

```bash
# Enable gcc using system module
scl enable gcc-toolset-11 bash

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

# Add custom module for system gcc
cat << 'EOF' >> /opt/rh/gcc-toolset-11/gcc-toolset.lua
--%Module
family("compiler")
help([[Wrapper module for gcc-toolset-11 using Software Collections]])
whatis("Description: GCC Toolset 11")

-- Execute 'scl enable' to load gcc-toolset-11 environment
execute {cmd="scl enable gcc-toolset-11 bash", modeA={"load"}}
EOF

# Add a number of default module locations to the lmod startup script.
cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/rh/gcc-toolset-11
EOF

# Log out completely, ssh back into the instance and check if lua modules work
exit
exit
```

### Clone `spack-stack`

```bash
# if in sudo su -
cd /opt
git clone -b develop --recursive https://github.com/jcsda/spack-stack.git
```

## Install Steps by Compiler

<details>
<summary><b>GCC Installation</b></summary>

```bash
sudo su -

cd /opt/spack-stack
source setup.sh

scl enable gcc-toolset-11 bash

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

# ACTION: Edit the site/packages.yaml and add these packages
# If not present.
cat << 'EOF' >> $PWD/site/packages.yaml
  gcc:
    buildable: false
    externals:
    - spec: gcc@11.2.1
      prefix: /usr
  gcc-runtime:
    buildable: false
    externals:
    - spec: gcc-runtime@11.2.1
      prefix: /usr
  qt:
    buildable: false
    externals:
    - spec: qt@5.15.3
      prefix: /usr
      version: [5.15.3]
EOF

# Continue configuration.
spack config add "packages:all:compiler:[gcc@11.2.1]"
spack config add "packages:all:providers:mpi:[openmpi@5.0.5]"
spack config add "packages:fontconfig:variants:+pic"
spack config add "packages:pixman:variants:+pic"
spack config add "packages:cairo:variants:+pic"
spack config add "packages:ewok-env:variants:+mysql"

# Concretize and install
spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d -c log.concretize
spack install --fail-fast -j 16 2>&1 | tee log.install

# Install modules
spack module lmod refresh
spack stack setup-meta-modules

cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/spack-stack/envs/unified-env-gcc/install/modulefiles/Core
EOF
```

</details>

<details>
<summary><b>Intel Installation</b></summary>

#### Install Intel Compiler

```bash
rm -rf /opt/intel
rm -rf /var/intel

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
```

#### Create Intel Environment
```bash
tmux -s intel
sudo su -
module load gcc-toolset

source /opt/intel/oneapi/compiler/2023.2.3/env/vars.sh
source /opt/intel/oneapi/mpi/2021.10.0/env/vars.sh
source /opt/intel/oneapi/setvars.sh

cd /opt/spack-stack
source ./setup.sh

spack stack create env --site linux.default --template unified-dev --name unified-env-intel --compiler intel
cd envs/unified-env-intel
spack env activate -p .

export SPACK_SYSTEM_CONFIG_PATH="${PWD}/site"

spack external find --scope system --exclude python --exclude curl
spack external find --scope system perl
spack external find --scope system wget
spack external find --scope system texlive
spack external find --scope system mysql
spack external find --scope system grep

# No external find for pre-installed intel-oneapi-mpi (from pcluster AMI),
# and no way to add object entry to list using "spack config add".
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  intel-oneapi-mpi:
    buildable: false
    externals:
    - spec: intel-oneapi-mpi@2021.10.0%intel@2021.10.0
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

export -n SPACK_SYSTEM_CONFIG_PATH

# spack config add "packages:mpi:buildable:False"
spack config add "packages:all:providers:mpi:[intel-oneapi-mpi@2021.10.0]"
spack config add "packages:all:compiler:[intel@2021.10.0, gcc@11.2.1]"

# Edit envs/unified-intel/spack.yaml.
# 1) Find this line:
#      compilers: ['%aocc', '%apple-clang', '%gcc', '%intel']
# 2) Delete all compilers except for your target compiler. In the case of intel
#    the line should look like this:
#      compilers: ['%intel']

# edit envs/unified-env/site/compilers.yaml and replace the following line in the **Intel** compiler section:
#     environment: {}
# -->
#     environment:
#       prepend_path:
#         PATH: /opt/rh/gcc-toolset-11/root/usr/bin
#         LD_LIBRARY_PATH: '/opt/intel/oneapi/compiler/2023.2.3/linux/compiler/lib/intel64_lin:/usr/lib:/usr/lib64'
#         CPATH: /opt/rh/gcc-toolset-11/root/usr/include

spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d log.concretize
spack install -j 12 --verbose 2>&1 | tee log.install
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
module load stack-gcc/11.2.1
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
module use /opt/spack-stack/envs/unified-dev-intel/install/modulefiles/Core
module load stack-intel/2021.10.0
module load stack-intel-oneapi-mpi/2021.10.0
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

**Note**: If the `make -j10` shows any errors, re-run it and it should be successful.

</details>

The installation and configuration is now complete for the instance.
