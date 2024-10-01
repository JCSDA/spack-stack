# Provisiong ParallelWorks Azure clusters

## Steps to perform before installing spack-stack version 1.8.0

sudo su -
chmod 777 /contrib
yum install -y qt5-qtbase-devel
yum install -y qt5-qtsvg-devel


## Steps to install spack-stack version 1.8.0

sudo su -
chmod 777 /contrib

module purge
module unuse /opt/cray/craype/default/modulefiles
module unuse /opt/cray/modulefiles
module load gnu
module load intel/2023.2.0
module load impi/2023.2.0 
module unload gnu

cd /contrib/spack-stack-rocky8/
git clone --recursive https://github.com/JCSDA/spack-stack -b release/1.8.0 spack-stack-1.8.0
cd spack-stack-1.8.0
. setup.sh
spack stack create env --name ue-intel-2021.10.0 --template unified-dev --site noaa-azure --compiler intel
cd envs/ue-intel-2021.10.0
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose 2>&1 | tee log.install
spack module lmod refresh -y
spack stack setup-meta-modules

## Steps to install GSI addon

sudo su -
chmod 777 /contrib

cd /contrib/spack-stack-rocky8/spack-stack-1.8.0
. setup.sh
spack stack create env --name gsi-intel-2021.10.0 --template gsi-addon-dev --site noaa-azure --upstream /contrib/spack-stack-rocky8/spack-stack-1.8.0/envs/ue-intel-2021.10.0/install --compiler intel
cd envs/gsi-intel-2021.10.0
spack concretize 2>&1 | tee log.concretize
spack install --verbose 2>&1 | tee log.install
spack module lmod refresh --upstream-modules
spack stack setup-meta-modules

## Steps to install external applications (MySQL, ecFlow)

 MySQL:
mkdir -p /contrib/spack-stack-rocky8/mysql-8.0.31/src
cd /contrib/spack-stack-rocky8/mysql-8.0.31/src
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz
tar -xvf mysql-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz
mv mysql-8.0.31-linux-glibc2.17-x86_64-minimal/* ..
rmdir mysql-8.0.31-linux-glibc2.17-x86_64-minimal

 ecFlow:
mkdir -p /contrib/spack-stack-rocky8/ecflow-5.8.4/src
cd /contrib/spack-stack-rocky8/ecflow-5.8.4/src
wget https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-5.8.4-Source.tar.gz?api=v2
wget https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.tar.gz
mv ecFlow-5.8.4-Source.tar.gz\?api\=v2 ecFlow-5.8.4-Source.tar.gz
tar -xvzf boost_1_78_0.tar.gz
tar -xvzf ecFlow-5.8.4-Source.tar.gz
export WK=/contrib/spack-stack-rocky8/ecflow-5.8.4/src/ecFlow-5.8.4-Source
export BOOST_ROOT=/contrib/spack-stack-rocky8/ecflow-5.8.4/src/boost_1_78_0
cd $BOOST_ROOT
./bootstrap.sh 2>&1 | tee bootstrap.log
$WK/build_scripts/boost_build.sh 2>&1 | tee boost_build.log
cd $WK
mkdir build
cd build
cmake .. -DPython3_EXECUTABLE=`which python3` -DCMAKE_INSTALL_PREFIX=/contrib/spack-stack-rocky8/ecflow-5.8.4 2>&1 | tee log.cmake
make -j4 2>&1 | tee log.make
make install 2>&1 | tee log.install
