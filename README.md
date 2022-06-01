# spack-stack

spack-stack is a collaborative effort between the NOAA Environmental Modeling Center (EMC), the UCAR Joint Center for Satellite Data Assimilation (JCSDA), and the Earth Prediction Innovation Center (EPIC). spack-stack is designed to support the various applications of the supporting agencies such as the Unified Forecast System (UFS) or the Joint Effort for Data assimilation Integration (JEDI). The stack can be installed on a range of platforms, from Linux and macOS laptops to HPC systems, and comes pre-configured for many systems. Users can install the necessary packages for a particular application and later add the missing packages for another application without having to rebuild the entire stack.

[spack](https://github.com/spack/spack) is a community-supported, multi-platform, Python-based package manager originally developed by the Lawrence Livermore National Laboratory (LLNL; https://computing.llnl.gov/projects/spack-hpc-package-manager). It is provided as a submodule so that a stable version can be referenced. [See the Spack Documentation for more information](https://spack.readthedocs.io/en/latest/)

spack-stack is mainly a collection of Spack configuration files, but provides a Spack extension to simplify the installation process:
- `spack stack create` is provided to copy common, site-specific, and application-specific configuration files into a coherent Spack environment and to create container recipes
- `spack stack setup-meta-modules` creates compiler, MPI and Python meta-modules for a convenient setup of a user environment using modules (lua and tcl)

Documentation for installing and using spack-stack can be found here:  https://spack-stack.readthedocs.io/en/latest

spack-stack is maintained by:
- Kyle Gerheiser (@kgerheiser), NOAA-EMC
- Dom Heinzeller (@climbfuji), JCSDA
- not yet appointed, EPIC

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
