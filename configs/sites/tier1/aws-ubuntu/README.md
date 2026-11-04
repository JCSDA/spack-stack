## spack-stack AMI (Ubuntu 26.04)

This document covers building and using the spack-stack 2.2 AMI for Ubuntu 26.04 LTS. This image has two environments: gnu (gcc-14.3.0), and intel (intel-oneapi 2026.1.1). You can use either one of these environments for development purposes.

### Using the Snapshot

Here is an example `aws cli` command-line to run a pre-built snapshot with your designated key-pair.

```bash
aws ec2 run-instances \
   --image-id "ami-0eec3117bdb2e6147" --instance-type "m6i.4xlarge" \
   --key-name YOUR-KEYPAIR \
   --block-device-mappings '{"DeviceName":"/dev/sda1","Ebs":{"Encrypted":false,"DeleteOnTermination":true,"Iops":3000,"SnapshotId":"snap-XXXXXXXXXXXXXXXXX","VolumeSize":200,"VolumeType":"gp3","Throughput":125}}' \
   --network-interfaces '{"SubnetId":"subnet-072fb62ff85b32a7a","AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-0091fa8e748fbe355"]}' \
   --tag-specifications '{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"ubuntu2604-spack-stack-2.2-gcc-oneapi"}]}' \
   --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' \
   --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":false,"EnableResourceNameDnsAAAARecord":false}' \
   --count 1
```

## Using this Site Config

This site tracks the current Ubuntu LTS. It started on 20.04, was
`tier2/aws-ubuntu2404` for spack-stack 2.0–2.1, and is 26.04 as of 2.2. When the
next LTS comes out, update this directory in place; don't create a new
versioned site.

JCSDA publishes a fully configured and built installation of spack stack derived
from this config as an AWS Snapshot. The easiest way to use this
configuration of spack stack is to launch a VM using that AMI. The instructions
below are included for maintainance of the history of this site config and
their possible relevance to debugging issues should they arise.

### Base Instance

This AMI was built on an instance with these properties:

* OS: Ubuntu 26.04.1 LTS (Resolute Raccoon), kernel 7.0.0-1014-aws
* AMI Name / ID: TODO
* 8 vCPU, 30 GiB RAM
* 200GB of gp3 storage as /

### Differences from the Ubuntu 24.04 site

* **Lmod comes from apt.** Ubuntu 26.04 packages Lmod 8.7.60 (on Lua 5.3),
  which meets spack's requirement, so the manual Lua 5.1 + Lmod 8.7 source
  build is gone. The package installs `/etc/profile.d/lmod.sh`, so `module`
  is available in every login shell.
* **The default system gcc is 15.2.0**, which is newer than spack-stack
  supports (up to 14.x). We install gcc/g++/gfortran 14.3.0 next to it and
  point spack at the `-14` binaries by full path. `/usr/bin/gcc` stays
  `gcc-15`. We don't use `update-alternatives` anymore: `/usr/bin/gcc` and
  `/usr/bin/g++` are symlinks owned by the `gcc`/`g++` packages, and an
  `apt upgrade` would reset them. The stack-gcc meta-module still exports
  `CC/CXX/FC` as the gcc-14 paths, so builds that load it use gcc-14. No
  unversioned `gfortran` is installed at all.
* **llvm-14 is not available** on 26.04 and nothing in the stack needs it,
  so it has been dropped, along with the `llvm-config` alternative.
* **coreutils is uutils (Rust)**, Ubuntu's default since 25.10
  (`ls (uutils coreutils) 0.10.0`). We keep the system default: switching to
  `coreutils-from-gnu` would remove the `build-essential` metapackage, which
  depends on `coreutils-from-uutils`. Spack doesn't detect uutils as a
  coreutils external. If a build fails in an `install`/`cp`/`sort`/`date`
  step, suspect uutils first.
* **`/tmp` is a RAM-backed tmpfs** (half of RAM, with per-user quotas). The
  24.04 site's `config.yaml` staged builds and cached sources in `/tmp`,
  which fills it with `Disk quota exceeded`. The site now uses the common
  default `${SPACK_STACK_DIR}/cache` on the root disk.
* The system ships Python 3.14 and CMake 4.2. Spack runs fine on Python 3.14,
  and both are still excluded from `spack external find`.

## Pre-requisites (For All Compilers)

### Installing Packages

```bash
# Update system software.
sudo apt update
sudo apt upgrade -y

# Build tools. build-essential pulls in the default gcc-15. We add gcc-14
# alongside it, since spack-stack supports gcc up to 14.x.
sudo apt install -y build-essential gcc-14 g++-14 gfortran-14 cpp-14 make cmake automake autoconf apt-utils

# Other requirements.
sudo apt install -y libgomp1 git git-lfs autopoint mysql-server libmysqlclient-dev qtbase5-dev qt5-qmake libqt5svg5-dev qt5dxcb-plugin wget curl file tcl-dev gnupg2 iproute2 locales unzip less bzip2 gettext libtree pkg-config libcurl4-openssl-dev libtool flex

# Lmod (8.7.60 on 26.04; installs /etc/profile.d/lmod.sh).
sudo apt install -y lmod

# Editors
sudo apt install -y vim nano

# Python develop.
sudo apt install -y python3 python3-pip python3-setuptools

# Configure git credential caching and git lfs for the ubuntu user and root.
git config --global credential.helper 'cache --timeout=3600'
git lfs install
sudo -H bash -c "git config --global credential.helper 'cache --timeout=3600' && git lfs install"

# Log out and back in (or `source /etc/profile.d/lmod.sh`), then check:
module --version     # Modules based on Lua: Version 8.7.60
gcc-14 --version     # gcc-14 (Ubuntu 14.3.0-14ubuntu1) 14.3.0
```

### Clone `spack-stack`

```bash
cd /opt
sudo git clone -b release/2.2 --depth 1 --recursive https://github.com/jcsda/spack-stack.git
sudo chown -R ubuntu:ubuntu /opt/spack-stack
```

Everything from here on runs as the `ubuntu` user. Use `sudo` only where it's
shown. These AMIs are single-user dev and test machines and everyone logs in
as `ubuntu`, so building as that user keeps the environments user-owned and
avoids root-owned files in `envs/`.

## Install Spack-Stack Steps by Compiler

<details>
<summary><b>GCC Installation</b></summary>

**Shortcut:** the committed site config reproduces this environment exactly
(verified: identical concretized hashes). On a prepared image you can skip
the external/compiler derivation and the `spack config add` steps below:

```bash
umask 0022
cd /opt/spack-stack && source setup.sh
spack stack create env --site aws-ubuntu --template unified-dev --name unified-gcc --compiler gcc
cd envs/unified-gcc && spack env activate -p .
spack concretize --fresh 2>&1 | tee log.concretize
```

The full steps below show how the site config was derived from
`linux.default`. Use them when moving to a new Ubuntu LTS.

```bash
# Ubuntu gives regular users umask 0002; spack-stack expects 0022 or 0027.
umask 0022
cd /opt/spack-stack
source setup.sh
# Swap default module type for default linux.
sed -i 's/tcl/lmod/g' configs/sites/tier2/linux.default/modules.yaml
spack stack create env --site linux.default --template unified-dev --name unified-gcc --compiler gcc
cd envs/unified-gcc
spack env activate -p .
unset SPACK_DISABLE_LOCAL_CONFIG
export SPACK_SYSTEM_CONFIG_PATH="$(pwd)/site"
spack external find --scope system \
    --exclude cmake \
    --exclude curl --exclude openssl \
    --exclude openssh --exclude python \
    --exclude zlib
# zlib: the system external (prefix /usr) breaks pmix's configure, which
# looks for libz in /usr/lib{,64} and not the multiarch
# /usr/lib/x86_64-linux-gnu ("ZLIB SUPPORT REQUESTED AND NOT FOUND").
spack external find --scope system wget grep
spack compiler find --scope system
# ACTION: Edit the generated compiler config (site/compilers.yaml and/or the
# compiler entries in site/packages.yaml) with the following.
#   1) Keep a single gcc@14.3.0 spec and delete the system default gcc@15.2.0
#      and any empty or duplicate gcc specs. Redundant/empty specs cause
#      cryptic build errors later. The entry should read:
#        gcc:
#          buildable: false
#          externals:
#          - spec: gcc@14.3.0 languages:='c,c++,fortran'
#            prefix: /usr
#            extra_attributes:
#              compilers:
#                c: /usr/bin/gcc-14
#                cxx: /usr/bin/g++-14
#                fortran: /usr/bin/gfortran-14
#   2) Delete or comment clang/llvm refs.
#   3) Add `buildable: false` to the tar and wget entries.
# coreutils (uutils on stock 26.04) and binutils (2.46, no gold) are not
# detected; let spack build them if needed. qt5 isn't detected either (qmake
# is a qtchooser shim), so declare the apt qtbase5-dev install by hand.
# common/packages.yaml requires qt@5.
cat << 'EOF' >> ${SPACK_SYSTEM_CONFIG_PATH}/packages.yaml
  qt:
    buildable: false
    externals:
    - spec: qt@5.15.18
      prefix: /usr
EOF
export SPACK_DISABLE_LOCAL_CONFIG=true
unset SPACK_SYSTEM_CONFIG_PATH

# Continue configuration. Don't use "packages:all:prefer:['%gcc']": gcc-14 is
# the only compiler, and that setting acts as a dependency constraint that
# pushes spack to rebuild system externals (gmake, perl, m4, ...) instead of
# using them. Pin MPI the way the Ubuntu CI does.
spack config add "packages:mpi:require:['openmpi@5.0.10']"
spack config add "packages:fontconfig:variants:+pic"
spack config add "packages:pixman:variants:+pic"
spack config add "packages:cairo:variants:+pic"
# met: with gcc 14, +lidar2nc and +modis can't be honored (they need hdf-eos2,
# and common pins hdf-eos2@2.20v1.00, which conflicts with %gcc@14:), so met
# builds without them.
spack config add "packages:met:variants:+python +grib2 +graphics +lidar2nc +modis"
spack config add "packages:ewok-env:require:[+ecflow]"
# Pin py-netcdf4
spack config add "packages:py-netcdf4:require:[\"@1.7.2\"]"
# Avoid duplicates: jedi-ufs-env needs jedi-python-env +bufrquery. Left
# unconstrained, jedi-tools-env falls back to py-myst-parser@1 and py-sphinx@6,
# which cap py-attrs@:21 and py-docutils@:0.19 and split py-attrs, py-eccodes,
# py-rasterio, jedi-python-env and awscli-v2. myst-parser 5 + sphinx 9 share
# docutils 0.22 with the rest of the stack.
spack config add "packages:jedi-python-env:require:[+bufrquery]"
spack config add "packages:py-myst-parser:require:['@5:']"
spack config add "packages:py-sphinx:require:['@9:']"

# Concretize and install
spack concretize --fresh 2>&1 | tee log.concretize
# py-versioneer is a known, unavoidable duplicate (see common/packages.yaml).
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i fms -i crtm -i crtm-fix -i esmf -i mapl -i py-cython -i py-versioneer
spack stack check-preferred-compiler
spack install --fail-fast -j 8 2>&1 | tee log.install

# Install modules
spack module lmod refresh -y --delete-tree
spack stack setup-meta-modules

# Add a number of default module locations to the lmod startup script.
echo 'module use /opt/spack-stack/envs/unified-gcc/modules/Core' | sudo tee -a /etc/profile.d/z01_lmod.sh
```

</details>

<details>
<summary><b>Intel OneAPI Installation</b></summary>

#### Install Intel OneAPI Compiler

Intel's `all` apt repo works unchanged on 26.04. 2026.1.1 is the latest
2026.1.x and is the release-tested version. Don't pick up 2026.2, which is
also in the repo.

```bash
wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
sudo apt update
sudo apt install -y intel-oneapi-compiler-dpcpp-cpp-2026.1 intel-oneapi-compiler-fortran-2026.1 intel-oneapi-mpi-devel-2021.18 intel-oneapi-tbb-devel-2023.1 intel-oneapi-mkl-devel-2026.1
```

**GCC toolchain note:** icx/icpx use the newest installed GCC for libstdc++
headers and libraries, and ifx uses it to link its runtime. On 26.04 that's
gcc-15, not the gcc-14 this stack uses (`icpx -v` prints
`Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/15`).
`packages_oneapi.yaml` pins them back to gcc 14 with compiler `flags:`
(`--gcc-install-dir=.../14` for C/C++, `-gcc-name`/`-gxx-name` for ifx), the
same way acorn and wcoss2 pin theirs.

#### Setup OneAPI Modules

```bash
# Create all modulefiles.
sudo /opt/intel/oneapi/modulefiles-setup.sh --output-dir=/opt/intel/oneapi/modulefiles
module use /opt/intel/oneapi/modulefiles

# Add the oneapi module files to lmod init (z01 sorts after the apt lmod.sh).
echo 'module use /opt/intel/oneapi/modulefiles' | sudo tee -a /etc/profile.d/z01_lmod.sh

# Create combined module file. Note that the compiler modulefile has a "tcm"
# prerequisite; omitting it fails the load with "Cannot load module
# compiler/2026.1.1. At least one of these module(s) must be loaded: tcm".
sudo mkdir -p /opt/intel/oneapi/modulefiles/intel-oneapi-full-env/
sudo tee /opt/intel/oneapi/modulefiles/intel-oneapi-full-env/2026.1.1 > /dev/null << 'EOF'
#%Module1.0
##
## intel-oneapi-full-env/2026.1.1
## Intel oneAPI full module environment

proc ModulesHelp { } {
    puts stderr "intel-oneapi-full-env defines the entire module set used for spack-stack intel builds"
}
module-whatis "intel-oneapi-full-env defines the entire module set used for spack-stack intel builds"
module load umf/1.1.0
module load tcm/1.5
module load tbb/2023.1
module load compiler-rt/2026.1.1
module load compiler/2026.1.1
module load mkl/2026.1
module load compiler-intel-llvm/2026.1.1
EOF
```

#### Install Intel OneAPI Spack-Stack Environment

The committed `packages_oneapi.yaml` is complete. Create the environment
straight from the site; don't re-run `spack external find` or
`spack compiler find` against it. Run everything in a **login shell with no
oneAPI modules loaded** (see "The module-load trap" below). Spack loads the
compiler's modules itself, even during concretization, so the oneAPI
modulefiles must be on `MODULEPATH` via `/etc/profile.d/z01_lmod.sh`.

```bash
module purge
umask 0022
cd /opt/spack-stack
source setup.sh

spack stack create env --site aws-ubuntu --template unified-dev --name unified-oneapi --compiler oneapi
cd envs/unified-oneapi
spack env activate -p .

spack concretize --fresh 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i fms -i crtm -i crtm-fix -i esmf -i mapl -i py-cython -i py-versioneer
spack stack check-preferred-compiler
spack install --fail-fast -j 8 2>&1 | tee log.install

spack module lmod refresh -y --delete-tree
spack stack setup-meta-modules

echo 'module use /opt/spack-stack/envs/unified-oneapi/modules/Core' | sudo tee -a /etc/profile.d/z01_lmod.sh
```

How `packages_oneapi.yaml` relates to the 24.04 version (check these when
moving to a new LTS or oneAPI release):

* `intel-oneapi-compilers` external: the 2026.1.1 compilers, `+fix_rt_linkage`
  (common requires it, PR #2150), the module chain
  `umf -> tcm -> tbb -> compiler-rt -> compiler`, and the gcc-14 `flags:`
  above. To regenerate it, `module load intel-oneapi-full-env/2026.1.1` and run
  `spack compiler find` in a scratch env, then copy the entry and `module purge`.
* `gcc` external: gcc@14.3.0 using the `-14` binaries, as in `packages_gcc.yaml`.
  common/packages_oneapi.yaml builds a handful of packages (cmake, rust, py-numpy, ...) with gcc.
* MPI is `intel-oneapi-mpi@2021.18` (`mpi: require:`, openmpi/mpich not
  buildable). MKL and TBB are externals, and MKL deliberately has no `modules:`.
* Dropped `all: prefer: ['%oneapi']`. common/packages_oneapi.yaml already
  prefers oneAPI per language (c/cxx/fortran), and the `all:` form makes spack
  rebuild system externals.
* New for 26.04, to avoid duplicates: `py-dask@2024.12.1` (otherwise
  py-setuptools-scm splits 8/9 and cascades) and `met +graphics +shared-intel`
  (otherwise one met concretizes `~graphics`). met's `+lidar2nc +modis` stay
  off, as in the gcc env (hdf-eos2 pin vs gcc 14).
* The shared `packages.yaml` (externals, jedi-python-env `+bufrquery`,
  myst-parser/sphinx) applies to both compilers.

#### The module-load trap

Spack loads an external's `modules:` itself and treats a load that does not change
`LOADEDMODULES` as a failure. So any oneAPI module already loaded in your shell
makes `spack install` die with a misleading `ModuleLoadError` partway through.
Purge before installing, and let spack do the loading.

For the same reason no two externals may list the same module. That is why
`intel-oneapi-mkl` above has no `modules:`: it would load before the compilers
entry and miss its `tbb`/`compiler-rt` prereqs, but listing those on mkl collides
with the compilers entry. It needs neither -- the recipe sets `MKLROOT` from
`prefix`.

</details>

## Test Installation

<details>
<summary>GCC</summary>

```bash
# Example given for building jedi-bundle
module use /opt/spack-stack/envs/unified-gcc/modules/Core
module load stack-gcc/14.3.0
module load stack-openmpi/5.0.10
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

mkdir ~/jedi
cd ~/jedi
git clone https://github.com/JCSDA-internal/jedi-bundle.git
cd jedi-bundle
mkdir build && cd build
ecbuild ../
make update
make -j10
ctest
```

</details>

<details>
<summary>Intel OneAPI</summary>

```bash
# Build jedi-bundle with oneapi
# stack-intel-oneapi-compilers exports CFLAGS/CXXFLAGS/FFLAGS that pin icx/icpx/ifx
# to gcc 14 (see packages_oneapi.yaml). Keep them: if you override them, the
# compilers fall back to the system gcc 15.
# ifx puts large temporary arrays on the stack. With the default 8 MB limit, the
# saber GSI and dirac_multiscale tests segfault. Raise the limit before running:
ulimit -s unlimited
module use /opt/spack-stack/envs/unified-oneapi/modules/Core
module load stack-intel-oneapi-compilers/2026.1.1
module load stack-intel-oneapi-mpi/2021.18
module load base-env
module load jedi-mpas-env
module load jedi-fv3-env
module load ewok-env
module load sp

mkdir ~/jedi
cd ~/jedi
git clone https://github.com/JCSDA-internal/jedi-bundle.git
cd jedi-bundle
mkdir build && cd build
ecbuild ../
make update
make -j10 2>&1 | tee log.make
ctest
```

</details>

The installation and configuration is now complete for the instance.
