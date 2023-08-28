![spack-stack-logo](https://user-images.githubusercontent.com/8006981/234488735-45b2c5fa-1de6-47ad-ae3b-4a6829ae49b9.png)

Spack-stack enables the installation of software required
for HPC system deployments of NOAA's Unified Forecast System (UFS) and
other weather and climate models, including components of the Joint
Effort for Data assimilation Integration (JEDI).

Spack-stack is a collaborative effort between:
* [NOAA Environmental Modeling Center (EMC)](https://www.emc.ncep.noaa.gov/emc_new.php)
* [UCAR Joint Center for Satellite Data Assimilation (JCSDA)](https://www.jcsda.org/)
* [Earth Prediction Innovation Center (EPIC)](https://epic.noaa.gov/).

Spack-stack is a thin layer around a fork of the
[spack](https://github.com/spack/spack) repository. Spack is a
community-supported, multi-platform, Python-based package manager
originally developed by the Lawrence Livermore National Laboratory
(LLNL). Spack is provided as a submodule to spack-stack so that a
stable version can be referenced. For more information about spack see
the [LLNL project page for
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

- NOAA-EMC: [Alex Richert](https://www.github.com/AlexanderRichert-NOAA), [Hang
  Lei](https://www.github.com/Hang-Lei-NOAA), [Ed
  Hartnett](https://www.github.com/edwardhartnett)
- JCSDA: [Dom Heinzeller](https://www.github.com/climbfuji), [Steve Herbener](https://github.com/srherbener)
- EPIC: [Cam Book](https://github.com/ulmononian), [Natalie Perlin](https://github.com/natalie-perlin)

For more information about the organization of the spack-stack
project, see the [Project Charter](project_charter.md).
