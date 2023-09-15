## Overview

To avoid hardcoding specs in the generic container recipes, we keep the specs list empty (`specs: []`) and manually add the specs for the particular spack-stack release and application as listed below, *after* running `spack stack create ctr`.

### spack-stack-1.5.0 / skylab-6.0.0 containers for fv3-jedi and mpas-jedi (but not for ufs-jedi)
```
  specs: [base-env@1.0.0, jedi-base-env@1.0.0 ~fftw, ewok-env@1.0.0, jedi-fv3-env@1.0.0,
    jedi-mpas-env@1.0.0, bacio@2.4.1, bison@3.8.2, bufr@12.0.0, ecbuild@3.7.2, eccodes@2.27.0, ecflow@5,
    eckit@1.24.4, ecmwf-atlas@0.34.0 +trans ~fftw, fiat@1.2.0, ectrans@1.2.0 ~fftw, eigen@3.4.0,
    fckit@0.11.0, fms@release-jcsda, g2@3.4.5, g2tmpl@1.10.0, gftl-shared@1.5.0,
    gsibec@1.1.3, hdf@4.2.15, hdf5@1.14.0, ip@4.3.0, jasper@2.0.32, jedi-cmake@1.4.0,
    libpng@1.6.37, nccmp@1.9.0.1, netcdf-c@4.9.2, netcdf-cxx4@4.3.1,
    netcdf-fortran@4.6.0, nlohmann-json@3.10.5, nlohmann-json-schema-validator@2.1.0,
    parallelio@2.5.10, parallel-netcdf@1.12.2, py-eccodes@1.4.2, py-f90nml@1.4.3,
    py-gitpython@3.1.27, py-h5py@3.7.0, py-numpy@1.22.3,
    py-pandas@1.5.3, py-pip, py-pyyaml@5.4.1, py-scipy@1.9.3, py-shapely@1.8.0, py-xarray@2022.3.0,
    sp@2.3.3, udunits@2.2.28, w3nco@2.4.1, w3emc@2.10.0, nco@5.0.6, esmf@8.4.2, mapl@2.35.2,
    yafyaml@0.5.1, zlib@1.2.13, zstd@1.5.2, odc@1.4.6, shumlib@macos_clang_linux_intel_port,
    awscli@1.27.84, py-globus-cli@3.16.0]
    # Don't build CRTM by default so that it gets built in the JEDI bundles:
    # crtm@v2.4.1-jedi
    # Comment out for now until build problems are solved
    # https://github.com/jcsda/spack-stack/issues/522
    # py-mysql-connector-python@8.0.32
```

### Create an AMI on AWS EC2 to build docker containers

AMI ami-0a934b7133c2b7102 (dom-docker-builder-full-backup-20230217; JCSDA-NOAA account, us-east-1) was created following the instructions below

- See https://docs.docker.com/desktop/install/ubuntu/
- Start with ami-052efd3df9dad4825
- c5n.2xlarge
- 350GB root volume is plenty
```
# Run as root
sudo su
apt update
apt -y upgrade
reboot
# ... wait for the instance to come back up again ...

# Install Docker, SingularityCE, and other basic packages
sudo su
apt install -y gnome-terminal
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-4.11.0-amd64.deb
apt -y install ./docker-desktop-4.11.0-amd64.deb
# IGNORE 'N: Download is performed unsandboxed as root as file '/home/ubuntu/docker-desktop-4.11.0-amd64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)'

apt install -y libpython3-dev
apt install -y python3-pip
apt install -y python3-poetry
python3 -c "import poetry"

python3 -m pip install awscli
aws configure

cd ~
wget https://github.com/sylabs/singularity/releases/download/v3.9.9/singularity-ce_3.9.9-focal_amd64.deb
apt install ./singularity-ce_3.9.7-bionic_amd64.deb
# Ignore "N: Download is performed unsandboxed as root as file '/root/singularity-ce_3.9.9-focal_amd64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)"
# Test:
singularity version

exit

# Run as user ubuntu
systemctl --user start docker-desktop
```
Then, build, run, upload containers as root user

### Converting spack-stack docker images to singularity
As root user:
```
singularity build docker-intel-oneapi-dev.sif docker-daemon://469205354006.dkr.ecr.us-east-1.amazonaws.com/docker-intel-oneapi-dev:latest
singularity shell docker-intel-oneapi-dev.sif
```
