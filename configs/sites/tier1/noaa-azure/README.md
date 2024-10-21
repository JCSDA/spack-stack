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
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose 2>&1 | tee log.install
spack module lmod refresh --upstream-modules
spack stack setup-meta-modules
