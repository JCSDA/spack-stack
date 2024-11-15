# Provisiong NRL ParallelWorks AWS clusters

## Steps to perform before installing spack-stack develop as of 2024/11/24

Note. Some of these packages may already be installed, but for the sake of completeness, they are listed here.
```
sudo su -
chmod 777 /contrib

yum install -y gcc-toolset-13
yum install -y gcc-toolset-13-runtime
yum install -y gcc-toolset-13-binutils
yum install -y gcc-toolset-13-gcc
yum install -y gcc-toolset-13-gcc-c++
yum install -y gcc-toolset-13-gcc-gfortran
yum install -y gcc-toolset-13-gdb

yum install -y binutils-devel
yum install -y m4
yum install -y wget
yum install -y git
yum install -y git-lfs
yum install -y bash-completion
yum install -y bzip2 bzip2-devel
yum install -y unzip
yum install -y patch
yum install -y automake
yum install -y xorg-x11-xauth
yum install -y xterm
yum install -y perl-IPC-Cmd
yum install -y gettext-devel
yum install -y texlive
yum install -y bison
yum install -y screen

yum install -y qt5-qtbase
yum install -y qt5-qttools-devel
yum install -y qt5-qtsvg-devel
```

For instructions for building spack-stack, see the spack-stack documentation on readthedocs (https://spack-stack.readthedocs.io/en/latest). For instructions for using pre-built spack-stack environments, see the spack-stack wiki (https://github.com/JCSDA/spack-stack/wiki).
