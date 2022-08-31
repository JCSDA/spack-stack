.. _Platforms:

Platforms
*************************

.. _Platforms_Preconfigured_Sites:

==============================
Pre-configured sites
==============================

Directory ``configs/sites`` contains site configurations for several HPC systems, as well as minimal configurations for macOS and Linux. The macOS and Linux configurations are **not** meant to be used as is, as user setups and package versions vary considerably. Instructions for adding this information can be found further down in :numref:`Section %s <Platform_New_Site_Configs>`.

Ready-to-use spack-stack installations are available on the following platforms. This table will be expanded as more platforms are added.

--------------
spack-stack-v1
--------------

.. note::
   This version supports the JEDI Skylab release end of June/beginning of July 2022, and can be used for testing spack-stack with other applications (e.g. the UFS Weather Model). Amazon Web Services AMI are available in the US East 1 region.

+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| System                                   | Maintained by (temporary) | Location                                                                                                     |
+==========================================+===========================+==============================================================================================================+
| MSU Orion Intel                          | Dom Heinzeller            | ``/work/noaa/da/role-da/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-2022.0.2/install``                |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| MSU Orion GNU                            | Dom Heinzeller            | ``/work/noaa/da/role-da/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-10.2.0-openmpi-4.0.4/install``      |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NASA Discover Intel                      | Dom Heinzeller            | ``/discover/swdev/jcsda/spack-stack/spack-stack-v1/envs/skylab-1.0.2-intel-2022.0.1/install``                |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NASA Discover GNU                        | Dom Heinzeller            | ``/discover/swdev/jcsda/spack-stack/spack-stack-v1/envs/skylab-1.0.2-gnu-10.1.0/install``                    |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne Intel              | Dom Heinzeller            | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-19.1.1.217/install``      |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne GNU                | Dom Heinzeller            | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-10.1.0/install``            |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA Parallel Works (AWS, Azure, Gcloud) |                           | not yet supported - coming soon                                                                              |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea                         | Dom Heinzeller            | ``/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v1/envs/skylab-1.0.2-intel-2021.3.0/install/``           |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera Intel                   | Kyle Gerheiser            | ``/lfs4/HFIP/hfv3gfs/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-2022.0.2/install``                   |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera GNU                     | Kyle Gerheiser            | ``/lfs4/HFIP/hfv3gfs/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-9.2.0/install``                        |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet Intel                    | Kyle Gerheiser            | ``/lfs4/HFIP/hfv3gfs/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-2022.0.2/install``                   |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet GNU                      | Kyle Gerheiser            | ``/lfs4/HFIP/hfv3gfs/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-9.2.0/install``                        |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| TACC Frontera Intel                      | Dom Heinzeller            | ``/work2/06146/tg854455/frontera/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-19.1.1.217/install``     |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| TACC Frontera GNU                        | Dom Heinzeller            | ``/work2/06146/tg854455/frontera/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-9.1.0/install``            |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| UW (Univ. of Wisc.) S4                   | Dom Heinzeller            | ``/data/prod/jedi/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-2021.5.0/install``                      |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| Amazon Web Services AMI Ubuntu 20.04 GNU | Dom Heinzeller            | AMI: skylab-1.0.0-ubuntu20 - ``/home/ubuntu/spack-stack-v1/envs/skylab-1.0.0/install``                       |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+
| Amazon Web Services AMI Red Hat 8 GNU    | Dom Heinzeller            | AMI: skylab-1.0.0-redhat8 - ``/home/ec2-user/spack-stack-v1/envs/skylab-1.0.0/install``                      |
+------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------+

For questions or problems, please consult the known issues in :numref:`Section %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/noaa-emc/spack-stack/issues>`_ and `discussions <https://github.com/noaa-emc/spack-stack/discussions>`_ first.

.. _Platforms_Orion:

------------------------------
MSU Orion
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work/noaa/da/role-da/spack-stack/modulefiles
   module load miniconda/3.9.7

For ``spack-stack-1.0.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/da/role-da/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-2022.0.2/install/modulefiles/Core
   module load stack-intel/2022.0.2
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.7
   module available

For ``spack-stack-1.0.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/da/role-da/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-10.2.0-openmpi-4.0.4/install/modulefiles/Core
   module load stack-gcc/10.2.0
   module load stack-openmpi/4.0.4
   module load stack-python/3.9.7
   module available

.. _Platforms_Discover:

------------------------------
NASA Discover
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7

For ``spack-stack-1.0.2`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   ulimit -s unlimited
   module use /discover/swdev/jcsda/spack-stack/spack-stack-v1/envs/skylab-1.0.2-intel-2022.0.1/install/modulefiles/Core
   module load stack-intel/2022.0.1
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.9.7
   module available

For ``spack-stack-1.0.2`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   ulimit -s unlimited
   module use /discover/swdev/jcsda/spack-stack/spack-stack-v1/envs/skylab-1.0.2-gnu-10.1.0/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.3
   module load stack-python/3.9.7
   module available

.. _Platforms_Cheyenne:

---------------------
NCAR-Wyoming Cheyenne
---------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module unuse /glade/u/apps/ch/modulefiles/default/compilers
   export MODULEPATH_ROOT=/glade/work/jedipara/cheyenne/spack-stack/modulefiles
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
   module load ecflow/5.8.4
   module load miniconda/3.9.12

For ``spack-stack-1.0.1`` with Intel, load the following modules after loading miniconda and ecflow. Note that there are problems with newer versions of the Intel compiler/MPI library when trying to run MPI jobs with just one task (``mpiexec -np 1``) - for JEDI, job hangs forever in a particular MPI communication call in oops.

.. code-block:: console

   ulimit -s unlimited
   module use /glade/work/jedipara/cheyenne/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-19.1.1.217/install/modulefiles/Core
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2019.7.217
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.0.1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   ulimit -s unlimited
   module use /glade/work/jedipara/cheyenne/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-10.1.0/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.1
   module load stack-python/3.9.12
   module available

.. _Platforms_Acorn:

-------------------------------
NOAA Acorn (WCOSS2 test system)
-------------------------------

.. note::
   ``spack-stack-1.0.0`` is currently not supported on this platform and will be added in the near future.

On WCOSS2 OpenSUSE sets `CONFIG_SITE` which causes libraries to be installed in `lib64`, breaking the `lib` assumption made by some packages.

CONFIG_SITE should be set to empty in `compilers.yaml`.

.. note::
   ``spack`` software installations are maintained by NCO on this platform.

.. _Platforms_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

.. note::
   ``spack-stack-1.0.0`` is currently not supported on this platform and will be added in the near future.

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
   module use /lustre/f2/pdata/esrl/gsd/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4

For ``spack-stack-1.0.2`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v1/envs/skylab-1.0.2-intel-2021.3.0/install/modulefiles/Core
   module load stack-intel/2021.3.0
   module load stack-cray-mpich/7.7.11
   module load stack-python/3.9.12
   module available

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE

.. _Platforms_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

.. note::
   ``spack-stack-1.0.0`` is currently not supported on this platform and will be added in the near future.

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /scratch1/NCEPDEV/jcsda/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.12

.. _Platforms_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

**WORK IN PROGRESS**

------------------------------
TACC Frontera
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work2/06146/tg854455/frontera/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4

For ``spack-stack-1.0.1`` with Intel, load the following modules after loading miniconda and ecflow:

   ulimit -s unlimited
   module use /work2/06146/tg854455/frontera/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-19.1.1.217/install/modulefiles/Core
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2020.4.304
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.0.1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   ulimit -s unlimited
   module use /work2/06146/tg854455/frontera/spack-stack/spack-stack-v1/envs/skylab-1.0.0-gnu-9.1.0/install/modulefiles/Core
   module load stack-gcc/9.1.0
   module load stack-mvapich2/2.3
   module load stack-python/3.9.12
   module available

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4

For ``spack-stack-1.0.2`` with Intel, load the following modules after loading miniconda and ecflow:

   ulimit -s unlimited
   module use /data/prod/jedi/spack-stack/spack-stack-v1/envs/skylab-1.0.0-intel-2021.5.0/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.9.12
   module available

--------------------------------
Amazon Web Services Ubuntu 20.04
--------------------------------

For ``spack-stack-1.0.0``, use a t2.2xlarge instance or similar with AMI "skylab-1.0.0-ubuntu20". After logging in, run:

.. code-block:: console

   ulimit -s unlimited
   module use /home/ubuntu/spack-stack-v1/envs/skylab-1.0.0/install/modulefiles/Core
   module load stack-gcc/9.4.0
   module load stack-mpich/4.0.2
   module load stack-python/3.8.10
   module available

-----------------------------
Amazon Web Services Red hat 8
-----------------------------

For ``spack-stack-1.0.0``, use a t2.2xlarge instance or similar with AMI "skylab-1.0.0-redhat8". After logging in, run:

.. code-block:: console

   scl enable gcc-toolset-11 bash
   ulimit -s unlimited
   module use /home/ec2-user/spack-stack-v1/envs/skylab-1.0.0/install/modulefiles/Core
   module load stack-gcc/11.2.1
   module load stack-openmpi/4.1.3
   module load stack-python/3.9.7
   module available

..  _Platform_New_Site_Configs:

==============================
Generating new site configs
==============================

In general, the recommended approach is as follows (see following sections for specific examples): Start with an empty/default site config (`linux.default` or `macos.default`). Then run ``spack external find`` to locate external packages such as build tools and a few other packages. Next, run ``spack compiler find`` to locate compilers in your path. Compilers or external packages with modules may need to be loaded prior to running ``spack external find``, or added manually. The instructions differ slightly for macOS and Linux and assume that the prerequisites for the platform have been installed as described in :numref:`Sections %s <Platform_macOS>` and :numref:`%s <Platform_Linux>`.

It is also instructive to peruse the GitHub actions scripts in ``.github/workflows`` and ``.github/actions`` to see how automated spack-stack builds are configured for CI testing, as well as the existing site configs in ``configs/sites``.

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
   brew install qt@5

4. Configure your terminal to use the homebrew installed bash

  After installing bash with homebrew, you need to change your terminal application's default command to use :code:`/usr/local/bin/bash`.
  For example with iterm2, you can click on the :code:`preferences` item in the :code:`iTerm2` menu.
  Then click on the :code:`Profiles` tab and enter :code:`/usr/local/bin/bash` in the :code:`Command` box.
  This is done to avoid issues with the macOS System Integrity Protection (SIP) mechanism when running bash scripts.
  See https://support.apple.com/en-us/HT204899 for more details about SIP.

5. Activate the ``lua`` module environment

.. code-block:: console

   source /usr/local/opt/lmod/init/profile

6. Install xquartz using the provided binary at https://www.xquartz.org. This is required for forwarding of remote X displays, and for displaying the ``ecflow`` GUI, amongst others.

7. Temporary workaround for pip installs in spack (see https://github.com/spack/spack/issues/29308). Make sure that ``python3`` points to the Homebrew version.

.. code-block:: console

   python3 -m pip install poetry
   # test - successful if no output
   python3 -c "import poetry"

8. Optional: Install MacTeX if planning to build the ``jedi-tools`` environment with LaTeX/PDF support

   If the ``jedi-tools`` application is built with variant ``+latex`` to enable building LaTeX/PDF documentation, install MacTeX 
   `MacTeX  <https://www.tug.org/mactex>`_ and configure your shell to have it in the search path, for example:

.. code-block:: console

   export PATH="/usr/local/texlive/2022/bin/universal-darwin:$PATH"

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

Creating a new environment
--------------------------

Remember to activate the ``lua`` module environment and have MacTeX in your search path, if applicable. It is also recommended to increase the stacksize limit to 65Kb using ``ulimit -S -s unlimited``.

1. Create a pre-configured environment with a default (nearly empty) site config and activate it (optional: decorate bash prompt with environment name; warning: this can scramble the prompt for long lines)

.. code-block:: console

   spack stack create env --site macos.default [--template jedi-ufs-all] --name jedi-ufs.mymacos
   spack env activate [-p] envs/jedi-ufs.mymacos

2. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/jedi-ufs.mymacos/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mymacos/site"

3. Find external packages, add to site config's ``packages.yaml``. If an external's bin directory hasn't been added to ``$PATH``, need to prefix command.

.. code-block:: console

   spack external find --scope system
   spack external find --scope system perl
   spack external find --scope system python
   spack external find --scope system wget

   PATH="/usr/local/opt/curl/bin:$PATH" \
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

   unset SPACK_SYSTEM_CONFIG_PATH

6. Set default compiler and MPI library and flag Python as non-buildable (make sure to use the correct ``apple-clang`` version for your system and the desired ``openmpi`` version)

.. code-block:: console

   spack config add "packages:python:buildable:False"
   spack config add "packages:all:providers:mpi:[openmpi@4.1.4]"
   spack config add "packages:all:compiler:[apple-clang@13.1.6]"

7. Optionally, edit site config files and common config files, for example to remove duplicate versions of external packages that are unwanted, add specs in ``envs/jedi-ufs.mymacos/spack.yaml``, etc.

.. code-block:: console

   vi envs/jedi-ufs.mymacos/spack.yaml
   vi envs/jedi-ufs.mymacos/common/*.yaml
   vi envs/jedi-ufs.mymacos/site/*.yaml

8. Process the specs and install

.. code-block:: console

   spack concretize
   spack install [--verbose] [--fail-fast]

9. Create lmod module files

.. code-block:: console

   spack module lmod refresh

10. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules

..  _Platform_Linux:

------------------------------
Linux
------------------------------

Note. Some Linux systems do not support recent ``lua/lmod`` environment modules, which are default in the spack-stack site configs. The instructions below therefore use ``tcl/tk`` environment modules.

Prerequisites: Red Hat/CentOS 8 (one-off)
-----------------------------------------

The following instructions were used to prepare a basic Red Hat 8 system as it is available on Amazon Web Services to build and install all of the environments available in spack-stack (see :numref:`Sections %s <Environments>`).

1. Install basic OS packages as `root`

.. code-block:: console

   sudo su
   yum -y update

   # Compilers - this includes environment module support
   yum -y install gcc-toolset-11-gcc-c++
   yum -y install gcc-toolset-11-gcc-gfortran
   yum -y install gcc-toolset-11-gdb

   # Do *not* install MPI with yum, this will be done with spack-stack

   # Misc
   yum -y install m4
   yum -y install wget
   # Do not install cmake (it's 3.20.2, which doesn't work with eckit)
   yum -y install git
   yum -y install git-lfs
   yum -y install bash-completion
   yum -y install bzip2 bzip2-devel
   yum -y install unzip
   yum -y install patch
   yum -y install automake
   yum -y install xorg-x11-xauth
   yum -y install xterm
   yum -y install texlive
   # Do not install qt@5 for now

   # Python
   yum -y install python39-devel
   alternatives --set python3 /usr/bin/python3.9
   python3 -m pip install poetry
   # test - successful if no output
   python3 -c "import poetry"

   # Exit root session
   exit

2. Log out and back in to be able to use the `tcl/tk` environment modules

3. As regular user, set up the environment to build spack-stack environments

.. code-block:: console

   scl enable gcc-toolset-11 bash

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

Prerequisites: Ubuntu 20.04 (one-off)
-------------------------------------

The following instructions were used to prepare a basic Ubuntu 20.04 system as it is available on Amazon Web Services to build and install all of the environments available in spack-stack (see :numref:`Sections %s <Environments>`).

1. Install basic OS packages as `root`

.. code-block:: console

   sudo su
   apt-get update
   apt-get upgrade

   # Compilers
   apt install -y gcc g++ gfortran gdb

   # Environment module support
   apt install -y environment-modules

   # Do *not* install MPI with yum, this will be done with spack-stack

   # Misc
   apt install -y build-essential
   apt install -y libcurl4-openssl-dev
   apt install -y libssl-dev
   #apt install krb5-user
   apt install -y libkrb5-dev
   apt install -y m4
   # Skip cmake, default version 3.16 is too old
   apt install -y git
   apt install -y git-lfs
   apt install -y bzip2
   apt install -y unzip
   apt install -y automake
   apt install -y xterm
   apt install -y texlive
   ### SKIP qt@5 FOR NOW

   # Python
   apt install python3-dev python3-pip
   ## pip3 install poetry
   python3 -m pip install poetry
   # Ignore error "ERROR: launchpadlib 1.10.13 requires testresources, which is not installed."
   # test - successful if no output
   python3 -c "import poetry"

   # Exit root session
   exit

2. Log out and back in to be able to use the `lmod/lua` environment modules

3. As regular user, set up the environment to build spack-stack environments

.. code-block:: console

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

.. note::
   The newer Ubuntu 22.04 system by default ships with Python 3.10, which we do not support due to numerous issues when building spack-stack.

Creating a new environment
--------------------------

It is recommended to increase the stacksize limit by using ``ulimit -S -s unlimited``, and to test if the module environment functions correctly (``module available``).

1. Create a pre-configured environment with a default (nearly empty) site config and activate it (optional: decorate bash prompt with environment name; warning: this can scramble the prompt for long lines)

.. code-block:: console

   spack stack create env --site linux.default [--template jedi-ufs-all] --name jedi-ufs.mylinux
   spack env activate [-p] envs/jedi-ufs.mylinux

2. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/jedi-ufs.mylinux/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/jedi-ufs.mylinux/site"

3. Find external packages, add to site config's ``packages.yaml``. If an external's bin directory hasn't been added to ``$PATH``, need to prefix command.

.. code-block:: console

   spack external find --scope system
   spack external find --scope system perl
   spack external find --scope system python
   spack external find --scope system wget

   # Red Hat: Do *not* execute the following line = do *not* use system curl, this breaks netcdf-c
   # Ubuntu: Execute the following line = use system curl and libssl
   spack external find --scope system curl

   # Skip qt@5 for now
   spack external find --scope system texlive

4. Find compilers, add to site config's ``compilers.yaml``

.. code-block:: console

   spack compiler find --scope system

5. Do **not** forget to unset the ``SPACK_SYSTEM_CONFIG_PATH`` environment variable!

.. code-block:: console

   unset SPACK_SYSTEM_CONFIG_PATH

6. Set default compiler and MPI library and flag Python as non-buildable (make sure to use the correct ``gcc`` version for your system and the desired ``openmpi`` version)

.. code-block:: console

   # Example for Red Hat 8 following the above instructions
   spack config add "packages:python:buildable:False"
   spack config add "packages:all:providers:mpi:[openmpi@4.1.4]"
   spack config add "packages:all:compiler:[gcc@11.2.1]"

   # Example for Ubuntu 20.04 following the above instructions
   spack config add "packages:python:buildable:False"
   spack config add "packages:openssl:buildable:False"
   spack config add "packages:all:providers:mpi:[mpich@4.0.2]"
   spack config add "packages:all:compiler:[gcc@9.4.0]"

7. Optionally, edit site config files and common config files, for example to remove duplicate versions of external packages that are unwanted, add specs in ``envs/jedi-ufs.mylinux/spack.yaml``, etc.

.. code-block:: console

   vi envs/jedi-ufs.mylinux/spack.yaml
   vi envs/jedi-ufs.mylinux/common/*.yaml
   vi envs/jedi-ufs.mylinux/site/*.yaml

8. Process the specs and install

.. code-block:: console

   spack concretize
   spack install [--verbose] [--fail-fast]

9. Create tcl module files

.. code-block:: console

   spack module tcl refresh

11. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules
