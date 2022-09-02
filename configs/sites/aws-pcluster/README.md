## spack-stack on AWS parallelcluster using Intel+Intel-MPI

### Base instance
- AMI ID: ami-091017c7508ac95f6
- Instance c5n.4xlarge

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
#apt install krb5-user
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

# This is because boost doesn't work with the Intel compiler
apt install -y libboost-all-dev

# Python
apt install python3-dev python3-pip
python3 -m pip install poetry
# Ignore error "ERROR: launchpadlib 1.10.13 requires testresources, which is not installed."
# test - successful if no output
python3 -c "import poetry"

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
4. For spack site configuration, to find Intel compiler
```
export PATH=/opt/intel/oneapi/compiler/2021.4.0/linux/bin/intel64:$PATH
```
5. Option 1: Use pre-defined site config in spack-stack (skip step 6 afterwards)
```
mkdir /home/ubuntu/jedi && cd /home/ubuntu/jedi
git clone -b develop --recursive https://github.com/noaa-emc/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site aws-pcluster --template=skylab-dev --name=skylab-1.0.0-intel-2021.4.0
export SPACK_SYSTEM_CONFIG_PATH=/home/ubuntu/jedi/spack-stack-dev-20220830/envs/skylab-1.0.0-intel-2021.4.0/site
```
6. Option 2: Configure site from scratch
```
mkdir /home/ubuntu/jedi && cd /home/ubuntu/jedi
git clone -b develop --recursive https://github.com/noaa-emc/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site linux.default --template=skylab-dev --name=skylab-1.0.0-intel-2021.4.0
export SPACK_SYSTEM_CONFIG_PATH=/home/ubuntu/jedi/spack-stack/envs/skylab-1.0.0-intel-2021.4.0/site

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

# edit envs/skylab-1.0.0-intel-2021.4.0/site/compilers.yaml and replace the following line in the **Intel** compiler section:
#     environment: {}
# -->
#     environment:
#       prepend_path:
#         LD_LIBRARY_PATH: '/opt/intel/oneapi/compiler/2021.4.0/linux/compiler/lib/intel64_lin'
```

7. Temporary workaround to avoid duplicate hdf5 etc. (no idea why)
```
spack remove fms@2022.01
```
8. Concretize and install
```
spack concretize 2>&1 | tee log.concretize
spack install -v 2>&1 | tee log.install
```
