# Stampede2

## General instructions/prerequisites

```
module purge
```

### One-off: prepare miniconda python3 environment
See instructions in `miniconda/README.md`. Don't forget to log off and back on to forget about the conda environment.

### One-off: install Intel oneAPI compilers

```
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18679/l_HPCKit_p_2022.2.0.191.sh
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18673/l_BaseKit_p_2022.2.0.262.sh
# Customize the installations to, for example, install in
# /work2/06146/tg854455/stampede2/spack-stack/intel-oneapi-2022.2
sh l_BaseKit_p_2022.2.0.262.sh
sh l_HPCKit_p_2022.2.0.191.sh
```

### One-off: install git-lfs

```
module purge
cd /work2/06146/tg854455/stampede2/spack-stack/

mkdir -p git-lfs-1.2.1/src
cd git-lfs-1.2.1/src
wget --content-disposition https://packagecloud.io/github/git-lfs/packages/el/7/git-lfs-1.2.1-1.el7.x86_64.rpm/download.rpm
rpm2cpio git-lfs-1.2.1-1.el7.x86_64.rpm | cpio -idmv
mv usr/* ../
```
Create module file `/work2/06146/tg854455/stampede2/spack-stack/modulefiles/git-lfs/1.2.1` with contents:
```
#%Module1.0

module-whatis "Provides git-lfs-1.2.1 for use with spack."

conflict git-lfs

proc ModulesHelp { } {
puts stderr "Provides git-lfs-1.2.1 for use with spack."
}

# Set this value
set GITLFS_PATH "/work2/06146/tg854455/stampede2/spack-stack/git-lfs-1.2.1"

prepend-path PATH "${GITLFS_PATH}/bin"
prepend-path MANPATH "${GITLFS_PATH}/share/man"
```

### Set up the user environment for working with spack/building new software environments
This needs to be done every time before installing packages with spack or before using spack-provided modules!
```
module purge
source /work2/06146/tg854455/stampede2/spack-stack/intel-oneapi-2022.2/setvars.sh
module use /work2/06146/tg854455/stampede2/spack-stack/modulefiles
module load miniconda/3.9.7
```
