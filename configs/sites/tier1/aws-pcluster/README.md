## spack-stack on AWS parallelcluster using Intel+Intel-MPI

**Note.** These instructions were used to create this site config. These steps are **not** necessary when building ``spack-stack`` - simply use the existing site config in this directory.

### Base instance
Installing spack-stack on Parallel Cluster requires a number of modifications to
the base Parallel Cluster AMI. You will need to start with a basic PCluster AMI
from the Community AMIs tab that matches your desired OS and PCluster version.
Select an instance type of the same family that you are planning to use for the
head and the compute nodes, and specify enough enough storage for a swap file
and a spack-stack installation.
- AMI Name: aws-parallelcluster-3.9.3-ubuntu-2204-lts-hvm-x86_64
- AMI ID: ami-08e88679103d6ab5f
- Instance r7a.4xlarge  (uses same processor architecture as hpc7a instances)
- Use 300GB of gp3 storage as /
- Attach security groups allowing ssh inbound traffic and NFS outbound traffic

The following command can be used to launch a build instance. In the command
make sure to use your own subnet ID and add appropriate security groups for SSH
and NFS access.

```
aws ec2 run-instances \
    --image-id ami-08e88679103d6ab5f \
    --count 1 \
    --instance-type r7a.4xlarge \
    --key-name YOUR-KEY-NAME \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=pcluster-ami-builder}]' \
    --subnet-id subnet-061b48f9950e18a0a \
    --security-group-ids sg-0091fa8e748fbe355 sg-014f295418636207d \
    --region us-east-2 \
    --block-device-mappings '[
        {
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "VolumeSize": 300,
                "VolumeType": "gp3",
                "Iops": 3000
            }
        }
    ]'
```

Once the instance is running you may want to mount the Elastic File System NFS
drive if you intend to install spack stack in this location. You can follow this
procedure to mount your dive.

```
EFS_MOUNT_POINT=/mnt/experiments-efs
EFS_ID=fs-064ec823dfe12d3d4
EFS_ZONE=us-east-2
mkdir -p "${EFS_MOUNT_POINT}"

apt-get update
apt-get -y install nfs-common

mount -t nfs4 \
    -o  nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport \
    ${EFS_ID}.efs.${EFS_ZONE}.amazonaws.com:/ \
    ${EFS_MOUNT_POINT}
echo ${EFS_ID}.efs.${EFS_ZONE}.amazonaws.com:/ $EFS_MOUNT_POINT nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0 >> /etc/fstab
```

### Installing Prerequisites

1. Install apt build prerequisites
```
# Initialize apt and update system
sudo su -
apt -y update
apt -y upgrade

# Install core dependencies
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    git \
    git-lfs \
    bzip2 \
    unzip \
    python3 \
    python3-pip \
    tcl-dev \
    nano
sudo -u ubuntu git lfs install
sudo -u ubuntu git config --global credential.helper 'cache --timeout=3600'


# Install compilers and various dev dependencies.
apt install -y \
    gcc \
    g++ \
    gfortran \
    gdb \
    build-essential \
    libkrb5-dev \
    m4 \
    apt-utils \
    automake \
    cmake \
    xterm \
    autopoint \
    texlive \
    gettext \
    meson \
    libcurl4-openssl-dev \
    libssl-dev \
    mysql-server \
    libmysqlclient-dev \
    libmysqlclient21 \
    python3-dev

# Additional external dependencies for Intel spack builds.
apt install -y \
    liblcms2-dev \
    liblcms2-2

# Install QT5 for ecflow
apt install -y \
    qtcreator \
    qtbase5-dev \
    qt5-qmake \
    libqt5svg5-dev \
    qt5dxcb-plugin

# This is because boost doesn't work with the Intel compiler
apt install -y \
    libboost1.74-dev \
    libboost-chrono1.74-dev \
    libboost-date-time1.74-dev \
    libboost-exception1.74-dev \
    libboost-filesystem1.74-dev \
    libboost-program-options1.74-dev \
    libboost-python1.74-dev \
    libboost-regex1.74-dev \
    libboost-serialization1.74-dev \
    libboost-system1.74-dev \
    libboost-test1.74-dev \
    libboost-thread1.74-dev \
    libboost-timer1.74-dev

# Configure X windows
echo "X11Forwarding yes" >> /etc/ssh/sshd_config
service sshd restart

# Bug fixes for libraries/headers expected in standard locations
cd /usr/lib64/
ln -sf /usr/lib/x86_64-linux-gnu/libcrypt.so .
cd /usr/include
ln -sf python3.10/pyconfig.h .

# Create swapfile - 100GB
dd if=/dev/zero of=/swapfile bs=128M count=800
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
swapon -s
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
```



2. The PCluster base image includes the Intel MPI library but does not include
the Intel compiler toolchain. Installing the Intel compiler toolchain with apt
shuffles the `/opt/intel` directory badly and places the libraries and tools in
nonstandard locations due to conflicts with the installed MPI library. The
following instructions are used to clear the existing Intel MPI and install a
clean and unified Intel toolchain.

```
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


3. Install docker
```
# Docker
# See https://docs.docker.com/engine/install/ubuntu/
apt-get update
apt-get install ca-certificates curl gnupg lsb-release
mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt install -y docker-ce \
    docker-ce-cli containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin
docker run hello-world
sudo usermod -aG docker $USER
# DH* TODO 2023/02/21: Add users to group docker so that non-root users can run it
# See https://docs.docker.com/engine/install/linux-postinstall/

# Exit root session
exit
```

4. Build ecflow outside of spack to be able to link against OS boost
```
mkdir -p /home/ubuntu/jedi/ecflow-5.8.4/src
cd /home/ubuntu/jedi/ecflow-5.8.4/src
wget -O ecFlow-5.8.4-Source.tar.gz \
     https://github.com/ecmwf/ecflow/releases/download/-5.8.4/ecFlow-5.8.4-Source.tar.gz
tar -xvzf ecFlow-5.8.4-Source.tar.gz
export WK=/home/ubuntu/jedi/ecflow-5.8.4/src/ecFlow-5.8.4-Source
export BOOST_ROOT=/usr

# Build ecFlow
cd $WK
mkdir build
cd build
cmake .. -DPython3_EXECUTABLE=/usr/bin/python3 -DENABLE_STATIC_BOOST_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/home/ubuntu/jedi/ecflow-5.8.4 2>&1 | tee log.cmake
make -j10 2>&1 | tee log.make
make install 2>&1 | tee log.install

# Create a modulefiles directory and the "ecflow/5.8.4" module file.
mkdir -p /home/ubuntu/jedi/modulefiles/ecflow

cat << 'EOF' > /home/ubuntu/jedi/modulefiles/ecflow/5.8.4
#%Module1.0

module-whatis "Provides an ecflow-5.8.4 server+ui installation for use with spack."

conflict ecflow

proc ModulesHelp { } {
puts stderr "Provides an ecflow-5.8.4 server+ui installation for use with spack."
}

# Set this value
set ECFLOW_PATH "/home/ubuntu/jedi/ecflow-5.8.4"

prepend-path PATH "${ECFLOW_PATH}/bin"
prepend-path LD_LIBRARY_PATH "${ECFLOW_PATH}/lib"
prepend-path LIBRARY_PATH "${ECFLOW_PATH}/lib"
prepend-path CPATH "${ECFLOW_PATH}/include"
prepend-path CMAKE_PREFIX_PATH "${ECFLOW_PATH}"
prepend-path PYTHONPATH "${ECFLOW_PATH}/lib/python3.10/site-packages"
EOF

```

5. Install lmod. This step must be done as `root`.
```
# Install lua/lmod manually because apt only has older versions
# that are not compatible with the modern lua modules spack produces
# https://lmod.readthedocs.io/en/latest/030_installing.html#install-lua-x-y-z-tar-gz
sudo su -
mkdir -p /opt/lua/5.1.4.9/src
cd /opt/lua/5.1.4.9/src
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


# Add custom module locations and fix existing modules

# Update the Intel MPI module to load AWS libfabric.
cat << 'EOF' >> /opt/intel/oneapi/mpi/2021.10.0/modulefiles/mpi
conflict openmpi
if { [ module-info mode load ] && ![ is-loaded libfabric-aws/1.19.0amzn4.0 ] } {
    module load libfabric-aws/1.19.0amzn4.0
}
EOF

# Update the AWS OpenMPI module to load AWS libfabric.
cat << 'EOF' >> /opt/amazon/modules/modulefiles/openmpi/4.1.6
conflict mpi
if { [ module-info mode load ] && ![ is-loaded libfabric-aws/1.19.0amzn4.0 ] } {
    module load libfabric-aws/1.19.0amzn4.0
}
EOF

# Add a number of default module locations to the lmod startup script.
cat << 'EOF' >> /etc/profile.d/z01_lmod.sh
module use /opt/amazon/modules/modulefiles
module use /usr/share/modules/modulefiles
module use /opt/intel/oneapi/mpi/2021.10.0/modulefiles
module use /home/ubuntu/jedi/modulefiles
EOF

# Log out completely, ssh back into the instance and check if lua modules work
exit
exit

ssh ...
# Now user ubuntu
module av
module load libfabric-aws/1.19.0amzn4.0
module load openmpi/4.1.6
module list
module unload openmpi/4.1.6
module load mpi
module list
module purge
module list
```

6. Install msql community server
```
cd /home/ubuntu/jedi
mkdir -p mysql-8.0.31/src
cd mysql-8.0.31/src
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-server_8.0.32-1ubuntu20.04_amd64.deb-bundle.tar
tar -xvf mysql-server_8.0.32-1ubuntu20.04_amd64.deb-bundle.tar
# Switch to root
sudo su
dpkg -i *.deb
apt --fix-broken install
dpkg -i *.deb
# Use an empty password for root, choose legacy authentication method; test connection
mysql -u root
show databases;
# exit mysql
exit
# exit root session
exit
rm *.deb
```

7. Option 1: Testing existing site config in spack-stack (skip steps
8-9 afterwards) this install is done directly on the NFS drive. If you are
testing an update to the configuration, do this on the faster EBS volume (use a
directory in /home/ubuntu) in order to ensure a faster build. Once you have
a verified working spack-stack install you can install it on EFS.

Note: The instructions below focus on the Intel toolchain because it is harder
to build and has some performance benefits over the GNU toolchain, but the
submitted site config can also be used to build the gnu toolchain

```
cd /mnt/experiments-efs
git clone --recurse-submodules -b release/1.7.0 https://github.com/JCSDA/spack-stack.git spack-stack-1.7
cd spack-stack-1.7/
. setup.sh
spack stack create env --site aws-pcluster --template=unified-dev --name=unified-intel
cd envs/unified-intel
spack env activate -p .

# Edit envs/unified-intel/spack.yaml.
# 1) Find this line:
#      compilers: ['%aocc', '%apple-clang', '%gcc', '%intel']
# 2) Delete all compilers except for your target compiler. In the case of intel
#    the line should look like this:
#      compilers: [%intel']

spack concretize 2>&1 | tee log.concretize.001
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d log.concretize.001
spack install -j 12 --verbose 2>&1 | tee log.install.001
spack module lmod refresh
spack stack setup-meta-modules
```

8. Option 2: Test configuring site from scratch
```
mkdir -p /home/ubuntu/jedi && cd /home/ubuntu/jedi
git clone -b develop --recursive https://github.com/jcsda/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site linux.default --template=unified-dev --name=unified-env
spack env activate -p envs/unified-env

export SPACK_SYSTEM_CONFIG_PATH=/home/ubuntu/jedi/spack-stack/envs/unified-env/site

spack external find --scope system
spack external find --scope system perl
spack external find --scope system python
spack external find --scope system wget
spack external find --scope system texlive
spack external find --scope system mysql

# No external find for pre-installed intel-oneapi-mpi (from pcluster AMI),
# and no way to add object entry to list using "spack config add".
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  intel-oneapi-mpi:
    externals:
    - spec: intel-oneapi-mpi@2021.10.0%intel@2022.1.0
      prefix: /opt/intel
      modules:
      - libfabric-aws/1.19.0amzn4.0
      - intelmpi
EOF

# Add external openmpi
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  openmpi:
    externals:
    - spec: openmpi@4.1.6%gcc@9.4.0~cuda~cxx~cxx_exceptions~java~memchecker+pmi~static~wrapper-rpath
        fabrics=ofi schedulers=slurm
      prefix: /opt/amazon/openmpi
      modules:
      - libfabric-aws/1.19.0amzn4.0
      - openmpi/4.1.6
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

# Add external ecflow
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  ecflow:
    buildable: False
    externals:
    - spec: ecflow@5.8.4 +ui
      prefix: /home/ubuntu/jedi/ecflow-5.8.4
EOF

spack compiler find --scope system

export -n SPACK_SYSTEM_CONFIG_PATH

spack config add "packages:mpi:buildable:False"
spack config add "packages:python:buildable:False"
spack config add "packages:openssl:buildable:False"
spack config add "packages:all:providers:mpi:[intel-oneapi-mpi@2021.10.0, openmpi@4.1.6]"
spack config add "packages:all:compiler:[intel@2021.10.0, gcc@11.4.0]"

# edit envs/unified-env/site/compilers.yaml and replace the following line in the **Intel** compiler section:
#     environment: {}
# -->
#     environment:
#       prepend_path:
#         LD_LIBRARY_PATH: '/opt/intel/oneapi/compiler/2023.2.3/linux/compiler/lib/intel64_lin'
#       set:
#         I_MPI_PMI_LIBRARY: '/opt/slurm/lib/libpmi.so'
```

9. Option 2: To avoid duplicate library versions edit ``envs/unified-dev/site/packages.yaml``
and remove entries for meson, ninja, hdf5, cmake and remove the external
`cmake` and `openssl` entries.


10. Concretize and install
```
spack concretize 2>&1 | tee log.concretize.unified-env.001
./util/show_duplicate_packages.py -d log.concretize.unified-env.001
spack install --verbose 2>&1 | tee log.install.unified-env.001
spack module lmod refresh
spack stack setup-meta-modules
```

11. Test spack-stack installation using your favorite application.

```
# Example given for building jedi-bundle
module use /mnt/experiments-efs/spack-stack-1.7/envs/unified-intel/install/modulefiles/Core
module load stack-gcc/11.4.0
module load stack-openmpi/4.1.6
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

git clone https://github.com/JCSDA-internal/jedi-bundle.git
cd jedi-bundle
mkdir build && cd build
ecbuild ../
make update
make -j10
ctest
```

12. (Optional) Remove test installs of spack-stack environments, if desired.

13. Create the AMI for use in the AWS parallelcluster config. You can follow
the official instructions for [Modifying an AWS ParallelCluster AMI](https://docs.aws.amazon.com/parallelcluster/latest/ug/building-custom-ami-v3.html#modify-an-aws-parallelcluster-ami-v3)

14. Use the install to build

```
# Load the intel toolchain into your environment.
source /opt/intel/oneapi/compiler/2023.2.3/env/vars.sh
source /opt/intel/oneapi/mpi/2021.10.0/env/vars.sh

# Activate spack stack modules.
module use /mnt/experiments-efs/spack-stack-1.7/envs/unified-intel/install/modulefiles/Core
module use $HOME/spack-stack-1.7/envs/unified-intel/install/modulefiles/Core
module load stack-intel/2021.10.0
module load stack-intel-oneapi-mpi/2021.10.0
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

# Build and test.
git clone https://github.com/JCSDA-internal/jedi-bundle.git
cd jedi-bundle
mkdir build && cd build
ecbuild -DCMAKE_CXX_COMPILER=mpiicpc \
    -DCMAKE_C_COMPILER=mpiicc \
    -DCMAKE_Fortran_COMPILER=mpiifort \
    ../
make update
make -j10
ctest
```

15. Once the parallel cluster head node image is fully configured and tested you
can create an AMI snapshot based on the configured instance using the
[instructions](https://docs.aws.amazon.com/parallelcluster/latest/ug/building-custom-ami-v3.html)
published by AWS. Included here is a short summary of those instructions.

```
# 1) In a SSH session on the instance delete any unwanted files and directories
#    in your home directory and in the /root directory.

# 2) Use the AMI cleanup script to prepare the instance for imaging.
sudo /usr/local/sbin/ami_cleanup.sh
sudo apt clean

# 3) From the AWS console navigate to the build instance and choose
#    "Instance state" and select "Stop instance"

# 4) Create a new AMI from the instance. From at the instance view in the prior
#    step select "Actions" and choose "Image" and then "Create image".
```
