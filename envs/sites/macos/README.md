#### macOS

##### Prerequisites

- Setup of x86_64 environment on arch64 systems
- Install command line utilities
- Install homebrew for x86_64 environment

It is recommended to install the following prerequisites via Homebrew, as installing them with Spack and Apple's native clang can be tricky.
```
brew install gcc@11.2.0
llvm ?
brew install mpich@3.4.3
brew install python@3.8.9
brew install git@2.34.1
brew install git-lfs@3.0.2
wget
# eccodes
# libtiff .. maybe not needed (skip)

````


To use the bundled libc++ please add the following LDFLAGS:
  LDFLAGS="-L/usr/local/opt/llvm/lib -Wl,-rpath,/usr/local/opt/llvm/lib"

llvm is keg-only, which means it was not symlinked into /usr/local,
because macOS already provides this software and installing another version in
parallel can cause all kinds of trouble.

If you need to have llvm first in your PATH, run:
  echo 'export PATH="/usr/local/opt/llvm/bin:$PATH"' >> ~/.profile

For compilers to find llvm you may need to set:
  export LDFLAGS="-L/usr/local/opt/llvm/lib"
  export CPPFLAGS="-I/usr/local/opt/llvm/include"