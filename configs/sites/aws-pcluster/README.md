## spack-stack on AWS parallelcluster using Intel+Intel-MPI

**Note.** These instructions were used to create this site config. These steps are **not** necessary when building ``spack-stack`` - simply use the existing site config in this directory.

### Base instance
Choose a basic AMI from the Community AMIs tab that matches your desired OS and parallelcluster version. Select an instance type of the same family that you are planning to use for the head and the compute nodes, and enough storage for a swap file and a spack-stack installation. For example:
- AMI ID: ami-093dab62f7840644b
- Instance c6i.8xlarge
- Use 500GB of gp3 storage as /

### Prerequisites
1. As `root`:
```
sudo su
apt-get -y update
apt-get -y upgrade
# These were already installed
apt install -y apt-utils

# Compilers - already installed
apt install -y gcc g++ gfortran gdb

# Install lua/lmod manually, because apt only has older versions
# that are not compatible with the modern lua modules spack produces
# https://lmod.readthedocs.io/en/latest/030_installing.html#install-lua-x-y-z-tar-gz
mkdir -p /opt/lua/5.1.4.9/src
cd /opt/lua/5.1.4.9/src
wget https://sourceforge.net/projects/lmod/files/lua-5.1.4.9.tar.bz2
tar -xvf lua-5.1.4.9.tar.bz2
cd lua-5.1.4.9
./configure --prefix=/opt/lua/5.1.4.9 2>&1 | tee log.config
make VERBOSE=1 2>&1 | tee log.make
make install 2>&1 | tee log.install
#
echo "# Set environment variables for lua" >> /etc/profile.d/02-lua.sh
echo "export PATH=\"/opt/lua/5.1.4.9/bin:\$PATH\"" >> /etc/profile.d/02-lua.sh
echo "export LD_LIBRARY_PATH=\"/opt/lua/5.1.4.9/lib:\$LD_LIBRARY_PATH\"" >> /etc/profile.d/02-lua.sh
echo "export CPATH=\"/opt/lua/5.1.4.9/include:\$CPATH\"" >> /etc/profile.d/02-lua.sh
echo "export MANPATH=\"/opt/lua/5.1.4.9/man:\$MANPATH\"" >> /etc/profile.d/02-lua.sh
#
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
#
# intelmpi
echo "conflict openmpi" >> /opt/intel/mpi/2021.6.0/modulefiles/intelmpi
echo 'if { [ module-info mode load ] && ![ is-loaded libfabric-aws/1.16.0~amzn4.0 ] } {' >> /opt/intel/mpi/2021.6.0/modulefiles/intelmpi
echo '    module load libfabric-aws/1.16.0~amzn4.0' >> /opt/intel/mpi/2021.6.0/modulefiles/intelmpi
echo '}' >> /opt/intel/mpi/2021.6.0/modulefiles/intelmpi
# openmpi
echo "conflict intelmpi" >> /usr/share/modules/modulefiles/openmpi/4.1.4
echo 'if { [ module-info mode load ] && ![ is-loaded libfabric-aws/1.16.0~amzn4.0 ] } {' >> /usr/share/modules/modulefiles/openmpi/4.1.4
echo '    module load libfabric-aws/1.16.0~amzn4.0' >> /usr/share/modules/modulefiles/openmpi/4.1.4
echo '}' >> /usr/share/modules/modulefiles/openmpi/4.1.4
#
echo "module use /usr/share/modules/modulefiles" >> /etc/profile.d/z01_lmod.sh
echo "module use /opt/intel/mpi/2021.6.0/modulefiles" >> /etc/profile.d/z01_lmod.sh
echo "module use /home/ubuntu/jedi/modulefiles" >> /etc/profile.d/z01_lmod.sh
#
# Log out completely, ssh back into the instance and check if lua modules work
exit
exit

ssh ...
# Now user ubuntu
module av
module load libfabric-aws/1.16.0~amzn4.0
module load openmpi/4.1.4
module list
module unload openmpi/4.1.4
module load intelmpi
module list
module purge
module list

# Continue as root
sudo su

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

### # Remove AWS openmpi
### apt remove -y openmpi40-aws

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
apt-get install -y intel-hpckit-2022.2.0/all

# Docker
# See https://docs.docker.com/engine/install/ubuntu/
apt-get update
apt-get install ca-certificates curl gnupg lsb-release
mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker run hello-world
# DH* TODO 2023/02/21: Add users to group docker so that non-root users can run it
# See https://docs.docker.com/engine/install/linux-postinstall/


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
cmake .. -DPython3_EXECUTABLE=/usr/bin/python3 -DENABLE_STATIC_BOOST_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/home/ubuntu/jedi/ecflow-5.8.4 2>&1 | tee log.cmake
make -j4 2>&1 | tee log.make
make install 2>&1 | tee log.install

# Create a modulefiles directory with the following ecflow/5.8.4 module in it (w/o the '%%%%...' lines):
mkdir -p /home/ubuntu/jedi/modulefiles/ecflow
vi /home/ubuntu/jedi/modulefiles/ecflow/5.8.4
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
prepend-path PYTHONPATH "${ECFLOW_PATH}/lib/python3.8/site-packages"
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

4. Install msql community server
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
# Set root password, choose strong password encryption option
exit
rm *.deb
```

5. Option 1: Testing existing site config in spack-stack (skip steps 5-7 afterwards)
```
mkdir -p /home/ubuntu/sandpit
cd /home/ubuntu/sandpit
git clone -b develop --recursive https://github.com/jcsda/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site aws-pcluster --template=unified-dev --name=unified-dev
spack env activate -p envs/unified-dev
sed -i "s/\['\%apple-clang', '\%gcc', '\%intel'\]/\['\%intel', '\%gcc'\]/g" envs/unified-dev/spack.yaml
```

6. Option 2: Test configuring site from scratch
```
mkdir /home/ubuntu/jedi && cd /home/ubuntu/jedi
git clone -b develop --recursive https://github.com/jcsda/spack-stack spack-stack
cd spack-stack/
. setup.sh
spack stack create env --site linux.default --template=unified-dev --name=unified-dev
spack env activate -p envs/unified-dev

export SPACK_SYSTEM_CONFIG_PATH=/home/ubuntu/jedi/spack-stack/envs/unified-dev/site

spack external find --scope system
spack external find --scope system perl
spack external find --scope system python
spack external find --scope system wget
spack external find --scope system curl
spack external find --scope system texlive
spack external find --scope system mysql

# No external find for pre-installed intel-oneapi-mpi (from pcluster AMI),
# and no way to add object entry to list using "spack config add".
echo "  intel-oneapi-mpi:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    externals:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    - spec: intel-oneapi-mpi@2021.6.0%intel@2022.1.0" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      prefix: /opt/intel" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      modules:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      - libfabric-aws/1.16.0~amzn4.0" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      - intelmpi" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml

# Add external openmpi
echo "  openmpi:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    externals:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "    - spec: openmpi@4.1.4%gcc@9.4.0~cuda~cxx~cxx_exceptions~java~memchecker+pmi~static~wrapper-rpath" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "        fabrics=ofi schedulers=slurm" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      prefix: /opt/amazon/openmpi" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      modules:" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      - libfabric-aws/1.16.0~amzn3.0" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
echo "      - openmpi/4.1.4" >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml

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

spack config add "packages:mpi:buildable:False"
spack config add "packages:python:buildable:False"
spack config add "packages:openssl:buildable:False"
spack config add "packages:all:providers:mpi:[intel-oneapi-mpi@2021.6.0, openmpi@4.1.4]"
spack config add "packages:all:compiler:[intel@2022.1.0, gcc@9.4.0]"

# edit envs/unified-dev/site/compilers.yaml and replace the following line in the **Intel** compiler section:
#     environment: {}
# -->
#     environment:
#       prepend_path:
#         LD_LIBRARY_PATH: '/opt/intel/oneapi/compiler/2021.6.0/linux/compiler/lib/intel64_lin'
#       set:
#         I_MPI_PMI_LIBRARY: '/opt/slurm/lib/libpmi.so'
```

7. Option 2: To avoid duplicate hdf5, cmake, ... versions, edit ``envs/unified-dev/site/packages.yaml`` and remove the external ``cmake`` and ``openssl`` entries.

8. Concretize and install
```
spack concretize 2>&1 | tee log.concretize
spack install --verbose --source 2>&1 | tee log.install
spack module lmod refresh
spack stack setup-meta-modules
```
9. Test spack-stack installation using your favorite application.
10. (Optional) Remove test installs of spack-stack environments, if desired.
11. Create the AMI for use in the AWS parallelcluster config.
