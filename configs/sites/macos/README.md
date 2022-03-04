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
- Activate the `lua` module environment:
```
source /usr/local/opt/lmod/init/profile
```

This environment enables working with spack and building new software environents, as well as loading modules that are created by spack for building JEDI and UFS software.

### Temporary workaround for pip installs in spack
See https://github.com/spack/spack/issues/29308
```
which pip3
# make sure this points to homebrew's pip3
pip3 install poetry
```
