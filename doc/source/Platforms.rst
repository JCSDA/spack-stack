.. _Platforms:

*************************
Platforms
*************************

==============================
Pre-configured sites
==============================

Directory ``configs/sites`` contains site configurations for several HPC systems, as well as reference configurations for macOS and Linux. The reference configurations are **not** meant to be used as is, as user setups and package versions vary considerably. They are merely for comparing new site configurations that are created following the instructions below to working setups.

Ready-to-use spack-stack installations are available on the following platforms:

**Note: this versions are for early testers - use at your own risk**

+-----------------------+---------------------------+---------------------------+
| System                | Maintained by (temporary) | jedi-ewok tested          |
+=======================+===========================+===========================+
| MSU Orion             | Dom Heinzeller            | yes                       |
+-----------------------+---------------------------+---------------------------+
| NASA Discover         | Dom Heinzeller            | yes                       |
+-----------------------+---------------------------+---------------------------+
| NCAR-Wyoming Cheyenne | Dom Heinzeller            | yes                       |
+-----------------------+---------------------------+---------------------------+
| NOAA NCO WCOSS2       |                           |                           |
+-----------------------+---------------------------+---------------------------+
| NOAA RDHPCS Gaea      | Dom Heinzeller            | yes                       |
+-----------------------+---------------------------+---------------------------+
| NOAA RDHPCS Hera      |                           |                           |
+-----------------------+---------------------------+---------------------------+
| NOAA RDHPCS Jet       |                           |                           |
+-----------------------+---------------------------+---------------------------+
| TACC Stampede2        | Dom Heinzeller            | install yes / not yet run |
+-----------------------+---------------------------+---------------------------+

+-----------------------+-------------------------------------------------------------------------------------------------------+
| System                | Location                                                                                              |
+=======================+=======================================================================================================+
| MSU Orion             | ``/work/noaa/gsd-hpcs/dheinzel/spack-stack-20220411-ewok-tmp``                                        |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NASA Discover         | ``/discover/swdev/jcsda/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.1/install``         |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.2/install`` |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA NCO WCOSS2       |                                                                                                       |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea      | ``/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v0.0.1``                                          |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera      |                                                                                                       |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet       |                                                                                                       |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| TACC Stampede2        | ``/work2/06146/tg854455/stampede2/spack-stack/spack-stack-0.0.1``                                     |
+-----------------------+-------------------------------------------------------------------------------------------------------+




For questions or problems, please consult the known issues in :numref:`Chapter %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/noaa-emc/spack-stack/issues>`_ and `discussions <https://github.com/noaa-emc/spack-stack/discussions>`_ first.



**MISSING**

------------------------------
NOAA RDHPCS Gaea
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module unload intel
   module unload cray-mpich
   module unload cray-python
   module unload darshan
   module load cray-python/3.7.3.2

------------------------------
TACC Stampede2
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   source /work2/06146/tg854455/stampede2/spack-stack/intel-oneapi-2022.2/setvars.sh
   module use /work2/06146/tg854455/stampede2/spack-stack/modulefiles
   module load miniconda/3.9.7

==============================
Generating new site configs
==============================
Recommended: Start with an empty (default) site config. Then run ``spack external find`` to locate external packages such as build tools and a few other packages. Next, run ``spack compiler find`` to locate compilers in your path. Compilers or external packages with modules may need to be loaded prior to running ``spack external find``, or added manually. The instructions differ slightly for macOS and Linux and assume that the prerequisites for the platform have been installed as described in **MISSING**.

It is also instructive to peruse the GitHub actions scripts in ``.github/workflows`` and ``.github/actions`` to see how automated spack-stack builds are configured for CI testing, as well as the existing site configs in ``configs/sites``, in particular the reference site configs for macOS (**NEEDS UPDATE**) and Linux (**MISSING**).

------------------------------
macOS
------------------------------

On macOS, it is important to use certain Homebrew packages as external packages, because the native macOS packages are incomplete (e.g. missing the development header files): ``curl``, ``python``, ``qt``, etc. The instructions provided in the following have been tested extensively on many macOS installations.

.. code-block:: console

   # Create a preconfigured environment with a default (nearly empty) site config
   spack stack create env --site default --app jedi-ufs --name jedi-ufs.mymacos

   # Temporarily set environment variable SPACK_SYSTEM_CONFIG_PATH to
   # modify site config files in envs/jedi-ufs.mymacos/site
   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mymacos/site"

   # Find external packages, add to packages.yaml
   spack external find --scope system
   spack external find --scope system perl
   spack external find --scope system python
   spack external find --scope system wget

   # If the curl bin directory hasn't been added to PATH, need to prefix command
   PATH="/usr/local/Cellar/curl/7.83.0/bin:$PATH" \
        spack external find --scope system curl

   # If the qt5 bin directory hasn't been added to PATH, need to prefix command
   PATH="/usr/local/opt/qt5/bin:$PATH" \
       spack external find --scope system qt

   # Optional, only if planning to build jedi-tools environment with LaTeX support
   # If the texlive bin directory hasn't been added to PATH, need to prefix command
   PATH="/usr/local/texlive/2022/bin/universal-darwin:$PATH" \
       spack external find --scope system texlive

   # Find compilers, add to compilers.yaml
   spack compiler find --scope system

   # Do NOT forget to unset the SPACK_SYSTEM_CONFIG_PATH environment variable!
   export -n SPACK_SYSTEM_CONFIG_PATH

   # Optionally edit site config files and common config files, for example to
   # remove duplicate versions of external packages that are unwanted
   vi envs/jedi-ufs.mymacos/spack.yaml
   vi envs/jedi-ufs.mymacos/packages.yaml
   vi envs/jedi-ufs.mymacos/site/*.yaml

   # Process the specs and install
   spack concretize
   spack install [--verbose] [--fail-fast]

   # Create lua module files
   spack module lmod refresh

   # Create meta-modules for compiler, mpi, python
   spack stack setup-meta-modules

------------------------------
Linux
------------------------------

Note. Some older Linux systems do not support ``lua/lmod`` environment modules, which are default in the spack-stack site configs. This can be changed to ``tcl/tk`` environment modules (see below).

.. code-block:: console

   # Create a preconfigured environment with a default (nearly empty) site config
   spack stack create env --site default --app jedi-ufs --name jedi-ufs.mylinux

   # Temporarily set environment variable SPACK_SYSTEM_CONFIG_PATH to
   # modify site config files in envs/jedi-ufs.mylinux/site
   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mylinux/site"

   # Find external packages, add to packages.yaml
   spack external find --scope system

   # MISSING - ADDITIONAL PACKAGES ADDED AS EXTERNALS, AND MODIFICATIONS OF PACKAGE VARIANTS ETC
   ...

   # Find compilers, add to compilers.yaml
   spack compiler find --scope system

   # Do NOT forget to unset the SPACK_SYSTEM_CONFIG_PATH environment variable!
   export -n SPACK_SYSTEM_CONFIG_PATH

   # Optionally edit site config files and common config files, for example to
   # remove duplicate versions of external packages that are unwanted
   vi envs/jedi-ufs.mylinux/spack.yaml
   vi envs/jedi-ufs.mylinux/packages.yaml
   vi envs/jedi-ufs.mylinux/site/*.yaml

   # Modules can be switched from ``lua/lmod`` to ``tcl/tk``
   # in envs/jedi-ufs.mylinux/site/modules.yaml

   # Process the specs and install
   spack concretize
   spack install [--verbose] [--fail-fast]

   # Create lua module files replace lmod with tcl, if necessary
   spack module lmod refresh

   # Create meta-modules for compiler, mpi, python
   spack stack setup-meta-modules

