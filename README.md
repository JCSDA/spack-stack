# spack-stack

spack-stack is a collaborative effort between the NOAA Environmental Modeling Center (EMC), the UCAR Joint Center for Satellite Data Assimilation (JCSDA), and the Earth Prediction Innovation Center (EPIC). spack-stack is designed to support the various applications of the supporting agencies such as the Unified Forecast System (UFS) or the Joint Effort for Data assimilation Integration (JEDI). The stack can be installed on a range of platforms, from Linux and macOS laptops to HPC systems, and comes pre-configured for many systems. Users can install the necessary packages for a particular application and later add the missing packages for another application without having to rebuild the entire stack.

[spack](https://github.com/spack/spack) is a community-supported, multi-platform, Python-based package manager originally developed by the Lawrence Livermore National Laboratory (LLNL; https://computing.llnl.gov/projects/spack-hpc-package-manager). It is provided as a submodule so that a stable version can be referenced. [See the Spack Documentation for more information](https://spack.readthedocs.io/en/latest/)

spack-stack is mainly a collection of Spack configuration files, but provides a few Python scripts to simplify the installation process:
- `create-env.py` is provided to copy common, site-specific, and application-specific configuration files into a coherent Spack environment
- `meta_modules/setup_meta_modules.py` creates compiler, MPI and Python meta-modules for a convenient setup of a user environment using modules (currently lua only)

spack-stack is maintained by:
- Kyle Gerheiser (@kgerheiser), NOAA-EMC
- Dom Heinzeller (@climbfuji), JCSDA
- not yet appointed, EPIC

Ready-to-use spack-stack installations are available on the following platforms:

**Note: this versions are for early testers - use at your own risk**

| System                | Location                                                                                            | Maintained by (temporary) |
| --------------------- | --------------------------------------------------------------------------------------------------- | ------------------------- |
| MSU Orion             | `/work/noaa/gsd-hpcs/dheinzel/spack-stack-20220411-ewok-tmp`                                        | Dom Heinzeller            |
| NASA Discover         | `/discover/swdev/jcsda/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.1/install`         | Dom Heinzeller            |
| NCAR-Wyoming Cheyenne | `/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.2/install` | Dom Heinzeller            |
| NOAA NCO WCOSS2       |                                                                                                     |                           |
| NOAA RDHPCS Gaea      | `/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v0.0.1`                                          | Dom Heinzeller            |
| NOAA RDHPCS Hera      |                                                                                                     |                           |
| NOAA RDHPCS Jet       |                                                                                                     |                           |

For questions or problems, please consult the currently open [issues](https://github.com/noaa-emc/spack-stack/issues) and the [current and past discussions](https://github.com/noaa-emc/spack-stack/discussions) first.

**Note. spack-stack is in early development and not yet ready for use. Instructions may be incomplete or invalid.**

## Quickstart

```
git clone https://github.com/NOAA-EMC/spack-stack.git
cd spack-stack

# Ensure Python 3.7+ is available and the default before sourcing spack

# Sources Spack from submodule and sets ${SPACK_STACK_DIR}
source setup.sh

# See a list of sites and apps
./create-env.py -h

# Creates a pre-configured Spack environment in envs/<app>.<site>
# Copies site-specific, application-specific, and common config files into the environment directory
./create-env.py --site hera --app jedi-fv3 --name jedi-fv3.hera

# Activate the newly created environment
# Optional: decorate the command line prompt using -p
#     Note: in some cases, this can mess up long lines in bash
#     because color codes are not escaped correctly. In this
#     case, use export SPACK_COLOR='never' first.
spack env activate [-p] envs/jedi-fv3.hera

# Optionally edit config files (spack.yaml, packages.yaml compilers.yaml, site.yaml)
cd envs/jedi-fv3.hera
emacs spack.yaml
emacs common/*.yaml
emacs site/*.yaml

# Process the specs and install
# Note: both steps will take some time!
spack concretize
spack install

# Create lua module files
spack module lmod refresh

# Create meta-modules for compiler, mpi, python
./meta_modules/setup_meta_modules.py
```

## Disclaimer

The United States Department of Commerce (DOC) GitHub project code is
provided on an "as is" basis and the user assumes responsibility for
its use. DOC has relinquished control of the information and no longer
has responsibility to protect the integrity, confidentiality, or
availability of the information. Any claims against the Department of
Commerce stemming from the use of its GitHub project will be governed
by all applicable Federal law. Any reference to specific commercial
products, processes, or services by service mark, trademark,
manufacturer, or otherwise, does not constitute or imply their
endorsement, recommendation or favoring by the Department of
Commerce. The Department of Commerce seal and logo, or the seal and
logo of a DOC bureau, shall not be used in any manner to imply
endorsement of any commercial product or activity by DOC or the United
States Government.
