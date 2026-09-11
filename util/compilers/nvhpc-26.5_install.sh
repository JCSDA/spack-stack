#!/usr/bin/env bash

# Note. nvhpc binds to the system gcc at install time. A system update
# that bumps the default gcc means reinstalling the SDK, not just
# rebuilding the software stack and the downstream applications.

if [ "$#" -lt 1 ]; then
  echo "Error: Not enough arguments. Provide NVHPC SDK installation prefix."
  exit 1
fi

# Configure install via command line arguments
export NVHPC_SILENT=true
export NVHPC_INSTALL_DIR=${1}
export NVHPC_INSTALL_TYPE=single # or "network" for heterogeneous systems; check installer doc for details
export NVHPC_DEFAULT_CUDA=13.2 # optional; sets the default CUDA version

# Download and install nvhpc
mkdir -p ${NVHPC_INSTALL_DIR}/src
cd ${NVHPC_INSTALL_DIR}/src
wget https://developer.download.nvidia.com/hpc-sdk/26.5/nvhpc_2026_265_Linux_x86_64_cuda_13.2.tar.gz
tar xpzf nvhpc_2026_265_Linux_x86_64_cuda_13.2.tar.gz
nvhpc_2026_265_Linux_x86_64_cuda_13.2/install

# Bug fix for missing include directory (symbolic link)
cd ${NVHPC_INSTALL_DIR}
ln -s Linux_x86_64/26.5/compilers/include include

cd ${NVHPC_INSTALL_DIR}/src
rm -fr nvhpc_2026_265_Linux_x86_64_cuda_13.2
