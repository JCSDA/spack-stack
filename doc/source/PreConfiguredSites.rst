.. _Preconfigured_Sites:

Pre-configured sites
*************************

Pre-configured sites are split into two categories: Tier 1 with officially supported spack-stack installations (see :numref:`Section %s <Preconfigured_Sites_Tier1>`), and Tier 2 (sites with configuration files that were tested or contributed by others in the past, but that are not officially supported by the spack-stack team; see :numref:`Section %s <Preconfigured_Sites_Tier2>`).

Directories ``configs/sites/tier1`` and ``configs/sites/tier2`` contain site configurations for several HPC systems, as well as minimal configurations for macOS and Linux. The macOS and Linux configurations are **not** meant to be used as is, as user setups and package versions vary considerably. Instructions for adding this information can be found in :numref:`Section %s <NewSiteConfigs>`.

As of spack-stack-1.8.0, this page provides general information on the supported platforms, such as the location of the spack-stack installations on tier 1 platforms and instructions on how to set up an environment for **building** spack-stack environments. Information on **using** spack-stack environments for development of downstream applications is available on the spack-stack wiki: https://github.com/JCSDA/spack-stack/wiki

.. _EnvironmentNamingConventions:

=============================================================
Environment naming conventions
=============================================================

The following naming conventions are used on all fully-supported (tier 1) sites. Environments are named using an abbreviated prefix that depends on the template/purpose, followed by the compiler name and version: `prefix-compiler-version`. The following table lists the prefices and gives a few examples.

+----------------------------------+---------------------------------------------------------+----------------+---------------------------+
| Template (``configs/templates``) | Description                                             | Prefix         | Examples                  |
+==================================+=========================================================+================+===========================+
| ``unified-dev``                  | Unified environment for all organizations/applications  | ``ue``         | ``ue-intel-2021.10.0``    |
+----------------------------------+---------------------------------------------------------+----------------+---------------------------+
| ``skylab-dev``                   | JEDI/Skylab environment for JEDI, models, EWOK          | ``se``         | ``se-apple-clang@14.0.6`` |
+----------------------------------+---------------------------------------------------------+----------------+---------------------------+
| ``neptune-dev``                  | NEPTUNE standalone environment (with xNRL Python)       | ``ne``         | ``ne-oneapi02024.2.1``    |
+----------------------------------+---------------------------------------------------------+----------------+---------------------------+
| ``gsi-addon-dev``                | GSI addon (chained) environment on top of unified env.  | ``gsi``        | ``gsi-gcc@13.3.0``        |
+----------------------------------+---------------------------------------------------------+----------------+---------------------------+
| ``unified-dev`` with new ESMF    | Unified environment with new ESMF (chained from ``ue``) | ``esmf870b99`` | ``esmf870b99-aocc-4.2.0`` |
+----------------------------------+---------------------------------------------------------+----------------+---------------------------+


.. _Preconfigured_Sites_Tier1:

=============================================================
Pre-configured sites (tier 1)
=============================================================

+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
| Organization        | System                | Compilers          | Location of top-level spack-stack directory            | Maintainers     |
+=====================+=======================+====================+========================================================+=================+
| **HPC platforms**                                                                                                                           |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Hercules              | GCC, Intel         | ``/work/noaa/epic/role-epic/spack-stack/hercules/``    | EPIC / JCSDA    |
| MSU                 +-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Orion                 | GCC, Intel         | ``/work/noaa/epic/role-epic/spack-stack/orion/``       | EPIC / JCSDA    |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Discover SCU16        | GCC, Intel         | ``/gpfsm/dswdev/jcsda/spack-stack/scu16/``             | JCSDA           |
| NASA                +-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Discover SCU17        | GCC, Intel         | ``/gpfsm/dswdev/jcsda/spack-stack/scu17/``             | JCSDA           |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
| NCAR-Wyoming        + Derecho               | GCC, Intel         | ``/glade/work/epicufsrt/contrib/spack-stack/derecho/`` | EPIC / JCSDA    |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
| NOAA (NCEP)         | Acorn                 | Intel              | ``/lfs/h1/emc/nceplibs/noscrub/spack-stack/``          | NOAA-EMC        |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Gaea                  | Intel              | ``/ncrc/proj/epic/spack-stack/``                       | EPIC / NOAA-EMC |
|                     +-----------------------+--------------------+--------------------------------------------------------+-----------------+
| NOAA (RDHPCS)       | Hera                  | GCC, Intel         | ``/scratch1/NCEPDEV/nems/role.epic/spack-stack/``      | EPIC / NOAA-EMC |
|                     +-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Jet                   | GCC, Intel         | ``/mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/``      | EPIC / NOAA-EMC |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Narwhal               | GCC, Intel, oneAPI | ``/p/app/projects/NEPTUNE/spack-stack/``               | NRL             |
| U.S. Navy (HPCMP)   +-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Nautilus              | Intel              | ``/p/app/projects/NEPTUNE/spack-stack/``               | NRL             |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
| Univ. of Wisconsin  | S4                    | Intel              | ``/data/prod/jedi/spack-stack/``                       | JCSDA           |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
| **Cloud platforms**                                                                                                                         |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | AMI Red Hat 8         | GCC                | ``/home/ec2-user/spack-stack/``                        | JCSDA           |
+ Amazon Web Services +-----------------------+--------------------+--------------------------------------------------------+-----------------+
|                     | Parallelcluster JCSDA | GCC, Intel         |  *currently unavailable*                               | JCSDA           |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+
| NOAA (RDHPCS)       | RDHPCS Parallel Works | Intel              | ``/contrib/spack-stack/``                              | EPIC / JCSDA    |
+---------------------+-----------------------+--------------------+--------------------------------------------------------+-----------------+

.. _Preconfigured_Sites_Orion:

------------------------------
MSU Orion
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /work/noaa/epic/role-epic/spack-stack/orion/modulefiles-rocky9


.. _Preconfigured_Sites_Hercules:

------------------------------
MSU Hercules
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /work/noaa/epic/role-epic/spack-stack/hercules/modulefiles
   module load ecflow/5.8.4
   module load git-lfs/3.1.2


.. _Preconfigured_Sites_Discover_SCU16:

------------------------------
NASA Discover SCU16
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /discover/swdev/gmao_SIteam/modulefiles-SLES12
   module use /discover/swdev/jcsda/spack-stack/scu16/modulefiles
   module load miniconda/3.9.7
   module load ecflow/5.8.4


.. _Preconfigured_Sites_Discover_SCU17:

------------------------------
NASA Discover SCU17
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /discover/swdev/gmao_SIteam/modulefiles-SLES15
   module use /discover/swdev/jcsda/spack-stack/scu17/modulefiles
   module load ecflow/5.11.4


.. _Preconfigured_Sites_Narwhal:

------------------------------
NAVY HPCMP Narwhal
------------------------------

The following is required for building new spack environments with Intel on this platform.. Don't use ``module purge`` on Narwhal!

.. code-block:: console

   umask 0022
   module unload PrgEnv-cray
   module load PrgEnv-intel/8.3.3
   module unload intel
   module load intel-classic/2023.2.0
   module unload cray-mpich
   module unload craype-network-ofi
   # Warning. Do not load craype-network-ucx
   # or cray-mpich-ucx/8.1.21!
   # There is a bug in the modulefile that prevents
   # spack from setting the environment for its
   # build steps when the module is already
   # loaded. Instead, let spack load it when the
   # package requires it.
   #module load craype-network-ucx
   #module load cray-mpich-ucx/8.1.21
   module load libfabric/1.12.1.2.2.1
   module unload cray-libsci
   module load cray-libsci/23.05.1.4

The following is required for building new spack environments with GNU on this platform.. Don't use ``module purge`` on Narwhal!

.. code-block:: console

   umask 0022
   module unload PrgEnv-cray
   module load PrgEnv-gnu/8.3.3
   module unload gcc
   module load gcc/10.3.0
   module unload cray-mpich
   module unload craype-network-ofi
   # Warning. Do not load craype-network-ucx
   # or cray-mpich-ucx/8.1.21!
   # There is a bug in the modulefile that prevents
   # spack from setting the environment for its
   # build steps when the module is already
   # loaded. Instead, let spack load it when the
   # package requires it.
   #module load craype-network-ucx
   #module load cray-mpich-ucx/8.1.21
   module load libfabric/1.12.1.2.2.1
   module unload cray-libsci
   module load cray-libsci/23.05.1.4


.. _Preconfigured_Sites_Nautilus:

------------------------------
NAVY HPCMP Nautilus
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

.. code-block:: console

   umask 0022
   module purge


.. _Preconfigured_Sites_Derecho:

--------------------
NCAR-Wyoming Derecho
--------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   # ignore that the sticky module ncarenv/... is not unloaded
   export LMOD_TMOD_FIND_FIRST=yes
   module load ncarenv/23.09
   module use /glade/work/epicufsrt/contrib/spack-stack/derecho/modulefiles
   module load ecflow/5.8.4


.. _Preconfigured_Sites_Acorn:

-------------------------------
NOAA Acorn (WCOSS2 test system)
-------------------------------

**NEEDS UPDATING**

For spack-stack-1.7.0, the meta modules are in ``/lfs/h1/emc/nceplibs/noscrub/spack-stack/spack-stack-1.7.0/envs/ue-intel{19,2022}/modulefiles/Core``.

On WCOSS2 OpenSUSE sets ``CONFIG_SITE`` which causes libraries to be installed in ``lib64``, breaking the ``lib`` assumption made by some packages. Therefore, ``CONFIG_SITE`` should be set to empty in ``compilers.yaml``. Also, don't use ``module purge`` on Acorn!

When installing an official ``spack-stack`` on Acorn, be mindful of umask and group ownership, as these can be finicky. The umask value should be 002, otherwise various files can be assigned to the wrong group. In any case, running something to the effect of ``chgrp nceplibs <spack-stack dir> -R`` and ``chmod o+rX <spack-stack dir> -R`` after the whole installation is done is a good idea.

Due to a combined quirk of Cray and Spack, the ``PrgEnv-gnu`` and ``gcc`` modules must be loaded when `ESMF` is being installed with ``gcc``.

As of spring 2023, there is an inconsistency in ``libstdc++`` versions on Acorn between the login and compute nodes. It is advisable to compile on the compute nodes, which requires running ``spack fetch`` prior to installing through a batch job.

Note that certain packages, such as recent versions of `py-scipy`, cannot be compiled on compute nodes because their build systems require internet access.

.. note::
   System-wide ``spack`` software installations are maintained by NCO on this platform which are not associated with spack-stack. The spack-stack official installations use those installations for one dependency (git-lfs).

.. _Preconfigured_Sites_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

The following is required for building new spack environments with any supported compiler on this platform. The default module path needs to be removed, otherwise spack detects the system as Cray.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module unuse /opt/cray/craype/default/modulefiles
   module unuse /opt/cray/modulefiles
   module use /contrib/spack-stack/modulefiles
   module load cmake/3.27.2
   module load ecflow/5.8.4
   module load git-lfs/2.4.1


.. _Preconfigured_Sites_Gaea_C5:

------------------------------
NOAA RDHPCS Gaea C5
------------------------------

The following is required for building new spack environments with Intel on this platform.. Don't use ``module purge`` on Gaea!

**NEEDS UPDATING**

.. code-block:: console

   module load PrgEnv-intel/8.3.3
   module load intel-classic/2023.1.0
   module load cray-mpich/8.1.25
   module load python/3.9.12

   module use /ncrc/proj/epic/spack-stack/modulefiles
   module load ecflow/5.8.4


.. note::
   On Gaea, running ``module available`` without the option ``-t`` can lead to an error: ``/usr/bin/lua5.3: /opt/cray/pe/lmod/lmod/libexec/Spider.lua:568: stack overflow``

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE


.. _Preconfigured_Sites_Gaea_C6:

------------------------------
NOAA RDHPCS Gaea C6
------------------------------

The following is required for building new spack environments with Intel on this platform.. Don't use ``module purge`` on Gaea!

**NEEDS UPDATING**

.. code-block:: console

   module load PrgEnv-intel/8.3.3
   module load intel-classic/2023.1.0
   module load cray-mpich/8.1.25
   module load python/3.9.12

   module use /ncrc/proj/epic/spack-stack/modulefiles
   module load ecflow/5.8.4


.. note::
   On Gaea, running ``module available`` without the option ``-t`` can lead to an error: ``/usr/bin/lua5.3: /opt/cray/pe/lmod/lmod/libexec/Spider.lua:568: stack overflow``

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE


.. _Preconfigured_Sites_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /scratch1/NCEPDEV/nems/role.epic/modulefiles
   module load miniconda3/4.12.0
   module load ecflow/5.8.4

.. note::
   On Hera, a dedicated node exists for ``ecflow`` server jobs (``hecflow01``). Users starting ``ecflow_server`` on the regular login nodes will see their servers being killed every few minutes, and may be barred from accessing the system.


.. _Preconfigured_Sites_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /lfs4/HFIP/hfv3gfs/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.5.3
   module use /lfs4/HFIP/hfv3gfs/role.epic/modulefiles


.. _Preconfigured_Sites_S4:

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4


.. _Preconfigured_Sites_AWS_Parallelcluster:

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

**NEEDS UPDATING**

The JCSDA-managed AWS Parallel Cluster is currently unavailable.


.. _Preconfigured_Sites_AWS_SingleNode_RH8:

-----------------------------------------
Amazon Web Services Single Node Red Hat 8
-----------------------------------------

**NEEDS UPDATING**

Use a c6i.4xlarge instance or larger if running out of memory with AMI "skylab-8.0.0-redhat8" (see JEDI documentation at https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest for more information).


.. _Preconfigured_Sites_Tier2:

=============================================================
Pre-configured sites (tier 2)
=============================================================

Tier 2 preconfigured site are not officially supported by spack-stack. As such, instructions for these systems may be provided here, in form of a `README.md` in the site directory, or may not be available. Also, these site configs are not updated on the same regular basis as those of the tier 1 systems and therefore may be out of date and/or not working.


.. _Preconfigured_Sites_Blackpearl:

------------------------------
Blackpearl
------------------------------

Blackpearl is an Oracle Linux 9 installation running under Windows Subsystem for Linux (WSL2) on Windows 11. This is the development system of one of the spack-stack developers and maybe useful as an example configuration for users with a similar setup.


.. _Preconfigured_Sites_Casper:

------------------------------
NCAR-Wyoming Casper
------------------------------

The following is required for building new spack environments with any supported compiler on this platform.

**NEEDS UPDATING**

.. code-block:: console

   module purge
   # ignore that the sticky module ncarenv/... is not unloaded
   export LMOD_TMOD_FIND_FIRST=yes
   module load ncarenv/23.10
   module use /glade/work/epicufsrt/contrib/spack-stack/casper/modulefiles
   module load ecflow/5.8.4


.. _Preconfigured_Sites_EMC_RHEL:

------------------------------
EMC RedHat Enterprise Linux 8
------------------------------

**NEEDS UPDATING**


.. _Preconfigured_Sites_Frontera:

------------------------------
??? Frontera
------------------------------

**NEEDS UPDATING**


------------------------------
Linux/macOS default configs
------------------------------

The Linux and macOS configurations are **not** meant to be used as is, as user setups and package versions vary considerably. Instructions for adding this information can be found in :numref:`Section %s <NewSiteConfigs>`.


.. _Configurable_Sites_CreateEnv:

========================
Create local environment
========================

The following instructions install a new spack environment on a pre-configured site. Instructions for creating a new site config on a configurable system (i.e. a generic Linux or macOS system) can be found in :numref:`Section %s <NewSiteConfigs>`. The options for the ``spack stack`` extension are explained in :numref:`Section %s <SpackStackExtension>`.

.. code-block:: console

   git clone --recurse-submodules https://github.com/jcsda/spack-stack.git
   cd spack-stack

   # Ensure Python 3.8+ is available and the default before sourcing spack

   # Sources Spack from submodule and sets ${SPACK_STACK_DIR}
   source setup.sh

   # See a list of sites and templates
   spack stack create env -h

   # Create a pre-configured Spack environment in envs/<template>.<site>
   # (copies site-specific, application-specific, and common config files into the environment directory)
   spack stack create env --site hera --template unified-dev --name unified-dev.hera.intel --compiler intel

   # Activate the newly created environment
   # Optional: decorate the command line prompt using -p
   #     Note: in some cases, this can mess up long lines in bash
   #     because color codes are not escaped correctly. In this
   #     case, use export SPACK_COLOR='never' first.
   cd envs/unified-dev.hera.intel/
   spack env activate [-p] .

   # Optionally edit config files (spack.yaml, packages.yaml compilers.yaml, modules.yaml, ...)
   emacs spack.yaml
   emacs common/*.yaml
   emacs site/*.yaml

   # Process/concretize the specs; optionally check for duplicate packages
   spack concretize | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -d [-c] log.concretize

   # Optional step for systems with a pre-configured spack mirror, see below.

   # Install the environment, recommended to always use --source
   # to install the source code with the compiled binary package
   spack install --source [--verbose] [--fail-fast]

   # Create lua module files
   spack module lmod refresh

   # Create meta-modules for compiler, mpi, python
   spack stack setup-meta-modules

   # Check permissions for systems where non-owning users/groups need access
   ${SPACK_STACK_DIR}/util/check_permissions.sh

.. note::
  You may want to capture the output from :code:`spack concretize` and :code:`spack install` comands in log files.
  For example:

  .. code-block:: bash

    spack concretize 2>&1 | tee log.concretize
    spack install [--verbose] [--fail-fast] 2>&1 | tee log.install


.. _Preconfigured_Sites_ExtendingEnvironments:

======================
Extending environments
======================

Additional packages (and their dependencies) or new versions of packages can be added to existing environments. It is recommended to take a backup of the existing environment directory (e.g. using ``rsync``) or test this first as described in :numref:`Section %s <MaintainersSection_Testing_New_Packages>`, especially if new versions of packages are added that act themselves as dependencies for other packages. In some cases, adding new versions of packages will require rebuilding large portions of the stack, for example if a new version of ``hdf5`` is needed. In this case, it is recommended to start over with an entirely new environment.

In the simplest case, a new package (and its basic dependencies) or a new version of an existing package that is not a dependency for other packages can be added as described in the following example for a new version of ``ecmwf-atlas``.

1. Check if the package has any variants defined in the common (``env_dir/common/packages.yaml``) or site (``env_dir/site/packages.yaml``) package config and make sure that these are reflected
   correctly in the ``spec`` command:

.. code-block:: console

   spack spec ecmwf-atlas@0.29.0

2. Add package to environment specs:

.. code-block:: console

   spack add ecmwf-atlas@0.29.0

3. Run ``concretize`` step

.. code-block:: console

   spack concretize

4. Install

.. code-block:: console

   spack install [--verbose] [--fail-fast]

Further information on how to define variants for new packages, how to use these non-standard versions correctly as dependencies, ..., can be found in the `Spack Documentation <https://spack.readthedocs.io/en/latest>`_. Details on the ``spack stack`` extension of the ``spack`` are provided in :numref:`Section %s <SpackStackExtension>`.

.. note::
   Instead of ``spack add ecmwf-atlas@0.29.0``, ``spack concretize`` and ``spack install``, one can also just use ``spack install ecmwf-atlas@0.29.0`` after checking in the first step (``spack spec``) that the package will be installed as desired.
