# spack-stack

Spack-stack makes it easy to build JEDI and UFS application environments using Spack, and comes pre-configured for many systems.

[Spack](https://github.com/spack/spack) is a mutli-platform, Python based, package manager suitable for HPC and workstation use. It is provided as a submodule so that a stable version can be referenced.

spack-stack is mainly a collection of Spack configuration files, but a simple Python script, `create-env.py`, is provided to copy common, site-specific, and application-specific configuration files into a coherent Spack environment.

[See the Spack Documentation for more information](https://spack.readthedocs.io/en/latest/)

## Quickstart

```
git clone https://github.com/NOAA-EMC/spack-stack.git
cd spack-stack

# Sources Spack from submodule and sets ${SPACK_STACK_DIR}
source setup.sh

# See a list of sites and apps
./create-env.py -h

# Creates a pre-configured Spack environment in envs/<app>.<site>
# Copies site-specific, application-specific, and common config files into the environment directory
./create-env.py --site hera --app jedi-fv3 --name jedi-fv3.hera

# Activate spack environment; optional: decorate the command line prompt
spack env activate [-p] envs/jedi-fv3.hera

# Optionally edit config files (spack.yaml, packages.yaml compilers.yaml, site.yaml)
emacs envs/jedi-fv3.hera/spack.yaml

# Process the specs and install
spack concretize
spack install

# Create lua module files
spack module lmod refresh

# Create meta modules for compiler, mpi, python
./meta_modules/setup_meta_modules.py
```
