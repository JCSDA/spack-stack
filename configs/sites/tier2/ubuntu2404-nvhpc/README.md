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
apt install -y gcc g++ gfortran gdb environment-modules build-essential libkrb5-dev m4 git git-lfs bzip2 unzip automake autopoint gettext libcurl4-openssl-dev libssl-dev wget

# additional packages in nvhpc setup
apt install -y  cmake ninja-build pkg-config libtool python3-dev python3-venv

exit
```

### Installing the Nvidia HPC SDK

The site config describes the versions of the packages above as installed in Feb 2025.
The specific versions may need to be periodically updated, this can be done by following the
standard Ubuntu spack-stack setup instructions.

Then, install the Nvidia HPC SDK

```bash
curl https://developer.download.nvidia.com/hpc-sdk/ubuntu/DEB-GPG-KEY-NVIDIA-HPC-SDK | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg] https://developer.download.nvidia.com/hpc-sdk/ubuntu/amd64 /' | sudo tee /etc/apt/sources.list.d/nvhpc.list
sudo su -
apt update
apt install -y nvhpc-25-1
exit
```

### Installing the Nvidia Drivers

Depending on your system and what GPU is installed, you may need to install the Nvidia drivers.

Run the following script:

```bash
sudo apt install -y ubuntu-drivers-common
ubuntu-drivers devices
```

This will provide a list of all vendors and their drivers. A sample output is below:

```console
== /sys/devices/pci0000:00/0000:00:1e.0 ==
modalias : pci:v000010DEd00002237sv000010DEsd0000152Fbc03sc02i00
vendor   : NVIDIA Corporation
model    : GA102GL [A10G]
manual_install: True
driver   : nvidia-driver-470 - distro non-free
driver   : nvidia-driver-535-server-open - distro non-free
driver   : nvidia-driver-470-server - distro non-free
driver   : nvidia-driver-535-server - distro non-free
driver   : nvidia-driver-570-server - distro non-free
driver   : nvidia-driver-570-server-open - distro non-free
driver   : nvidia-driver-535-open - distro non-free
driver   : nvidia-driver-535 - distro non-free
driver   : nvidia-driver-550-open - distro non-free
driver   : nvidia-driver-550 - distro non-free recommended
driver   : xserver-xorg-video-nouveau - distro free builtin
```

You should generally install the latest version of the driver. In the example above, this the `nvidia-driver-570-server`.

__NOTE__: For latest HPC SDK versions from Nvidia, you should always use the latest driver unless directed otherwise.

To install the driver run:

```bash
sudo ubuntu-drivers install --gpgpu nvidia:driver-570
sudo apt install nvidia-utils-570-server
sudo reboot # The system need to be rebooted for the driver to take effect
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
spack install --verbose --fail-fast 2>&1 | tee log.install
spack module lmod refresh
spack stack setup-meta-modules
```

You should now have a spack-stack environment that can be accessed by running

```bash
module use /opt/nvidia/hpc_sdk/modulefiles
module use ${SPACK_STACK_DIR}/envs/nvidia-env/install/modulefiles/Core

module load nvhpc/25.1
module load stack-nvhpc/25.1
module load stack-openmpi/4.1.5
```

Note this environment does not provide the usual meta modules like `jedi-mpas-env` and so on,
therefore each module must be loaded on its own.
