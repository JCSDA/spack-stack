<img src="https://user-images.githubusercontent.com/8006981/234488735-45b2c5fa-1de6-47ad-ae3b-4a6829ae49b9.png" width="425">

Spack-stack is a framework for installing software libraries to support
NOAA's Unified Forecast System (UFS) applications and the
Joint Effort for Data assimilation Integration (JEDI) coupled to
several Earth system prediction models (MPAS, NEPTUNE, UM, GEOS).

Spack-stack supports installations on a range of R&D and operational platforms.
It provides a set of installation templates (package lists), default package settings,
system configurations for a range of [macOS and Linux workstation, HPC, and cloud
platforms](https://spack-stack.readthedocs.io/en/latest/PreConfiguredSites.html), and Spack extensions, and uses a fork of the
[Spack repository](https://github.com/spack/spack). [Spack](https://spack.io/) is a
community-supported, multi-platform package manager
developed by Lawrence Livermore National Laboratory
(LLNL). Spack is provided as a submodule to spack-stack so that a
stable version can be referenced. For more information about Spack, see
the [LLNL project page for Spack](https://computing.llnl.gov/projects/spack-hpc-package-manager)
and the [Spack documentation](https://spack.readthedocs.io/en/latest/).

**To get started with spack-stack**, either by using an existing
installation on a [supported platform](https://spack-stack.readthedocs.io/en/latest/PreConfiguredSites.html)
or by [creating a new installation](https://spack-stack.readthedocs.io/en/latest/CreatingEnvironments.html), see the
[Getting Started](https://spack-stack.readthedocs.io/en/latest/Overview.html#getting-started) documentation page.
Full documentation with table of contents can be found at https://spack-stack.readthedocs.io/en/latest/.

Spack-stack is a collaborative effort between:
* [NOAA Environmental Modeling Center (EMC)](https://www.emc.ncep.noaa.gov/emc_new.php): [Alex Richert](https://www.github.com/AlexanderRichert-NOAA), [Hang Lei](https://www.github.com/Hang-Lei-NOAA), [Ed Hartnett](https://www.github.com/edwardhartnett)
* [UCAR Joint Center for Satellite Data Assimilation (JCSDA)](https://www.jcsda.org/): [Dom Heinzeller](https://www.github.com/climbfuji), [Steve Herbener](https://github.com/srherbener)
* [Earth Prediction Innovation Center (EPIC)](https://epic.noaa.gov/): [Cam Book](https://github.com/ulmononian), [Natalie Perlin](https://github.com/natalie-perlin)

For more information about the organization of the spack-stack
project, see the [Project Charter](project_charter.md).
