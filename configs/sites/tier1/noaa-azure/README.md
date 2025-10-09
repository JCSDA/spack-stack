# Provisiong ParallelWorks Azure clusters

## Steps to perform before installing spack-stack version 1.9.3

sudo su -
chmod 777 /contrib
yum install -y qt5-qtbase-devel
yum install -y qt5-qtsvg-devel


## Steps to install spack-stack version 1.8.0

sudo su -
chmod 777 /contrib

module purge

cd /contrib/spack-stack-rocky8/
git clone --recursive https://github.com/JCSDA/spack-stack -b release/1.9.0 spack-stack-1.9.3
cd spack-stack-1.9.3
. setup.sh
spack stack create env --name ue-oneapi-2024.2.1 --template unified-dev --site noaa-azure --compiler oneapi
cd envs/ue-oneapi-2024.2.1
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
spack module lmod refresh -y
spack stack setup-meta-modules

## Steps to install GSI addon

sudo su -
chmod 777 /contrib

cd /contrib/spack-stack-rocky8/spack-stack-1.9.3
. setup.sh
spack stack create env --name gsi-oneapi-2024.2.1 --template gsi-addon-dev --site noaa-azure --upstream /contrib/spack-stack-rocky8/spack-stack-1.9.3/envs/ue-oneapi-2024.2.1/install --compiler oneapi
cd envs/gsi-oneapi-2024.2.1
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
spack module lmod refresh --upstream-modules
spack stack setup-meta-modules
