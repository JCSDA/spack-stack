WSL 2 Alma Linux 9 installation notes for NVHPC 26.5 compiler

# Download and install nvhpc, for example:
wget https://developer.download.nvidia.com/hpc-sdk/26.5/nvhpc_2026_265_Linux_x86_64_cuda_13.2.tar.gz
tar xpzf nvhpc_2026_265_Linux_x86_64_cuda_13.2.tar.gz
nvhpc_2026_265_Linux_x86_64_cuda_13.2/install

# Bug fix for missing include directory (symbolic link)
cd <nvhpc-top-level-install-dir>
ln -s Linux_x86_64/26.5/compilers/include include

# Needed for hpcx
yum install libnl3
