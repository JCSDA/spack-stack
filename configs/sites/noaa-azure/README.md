# NOAA AWS Parallel Works
## General instructions/prerequisites

### Set up the user environment for working with spack/building new software environments
```
# Remove default module locations.
module unuse /opt/cray/craype/default/modulefiles
module unuse opt/cray/modulefiles
# Add git-lfs and some other utilities to your PATH
export PATH="${PATH}:/contrib/spack-stack/apps/utils/bin"

module use /contrib/spack-stack/modulefiles/core
module load miniconda/3.9.7
```

### Known issues
1. With default modulepath, Spack will detect the system as Cray because of modulepath.
2. libxml2 won't untar because of an issue with the filesystem, so use libxml2 as external
