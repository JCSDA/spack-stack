.. _Overview:

Overview
*************************

spack-stack is a collaborative effort between the NOAA Environmental Modeling Center (EMC), the UCAR Joint Center for Satellite Data Assimilation (JCSDA), and the Earth Prediction Innovation Center (EPIC). spack-stack is designed to support the various applications of the supporting agencies such as the Unified Forecast System (UFS) or the Joint Effort for Data assimilation Integration (JEDI). The stack can be installed on a range of platforms, from Linux and macOS laptops to HPC systems, and comes pre-configured for many systems. Users can install the necessary packages for a particular application and later add the missing packages for another application without having to rebuild the entire stack.

 `Spack <https://github.com/spack/spack>`_ is a community-supported, multi-platform, Python-based package manager originally developed by the Lawrence Livermore National Laboratory (LLNL; https://computing.llnl.gov/projects/spack-hpc-package-manager). It is provided as a submodule so that a stable version can be referenced. See the `Spack Documentation <https://spack.readthedocs.io/en/latest>`_ for more information.

spack-stack is mainly a collection of Spack configuration files, but provides a Spack extension to simplify the installation process (see :numref:`Section %s <SpackStackExtension>` for details):

- ``spack stack create`` is provided to copy common, site-specific, and application-specific configuration files into a coherent Spack environment and to create container recipes

- ``spack stack setup-meta-modules`` creates compiler, MPI and Python meta-modules for a convenient setup of a user environment using modules (``lua`` and ``tcl``)

spack-stack is maintained by:

- Alex Richert (@AlexanderRichert-NOAA), NOAA-EMC

- Dom Heinzeller (@climbfuji), JCSDA

- not yet appointed, EPIC

.. note::
   spack-stack is in early development and not yet ready for use. Instructions may be incomplete or invalid.


===============
Getting Started
===============

Many of supported platforms ready-to-use spack-stack installations already available locally. You can see a list of those sites and site-specific instructions and caveats in :numref:`Section %s <Preconfigured_Sites>`.

If you are a developer looking to build and run software locally using spack-stack, or if you are looking to install spack-stack on a new platform you can follow the instructions in :numref:`Section %s <NewSiteConfigs>`.
