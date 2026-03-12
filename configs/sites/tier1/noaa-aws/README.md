# Provisiong ParallelWorks AWS clusters

## Use ParallelWorks NOAA-AWS Rocky9 cluster
## Steps to install ue-oneapi-2025.3.0 environment

module purge

mkdir -p /contrib/spack-stack-rocky9
cd /contrib/spack-stack-rocky9/
git clone --recurse-submodules -b release/2.1 https://github.com/jcsda/spack-stack.git spack-stack-2.1
cd spack-stack-2.1
source setup.sh

. setup.sh
spack stack create env --site noaa-aws --template unified-dev --compiler oneapi-2025.3.0 --name ue-oneapi-2025.3.0
spack env activate -p envs/ue-oneapi-2025.3.0
cd ./envs/ue-oneapi-2025.3.0

export MODULES_AUTO_HANDLING=1
module use /pw/apps/modules/intel/2025.3.0
module load compiler/2025.3.0
module load mpi

spack concretize 2>&1 | tee log.concretize
spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
spack module lmod refresh -y
spack stack setup-meta-modules

## Steps to install gcc-12.4.0 environment

module purge
mkdir -p /contrib/spack-stack-rocky9
cd /contrib/spack-stack-rocky9/
cd spack-stack-2.1
source setup.sh

spack stack create env --site noaa-aws --template unified-dev --compiler gcc-12.4.0 --name ue-gcc-12.4.0

spack env activate -p envs/ue-gcc-12.4.0
cd ./envs/ue-gcc-12.4.0

spack concretize 2>&1 | tee log.concretize

spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install

spack module lmod refresh -y
spack stack setup-meta-modules
