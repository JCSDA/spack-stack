This README provides step by step instructions for installing the basic packages
(OS packages, external packages) for spack-stack. Following these steps ensures
that the site configuration files in `configs/sites/noaa-aws` work out of the box.

# Basic system packages (need to be installed each time a cluster is spun up)

sudo su
chmod 777 /contrib
yum install -y qt5-qtbase-devel
yum install -y qt5-qtsvg-devel
yum install -y xorg-x11-xauth
yum install -y xorg-x11-apps
yum install -y perl-IPC-Cmd
yum install -y gettext-devel
yum install -y m4
exit

# Create a script that can be added to the cluster resource config so that these packages get installed automatically

mkdir -p /contrib/admin
cat <<EOF > /contrib/admin/basic_setup.sh
#!/bin/bash

chmod 777 /contrib
yum install -y qt5-qtbase-devel
yum install -y qt5-qtsvg-devel
yum install -y xorg-x11-xauth
yum install -y xorg-x11-apps
yum install -y perl-IPC-Cmd
yum install -y gettext-devel
yum install -y m4
EOF

chmod a+x /contrib/admin/basic_setup.sh

# Create a mysql config for local R2D2 use (if applicable)

sudo su
cat <<EOF > /contrib/admin/my.cnf
[mysqld]
datadir=/mysql_local/data
socket=/mysql_local/data/mysql.sock
symbolic-links=0
default-authentication-plugin=mysql_native_password

[mysqld_safe]
log-error=/mysql_local/log/mariadb.log
pid-file=/mysql_local/run/mariadb.pid
EOF
chmod 644 /contrib/admin/my.cnf
exit

# Build external packages for spack-stack

mkdir -p /contrib/spack-stack
mkdir /contrib/spack-stack/modulefiles
cd /contrib/spack-stack/

mkdir -p git-lfs-2.4.1/src
cd git-lfs-2.4.1/src
wget http://mirror.centos.org/centos/7/sclo/x86_64/rh/Packages/r/rh-git218-git-lfs-2.4.1-3.el7.x86_64.rpm
rpm2cpio rh-git218-git-lfs-2.4.1-3.el7.x86_64.rpm | cpio -idmv
mv opt/rh/rh-git218/root/usr/* ..
rm -fr opt
cd /contrib/spack-stack/modulefiles
mkdir git-lfs
# Create the modulefile from the template in doc/modulefile_templates

cd /contrib/spack-stack/
mkdir -p mysql-8.0.31/src
cd mysql-8.0.31/src
ldd --version
wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz
tar -xvf mysql-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz
mv mysql-8.0.31-linux-glibc2.17-x86_64-minimal/* ..
rmdir mysql-8.0.31-linux-glibc2.17-x86_64-minimal
cd /contrib/spack-stack/modulefiles
mkdir mysql
# Create the modulefile from the template in doc/modulefile_templates

cd /contrib/spack-stack/
mkdir -p cmake-3.27.2/src
cd cmake-3.27.2/src
wget https://github.com/Kitware/CMake/releases/download/v3.27.2/cmake-3.27.2-linux-x86_64.tar.gz
tar -xvzf cmake-3.27.2-linux-x86_64.tar.gz
mv cmake-3.27.2-linux-x86_64/* ..
rmdir cmake-3.27.2-linux-x86_64
cd /contrib/spack-stack/modulefiles
mkdir cmake
# Create the modulefile from the template in doc/modulefile_templates

# Set up basic modules for building the external ecflow package
module unuse /opt/cray/craype/default/modulefiles
module unuse /opt/cray/modulefiles

module purge
module load gnu/9.2.0
module use /contrib/spack-stack/modulefiles
module load cmake/3.27.2

mkdir -p /contrib/spack-stack/ecflow-5.8.4/src
cd /contrib/spack-stack/ecflow-5.8.4/src
wget https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-5.8.4-Source.tar.gz?api=v2
wget https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.tar.gz
mv ecFlow-5.8.4-Source.tar.gz\?api\=v2 ecFlow-5.8.4-Source.tar.gz
tar -xvzf boost_1_78_0.tar.gz
tar -xvzf ecFlow-5.8.4-Source.tar.gz
export WK=/contrib/spack-stack/ecflow-5.8.4/src/ecFlow-5.8.4-Source
export BOOST_ROOT=/contrib/spack-stack/ecflow-5.8.4/src/boost_1_78_0

# Build static boost (to not interfere with spack-stack boost)
cd $BOOST_ROOT
./bootstrap.sh 2>&1 | tee bootstrap.log
$WK/build_scripts/boost_build.sh 2>&1 | tee boost_build.log

# Build ecFlow
cd $WK
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/contrib/spack-stack/ecflow-5.8.4 2>&1 | tee log.cmake
make -j4 2>&1 | tee log.make
make install 2>&1 | tee log.install

cd /contrib/spack-stack/modulefiles
mkdir ecflow
# Create the modulefile from the template in doc/modulefile_templates

############## Steps to perform when starting a new cluster ##############
source /contrib/admin/basic_setup.sh  # sudo privileges requred to install packages
module unuse /opt/cray/craype/default/modulefiles
module unuse /opt/cray/modulefiles
module use /contrib/spack-stack/modulefiles
module load cmake/3.27.2
module load ecflow/5.8.4
module load mysql/8.0.31
module load git-lfs/2.4.1

