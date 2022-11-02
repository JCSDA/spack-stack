.. _MaintainersSection:

Maintainers/Developers Section
******************************

==============================
Pre-configuring sites
==============================

.. _MaintainersSection_Orion:

------------------------------
MSU Orion
------------------------------

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`. Note that the default/system ``qt@5`` can be used on Orion.

.. code-block:: console

   module purge
   module use /work/noaa/da/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.7
   module load cmake/3.22.1
   module load gcc/10.2.0

.. _MaintainersSection_Discover:

------------------------------
NASA Discover
------------------------------

On Discover, ``miniconda``, ``qt``, and ``ecflow`` need to be installed as a one-off before spack can be used. When using the GNU compiler, it is also necessary to build your own ``openmpi`` or other MPI library, which requires adapting the installation to the network hardware and ``slurm`` scheduler.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.2`` in ``/discover/swdev/jcsda/spack-stack/qt-5.15.2``.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7
   module load cmake/3.21.0
   module load qt/5.15.2
   module load comp/gcc/10.1.0

openmpi
   Installing ``openmpi`` requires adapting the installation to the network hardware and ``slurm`` scheduler. It is easier to build and test ``openmpi`` manually and use it as an external package, instead of building it as part of spack-stack. These instructions were used to build the ``openmpi@4.1.3`` MPI library with ``gcc@10.1.0`` as referenced in the Discover site config. After the installation, create modulefile `openmpi/4.1.3-gcc-10.1.0` using the template ``doc/modulefile_templates/openmpi``. Note the site-specific module settings at the end of the template, this will likely be different for other HPCs.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7
   module load comp/gcc/10.1.0
   CPATH="/usr/include/slurm:$CPATH" ./configure \
       --prefix=/discover/swdev/jcsda/spack-stack/openmpi-4.1.3/gcc-10.1.0/ \
       --with-pmi=/usr/slurm \
       --with-ucx \
       --without-ofi \
       --without-verbs \
       --with-gpfs
   CPATH="/usr/include/slurm:$CPATH" make VERBOSE=1 -j4
   CPATH="/usr/include/slurm:$CPATH" make check
   CPATH="/usr/include/slurm:$CPATH" make install

.. _MaintainersSection_Narwhal:

------------------------------
NAVY HPCMP Narwhal
------------------------------

On Narwhal, ``git-lfs``, ``qt``, and ``ecflow`` need to be installed as a one-off before spack can be used.

git-lfs
   The following instructions install ``git-lfs`` in ``/p/app/projects/NEPTUNE/spack-stack/git-lfs-2.10.0``. Version 2.10.0 is the default version for Narwhal. First, download the ``git-lfs`` RPM on a system with full internet access (e.g., Cheyenne) using ``wget https://download.opensuse.org/repositories/openSUSE:/Leap:/15.2/standard/x86_64/git-lfs-2.10.0-lp152.1.2.x86_64.rpm`` and copy this file to ``/p/app/projects/NEPTUNE/spack-stack/git-lfs-2.10.0/src``. Then switch to Narwhal and run the following commands. 

   .. code-block:: console

      cd /p/app/projects/NEPTUNE/spack-stack/git-lfs-2.10.0/src
      rpm2cpio git-lfs-2.10.0-lp152.1.2.x86_64.rpm | cpio -idmv
      mv usr/* ../

   Create modulefile ``/p/app/projects/NEPTUNE/spack-stack/modulefiles/git-lfs/2.10.0`` from template ``doc/modulefile_templates/git-lfs`` and update ``GITLFS_PATH`` in this file.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.2`` in ``/p/app/projects/NEPTUNE/spack-stack/qt-5.15.2``.

.. code-block:: console

   module unload PrgEnv-cray
   module load PrgEnv-intel/8.1.0
   module unload intel

   module unload cray-python
   module load cray-python/3.9.7.1
   module unload cray-libsci
   module load cray-libsci/22.08.1.1

   module load gcc/10.3.0

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>` to install ``ecflow`` in ``/p/app/projects/NEPTUNE/spack-stack/ecflow-5.8.4-cray-python-3.9.7.1``. Ensure to follow the extra instructions in that section for Narwhal.

   module unload PrgEnv-cray
   module load PrgEnv-intel/8.1.0
   module unload intel

   module unload cray-python
   module load cray-python/3.9.7.1
   module unload cray-libsci
   module load cray-libsci/22.08.1.1

   module load gcc/10.3.0
   module load qt/5.15.2

.. _MaintainersSection_Cheyenne:

------------------------------
NCAR-Wyoming Cheyenne
------------------------------

On Cheyenne, a workaround is needed to avoid the modules provided by CISL take precedence over the spack modules. The default module path for compilers is removed, the module path is set to a different location and that location is then loaded into the module environment. If new compilers or MPI libraries are
added to ``/glade/u/apps/ch/modulefiles/default/compilers`` by CISL, the spack-stack maintainers need to make the corresponding changes in ``/glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers``. See :numref:`Section %s <Platforms_Cheyenne>` for details.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Because of the workaround for the compilers, the ``miniconda`` module should be placed in ``/glade/work/jedipara/cheyenne/spack-stack/misc``. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.2`` in ``/glade/work/jedipara/cheyenne/spack-stack/qt-5.15.2``. Because of the workaround for the compilers, the ``qt`` module should be placed in ``/glade/work/jedipara/cheyenne/spack-stack/misc``.

.. code-block:: console

   module purge
   module unuse /glade/u/apps/ch/modulefiles/default/compilers
   export MODULEPATH_ROOT=/glade/work/jedipara/cheyenne/spack-stack/modulefiles
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers
   module load gnu/10.1.0

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`. Because of the workaround for the compilers, the ``qt`` module should be placed in ``/glade/work/jedipara/cheyenne/spack-stack/misc``. Also, because of the dependency on ``miniconda``, that module must be loaded automatically in the ``ecflow`` module (similar to ``qt@5.15.2``).

.. code-block:: console

   module purge
   module unuse /glade/u/apps/ch/modulefiles/default/compilers
   export MODULEPATH_ROOT=/glade/work/jedipara/cheyenne/spack-stack/modulefiles
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
   module load gnu/10.1.0
   module load miniconda/3.9.12
   module load qt/5.15.2
   module load cmake/3.18.2

.. _MaintainersSection_WCOSS2:

------------------------------
NOAA NCO WCOSS2
------------------------------

**WORK IN PROGRESS**

.. _MaintainersSection_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

**WORK IN PROGRESS**

.. _MaintainersSection_Gaea:

------------------------------
NOAA RDHPCS Gaea
------------------------------

On Gaea, ``miniconda``, ``qt``, and ``ecflow`` need to be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment. Use the following workaround to avoid the terminal being spammed by error messages about missing version information (``/bin/bash: /lustre/f2/pdata/esrl/gsd/spack-stack/miniconda-3.9.12/lib/libtinfo.so.6: no version information available (required by /lib64/libreadline.so.7)``):

.. code-block:: console

   cd /lustre/f2/pdata/esrl/gsd/spack-stack/miniconda-3.9.12/lib
   mv libtinfow.so.6.3 libtinfow.so.6.3.conda.original
   ln -sf /lib64/libtinfo.so.6 libtinfow.so.6.3

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.2`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.2``.

.. code-block:: console

   module unload intel cray-mpich cray-python darshan PrgEnv-intel
   module load gcc/10.3.0
   module load PrgEnv-gnu/6.0.5

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`. Because of the dependency on ``miniconda``, that module must be loaded automatically in the ``ecflow`` module (similar to ``qt@5.15.2``).  Ensure to follow the extra instructions in that section for Gaea.

   module unload intel cray-mpich cray-python darshan PrgEnv-intel
   module load gcc/10.3.0
   module load PrgEnv-gnu/6.0.5
   module load cmake/3.20.1
   module use /lustre/f2/pdata/esrl/gsd/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load qt/5.15.2

.. _MaintainersSection_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

On Hera, ``miniconda`` must be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

Hera sits behind the NOAA firewall and doesn't have access to all packages on the web. It is therefore necessary to create a spack mirror on another platform (e.g. Cheyenne). This can be done as follows.

1. (On Hera) Create an environment as usual and run the concretization step (``spack concretize``), but do not start the installation yet.

2. (On Cheyenne) Load the basic external modules (see :numref:`Section %s <Platforms_Cheyenne>`) and load module ``git/2.33.1`` (for ``git lfs``). Check out a fresh clone of ``spack-stack`` and run ``source setup.sh``.

3. (On Hera) Copy (e.g. using ``scp``) the environment's ``spack.lock`` file to Cheyenne into the ``spack-stack`` directory.

4. (On Cheyenne) Run the following sequence of commands:

.. code-block:: console

   spack env create hera_mirror_env spack.lock
   spack env activate hera_mirror_env
   spack mirror create -a

   The mirror will be created in directory ``./spack/var/spack/environments/hera_mirror_env``

5. (On Hera) Copy the directory from Cheyenne to ``/scratch1/NCEPDEV/global/spack-stack/mirror``. It is recommended to use ``rsync`` to avoid deleting existing packages in the mirror directory on Hera.

6. (On Hera) Add the mirror to the spack environment's mirror list. Note that this is already included in the Hera site config in ``spack-stack`` (``configs/sites/hera/mirrors.yaml``).

.. code-block:: console

   spack mirror add local file:///scratch1/NCEPDEV/global/spack-stack/mirror
   spack mirror list

   The newly created local mirror should be listed at the top, which means that spack will search this directory first.

7. (On Hera) Proceed with the installation as usual.

.. _MaintainersSection_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

.. code-block:: console

   module use /lfs4/HFIP/hfv3gfs/spack-stack/modulefiles
   module load miniconda/3.9.12
   # Need a newer gcc compiler than the default OS compiler gcc-4.8.5
   module load gnu/9.2.0

.. _MaintainersSection_Frontera:

------------------------------
TACC Frontera
------------------------------

Several packages need to be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation in ``/work2/06146/USERNAME/frontera/spack-stack/miniconda-3.9.12`` and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`.

.. code-block:: console

   module purge
   module use /work2/06146/tg854455/frontera/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load qt5/5.14.2
   module load gcc/9.1.0
   module load cmake/3.20.3

git-lfs
   The following instructions install ``git-lfs`` in ``/work2/06146/tg854455/frontera/spack-stack/git-lfs-2.10.0``. Version 2.10.0 is the Centos7 default version.

.. code-block:: console

   module purge
   cd /work2/06146/tg854455/frontera/spack-stack/
   mkdir -p git-lfs-2.10.0/src
   cd git-lfs-2.10.0/src
   wget --content-disposition https://packagecloud.io/github/git-lfs/packages/el/7/git-lfs-2.10.0-1.el7.x86_64.rpm/download.rpm
   rpm2cpio git-lfs-2.10.0-1.el7.x86_64.rpm | cpio -idmv
   mv usr/* ../

Create modulefile ``/work2/06146/tg854455/frontera/spack-stack/modulefiles/git-lfs/2.10.0`` from template ``doc/modulefile_templates/git-lfs`` and update ``GITLFS_PATH`` in this file.

.. _MaintainersSection_S4:

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

gnu (module only)
   The ``gnu/9.3.0`` module provided by the system administrators is broken (circular dependencies etc.). To create a usable version, copy ``/data/prod/hpc-stack/modulefiles/core/gnu/9.3.0.lua`` into directory ``/data/prod/jedi/spack-stack/modulefiles/gnu`.`

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load gcc/9.3.0

.. _MaintainersSection_AWS_Pcluster_Ubuntu:

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

See ``configs/sites/aws-pcluster/README.md``.

.. _MaintainersSection_Testing_New_Packages:

==============================
Testing new packages
==============================

--------------------------------
Using spack to test/add packages
--------------------------------

The simplest case of adding new packages that are available in spack-stack is described in :numref:`Section %s <QuickstartExtendingEnvironments>`. As mentioned there, it is advised to take a backup of the spack environment (and install directories if outside the spack environment directory tree). It is also possible to chain spack installations, which means creating a test environment that uses installed packages and modulefiles from another (e.g. authoritative) spack environment and build the packages to be tested in isolation.

Chaining spack-stack installations
----------------------------------

Chaining spack-stack installations is a powerful way to test adding new packages without affecting the existing packages. The idea is to define one or more upstream spack installations that the environment can use as dependencies. One possible way to do this is:

1. Mirror the environment config of the upstream repository, i.e. copy the entire directory without the ``install`` and ``.spack_env`` directories and without `spack.lock`. For example:

.. code-block:: console

   rsync -av --exclude='install' --exclude='.spack-env' --exclude='spack.lock' \
       envs/jedi-ufs/ \
       envs/jedi-ufs-chain-test/

2. Edit `envs/jedi-ufs-chain-test/spack.yaml`` and add an upstream configuration entry directly under the ``spack:`` config so that the contents looks like:

.. code-block:: console

   spack:
     upstreams:
       spack-instance-1:
         install_tree: /path/to/spack-stack-1.0.0/envs/jedi-ufs/install
     concretizer:
       unify: when_possible
     ...

3. Activate the environment

4. Install the new packages, for example:

.. code-block:: console

    spack install -v --reuse esmf@8.3.0b09+debug

5. Create modulefiles

.. code-block:: console

    spack module [lmod|tcl] refresh

6. When using ``tcl`` module files, run the ``spack stack setup-meta-modules`` script. This is not needed when using ``lmod`` modulefiles, because the meta modules in ``/path/to/spack-stack-1.0.0/envs/jedi-ufs-chain-test/install/modulefiles/Core`` will be ignored entirely.

To use the chained spack environment, first load the usual modules from the upstream spack environment. Then add the full path to the newly created modules manually, ignoring the meta modules (``.../Core``), for example:

.. code-block:: console

    module use /path/to/spack-stack-1.0.0/envs/jedi-ufs-chain-test/install/modulefiles/openmpi/4.1.3/apple-clang/13.1.6

7. Load the newly created modules. When using `tcl` module files, make sure that conflicting modules are unloaded (`lmod` takes care of this).

.. note::
   After activating the chained environment, ``spack find`` doesn't show the packages installed in upstream, unfortunately.

.. note::
   More details and a few words of caution can be found in the  `Spack documentation <https://spack.readthedocs.io/en/latest/chain.html?highlight=chaining%20spack%20installations>`_. Those words of caution need to be taken seriously, especially those referring to not deleting modulefiles and dependencies in the upstream spack environment (if having permissions to do so)!

----------------------------------------
Testing/adding packages outside of spack
----------------------------------------

Sometimes, users may want to build new versions of packages frequently without using spack, for example as part of an existing build system (e.g. a ``cmake`` submodule or an ``ecbuild`` bundle). Also, users may wish to test developmental code that is not available and/or not ready for release in spack-stack. In this case, users need to unload the modules of the packages that are to be replaced, including their dependencies, and build the new version(s) themselves within the existing build system or manually. The loaded modules from the spack environment in this case provide the necessary dependencies, just like for any other build system.

.. note::
   Users are strongly advised to not interfere with the spack install tree. The environment install tree and module files should only be modified using spack.

Users can build multiple packages outside of spack and install them in a separate install tree, for example ``MY_INSTALL_TREE``. In order to find these packages, users must extend their environment as required for the system/the packages to be installed:

.. code-block:: console

   export PATH="$MY_INSTALL_TREE/bin:$PATH"
   export CPATH="$MY_INSTALL_TREE/include:$PATH"
   export LD_LIBRARY_PATH="$MY_INSTALL_TREE/lib64:$MY_INSTALL_TREE/lib:$LD_LIBRARY_PATH"
   # macOS
   export DYLD_LIBRARY_PATH="$MY_INSTALL_TREE/lib64:$MY_INSTALL_TREE/lib:$DYLD_LIBRARY_PATH"
   # Python packages, use correct lib/lib64 and correct python version
   export PYTHONPATH="$MY_INSTALL_TREE/lib/pythonX.Y/site-packages:$PYTHONPATH"

Python packages can be added in various ways:

1. Using ``python setup.py install --prefix=$MY_INSTALL_TREE ...`` or ``python3 -m pip install --no-deps --prefix=$MY_INSTALL_TREE ...``. The ``--no-deps`` options is very important, because ``pip`` may otherwise attempt to install dependencies that already exist in spack-stack. These dependencies are not only duplicates, they may also be different versions and/or compiled with different compilers/libraries (because they are wheels). This approach requires adding the appropriate subdirectories of ``$MY_INSTALL_TREE`` to the different search paths, as shown above.

2. Using Python virtual environments. Two important flags need to be passed to the command that creates the environment ``--system-site-packages`` and ``--without-pip``. After activating the environment, packages can be installed using `python3 -m pip` without having to specify ``--no-deps`` or ``--prefix``, and without having to manually modify ``PATH``, ``PYTHONPATH``, etc.

.. code-block:: console

   python3 -m venv --system-site-packages --without-pip $MY_INSTALL_TREE
   source $MY_INSTALL_TREE/bin/activate
   python3 -m pip install ...

.. note::
   Users are equally strongly advised to not use ``conda`` or ``miniconda`` in combination with Python modules provided by spack-stack, as well as not installing packages other than ``poetry`` in the basic ``miniconda`` installation for spack-stack (if using such a setup).

.. _MaintainersSection_Directory_Layout:

==============================
Recommended Directory Layout
==============================

To support multiple installs it is recommended to use `bootstrap.sh` to setup Miniconda and create a standard directory layout.

After running `bootstrap.sh -p <prefix>` the directory will have the following directories:

* apps - Externally installed pre-requisites such as Miniconda and git-lfs.
* modulefiles - External modules such as Miniconda that are not tied to Spack.
* src - Prerequisite and spack-stack sources.
* envs - Spack environment installation location.

A single checkout of Spack can support multiple environments. To differentiate them spack-stack sources in `src` and corresponding environments in `envs` should be grouped by major version.

For example, major versions of spack-stack v1.x.y should be checked out in the `src/spack-stack` directory as `v1` and each corresponding environment should be installed in `envs/v1`.

.. code-block:: console

   spack-stack
   ├── apps
   │   └── miniconda
   │       └── py39_4.12.0
   ├── envs
   │   └── v1
   │       ├── jedi-ufs-all
   │       └── skylab-1.0.0
   ├── modulefiles
   │   └── miniconda
   │       └── py39_4.12.0
   └── src
      ├── miniconda
      │   └── py39_4.12.0
      │       └── Miniconda3-py39_4.12.0-MacOSX-x86_64.sh
      └── spack-stack
         └── v1
               ├── envs
               │   ├── jedi-ufs-all
               │   └── skylab-1.0.0


The install location can be set from the command line with:

.. code-block:: console

   spack config add "config:install_tree:root:<prefix>/envs/v1/jedi-ufs-all"
   spack config add "modules:default:roots:lmod:<prefix>/envs/v1/jedi-ufs-all/modulefiles"
