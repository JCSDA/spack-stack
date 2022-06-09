.. _Platforms:

*************************
Platforms
*************************

.. _Platforms_Preconfigured_Sites:

==============================
Pre-configured sites
==============================

Directory ``configs/sites`` contains site configurations for several HPC systems, as well as reference configurations for macOS and Linux. The reference configurations are **not** meant to be used as is, as user setups and package versions vary considerably. They are merely for comparing new site configurations that are created following the instructions below to working setups.

Ready-to-use spack-stack installations are available on the following platforms:

**Note: this versions are for early testers - use at your own risk**

+------------------------------------------+---------------------------+---------------------------+
| System                                   | Maintained by (temporary) | jedi-ewok tested          |
+==========================================+===========================+===========================+
| MSU Orion                                | Dom Heinzeller            | yes                       |
+------------------------------------------+---------------------------+---------------------------+
| NASA Discover                            | Dom Heinzeller            | yes                       |
+------------------------------------------+---------------------------+---------------------------+
| NCAR-Wyoming Cheyenne                    | Dom Heinzeller            | yes                       |
+------------------------------------------+---------------------------+---------------------------+
| NOAA NCO WCOSS2                          |                           |                           |
+------------------------------------------+---------------------------+---------------------------+
| NOAA Parallel Works (AWS, Azure, Gcloud) | Kyle Gerheiser            | yes                       |
+------------------------------------------+---------------------------+---------------------------+
| NOAA RDHPCS Gaea                         | Dom Heinzeller            | yes                       |
+------------------------------------------+---------------------------+---------------------------+
| NOAA RDHPCS Hera                         |                           |                           |
+------------------------------------------+---------------------------+---------------------------+
| NOAA RDHPCS Jet                          |                           |                           |
+------------------------------------------+---------------------------+---------------------------+
| TACC Stampede2                           | Dom Heinzeller            | yes                       |
+------------------------------------------+---------------------------+---------------------------+
| UW (Univ. of Wisc.) S4                   | Dom Heinzeller            | yes                       |
+------------------------------------------+---------------------------+---------------------------+

+----------------------------+-------------------------------------------------------------------------------------------------------+
| System                     | Location                                                                                              |
+============================+=======================================================================================================+
| MSU Orion                  | ``/work/noaa/da/role-da/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.1.2/install``         |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NASA Discover              | ``/discover/swdev/jcsda/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.1/install``         |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne      | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.2/install`` |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA NCO WCOSS2            |                                                                                                       |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA Parallel Works        |                                                                                                       |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea           | ``/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v0.0.2/envs/jedi-all-intel-2021.3.0/install``     |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera           |                                                                                                       |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet            |                                                                                                       |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| TACC Stampede2             | ``/work2/06146/tg854455/stampede2/spack-stack/spack-stack-0.0.1/envs/ENV_DIR_MISSING/install``        |
+----------------------------+-------------------------------------------------------------------------------------------------------+
| UW (Univ. of Wisc.) S4     | ``/data/prod/jedi/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.1/install``               |
+----------------------------+-------------------------------------------------------------------------------------------------------+

For questions or problems, please consult the known issues in :numref:`Chapter %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/noaa-emc/spack-stack/issues>`_ and `discussions <https://github.com/noaa-emc/spack-stack/discussions>`_ first.

.. _Platforms_Orion:

------------------------------
MSU Orion
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use module use /work/noaa/da/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.7

.. _Platforms_Discover:

------------------------------
NASA Discover
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7

.. _Platforms_Cheyenne:

------------------------------
NCAR-Wyoming Cheyenne
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module unuse /glade/u/apps/ch/modulefiles/default/compilers
   export MODULEPATH_ROOT=/glade/work/jedipara/cheyenne/spack-stack/modulefiles
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers
   module load python/3.7.9

.. _Platforms_WCOSS2:

------------------------------
NOAA NCO WCOSS2
------------------------------

**WORK IN PROGRESS**

.. _Platforms_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

The following is required for building new spack environments and for using spack to build and run software. The default module path needs to be removed, otherwise spack detect the system as Cray. It is also necessary to add ``git-lfs`` and some other utilities to the search path.

.. code-block:: console

   module unuse /opt/cray/craype/default/modulefiles
   module unuse opt/cray/modulefiles
   export PATH="${PATH}:/contrib/spack-stack/apps/utils/bin"
   module use /contrib/spack-stack/modulefiles/core
   module load miniconda/3.9.7

.. _Platforms_Gaea:

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

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. Work is in progress to augment ``ecbuild`` with the ability to prefix serial runs with a launcher, e.g. ``srun -n1`` on Gaea.

.. _Platforms_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. note::
   Temporary location, this needs to be moved elsewhere.

.. code-block:: console

   module purge
   module use /scratch1/BMC/gsd-hpcs/Dom.Heinzeller/spack-stack/modulefiles
   module load miniconda/3.9.7

.. _Platforms_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

**WORK IN PROGRESS**

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

..  _Platform_New_Site_Configs:

==============================
Generating new site configs
==============================

In general, the recommended approach is as follows (see following sections for specific examples): Start with an empty/default site config (`linux.default` or `macos.default`). Then run ``spack external find`` to locate external packages such as build tools and a few other packages. Next, run ``spack compiler find`` to locate compilers in your path. Compilers or external packages with modules may need to be loaded prior to running ``spack external find``, or added manually. The instructions differ slightly for macOS and Linux and assume that the prerequisites for the platform have been installed as described in :numref:`Sections %s <Platform_macOS>` and :numref:`%s <Platform_Linux>`.

It is also instructive to peruse the GitHub actions scripts in ``.github/workflows`` and ``.github/actions`` to see how automated spack-stack builds are configured for CI testing, as well as the existing site configs in ``configs/sites``, in particular the reference site configs for macOS (**NEEDS UPDATE AFTER spack v0p18p0 merge**) and Linux (**MISSING - create after spack v0p18p0 merge**).

..  _Platform_macOS:

------------------------------
macOS
------------------------------

On macOS, it is important to use certain Homebrew packages as external packages, because the native macOS packages are incomplete (e.g. missing the development header files): ``curl``, ``python``, ``qt``, etc. The instructions provided in the following have been tested extensively on many macOS installations.

The instructions below also assume a clean Homebrew installation with a clean Python installation inside. This means that the Homebrew Python only contains nothing but what gets installed with ``pip install poetry`` (which is a temporary workaround). If this is not the case, users can try to install a separate Python using Miniconda as described in :numref:`Sections %s <Prerequisites_Miniconda>`.

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

5. Install xquartz using the provided binary at https://www.xquartz.org. This is required for forwarding of remote X displays, and for displaying the ``ecflow`` GUI, amongst others.

6. Temporary workaround for pip installs in spack (see https://github.com/spack/spack/issues/29308). Make sure that ``python3`` points to the Homebrew version.

.. code-block:: console

   python3 -m pip install poetry
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

   spack stack create env --site macos.default --app jedi-ufs --name jedi-ufs.mymacos

2. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/jedi-ufs.mymacos/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mymacos/site"


3. Find external packages, add to site config's ``packages.yaml``. If an external's bin directory hasn't been added to ``$PATH``, need to prefix command.

.. code-block:: console

   spack external find --scope system
   spack external find --scope system perl
   spack external find --scope system python
   spack external find --scope system wget

   PATH="/usr/local/Cellar/curl/7.83.0/bin:$PATH" \
        spack external find --scope system curl

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

7. Optionally edit site config files and common config files, for example to emove duplicate versions of external packages that are unwanted

.. code-block:: console

   vi envs/jedi-ufs.mymacos/spack.yaml
   vi envs/jedi-ufs.mymacos/packages.yaml
   vi envs/jedi-ufs.mymacos/site/*.yaml

8. Activate the environment (optional: decorate bash prompt with environment name; warning: this can scramble the prompt for long lines)

.. code-block:: console

   spack env activate [-p] envs/jedi-ufs.mymacos

9. Process the specs and install

.. code-block:: console

   spack concretize
   spack install [--verbose] [--fail-fast]

10. Create lua module files

.. code-block:: console

   spack module lmod refresh

11. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules

..  _Platform_Linux:

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

   spack stack create env --site linux.default --app jedi-ufs --name jedi-ufs.mylinux

2. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/jedi-ufs.mymacos/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mylinux/site"

3. Find external packages, add to site config's ``packages.yaml``. If an external's bin directory hasn't been added to ``$PATH``, need to prefix command.

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

7. Activate the environment (optional: decorate bash prompt with environment name; warning: this can scramble the prompt for long lines)

.. code-block:: console

   spack env activate [-p] envs/jedi-ufs.mymacos

8. Process the specs and install

.. code-block:: console

   spack concretize
   spack install [--verbose] [--fail-fast]

9. Create lua module files

.. code-block:: console

   spack module lmod refresh

10. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules
