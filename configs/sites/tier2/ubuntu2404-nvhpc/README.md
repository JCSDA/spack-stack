## Azure VM for Ubuntu 24.04 with Nvidia HPC SDK 25.1

This site config describes the spack-stack install for an Azure VM running Ubuntu 24.04 and the
Nvidia HPC SDK 25.1.

To obtain the correctly configured VM, please follow the steps below.

### Obtain an Ubuntu 24.04 machine

These instructions were tested on an Azure VM size NC6s v3, but should be agnostic to the specific
hardware and provider.

However Ubuntu 24.04 LTS is assumed in the site config's version of individual packages.


### Set up the Ubuntu environment

First we install low-level build tools and system packages from the package manager, so we don't
have to build everything using spack-stack. Then we install the Nvidia HPC SDK.

```bash
sudo su -
apt update
apt upgrade -y

# packages from default Ubuntu setup
apt install -y gcc g++ gfortran gdb
apt install -y environment-modules
apt install -y build-essential
apt install -y libkrb5-dev
apt install -y m4
apt install -y git
apt install -y git-lfs
apt install -y bzip2
apt install -y unzip
apt install -y automake
apt install -y autopoint
apt install -y gettext
apt install -y libcurl4-openssl-dev
apt install -y libssl-dev
apt install -y wget

# additional packages in nvhpc setup
cmake
ninja-build
pkg-config
libtool
python3-dev python3-venv

exit
```

The site config describes the versions of the packages above as installed in Feb 2025.
The specific versions may need to be periodically updated, this can be done by following the
standard Ubuntu spack-stack setup instructions.

Then, install the Nvidia HPC SDK

```bash
curl https://developer.download.nvidia.com/hpc-sdk/ubuntu/DEB-GPG-KEY-NVIDIA-HPC-SDK | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg] https://developer.download.nvidia.com/hpc-sdk/ubuntu/amd64 /' | sudo tee /etc/apt/sources.list.d/nvhpc.list
sudo su
apt update
apt install -y nvhpc-25-1
exit
```


### Set up spack-stack

Follow the standard Ubuntu spack-stack setup instructions, but note the tweaking of the site via
spack's "find" commands should not be needed. Thus, run just these steps,

```bash
git clone -b release/1.9.0 --recurse-submodules https://github.com/jcsda/spack-stack.git
cd spack-stack
source setup.sh
spack stack create env --site ubuntu2404-nvhpc --template jedi-mpas-nvidia-dev --name nvidia-env --compiler=nvhpc
cd envs/nvidia-env/
spack env activate -p .
spack concretize 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d log.concretize
spack install [--verbose] [--fail-fast] 2>&1 | tee log.install
spack module tcl refresh
spack stack setup-meta-modules
```

You should now have a spack-stack environment that can be accessed by running

```bash
module use ${SPACK_STACK_DIR}/envs/jedi-mpas-nvidia-env/install/modulefiles/Core
```

Note this environment does not provide the usual meta modules like `jedi-mpas-env` and so on,
therefore each module must be loaded on its own.



