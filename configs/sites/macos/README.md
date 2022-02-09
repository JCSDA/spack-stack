# macOS

## General instructions/prerequisites

### Install Apple's command line utilities
- Launch the Terminal, found in `/Applications/Utilities`
- Type the following command string:
```
xcode-select --install
```

### Setup of x86_64 environment on arch64 systems
This step is only required on the new arch64 systems that are equipped with a Apple M1 silicon chip.
- Open `Applications` in Finder
- Duplicate your preferred terminal application (e.g. `Terminal` or `iTerm`)
- Rename the duplicate to, for example, `Terminal x86_64`
- Right-click / control+click on `Terminal x86_64`, choose `Get Info`
- Select the box `Open using Rosetta` and close the window

### Install homebrew for x86_64 environment
- If your system is an arch64 system, make sure to open the newly created `Terminal x86_64` application. Type `arch` in the terminal to confirm, if correct the output is `i386` (and not `arm64`)
- Install `homebrew` from the command line. On x86_64 systems and on arch64 systems using the x86_64 emulator, `homebrew` is installed in `/usr/local`
- It is recommended to install the following prerequisites via Homebrew, as installing them with Spack and Apple's native clang can be tricky.
```
brew install coreutils@9.0
brew install gcc@11.2.0
brew install llvm13.0.0
brew install mpich@3.4.3
brew install python@3.9.10
brew install git@2.34.1
brew install git-lfs@3.0.2
brew install lmod@8.6.6
brew install wget@1.21.2
brew install bash@5.1.16
```
- DH This should not be required, check!
```
#brew install libtiff
```
- DH Todo: fix stack build problems of eccodes on macOS!
```
# this also install jasper, zlib/szip, hdf5, netcdf which we
# don't use but which we also don't want to have on the system
# brew install eccodes@2.24.2
```
- Activate the `lua` module environment:
```
source /usr/local/opt/lmod/init/profile
```

## Building your own spack stack
```
git clone -b jcsda_emc_spack_stack --recursive https://github.com/climbfuji/spack-stack
cd spack-stack
export SPACK_BASE_DIR=$PWD
source spack/share/spack/setup-env.sh
rsync -av envs/ envs_macos/
vi envs_macos/spack.yaml
# comment out the "please_configure_your_site" site config and activate the macos site config
spack env activate -p -d envs_macos
spack install -v fv3-bundle-env 2>&1 | tee spack.install.fv3-bundle-env.log
spack install -v ufs-bundle-env 2>&1 | tee spack.install.ufs-bundle-env.log
spack module lmod refresh
./meta_modules/setup_meta_modules.py
```

