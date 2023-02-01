## spack-stack on AWS parallelcluster using Intel+Intel-MPI

**Note.** These instructions were used to create this site config. These steps are **not** necessary when building ``spack-stack`` - simply use the existing site config in this directory.

### Base instance
Choose a basic AMI from the Community AMIs tab that matches your desired OS and parallelcluster version. Select an instance type of the same family that you are planning to use for the head and the compute nodes, and enough storage for a swap file and a spack-stack installation. For example:
- AMI ID: ami-091017c7508ac95f6
- Instance c5n.4xlarge
- Use 250GB of gp3 storage as /

### Prerequisites
1. As `root`:
```
sudo su
apt-get -y update
apt-get -y upgrade
# These were already installed
#apt install -y apt-utils

# Compilers - already installed
#apt install -y gcc g++ gfortran gdb

# Environment module support - already installed
#apt install -y environment-modules

# Misc
apt install -y build-essential
apt install -y libcurl4-openssl-dev
apt install -y libssl-dev
apt install -y libkrb5-dev
apt install -y m4
apt install -y git
apt install -y git-lfs
apt install -y bzip2
apt install -y unzip
apt install -y automake
apt install -y xterm
apt install -y texlive

# This is for ecflow
apt install -y qt5-default
apt install -y libqt5svg5-dev
apt install -y qt5dxcb-plugin

# For R2D2 mysql backend, already installed
#apt install -y mysql-server

# Remove AWS openmpi
apt remove -y openmpi40-aws

# This is because boost doesn't work with the Intel compiler
apt install -y libboost1.71-dev
apt install -y libboost-chrono1.71-dev
apt install -y libboost-date-time1.71-dev
apt install -y libboost-exception1.71-dev
apt install -y libboost-filesystem1.71-dev
apt install -y libboost-program-options1.71-dev
apt install -y libboost-python1.71-dev
apt install -y libboost-regex1.71-dev
apt install -y libboost-serialization1.71-dev
apt install -y libboost-system1.71-dev
apt install -y libboost-test1.71-dev
apt install -y libboost-thread1.71-dev
apt install -y libboost-timer1.71-dev

# Python
apt install -y python3-dev python3-pip

# Intel compiler
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list 
apt-get update
apt-get install -y intel-hpckit-2021.4.0/all

# Configure X windows
echo "X11Forwarding yes" >> /etc/ssh/sshd_config
service sshd restart

# Bug fixes for libraries/headers expected in standard locations
cd /usr/lib64/
ln -sf /usr/lib/x86_64-linux-gnu/libcrypt.so .
cd /usr/include
ln -sf python3.8/pyconfig.h .

# Create swapfile - 100GB
dd if=/dev/zero of=/swapfile bs=128M count=800
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
swapon -s
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab

# Exit root session
exit
```

2. Log out and back in to enable x11 forwarding

3. Build ecflow outside of spack to be able to link against OS boost
```
mkdir -p /home/ubuntu/jedi/ecflow-5.8.4/src
cd /home/ubuntu/jedi/ecflow-5.8.4/src
wget https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-5.8.4-Source.tar.gz?api=v2
mv ecFlow-5.8.4-Source.tar.gz\?api\=v2 ecFlow-5.8.4-Source.tar.gz
tar -xvzf ecFlow-5.8.4-Source.tar.gz
export WK=/home/ubuntu/jedi/ecflow-5.8.4/src/ecFlow-5.8.4-Source
export BOOST_ROOT=/usr

# Build ecFlow
cd $WK
mkdir build
cd build
cmake .. -DENABLE_STATIC_BOOST_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/home/ubuntu/jedi/ecflow-5.8.4 2>&1 | tee log.cmake
make -j4 2>&1 | tee log.make
make install 2>&1 | tee log.install
```
4. Option 1: Use pre-defined site config in spack-stack (skip steps 5-7 afterwards)
```
cd /home/ubuntu/jedi
git clone -b develop --recursive https://github.com/noaa-emc/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site aws-pcluster --template=skylab-dev --name=skylab-2.0.0-intel-2021.4.0
spack env activate -p envs/skylab-2.0.0-intel-2021.4.0
```
5. Option 2: For spack site configuration, to find Intel compiler
```
export PATH=/opt/intel/oneapi/compiler/2021.4.0/linux/bin/intel64:$PATH
```

6. Option 2: Configure site from scratch
```
mkdir /home/ubuntu/jedi && cd /home/ubuntu/jedi
git clone -b develop --recursive https://github.com/noaa-emc/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site linux.default --template=skylab-dev --name=skylab-2.0.0-intel-2021.4.0
spack env activate -p envs/skylab-2.0.0-intel-2021.4.0

export SPACK_SYSTEM_CONFIG_PATH=/home/ubuntu/jedi/spack-stack/envs/skylab-2.0.0-intel-2021.4.0/site

spack external find --scope system
spack external find --scope system perl
spack external find --scope system python
spack external find --scope system wget
spack external find --scope system curl
spack external find --scope system texlive

# No external find for pre-installed intel-oneapi-mpi (from pcluster AMI),
# and no way to add object entry to list using "spack config add".
echo "  intel-oneapi-mpi:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    buildable: False" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    externals:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    - spec: intel-oneapi-mpi@2021.4.0%intel@2021.4.0" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      prefix: /opt/intel" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      modules:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      - intelmpi" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml

# Can't find qt5 because qtpluginfo is broken,
# and no way to add object entry to list using "spack config add".
echo "  qt:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    buildable: False" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    externals:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    - spec: qt@5.12.8" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      prefix: /usr" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml

# Add external boost
echo "  boost:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    buildable: False" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    externals:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    - spec: boost@1.71.0 +atomic +chrono +date_time +exception +filesystem +graph +iostreams +locale +log +math +mpi +numpy +pic +program_options +python +random +regex +serialization +signals +system +test +thread +timer ~wave cxxstd=14 visibility=hidden" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      prefix: /usr" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml

# Add external ecflow
echo "  ecflow:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    buildable: False" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    externals:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    - spec: ecflow@5.8.4 +ui" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      prefix: /home/ubuntu/jedi/ecflow-5.8.4" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml

spack compiler find --scope system

export -n SPACK_SYSTEM_CONFIG_PATH

spack config add "packages:python:buildable:False"
spack config add "packages:openssl:buildable:False"
spack config add "packages:all:providers:mpi:[intel-oneapi-mpi@2021.4.0]"
spack config add "packages:all:compiler:[intel@2021.4.0]"

# edit envs/skylab-2.0.0-intel-2021.4.0/site/compilers.yaml and replace the following line in the **Intel** compiler section:
#     environment: {}
# -->
#     environment:
#       prepend_path:
#         LD_LIBRARY_PATH: '/opt/intel/oneapi/compiler/2021.4.0/linux/compiler/lib/intel64_lin'
#       set:
#         I_MPI_PMI_LIBRARY: '/opt/slurm/lib/libpmi.so'

# edit envs/skylab-2.0.0-intel-2021.4.0/site/packages.yaml and remove the older Python versions, keep 3.8.10 only
```

7. Option 2: Temporary workarounds to avoid duplicate hdf5, cmake etc. versions. Edit ``envs/skylab-2.0.0-intel-2021.4.0/site/packages.yaml`` and remove the external ``cmake`` and ``openssl`` entries.

8. Concretize and install
```
spack concretize 2>&1 | tee log.concretize
spack install --verbose --source 2>&1 | tee log.install
```
9. Create the AMI for use in the AWS parallelcluster config.
