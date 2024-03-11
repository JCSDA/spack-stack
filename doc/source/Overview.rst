.. _Overview:

Overview
*************************

spack-stack is a collaborative effort between the NOAA Environmental Modeling Center (EMC), the UCAR Joint Center for Satellite Data Assimilation (JCSDA), and the Earth Prediction Innovation Center (EPIC). spack-stack is designed to support the various applications of the supporting agencies such as the Unified Forecast System (UFS) or the Joint Effort for Data assimilation Integration (JEDI). The stack can be installed on a range of platforms, from Linux and macOS laptops to HPC systems, and comes pre-configured for many systems. Users can install the necessary packages for a particular application and later add the missing packages for another application without having to rebuild the entire stack.

 `Spack <https://github.com/spack/spack>`_ is a community-supported, multi-platform, Python-based package manager originally developed by the Lawrence Livermore National Laboratory (LLNL; https://computing.llnl.gov/projects/spack-hpc-package-manager). It is provided as a submodule so that a stable version can be referenced. See the `Spack Documentation <https://spack.readthedocs.io/en/latest>`_ for more information.

spack-stack is mainly a collection of Spack configuration files, but provides a Spack extension to simplify the installation process (see :numref:`Section %s <SpackStackExtension>` for details):

- ``spack stack create`` is provided to copy common, site-specific, and application-specific configuration files into a coherent Spack environment and to create container recipes

- ``spack stack setup-meta-modules`` creates compiler, MPI and Python meta-modules for a convenient setup of a user environment using modules (``lua`` and ``tcl``)

spack-stack is maintained by:

- Alex Richert (@AlexanderRichert-NOAA), Hang Lei (@Hang-Lei-NOAA) and Ed Hartnett (@edwardhartnett), NOAA-EMC

- Dom Heinzeller (@climbfuji) and Steve Herbener (@srherbener), JCSDA

- Cameron Book (@ulmononian), Natalie Perlin (@natalie-perlin) and Ratko Vasic (@ratkovasic-noaa), EPIC

===============
Getting started
===============

If you wish to **access an existing spack-stack installation** on a given system, such as to load packages and compile and run a UFS or JEDI application, see the instructions in :numref:`Section %s <UsingSpackEnvironments>`. Ready-to-use spack-stack installations are available on a number of HPC and cloud platforms. A list of those platforms, along with special instructions and caveats for each, can be found in :numref:`Section %s <Preconfigured_Sites>`.

If you wish to quickly **create a new spack-stack environment (stack installation)**, either on a personal machine or on a supported platform where you are the maintainer, see :numref:`Section %s <CreatingEnvironment>`. To find other details related to maintaining installations, including problematic packages and system-specific issues, see :numref:`Section %s <MaintainersSection>`.

If you wish to **chain a new spack-stack environment to an existing installation**, such as to test a new package version on one of our supported HPC or cloud platforms based on already installed dependencies, see :numref:`Section %s <Add_Test_Packages>`.

If you wish to **create a new site configuration** on a not-yet supported machine, including detailed instructions for Linux and macOS workstations, see :numref:`Section %s <NewSiteConfigs>`.

.. note::
   As spack-stack is intended to support NOAA EMC, JCSDA, and EPIC applications, users seeking to install software for other purposes, such as developing non-NOAA/JCSDA/EPIC applications, even those that use weather-related libraries, are recommended to simply use `Spack <https://github.com/spack/spack>`_ instead.
