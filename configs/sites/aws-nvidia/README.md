# These instructions are for Ubuntu 20.04 x86_64 using a c5n.4xlarge instance type

Follow the instructions in https://spack-stack.readthedocs.io/en/1.7.0/NewSiteConfigs.html#prerequisites-ubuntu-one-off to install the basic packages.

Download the latest version of the Nvidida HPC SDK following the instructions on the Nvidia website. For nvhpc@24.3:
```
url https://developer.download.nvidia.com/hpc-sdk/ubuntu/DEB-GPG-KEY-NVIDIA-HPC-SDK | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg] https://developer.download.nvidia.com/hpc-sdk/ubuntu/amd64 /' | sudo tee /etc/apt/sources.list.d/nvhpc.list
sudo apt-get install -y nvhpc-24-3
```
To use the environment files that are shipped with nvhpc-24-3, run
```
module use /opt/nvidia/hpc_sdk/modulefiles
```
This command needs to be run before building environments with spack-stack as well as before loading the spack-generated `stack-*` meta-modules.
