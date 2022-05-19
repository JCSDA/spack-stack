# macOS

## General instructions/prerequisites

This instructions are meant to be a reference that users can follow to set up their own system. Depending on the user's setup and needs, some steps will differ, some may not be needed and others may be missing. Also, the package versions may change over time. This setup is valid as of 2022/03/01.

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
brew install python@3.9.10
brew install git@2.34.1
brew install git-lfs@3.0.2
brew install lmod@8.6.6
brew install wget@1.21.2
brew install bash@5.1.16
brew install curl@7.82.0
brew install cmake@3.22.1
brew install openssl@1.1
# Note - need to pin to version 5, not 6
brew install qt@5.15.3
```
- Activate the `lua` module environment:
```
source /usr/local/opt/lmod/init/profile
```

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

### Install MacTeX
If the `jedi-tools`` application is built with variant `+latex` to enable building LaTeX/PDF documentation, install MacTeX (https://www.tug.org/mactex) and configure your shell to have it in the search path, for example:
```
export PATH="/usr/local/texlive/2022/bin/universal-darwin:$PATH"
```

### Temporary workaround for pip installs in spack
See https://github.com/spack/spack/issues/29308
```
which pip3
# make sure this points to homebrew's pip3
pip3 install poetry
# test - successful if no output
python3 -c "import poetry"
```

### Known issues
1. Error `invalid argument '-fgnu89-inline' not allowed with 'C++'`
This error came up on macOS Monterey with mpich-3.4.3 installed via homebrew when trying to build the jedi bundles that use `ecbuild`. The reason was that the C compiler flag `-fgnu89-inline` from `/usr/local/Cellar/mpich/3.4.3/lib/pkgconfig/mpich.pc` was added to the C++ compiler flags by ecbuild. The solution was to set
`CC=mpicc FC=mpif90 CXX=mpicxx` when calling `ecbuild` for those bundles.
2. Installation of `poetry` using `pip3` or test with `python3` fails
This can happen when multiple versions of Python were installed with `brew` and `pip3`/`python3` point to different versions. Run `brew doctor` and check if there are issues with Python not being properly linked. Follow the instructions given by `brew`, if applicable.
3. Errors handling exceptions on macOS. A large number of errors handling exceptions thrown by applications was found when using default builds of mpich or openmpi, which use flat
namespaces. This is the case for both mpich and openmpi when installed via homebrew. With our spack version, mpich and openmpi can be installed with a `+two_level_namespace` option that fixes the problem (tested with mpich-3.4.2 and openmpi-4.1.3).