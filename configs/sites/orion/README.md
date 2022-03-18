# Orion

## General instructions/prerequisites

module purge

### One-off: prepare miniconda python3 environment
See instructions in miniconda/README.md. Don't forget to log off and back on to forget about the conda environment.

### Set up the user environment for working with spack/building new software environments
This needs to be done every time before installing packages with spack or before using spack-provided modules!

Note. Temporary location, this needs to be moved elsewhere.
```
module use /work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles
module load miniconda/3.9.7
```
