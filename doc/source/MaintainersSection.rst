.. _MaintainersSection:

Maintainers/Developers Section
******************************

==============================
Pre-configuring sites
==============================

.. _MaintainersSection_Preface:

------------------------------
Preface/general instructions
------------------------------

Preconfigured sites are defined through spack configuration files in the spack-stack directory ``configs/sites``, for example ``configs/sites/orion``. All files in the site-specific subdirectory will be copied into the environment into ``envs/env-name/site``. Site-specific configurations consist of general definitions (``config.yaml``), packages (``packages.yaml``), compilers (``compilers.yaml``), modules (``modules.yaml``), mirrors (``mirrors.yaml``) etc. These configurations overwrite the common configurations that are copied from ``configs/common`` into ``envs/env-name/common``.

The instructions below are platform-specific tasks that only need to be done once and can be reused for new spack environments. To build new environments on preconfigured platforms, follow the instructions in :numref:`Section %s <Preconfigured_Sites_ExtendingEnvironments>`.

.. _MaintainersSection_Orion:

------------------------------
MSU Orion
------------------------------

On Orion, it is necessary to change the default ``umask`` from ``0027`` to ``0022`` so that users not in the group of the role account can still see and use the software stack. This can be done by running ``umask 022`` after logging into the role account.

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

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/work/noaa/da/role-da/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_Hercules:

------------------------------
MSU Hercules
------------------------------

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After unloading all modules (``module purge``), refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.2`` in ``/discover/swdev/jcsda/spack-stack/qt-5.15.2``.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After unloading all modules (``module purge``), follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`.

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Since Orion and Hercules share the filesystems and since the MySQL community server comes pre-installed, it is possible to reuse the Orion installation in ``/work/noaa/da/role-da/spack-stack/mysql-8.0.31``.

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

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/discover/swdev/jcsda/spack-stack/mysql-8.0.31``. Note that the ``glibc`` version on Discover is 2.22, which works with the latest available ``glibc`` version for the ``mysql`` server ``2.17``.

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
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>` to install ``ecflow`` in ``/p/app/projects/NEPTUNE/spack-stack/ecflow-5.8.4``. Ensure to follow the extra instructions in that section for Narwhal.

.. code-block:: console

   module unload PrgEnv-cray
   module load PrgEnv-intel/8.1.0
   module unload intel

   module unload cray-python
   module load cray-python/3.9.7.1
   module unload cray-libsci
   module load cray-libsci/22.08.1.1

   module load gcc/10.3.0
   module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
   module load qt/5.15.2

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/p/app/projects/NEPTUNE/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_Casper:

------------------------------
NCAR-Wyoming Casper
------------------------------

Casper is co-located with Cheyenne and shares the parallel filesystem ``/glade`` and more with it. It is, however, a different operating system with a somewhat different software stack. spack-stack was installed on Casper after it was installed on Cheyenne, and prerequisites from Cheyenne were reused where possible (``miniconda``, ``qt``, ``ecflow``, ``mysql``). See below for information on how to install these packages.

.. _MaintainersSection_Cheyenne:

------------------------------
NCAR-Wyoming Cheyenne
------------------------------

On Cheyenne, a workaround is needed to avoid the modules provided by CISL take precedence over the spack modules. The default module path for compilers is removed, the module path is set to a different location and that location is then loaded into the module environment. If new compilers or MPI libraries are
added to ``/glade/u/apps/ch/modulefiles/default/compilers`` by CISL, the spack-stack maintainers need to make the corresponding changes in ``/glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers``. See :numref:`Section %s <Preconfigured_Sites_Cheyenne>` for details.

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

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/glade/work/jedipara/cheyenne/spack-stack/mysql-8.0.31``.

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

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/contrib/spack-stack/mysql-8.0.31``.

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

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

On Hera, ``miniconda`` must be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/scratch1/NCEPDEV/global/spack-stack/apps/mysql-8.0.31``. Since Hera cannot access the MySQL community URL, the tarball needs to be downloaded on a different machine and then copied over.

Hera sits behind the NOAA firewall and doesn't have access to all packages on the web. It is therefore necessary to create a spack mirror on another platform (e.g. Cheyenne). This can be done as described in section :numref:`Section %s <MaintainersSection_spack_mirrors>` for air-gapped systems.

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
   
mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/lfs4/HFIP/hfv3gfs/role.epic/apps/mysql-8.0.31``. Since Jet cannot access the MySQL community URL, the tarball needs to be downloaded on a different machine and then copied over.


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
   The ``gnu/9.3.0`` module provided by the system administrators is broken. To create a usable version, turn ``/data/prod/hpc-stack/modulefiles/core/gnu/9.3.0.lua`` into a simple environment module (``tcl``) in ``/data/prod/jedi/spack-stack/modulefiles/gnu``.

mpich (module only)
   The ``mpich/4.0.1`` module provided by the system administrators is broken. To create a usable version, turn ``/data/prod/hpc-stack/modulefiles/compiler/gnu/9.3.0/mpich/4.0.1.lua`` into a simple environment module (``tcl``) in ``/data/prod/jedi/spack-stack/modulefiles/mpich``.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <Prerequisites_ecFlow>`.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load gcc/9.3.0

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <Prerequisites_MySQL>` to install ``mysql`` in ``/data/prod/jedi/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_AWS_Pcluster_Ubuntu:

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

See ``configs/sites/aws-pcluster/README.md``.

.. _MaintainersSection_Testing_New_Packages:

.. _MaintainersSection_spack_mirrors:

==================================
Creating/maintaining spack mirrors
==================================

Spack mirrors allow downloading the source code required to build environments once to a local directory (in the following also referred to as source cache), and then use this directory for subsequent installations. If a package cannot be found in the mirror (e.g. because a newer version is required), it will automatically be pulled from the web. It won't be added to the source cache automatically, this is a step that needs to be done manually.

Spack mirrors also make it possible to download the source code for an air-gapped machine on another system, then transferring the entire mirror to the system without internet access and using it during the installation.

-----------------------------
Spack mirrors for local reuse
-----------------------------

Since all spack-stack installations are based on environments, we only cover spack mirrors for environments here. For a more general discussion, users are referred to the `Spack Documentation <https://spack.readthedocs.io/en/latest>`_.

1. Create an environment as usual, activate it and run the concretization step (``spack concretize``), but do not start the installation yet.

2. Create the spack mirror in ``/path/to/spack-mirror``.

.. code-block:: console

   spack mirror create -a -d /path/to/spack-source

3. If the spack mirror already exists, then existing packages will be ignored and only new packages will be added to the mirror.

4. If not already included in the environment (e.g. from the spack-stack site config), add the mirror:

.. code-block:: console
   spack mirror list
   spack mirror add local-source file:///path/to/spack-source

   The newly created local mirror should be listed at the top, which means that spack will search this directory first.

7. Proceed with the installation as usual.

------------------------------------
Spack mirrors for air-gapped systems
------------------------------------

The procedure is similar to using spack mirrors for local reuse, but a few additional steps are needed in between.

1. On the air-gapped system: Create an environment as usual, activate it and run the concretization step (``spack concretize``), but do not start the installation yet.

2. Copy the file ``spack.lock`` (in ``envs/env-name/``) to the machine with full internet access using ``scp``, for example.

3. On the machine with full internet access: Load the basic external modules, if using a machine that is preconfigured for spack-stack (see :numref:`Section %s <Preconfigured_Sites>`) and make sure that ``git`` supports ``lfs`` (if necessary, load the external modules that spack-stack also uses).

4. On the machine with full internet access: check out the same version of ``spack-stack``, run ``setup.sh``, and then the following sequence of commands. The mirror will be created in directory ``./spack/var/spack/environments/air_gapped_mirror_env``, while the mirror source code downloaded based on ``spack.lock`` will be placed in the directory specified by the ``-d`` argument passed to ``spack mirror create`` (below).

.. code-block:: console

   spack env create air_gapped_mirror_env spack.lock
   spack env activate air_gapped_mirror_env
   spack mirror create -a -d ./mirror/ 

5. On the air-gapped system: Copy the directory from the system with internet access to the local destination for the spack mirror. It is recommended to use ``rsync`` to avoid deleting existing packages, if updating an existing mirror on the air-gapped system. For example, to use ``rsync`` to copy the mirror directory from the machine with full internet access to the air-gapped system (with the ``rsync`` initiated from the air-gapped system):

.. code-block:: console

   rsync -av <username>@<source-host>:<path-to-mirror-directory-on-source-host> <destination-path-on-air-gapped-system>

6.. On the air-gapped system: Add the mirror to the spack environment's mirror list, unless already included in the site config.

.. code-block:: console

   spack mirror add locals-source  file:///path/to/spack-source
   spack mirror list

   The newly created local mirror should be listed at the top, which means that spack will search this directory first.

7. On the air-gapped system: Proceed with the installation as usual.

==============================
Testing new packages
==============================

--------------------------------
Using spack to test/add packages
--------------------------------

The simplest case of adding new packages that are available in spack-stack is described in :numref:`Section %s <Preconfigured_Sites_ExtendingEnvironments>`. As mentioned there, it is advised to take a backup of the spack environment (and install directories if outside the spack environment directory tree). It is also possible to chain spack installations, which means creating a test environment that uses installed packages and modulefiles from another (e.g. authoritative) spack environment and build the packages to be tested in isolation.

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
