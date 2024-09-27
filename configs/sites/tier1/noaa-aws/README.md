# Provisiong ParallelWorks AWS clusters

## Steps to perform to install spack-stack version 1.8.0

sudo su -
chmod 777 /contrib

cd /contrib/spack-stack-rocky8/
git clone --recursive https://github.com/JCSDA/spack-stack -b release/1.8.0 spack-stack-1.8.0
cd spack-stack-1.8.0
. setup.sh
spack stack create env --name ue-intel-2021.10.0 --template unified-dev --site noaa-aws --compiler intel
cd envs/ue-intel-2021.10.0
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose 2>&1 | tee log.install
spack module lmod refresh -y
spack stack setup-meta-modules
