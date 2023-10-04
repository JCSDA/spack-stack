## Overview

The list of specs to be installed in the containers is defined in `specs.yaml` and included in the three container recipes. In the future, we will provide the option to specify different specs as a command line argument.

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
