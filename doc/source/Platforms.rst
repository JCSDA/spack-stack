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

+------------------------+---------------------------+---------------------------+
| System                 | Maintained by (temporary) | jedi-ewok tested          |
+========================+===========================+===========================+
| MSU Orion              | Dom Heinzeller            | yes                       |
+------------------------+---------------------------+---------------------------+
| NASA Discover          | Dom Heinzeller            | yes                       |
+------------------------+---------------------------+---------------------------+
| NCAR-Wyoming Cheyenne  | Dom Heinzeller            | yes                       |
+------------------------+---------------------------+---------------------------+
| NOAA NCO WCOSS2        |                           |                           |
+------------------------+---------------------------+---------------------------+
| NOAA RDHPCS Gaea       | Dom Heinzeller            | yes                       |
+------------------------+---------------------------+---------------------------+
| NOAA RDHPCS Hera       |                           |                           |
+------------------------+---------------------------+---------------------------+
| NOAA RDHPCS Jet        |                           |                           |
+------------------------+---------------------------+---------------------------+
| TACC Stampede2         | Dom Heinzeller            | install yes / not yet run |
+------------------------+---------------------------+---------------------------+
| UW (Univ. of Wisc.) S4 | Dom Heinzeller            |                           |
+------------------------+---------------------------+---------------------------+

+------------------------+-------------------------------------------------------------------------------------------------------+
| System                 | Location                                                                                              |
+========================+=======================================================================================================+
| MSU Orion              | ``/work/noaa/da/role-da/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.1.2/install``         |
+------------------------+-------------------------------------------------------------------------------------------------------+
| NASA Discover          | ``/discover/swdev/jcsda/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.1/install``         |
+------------------------+-------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne  | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.2/install`` |
+------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA NCO WCOSS2        |                                                                                                       |
+------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea       | ``/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v0.0.2/envs/jedi-all-intel-2021.3.0/install``     |
+------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera       |                                                                                                       |
+------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet        |                                                                                                       |
+------------------------+-------------------------------------------------------------------------------------------------------+
| TACC Stampede2         | ``/work2/06146/tg854455/stampede2/spack-stack/spack-stack-0.0.1/envs/ENV_DIR_MISSING/install``        |
+------------------------+-------------------------------------------------------------------------------------------------------+
| UW (Univ. of Wisc.) S4 |                                                                                                       |
+------------------------+-------------------------------------------------------------------------------------------------------+

For questions or problems, please consult the known issues in :numref:`Chapter %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/noaa-emc/spack-stack/issues>`_ and `discussions <https://github.com/noaa-emc/spack-stack/discussions>`_ first.

------------------------------
NASA Discover
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7

------------------------------
NOAA RDHPCS Gaea
------------------------------

The following is required for building new spack environments and for using spack to build and run software. Don't use ``module purge`` on Gaea!

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

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.7

==============================
Generating new site configs
==============================
In general, the recommended approach is as follows (see following sections for specific examples): Start with an empty (default) site config. Then run ``spack external find`` to locate external packages such as build tools and a few other packages. Next, run ``spack compiler find`` to locate compilers in your path. Compilers or external packages with modules may need to be loaded prior to running ``spack external find``, or added manually. The instructions differ slightly for macOS and Linux and assume that the prerequisites for the platform have been installed as described in **MISSING**.

It is also instructive to peruse the GitHub actions scripts in ``.github/workflows`` and ``.github/actions`` to see how automated spack-stack builds are configured for CI testing, as well as the existing site configs in ``configs/sites``, in particular the reference site configs for macOS (**NEEDS UPDATE**) and Linux (**MISSING**).

------------------------------
macOS
------------------------------

On macOS, it is important to use certain Homebrew packages as external packages, because the native macOS packages are incomplete (e.g. missing the development header files): ``curl``, ``python``, ``qt``, etc. The instructions provided in the following have been tested extensively on many macOS installations.

The instructions below also assume a clean Homebrew installation with a clean Python installation inside. This means that the Homebrew Python only contains nothing but what gets installed with ``pip install poetry`` (which is a temporary workaround). If this is not the case, users can try to install a separate Python using Miniconda as described in **MISSING REF TO MAINTAINERSSECTION**.

Further, it is recommended to not use ``mpich`` or ``openmpi`` installed by Homebrew, because these packages are built using a flat namespace that is incompatible with the JEDI software. The spack-stack installations of ``mpich`` and ``openmpi`` use two-level namespaces as required.

Prerequisites (one-off)
-----------------------

This instructions are meant to be a reference that users can follow to set up their own system. Depending on the user's setup and needs, some steps will differ, some may not be needed and others may be missing. Also, the package versions may change over time.

1. Install Apple's command line utilities

   - Launch the Terminal, found in ``/Applications/Utilities``

   - Type the following command string:

.. code-block:: console

   xcode-select --install

2. This step is only required on the new ``aarch64`` systems that are equipped with a Apple M1 silicon chip: Setup of ``x86_64`` environment on ``aarch64`` systems

   - Open Applications in Finder

   - Duplicate your preferred terminal application (e.g. Terminal or iTerm)

   - Rename the duplicate to, for example, "Terminal x86_64"

   - Right-click / control+click on "Terminal x86_64", choose "Get Info"

   - Select the box "Open using Rosetta" and close the window

3. Install Homebrew for ``x86_64`` environment

   - If your system is an ``aarch64`` system, make sure to open the newly created "Terminal x86_64" application. Type ``arch`` in the terminal to confirm, if correct the output is ``i386`` (and not ``arm64``)

   - Install Homebrew from the command line. On ``x86_64`` systems and on ``aarch64`` systems using the ``x86_64`` emulator, Homebrew` is installed in ``/usr/local``

   - It is recommended to install the following prerequisites via Homebrew, as installing them with Spack and Apple's native clang compiler can be tricky.

.. code-block:: console

   brew install coreutils
   brew install gcc
   brew install python
   brew install git
   brew install git-lfs
   brew install lmod
   brew install wget
   brew install bash
   brew install curl
   brew install cmake
   brew install openssl
   # Note - need to pin to version 5
   brew install qt@5.15.3

4. Activate the ``lua`` module environment

.. code-block:: console

   source /usr/local/opt/lmod/init/profile

5. **MISSING** Install xquartz

6. Temporary workaround for pip installs in spack (see https://github.com/spack/spack/issues/29308)

.. code-block:: console

   which pip3
   # make sure this points to homebrew's pip3
   pip3 install poetry
   # test - successful if no output
   python3 -c "import poetry"

7. Optional: Install MacTeX if planning to build the ``jedi-tools`` environment with LaTeX/PDF support

   If the ``jedi-tools`` application is built with variant ``+latex`` to enable building LaTeX/PDF documentation, install MacTeX 
   `MacTeX  <https://www.tug.org/mactex>`_ and configure your shell to have it in the search path, for example:

.. code-block:: console

   export PATH="/usr/local/texlive/2022/bin/universal-darwin:$PATH"

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

Creating a new environment
--------------------------

Remember to activate the ``lua`` module environment and have MacTeX in your search path, if applicable. It is also recommended to increase the stacksize limit to 65Kb using ``ulimit -S -s unlimited``.

1. Create a pre-configured environment with a default (nearly empty) site config

.. code-block:: console

   spack stack create env --site default --app jedi-ufs --name jedi-ufs.mymacos

2. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/jedi-ufs.mymacos/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mymacos/site"


3. Find external packages, add to site config's ``packages.yaml``

.. code-block:: console

   spack external find --scope system
   spack external find --scope system perl
   spack external find --scope system python
   spack external find --scope system wget

   #If the curl bin directory hasn't been added to PATH, need to prefix command
   PATH="/usr/local/Cellar/curl/7.83.0/bin:$PATH" \
        spack external find --scope system curl

   # If the qt5 bin directory hasn't been added to PATH, need to prefix command
   PATH="/usr/local/opt/qt5/bin:$PATH" \
       spack external find --scope system qt

   # Optional, only if planning to build jedi-tools environment with LaTeX support
   # The texlive bin directory must have been added to PATH (see above)
   spack external find --scope system texlive

4. Find compilers, add to site config's ``compilers.yaml``

.. code-block:: console

   spack compiler find --scope system

5. Do **not** forget to unset the ``SPACK_SYSTEM_CONFIG_PATH`` environment variable!

.. code-block:: console

   export -n SPACK_SYSTEM_CONFIG_PATH

6. Set default compiler and MPI library and flag Python as non-buildable

.. code-block:: console

   spack config add "packages:python:buildable:False"
   spack config add "packages:all:providers:mpi:[openmpi@4.1.3]"
   spack config add "packages:all:compiler:[apple-clang@13.1.6]"

7. If ``mpich`` or ``openmpi`` are installed with spack-stack, whitelist the mpi provider so that spack creates the module

.. code-block:: console

   spack config add "modules:default:lmod:whitelist:[openmpi]"

8. Turn off OpenMP for a number of packages when using ``apple-clang`` or ``clang``

.. code-block:: console

   spack config add "packages:wgrib2:variants: ~openmp"
   spack config add "packages:fms:variants: ~openmp"
   spack config add "packages:fms-jcsda:variants: ~openmp"

9. Optionally edit site config files and common config files, for example to emove duplicate versions of external packages that are unwanted

.. code-block:: console

   vi envs/jedi-ufs.mymacos/spack.yaml
   vi envs/jedi-ufs.mymacos/packages.yaml
   vi envs/jedi-ufs.mymacos/site/*.yaml

10. Process the specs and install

.. code-block:: console

   spack concretize
   spack install [--verbose] [--fail-fast]

11. Create lua module files

.. code-block:: console

   spack module lmod refresh

12. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules

------------------------------
Linux
------------------------------

Note. Some older Linux systems do not support ``lua/lmod`` environment modules, which are default in the spack-stack site configs. This can be changed to ``tcl/tk`` environment modules (see below).

Prerequisites (one-off)
-----------------------

**MISSING**

Creating a new environment
--------------------------

1. Create a pre-configured environment with a default (nearly empty) site config

.. code-block:: console

   spack stack create env --site default --app jedi-ufs --name jedi-ufs.mylinux

2. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/jedi-ufs.mymacos/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mylinux/site"

3. Find external packages, add to site config's ``packages.yaml``

.. code-block:: console

   spack external find --scope system

   # MISSING - ADDITIONAL PACKAGES ADDED AS EXTERNALS, AND MODIFICATIONS OF PACKAGE VARIANTS ETC
   ...

**MISSING**

4. Find compilers, add to site config's ``compilers.yaml``

.. code-block:: console

   spack compiler find --scope system

5. Do **not** forget to unset the ``SPACK_SYSTEM_CONFIG_PATH`` environment variable!

.. code-block:: console

   export -n SPACK_SYSTEM_CONFIG_PATH


6. Optionally edit site config files and common config files, for example to emove duplicate versions of external packages that are unwanted

.. code-block:: console

   vi envs/jedi-ufs.mylinux/spack.yaml
   vi envs/jedi-ufs.mylinux/packages.yaml
   vi envs/jedi-ufs.mylinux/site/*.yaml

7. Process the specs and install

.. code-block:: console

   spack concretize
   spack install [--verbose] [--fail-fast]

8. Create lua module files

.. code-block:: console

   spack module lmod refresh

9. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules
