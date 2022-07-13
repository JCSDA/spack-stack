# spack-stack

Spack-stack enables the installation of software required
for HPC system deployments of NOAA's Unified Forecast System (UFS) and
other weather and climate models, including components of the Joint
Effort for Data assimilation Integration (JEDI).

Spack-stack is a collaborative effort between:
* [NOAA Environmental Modeling Center (EMC)](https://www.emc.ncep.noaa.gov/emc_new.php)
* [UCAR Joint Center for Satellite Data Assimilation (JCSDA)](https://www.jcsda.org/)
* [Earth Prediction Innovation Center (EPIC)](https://epic.noaa.gov/).

Spack-stack is a fork of the [spack](https://github.com/spack/spack)
repository. Spack is a community-supported, multi-platform,
Python-based package manager originally developed by the Lawrence
Livermore National Laboratory (LLNL). Spack is provided as a submodule
to spack-stack so that a stable version can be referenced. For more
information about spack see the [LLNL project page for
spack](https://computing.llnl.gov/projects/spack-hpc-package-manager)
and the [spack
documentation](https://spack.readthedocs.io/en/latest/).

The stack can be installed on a range of platforms, from Linux and
macOS laptops to HPC systems, and comes pre-configured for many
systems. Users can install the necessary packages for a particular
application and later add the missing packages for another application
without having to rebuild the entire stack.

spack-stack is mainly a collection of Spack configuration files, but
provides a Spack extension to simplify the installation process:

- `spack stack create` is provided to copy common, site-specific, and
  application-specific configuration files into a coherent Spack
  environment and to create container recipes

- `spack stack setup-meta-modules` creates compiler, MPI and Python
  meta-modules for a convenient setup of a user environment using
  modules (lua and tcl)

Documentation for installing and using spack-stack can be found here:
https://spack-stack.readthedocs.io/en/latest/

spack-stack is maintained by:

- [Kyle Gerheiser](https://www.github.com/kgerheiser), [Hang
  Lei](https://www.github.com/Hang-Lei-NOAA), [Ed
  Hartnett](https://www.github.com/edwardhartnett) NOAA-EMC

- [Dom Heinzeller](https://www.github.com/climbfuji), JCSDA

For more information about the organization of the spack-stack
project, see the [Project Charter](project_charter.md).

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
