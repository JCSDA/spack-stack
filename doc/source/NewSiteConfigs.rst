.. _NewSiteConfigs:

Generating new site configs
*****************************

The instructions here describe how to generate a new site config. In addition to configuring new production and testing systems, this is the recommended way for developers to use spack-stack locally on their Linux or MacOS workstations. In general, the recommended approach is to start with an empty/default site config (`linux.default` or `macos.default`). The instructions differ slightly for macOS and Linux and assume that the prerequisites for the platform have been installed as described in :numref:`Sections %s <NewSiteConfigs_macOS>` and :numref:`%s <NewSiteConfigs_Linux>`.

It is also instructive to peruse the GitHub actions scripts in ``.github/workflows`` and ``.github/actions`` to see how automated spack-stack builds are configured for CI testing, as well as the existing site configs in ``configs/sites``.

.. note::
   We try to maintain compatibility with as many compilers and compiler versions as possible. The following table lists the compilers that are known to work. Please be aware that if you choose to use a different, older or newer compiler, spack-stack may not work as expected and we have limited resources available for support. Further note that Intel compiler versions are confusing, because the oneAPI version doesn't match the compiler version. We generally refer to the compiler version being the version string in the path to the compiler, e.g, `/apps/oneapi/compiler/2022.0.2/linux/bin/intel64/ifort`.

+-------------------------------------------+----------------------------------------------------------------------+---------------------------+
| Compiler                                  | Versions tested/in use in one or more site configs                   | Spack compiler identifier |
+===========================================+======================================================================+===========================+
| Intel classic (icc, icpc, ifort)          | 18.0.5.274 to the latest available version in oneAPI 2023.1.0        | ``intel@``                |
+-------------------------------------------+----------------------------------------------------------------------+---------------------------+
| Intel mixed (icx, icpx, ifort)            | all versions up to latest available version in oneAPI 2023.1.0       | ``intel@``                |
+-------------------------------------------+----------------------------------------------------------------------+---------------------------+
| GNU (gcc, g++, gfortran)                  | 9.2.0 to 12.2.0 (note: 13.x.y is **not** yet supported)              | ``gcc@``                  |
+-------------------------------------------+----------------------------------------------------------------------+---------------------------+
| Apple clang (clang, clang++, w/ gfortran) | 10.0.0 to 14.0.3                                                     | ``apple-clang@``          |
+-------------------------------------------+----------------------------------------------------------------------+---------------------------+
| LLVM clang (clang, clang++, w/ gfortran)  | 10.0.0 to 14.0.3                                                     | ``clang@``                |
+-------------------------------------------+----------------------------------------------------------------------+---------------------------+

..  _NewSiteConfigs_macOS:

------------------------------
macOS
------------------------------

On macOS, it is important to use certain Homebrew packages as external packages, because the native macOS packages are incomplete (e.g. missing the development header files): ``curl``, ``qt``, etc. The instructions provided in the following have been tested extensively on many macOS installations. Occasionally, the use of external packages may lead to concretization issues in the form of duplicate packages (i.e., more than one spec per package). This is the case with ``bison``, therefore the package should be installed by ``spack``.

Unlike in previous versions, the instructions below assume that ``Python`` is built by ``spack``. That means that when using the ``spack`` environments (i.e., loading the modules for building or running code), the ``spack`` installation of ``Python`` with its available ``Python`` modules should be used to ensure consistency. However, a Homebrew ``Python`` installation may still be needed to build new ``spack`` environments. It can also be beneficial for the user to have a version of ``Python`` installed with Homebrew that can be used for virtual environments that are completely independent of any ``spack``-built environment.

It is recommended to not use ``mpich`` or ``openmpi`` installed by Homebrew, because these packages are built using a flat namespace that is incompatible with the JEDI software. The spack-stack installations of ``mpich`` and ``openmpi`` use two-level namespaces as required.

Intel Arm platform notes
------------------------
With the introduction of the Arm architecture M1 and M2 chips on Mac, the OS offers execution and building of two architectures via Apple's Rosetta tool. Rosetta is a binary translator that can convert Intel executable instructions to native Arm instructions at runtime. The Arm architecture is denoted by ``arm64`` and ``aarch64``, while the Intel architecture supported by Rosetta is denoted by ``x86_64`` and ``i386``.

When you get a new Arm mac, you may need to install Rosetta. This can be done with the shell command ``softwareupdate --install-rosetta``. Note that applications are expected to run faster when the native Arm architecture is utilized, although Intel binaries are very close to native performance.

A lot of binaries (iTerm2 for example) come in a "universal form" meaning they can run as Arm or Intel (you can toggle this by right clicking on the application in finder, selecting "get info", then checking the "Open using Rosetta" box). MacOS provides a utility called ``arch`` which is handy for monitoring which architecture you are running on. For example, entering ``arch`` without any arguments will return which architecture is running in your terminal window.

Homebrew notes
--------------

When running with the Intel architecture, homebrew manages its downloads in ``/usr/local`` (as it has been doing in the past). When running with the Arm architecture, homebrew manages its downloads in ``/opt/homebrew``. Other than the different prefixes for Arm versus Intel, the paths for all the pieces of a given package are identical. This separation allows for both Arm and Intel environments to exist on one machine.

For these instructions we will use the variable ``$HOMEBREW_ROOT`` to hold the prefix where homebrew manages its downloads (according to the architecture being used).

.. code-block:: console

    # If building on Arm architecture:
    export HOMEBREW_ROOT=/opt/homebrew
    
    # If building on Intel architecture:
    export HOMEBREW_ROOT=/usr/local

.. note::
   By default, every call to ``brew`` attempts to update the entire ``brew`` installation, which often means that existing spack-stack installations and other builds won't work anymore. With ``export HOMEBREW_NO_AUTO_UPDATE=1`` before running ``brew``, this automatic update is disabled.

Prerequisites (one-off)
-----------------------

These instructions are meant to be a reference that users can follow to set up their own system. Depending on the user's setup and needs, some steps will differ, some may not be needed and others may be missing. Also, the package versions may change over time.

1. Install Apple's command line utilities.

   - Launch the Terminal, found in ``/Applications/Utilities``

   - Type the following command string:

.. code-block:: console

   xcode-select --install
   sudo xcode-select --switch /Library/Developer/CommandLineTools

.. note::
   If you encounter build errors for gdal later on in spack-stack (see :numref:`Section %s <KnownIssues>`), you may need to install the full ``Xcode`` application and then switch ``xcode-select`` over with ``sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`` (change the path if you installed Xcode somewhere else).

2. Set up a terminal and environment using the appropriate architecture

    a. Arm

       In this case the Terminal application should already be running with the Arm architecture.
       Open a terminal and verify that this is the case:

       .. code-block:: console
           
           # In the terminal enter
           arch
           # this should respond with "arm64"

       Add the homebrew bin directory to your PATH variable.
       Make sure the homebrew bin path goes before ``/usr/local/bin``.

       .. code-block:: console
           
           export PATH=$HOMEBREW_ROOT/bin:$PATH

    b. Intel

       In this case, the idea is to create a new Terminal application that automatically runs bash in the Intel mode (using Rosetta2 underneath the hood.

       - Open Applications in Finder

       - Duplicate your preferred terminal application (e.g. Terminal or iTerm)

       - Rename the duplicate to, for example, "Terminal x86_64"

       - Right-click / control+click on "Terminal x86_64", choose "Get Info"

       - Select the box "Open using Rosetta" and close the window

       Check to make sure you have ``/usr/local/bin`` in your PATH variable for homebrew.

   From this point on, make sure you run the commands from the Terminal application matching the arhcitecture you are building.
   That is, use "Terminal" if building for Arm, or use "Terminal x86_64" if building for Intel.
   Verify that you have the correct architecture by running ``arch`` in the terminal window.
   From ``arch`` you should see ``arm64`` for Arm, or see ``x86_64`` or ``i386`` for Intel.

3. Install Homebrew

   It is recommended to install the following prerequisites via Homebrew, as installing them with Spack and Apple's native clang compiler can be tricky.

.. code-block:: console

   brew install coreutils
   # For now, use gcc@12
   brew install gcc@12
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
   brew install mysql

.. note::
  On an Intel based Mac, you will need to also install pkg-config using homebrew.
  This is done to work around an issue where libraries (eg, openssl) cannot be properly found during code compilation.

.. code-block:: console

  brew install pkg-config  # Intel based Mac only

4. Configure your terminal to use the homebrew installed bash

  After installing bash with homebrew, you need to change your terminal application's default command to use :code:`$HOMEBREW_ROOT/bin/bash`.
  For example with iterm2, you can click on the :code:`preferences` item in the :code:`iTerm2` menu.
  Then click on the :code:`Profiles` tab and enter :code:`$HOMEBREW_ROOT/bin/bash` in the :code:`Command` box.
  This is done to avoid issues with the macOS System Integrity Protection (SIP) mechanism when running bash scripts.
  See https://support.apple.com/en-us/HT204899 for more details about SIP.

  It's recommended to quit the terminal window at this point and then start up a fresh terminal window to make sure you proceed using a terminal that is running the :code:`$HOMEBREW_ROOT/bin/bash` shell.

5. Activate the ``lua`` module environment (note: This is not persistent and must be done at the beginning of each session you intend to use spack-stack modules).

.. code-block:: console

   source $HOMEBREW_ROOT/opt/lmod/init/profile

6. Install xquartz using the provided binary at https://www.xquartz.org. This is required for forwarding of remote X displays, and for displaying the ``ecflow`` GUI, amongst others.

7. Optional: Install MacTeX if planning to build the ``jedi-tools`` environment with LaTeX/PDF support

   If the ``jedi-tools`` application is built with variant ``+latex`` to enable building LaTeX/PDF documentation, install MacTeX 
   `MacTeX  <https://www.tug.org/mactex>`_ and configure your shell to have it in the search path, for example:

.. code-block:: console

   export PATH="/usr/local/texlive/2023/bin/universal-darwin:$PATH"

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

Creating a new environment
--------------------------

Remember to activate the ``lua`` module environment and have MacTeX in your search path, if applicable. It is also recommended to increase the stacksize limit to 65Kb using ``ulimit -S -s unlimited``.

1. You will need to clone spack-stack and its dependencies and activate the spack-stack tool. It is also a good idea to save the directory in your environment for later use.

.. code-block:: console

   git clone --recursive https://github.com/jcsda/spack-stack.git
   cd spack-stack

   # Sources Spack from submodule and sets ${SPACK_STACK_DIR}
   source setup.sh

2. Create a pre-configured environment with a default (nearly empty) site config and activate it (optional: decorate bash prompt with environment name; warning: this can scramble the prompt for long lines). The choice of the template depends on the applications you want to run, see ``configs/templates/`` in the spack-stack repo for the available options. The ``unified-dev`` templates creates the largest of all environments, because it contains everything needed for the NOAA Unified Forecast System, the JCSDA JEDI application, ...

.. code-block:: console

   spack stack create env --site macos.default [--template unified-dev] --name unified-env.mymacos
   spack env activate [-p] envs/unified-env.mymacos

3. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/unified-env.mymacos/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/unified-env.mymacos/site"

4. Find external packages, add to site config's ``packages.yaml``. If an external's bin directory hasn't been added to ``$PATH``, need to prefix command.

.. code-block:: console

   spack external find --scope system --exclude bison --exclude openssl
   spack external find --scope system libiconv
   spack external find --scope system perl
   spack external find --scope system wget
   spack external find --scope system mysql

   PATH="$HOMEBREW_ROOT/opt/curl/bin:$PATH" \
        spack external find --scope system curl

   PATH="$HOMEBREW_ROOT/opt/qt5/bin:$PATH" \
       spack external find --scope system qt

   # Optional, only if planning to build jedi-tools environment with LaTeX support
   # The texlive bin directory must have been added to PATH (see above)
   spack external find --scope system texlive

.. note::
  On an Intel based Mac, you need to add the following spack config command to prevent spack from building pkg-config.
  This will force spack to use the pkg-config installed by homebrew (see above).

.. code-block:: console

  spack config --scope system add packages:pkg-config:buildable:false  # Intel based Mac only

5. Find compilers, add to site config's ``compilers.yaml``

.. code-block:: console

   spack compiler find --scope system

6. Do **not** forget to unset the ``SPACK_SYSTEM_CONFIG_PATH`` environment variable!

.. code-block:: console

   unset SPACK_SYSTEM_CONFIG_PATH

7. Set default compiler and MPI library (make sure to use the correct ``apple-clang`` version for your system and the desired ``openmpi`` version)

.. code-block:: console

   # Check your clang version then add it to your site compiler config.
   clang --version
   spack config add "packages:all:compiler:[apple-clang@YOUR-VERSION]"
   spack config add "packages:all:providers:mpi:[openmpi@4.1.5]"

8. If applicable (depends on the environment), edit the main config file for the environment and adjust the compiler matrix to match the compilers for macOS, as above:

.. code-block:: console

   definitions:
   - compilers: ['%apple-clang']

9. If needed, edit site config files and common config files, for example to remove duplicate versions of external packages that are unwanted, add specs in ``envs/unified-env.mymacos/spack.yaml``, etc.

.. code-block:: console

   vi envs/unified-env.mymacos/spack.yaml
   vi envs/unified-env.mymacos/common/*.yaml
   vi envs/unified-env.mymacos/site/*.yaml

10. Process the specs and install

It is recommended to save the output of concretize in a log file and inspect that log file using the :ref:`show_duplicate_packages.py <Duplicate_Checker>` utility.
This is done to find and eliminate duplicate package specifications which can cause issues at the module creation step below.
Note that in the unified environment, there may be deliberate duplicates; consult the specs in spack.yaml to determine which ones are desired.

.. code-block:: console

   spack concretize 2>&1 | tee log.concretize
   util/show_duplicate_packages.py -d log.concretize
   spack install [--verbose] [--fail-fast]

11. Create lmod module files

.. code-block:: console

   spack module lmod refresh

12. Create meta-modules for compiler, mpi, python. This will create a meta module at ``envs/unified-env.mymacos/modulefiles/Core``.

.. code-block:: console

   spack stack setup-meta-modules

.. note::
   Unlike preconfigured environments and linux environments, MacOS users typically need to activate lmod's ``module`` tool within each shell session. This can be done by running ``source $HOMEBREW_ROOT/opt/lmod/init/profile``

13. You now have a spack-stack environment that can be accessed by running ``module use ./envs/unified-env.mymacos/install/modulefiles/Core``. The modules defined here can be loaded to build and run code as described in :numref:`Section %s <UsingSpackEnvironments>`.


..  _NewSiteConfigs_Linux:

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
   yum -y install mysql-server

   # For screen utility (optional)
   yum -y remove https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
   yum -y update --nobest
   yum -y install screen

   # Python
   yum -y install python39-devel
   alternatives --set python3 /usr/bin/python3.9

   # Exit root session
   exit

2. Log out and back in to be able to use the `tcl/tk` environment modules

3. As regular user, set up the environment to build spack-stack environments

.. code-block:: console

   scl enable gcc-toolset-11 bash

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

Prerequisites: Ubuntu (one-off)
-------------------------------------

The following instructions were used to prepare a basic Ubuntu 20.04 or 22.04 LTS system as it is available on Amazon Web Services to build and install all of the environments available in spack-stack (see :numref:`Sections %s <Environments>`).

1. Install basic OS packages as `root`

.. code-block:: console

   sudo su
   apt-get update
   apt-get upgrade

   # Compilers
   apt install -y gcc g++ gfortran gdb

   # Environment module support
   # Note: lmod is available in 22.04, but is out of date: https://github.com/JCSDA/spack-stack/issues/593
   apt install -y environment-modules

   # Misc
   apt install -y build-essential
   apt install -y libkrb5-dev
   apt install -y m4
   apt install -y git
   apt install -y git-lfs
   apt install -y bzip2
   apt install -y unzip
   apt install -y automake
   apt install -y xterm
   apt install -y texlive
   apt install -y libcurl4-openssl-dev
   apt install -y libssl-dev
   apt install -y meson
   apt install -y mysql-server
   apt install -y libmysqlclient-dev

   # Python
   apt install -y python3-dev python3-pip

   # Exit root session
   exit

2. Log out and back in to be able to use the environment modules

3. As regular user, set up the environment to build spack-stack environments

This environment enables working with spack and building new software environments, as well as loading modules that are created by spack for building JEDI and UFS software.

Creating a new environment
--------------------------

It is recommended to increase the stacksize limit by using ``ulimit -S -s unlimited``, and to test if the module environment functions correctly (``module available``).

1. You will need to clone spack-stack and its dependencies and activate the spack-stack tool. It is also a good idea to save the directory in your environment for later use.

.. code-block:: console

   git clone --recursive https://github.com/jcsda/spack-stack.git
   cd spack-stack

   # Sources Spack from submodule and sets ${SPACK_STACK_DIR}
   source setup.sh


2. Create a pre-configured environment with a default (nearly empty) site config and activate it (optional: decorate bash prompt with environment name; warning: this can scramble the prompt for long lines). The choice of the template depends on the applications you want to run, see ``configs/templates/`` in the spack-stack repo for the available options. The ``unified-dev`` templates creates the largest of all environments, because it contains everything needed for the NOAA Unified Forecast System, the JCSDA JEDI application, ...

.. code-block:: console

   spack stack create env --site linux.default [--template unified-env-all] --name unified-env.mylinux
   spack env activate [-p] envs/unified-env.mylinux

3. Temporarily set environment variable ``SPACK_SYSTEM_CONFIG_PATH`` to modify site config files in ``envs/unified-env.mylinux/site``

.. code-block:: console

   export SPACK_SYSTEM_CONFIG_PATH="$PWD/envs/unified-env.mylinux/site"

4. Find external packages, add to site config's ``packages.yaml``. If an external's bin directory hasn't been added to ``$PATH``, need to prefix command.

.. code-block:: console

   spack external find --scope system # use '--exclude' for troublesome packages like bison@:3.3, openssl@1.1.1
   spack external find --scope system perl
   spack external find --scope system wget
   spack external find --scope system mysql
   spack external find --scope system texlive
   # On Ubuntu (but not on Red Hat):
   spack external find --scope system curl

5. Find compilers, add to site config's ``compilers.yaml``

.. code-block:: console

   spack compiler find --scope system

6. Do **not** forget to unset the ``SPACK_SYSTEM_CONFIG_PATH`` environment variable!

.. code-block:: console

   unset SPACK_SYSTEM_CONFIG_PATH

7. Set default compiler and MPI library (make sure to use the correct ``gcc`` version for your system and the desired ``openmpi`` version)

.. code-block:: console

   # Check your gcc version then add it to your site compiler config.
   gcc --version
   spack config add "packages:all:compiler:[gcc@YOUR-VERSION]"

   # Example for Red Hat 8 following the above instructions
   spack config add "packages:all:providers:mpi:[openmpi@4.1.5]"

   # Example for Ubuntu 20.04 or 22.04 following the above instructions
   spack config add "packages:all:providers:mpi:[mpich@4.1.1]"

.. warning::
   On some systems, the default compiler (e.g., ``gcc`` on Ubuntu 20) may not get used by spack if a newer version is found. Compare your entry to the output of the concretization step later and adjust the entry, if necessary.

8. Set a few more package variants and versions to avoid linker errors and duplicate packages being built (for both Red Hat and Ubuntu):

.. code-block:: console

   spack config add "packages:fontconfig:variants:+pic"
   spack config add "packages:pixman:variants:+pic"
   spack config add "packages:cairo:variants:+pic"
   spack config add "packages:libffi:version:[3.3]"
   spack config add "packages:flex:version:[2.6.4]"

9. If you have manually installed lmod, you will need to update the site module configuration to use lmod instead of tcl. Skip this step if you followed the Ubuntu or Red Hat instructions above.

.. code-block:: console

   sed -i 's/tcl/lmod/g' envs/unified-env.mylinux/site/modules.yaml

10. If applicable (depends on the environment), edit the main config file for the environment and adjust the compiler matrix to match the compilers for Linux, as above:

.. code-block:: console

   definitions:
   - compilers: ['%gcc']

11. Edit site config files and common config files, for example to remove duplicate versions of external packages that are unwanted, add specs in ``envs/unified-env.mylinux/spack.yaml``, etc.

.. warning::
   **Important:** Remove any external ``cmake@3.20`` package from ``envs/unified-env.mylinux/site/packages.yaml``. It is in fact recommended to remove all versions of ``cmake`` up to ``3.20``. Further, on Red Hat/CentOS, remove any external curl that might have been found.

.. code-block:: console

   vi envs/unified-env.mylinux/spack.yaml
   vi envs/unified-env.mylinux/common/*.yaml
   vi envs/unified-env.mylinux/site/*.yaml

12. Process the specs and install

It is recommended to save the output of concretize in a log file and inspect that log file using the :ref:`show_duplicate_packages.py <Duplicate_Checker>` utility.
This is done to find and eliminate duplicate package specifications which can cause issues at the module creation step below.
Note that in the unified environment, there may be deliberate duplicates; consult the specs in spack.yaml to determine which ones are desired.

.. code-block:: console

   spack concretize 2>&1 | tee log.concretize
   util/show_duplicate_packages.py -d log.concretize
   spack install [--verbose] [--fail-fast]

13. Create tcl module files (replace ``tcl`` with ``lmod`` if you have manually installed lmod)

.. code-block:: console

   spack module tcl refresh

14. Create meta-modules for compiler, mpi, python

.. code-block:: console

   spack stack setup-meta-modules

15. You now have a spack-stack environment that can be accessed by running ``module use ./envs/unified-env.mymacos/install/modulefiles/Core``. The modules defined here can be loaded to build and run code as described in :numref:`Section %s <UsingSpackEnvironments>`.
