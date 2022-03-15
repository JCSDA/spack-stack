# Gaea
## General instructions/prerequisites

### Set up the user environment for working with spack/building new software environments
```
module unload intel
module unload cray-mpich
module unload cray-python
module unload darshan
module load cray-python/3.7.3.2
```

### Known issues
1. Random "permission denied" errors during the spack install phase
If random errors during the spack install phase occur related to "permission denied" when building packages, edit `envs/env_name/config.yaml` and comment out the lines `build_stage` and `test_stage`.
