.. _Preconfigured_Sites:

Pre-configured sites
*************************

Directory ``configs/sites`` contains site configurations for several HPC systems, as well as minimal configurations for macOS and Linux. The macOS and Linux configurations are **not** meant to be used as is, as user setups and package versions vary considerably. Instructions for adding this information can be found in :numref:`Section %s <NewSiteConfigs>`.

Pre-configured sites are split into two categories: Tier 1 with officially supported spack-stack installations (see :numref:`Section %s <Preconfigured_Sites_Tier1>`), and Tier 2 (sites with configuration files that were tested or contributed by others in the past, but that are not officially supported by the spack-stack team; see :numref:`Section %s <Preconfigured_Sites_Tier2>`).

=============================================================
Officially supported spack-stack 1.7.0 installations (tier 1)
=============================================================

Ready-to-use spack-stack 1.7.0 installations are available on the following, fully supported platforms. This version supports JEDI-Skylab and various UFS and related applications (UFS Weather Model, EMC Global Workflow, GSI, UFS Short Range Weather Application). Amazon Web Services AMI are available in the US East 1 or 2 regions.

+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| Organization        | System                           | Compilers       | Location                                                                     | Maintainers (principal/backup)|
+=====================+==================================+=================+==============================================================================+===============================+
| **HPC platforms**                                                                                                                                                                       |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Hercules                         | GCC, Intel      | ``/work/noaa/epic/role-epic/spack-stack/hercules/spack-stack-1.7.0/envs``    | EPIC / JCSDA                  |
| MSU                 +----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Orion                            | GCC, Intel      | ``/work/noaa/epic/role-epic/spack-stack/orion/spack-stack-1.7.0/envs``       | EPIC / JCSDA                  |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Discover SCU16                   | GCC, Intel      | ``/gpfsm/dswdev/jcsda/spack-stack/scu16/spack-stack-1.7.0/envs``             | JCSDA                         |
| NASA                +----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Discover SCU17                   | GCC, Intel      | ``/gpfsm/dswdev/jcsda/spack-stack/scu17/spack-stack-1.7.0/envs``             | JCSDA                         |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| NCAR-Wyoming        + Derecho                          | GCC, Intel      | ``/glade/work/epicufsrt/contrib/spack-stack/derecho/spack-stack-1.7.0/envs`` | EPIC / JCSDA                  |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| NOAA (NCEP)         | Acorn                            | Intel           | ``/lfs/h1/emc/nceplibs/noscrub/spack-stack/spack-stack-1.7.0/envs``          | NOAA-EMC                      |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Gaea                             | Intel           | ``/ncrc/proj/epic/spack-stack/spack-stack-1.7.0/envs``                       | EPIC / NOAA-EMC               |
|                     +----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| NOAA (RDHPCS)       | Hera                             | GCC, Intel      | ``/scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.7.0/envs``      | EPIC / NOAA-EMC               |
|                     +----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Jet                              | GCC, Intel      | ``/mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.7.0/envs``      | EPIC / NOAA-EMC               |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Narwhal                          | GCC, Intel      | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.7.0/envs``               | NRL                           |
| U.S. Navy (HPCMP)   +----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Nautilus                         | Intel           | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.7.0/envs``               | NRL                           |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| Univ. of Wisconsin  | S4                               | Intel           | ``/data/prod/jedi/spack-stack/spack-stack-1.7.0/envs``                       | JCSDA                         |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| **Cloud platforms**                                                                                                                                                                     |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | AMI Red Hat 8                    | GCC             | ``/home/ec2-user/spack-stack/spack-stack-1.7.0/envs``                        | JCSDA                         |
+ Amazon Web Services +----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
|                     | Parallelcluster JCSDA R&D        | GCC, Intel      |  *currently unavailable*                                                     | JCSDA                         |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+
| NOAA (RDHPCS)       | RDHPCS Cloud (Parallel Works)    | Intel           | ``/contrib/spack-stack/spack-stack-1.7.0/envs``                              | EPIC / JCSDA                  |
+---------------------+----------------------------------+-----------------+------------------------------------------------------------------------------+-------------------------------+

.. note::
  This release of spack-stack uses different versions of ``mapl`` with different variants, depending on the version of the compiler and whether the system is used for UFS or GEOS. Please see the following table.

+----------------------------+--------------------------------------+-----------------------------------------------------------------------+
| Compiler                   | mapl configuration                   | Affected systems                                                      |
+============================+======================================+=======================================================================+
| gcc (any)                  | ``mapl@2.40.3 +pflogger +extdata2g`` | All systems with GCC stacks                                           |
+----------------------------+--------------------------------------+-----------------------------------------------------------------------+
| intel@2021.6.0 and earlier | ``mapl@2.40.3 +pflogger +extdata2g`` | Discover SCU16, Acorn, Hera, Jet, Narwhal, Nautilus, S4, RDHPCS Cloud |
+----------------------------+--------------------------------------+-----------------------------------------------------------------------+
| intel@2021.7.0 and later   | ``mapl@2.40.3 ~pflogger ~extdata2g`` | Hercules, Orion, Acorn, Gaea and Derecho                              |
+----------------------------+--------------------------------------+-----------------------------------------------------------------------+
| intel@2021.7.0 and later   | ``mapl@2.43.0 +pflogger +extdata2g`` | Discover SCU17                                                        |
+----------------------------+--------------------------------------+-----------------------------------------------------------------------+

.. note::
  We have noted problems on some - not all - platforms with ``intel@2021.5.0`` when we switched from ``zlib`` to ``zlib-ng`` in spack-stack-1.7.0. These issues went away when using a different version of the compiler (anything between 2021.3.0 and 2021.11.0). It is therefore recommended to avoid using ``intel@2021.5.0`` unless it is the only option.

**To use one of the above installations** via the system default environment module system, and adding certain modules first (see individual sections below), add ``/install/modulefiles/Core`` to the path from the above table and prepend that path to $MODULEPATH, e.g.,

.. code-block:: console

  # On Gaea:
  module use /ncrc/proj/epic/spack-stack/spack-stack-1.6.0/envs/unified-env/install/modulefiles/Core
  module load stack-intel
  module load bacio netcdf-c ...

For more information about a specific platform, please see the individual sections below.

For questions or problems, please consult the known issues in :numref:`Section %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/jcsda/spack-stack/issues>`_ and `discussions <https://github.com/jcsda/spack-stack/discussions>`_ first.

.. _supplemental_environments:

=========================
Supplemental environments
=========================
 
The following is a list of supplemental or "add-on" environments that are maintained through spack-stack. Note that not all are included with every release; see the third column to determine release location and look under ``envs/`` subdirectory (i.e., same parent directory as ``ue-*`` directories per the above table). Check the installation directories to verify which package versions are available before using them.

+------------------+---------------------------------------------------------+------------------------+-------------------------------------------+
| Environment name | Description                                             | spack-stack release(s) | Platforms                                 |
+==================+=========================================================+========================+===========================================+
| gsi-addon-*      | Supports GSI and related applications                   | 1.6.0, 1.7.0           | Hera, Hercules, Gaea, Jet, S4             |
+------------------+---------------------------------------------------------+------------------------+-------------------------------------------+
| ufswm-*          | Supports UFS Weather Model with WCOSS2 package versions | 1.6.0                  | Acorn, Hera, Hercules, Jet, Orion         |
+------------------+---------------------------------------------------------+------------------------+-------------------------------------------+

.. _Preconfigured_Sites_Tier1:

=============================================================
Pre-configured sites (tier 1)
=============================================================

.. _Preconfigured_Sites_Orion:

------------------------------
MSU Orion
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work/noaa/epic/role-epic/spack-stack/orion/modulefiles
   module load python/3.9.2
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/orion/spack-stack-1.7.0/envs/ue-intel/install/modulefiles/Core
   module load stack-intel/2021.9.0
   module load stack-intel-oneapi-mpi/2021.9.0
   module load stack-python/3.10.13

For ``spack-stack-1.7.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/orion/spack-stack-1.7.0/envs/ue-gcc/install/modulefiles/Core
   module load stack-gcc/12.2.0
   module load stack-openmpi/4.1.6
   module load stack-python/3.10.13

.. note::
   The unified environment on Orion uses ``cdo@2.3.0`` instead of the default ``cdo@2.2.0``. This is a temporary change for release/1.7.0 and no longer needed on develop.

------------------------------
MSU Hercules
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work/noaa/epic/role-epic/spack-stack/hercules/modulefiles
   module load ecflow/5.8.4
   module load git-lfs/3.1.2

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/hercules/spack-stack-1.7.0/envs/ue-intel/install/modulefiles/Core
   module load stack-intel/2021.9.0
   module load stack-intel-oneapi-mpi/2021.9.0
   module load stack-python/3.10.13

For ``spack-stack-1.7.0`` with GNU, proceed with loading the following modules:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/hercules/spack-stack-1.7.0/envs/ue-gcc/install/modulefiles/Core
   module load stack-gcc/12.2.0
   module load stack-openmpi/4.1.6
   module load stack-python/3.10.13

.. _Preconfigured_Sites_Discover_SCU16:

------------------------------
NASA Discover SCU16
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /discover/swdev/gmao_SIteam/modulefiles-SLES12
   module use /discover/swdev/jcsda/spack-stack/scu16/modulefiles
   module load miniconda/3.9.7
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/scu16/spack-stack-1.7.0/envs/ue-intel-2021.6.0/install/modulefiles/Core
   module load stack-intel/2021.6.0
   module load stack-intel-oneapi-mpi/2021.6.0
   module load stack-python/3.10.13

For ``spack-stack-1.7.0`` with GNU, proceed with loading the following modules:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/scu16/spack-stack-1.7.0/envs/ue-gcc-12.1.0/install/modulefiles/Core
   module load stack-gcc/12.1.0
   module load stack-openmpi/4.1.3
   module load stack-python/3.10.13

------------------------------
NASA Discover SCU17
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /discover/swdev/gmao_SIteam/modulefiles-SLES15
   module use /discover/swdev/jcsda/spack-stack/scu17/modulefiles
   module load ecflow/5.11.4

For ``spack-stack-1.7.0`` with Intel, load the following modules after loading ecflow:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/scu17/spack-stack-1.7.0/envs/ue-intel-2021.10.0/install/modulefiles/Core
   module load stack-intel/2021.10.0
   module load stack-intel-oneapi-mpi/2021.10.0
   module load stack-python/3.10.13

For ``spack-stack-1.7.0`` with GNU, load the following modules after loading ecflow:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/scu17/spack-stack-1.7.0/envs/ue-gcc-12.3.0/install/modulefiles/Core
   module load stack-gcc/12.3.0
   module load stack-openmpi/4.1.6
   module load stack-python/3.10.13

.. _Preconfigured_Sites_Narwhal:

------------------------------
NAVY HPCMP Narwhal
------------------------------

With Intel, the following is required for building new spack environments and for using spack to build and run software. Don't use ``module purge`` on Narwhal!

.. code-block:: console

   umask 0022
   module unload PrgEnv-cray
   module load PrgEnv-intel/8.3.2
   module unload intel
   module load intel-classic/2021.4.0
   module unload cray-mpich
   module load cray-mpich/8.1.14
   module unload cray-python
   module load cray-python/3.9.7.1
   module unload cray-libsci
   module load cray-libsci/22.08.1.1

   module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   # These extra steps are required for performance reason, ofi is about 30% slower than ucx
   # Note we can't load craype-network-ucx for building spack-stack environments, must do here
   module unload craype-network-ofi
   module load craype-network-ucx
   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.7.0/envs/ue-intel-2021.4.0/install/modulefiles/Core
   module load stack-intel/2021.4.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.10.13

With GNU, the following is required for building new spack environments and for using spack to build and run software.  Don't use ``module purge`` on Narwhal!

.. code-block:: console

   umask 0022
   module unload PrgEnv-cray
   module load PrgEnv-gnu/8.3.2
   module unload gcc
   module load gcc/10.3.0
   module unload cray-mpich
   module load cray-mpich/8.1.14
   module unload cray-python
   module load cray-python/3.9.7.1
   module unload cray-libsci
   module load cray-libsci/22.08.1.1

   module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with GNU, proceed with loading the following modules:

.. code-block:: console

   # These extra steps are required for performance reason, ofi is about 30% slower than ucx
   # Note we can't load craype-network-ucx for building spack-stack environments, must do here
   module unload craype-network-ofi
   module load craype-network-ucx
   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.7.0/envs/ue-gcc-10.3.0/install/modulefiles/Core
   module load stack-gcc/10.3.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.10.13

.. _Preconfigured_Sites_Nautilus:

------------------------------
NAVY HPCMP Nautilus
------------------------------

With Intel, the following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   umask 0022
   module purge

   module load slurm
   module load intel/compiler/2022.0.2
   module load penguin/openmpi/4.1.6/intel-classic-2022.0.2

   module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.7.0/envs/ue-intel-2021.5.0/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-openmpi/4.1.6
   module load stack-python/3.10.13

With AMD clang/flang (aocc), the following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   umask 0022
   module purge

   module load slurm
   module load amd/aocc/4.0.0
   module load amd/aocl/aocc/4.0
   module load penguin/openmpi/4.1.4/aocc

   module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
   module load ecflow/5.8.4

.. note::

   ``spack-stack-1.7.0`` is not yet supported with the Arm clang/flang compilers. Use Intel instead.

.. note::

   `wgrib2@2.0.8` does not build on Nautilus, therefore we are using `wgrib2@3.1.1` on this system.

.. _Preconfigured_Sites_Derecho:

--------------------
NCAR-Wyoming Derecho
--------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   # ignore that the sticky module ncarenv/... is not unloaded
   export LMOD_TMOD_FIND_FIRST=yes
   module load ncarenv/23.09
   module use /glade/work/epicufsrt/contrib/spack-stack/derecho/modulefiles
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/derecho/spack-stack-1.7.0/envs/ue-intel/install/modulefiles/Core
   module load stack-intel/2021.10.0
   module load stack-cray-mpich/8.1.25
   module load stack-python/3.10.13

For ``spack-stack-1.7.0`` with GNU, proceed with loading the following modules:

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/derecho/spack-stack-1.7.0/envs/ue-gcc/install/modulefiles/Core
   module load stack-gcc/12.2.0
   module load stack-cray-mpich/8.1.25
   module load stack-python/3.10.13

.. note::
   CISL restricts the amount of memory available for processes on the login nodes. For example, it is impossible to compile JEDI with even one task (``make -j1``) with the Intel compiles in release mode (``-O2``). We therefore recommend compiling on compute nodes using interactive jobs, if possible.

.. _Preconfigured_Sites_Acorn:

-------------------------------
NOAA Acorn (WCOSS2 test system)
-------------------------------

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

The following is required for building new spack environments and for using spack to build and run software. The default module path needs to be removed, otherwise spack detects the system as Cray.

.. code-block:: console

   module purge
   module unuse /opt/cray/craype/default/modulefiles
   module unuse /opt/cray/modulefiles
   module use /contrib/spack-stack/modulefiles
   module load cmake/3.27.2
   module load ecflow/5.8.4
   module load git-lfs/2.4.1

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /contrib/spack-stack/spack-stack-1.7.0/envs/ue-intel-2021.3.0/install/modulefiles/Core
   module load stack-intel/2021.3.0
   module load stack-intel-oneapi-mpi/2021.3.0
   module load stack-python/3.10.13

.. _Preconfigured_Sites_Gaea:

------------------------------
NOAA RDHPCS Gaea
------------------------------

The following is required for building new spack environments and for using spack to build and run software. Log into a head node, and don't use ``module purge`` on Gaea!

.. code-block:: console

   module load PrgEnv-intel/8.3.3
   module load intel-classic/2023.1.0
   module load cray-mpich/8.1.25
   module load python/3.9.12

   module use /ncrc/proj/epic/spack-stack/modulefiles
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /ncrc/proj/epic/spack-stack/spack-stack-1.7.0/envs/ue-intel/install/modulefiles/Core
   module load stack-intel/2023.1.0
   module load stack-cray-mpich/8.1.25
   module load stack-python/3.10.13
   module -t available

.. note::
   On Gaea, running ``module available`` without the option ``-t`` leads to an error: ``/usr/bin/lua5.3: /opt/cray/pe/lmod/lmod/libexec/Spider.lua:568: stack overflow``

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE

.. _Preconfigured_Sites_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /scratch1/NCEPDEV/nems/role.epic/modulefiles
   module load miniconda3/4.12.0
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.7.0/envs/ue-intel/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.10.13

For ``spack-stack-1.7.0`` with GNU, proceed with loading the following modules:

.. code-block:: console

   module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.7.0/envs/ue-gcc/install/modulefiles/Core
   module load stack-gcc/9.2.0
   module load stack-openmpi/4.1.5
   module load stack-python/3.10.13

Note that on Hera, a dedicated node exists for ``ecflow`` server jobs (``hecflow01``). Users starting ``ecflow_server`` on the regular login nodes will see their servers being killed every few minutes, and may be barred from accessing the system.

.. _Preconfigured_Sites_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /lfs4/HFIP/hfv3gfs/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.5.3
   module use /lfs4/HFIP/hfv3gfs/role.epic/modulefiles

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.7.0/envs/ue-intel/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.10.8

For ``spack-stack-1.7.0`` with GNU, proceed with loading the following modules:

.. code-block:: console

   module use /mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.7.0/envs/ue-gcc/install/modulefiles/Core
   module load stack-gcc/9.2.0
   module load stack-openmpi/3.1.4
   module load stack-python/3.10.8

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4

For ``spack-stack-1.7.0`` with Intel, proceed with loading the following modules:

.. code-block:: console

   module use /data/prod/jedi/spack-stack/spack-stack-1.7.0/envs/ue-intel-2021.5.0/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.10.13
   module unuse /opt/apps/modulefiles/Compiler/intel/non-default/22
   module unuse /opt/apps/modulefiles/Compiler/intel/22

Note the two `module unuse` commands, that need to be run after the stack metamodules are loaded. Loading the Intel compiler meta module loads the Intel compiler module provided by the sysadmins, which adds those two directories to the module path. These contain duplicate libraries that are not compatible with our stack, such as ``hdf4``.

.. note::
   There is currently no support for GNU on S4, because recent updates to ``hdf5`` require a newer version of ``mpich`` (or other MPI library) than available on the system. Also, for spack-stack-1.7.0, S4 is the only system that uses ``zlib`` instead of ``zlib-ng`` due to the issues described in https://github.com/JCSDA/spack-stack/issues/1055.

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

The JCSDA-managed AWS Parallel Cluster is currently unavailable.

-----------------------------
Amazon Web Services Red Hat 8
-----------------------------

Use a c6i.4xlarge instance or larger if running out of memory with AMI "skylab-8.0.0-redhat8" (see JEDI documentation at https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest for more information).

For ``spack-stack-1.7.0``, run:

.. code-block:: console

   ulimit -s unlimited
   scl_source enable gcc-toolset-11
   module use /home/ec2-user/spack-stack/spack-stack-1.7.0/envs/unified-env-gcc-11.2.1/install/modulefiles/Core
   module load stack-gcc/11.2.1
   module load stack-openmpi/5.0.1
   module load stack-python/3.10.13

.. _Preconfigured_Sites_Tier2:

=============================================================
Pre-configured sites (tier 2)
=============================================================

Tier 2 preconfigured site are not officially supported by spack-stack. As such, instructions for these systems may be provided here, in form of a `README.md` in the site directory, or may not be available. Also, these site configs are not updated on the same regular basis as those of the tier 1 systems and therefore may be out of date and/or not working.

The following sites have site configurations in directory `configs/sites/`:
- TACC Frontera (`configs/sites/frontera/`)
- AWS Single Node with Nvidia (NVHPC) compilers (`configs/sites/aws-nvidia/`)

.. _Preconfigured_Sites_Casper:

------------------------------
NCAR-Wyoming Casper
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   # ignore that the sticky module ncarenv/... is not unloaded
   export LMOD_TMOD_FIND_FIRST=yes
   module load ncarenv/23.10
   module use /glade/work/epicufsrt/contrib/spack-stack/casper/modulefiles
   module load ecflow/5.8.4

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
   spack stack create env --site hera --template unified-dev --name unified-dev.hera

   # Activate the newly created environment
   # Optional: decorate the command line prompt using -p
   #     Note: in some cases, this can mess up long lines in bash
   #     because color codes are not escaped correctly. In this
   #     case, use export SPACK_COLOR='never' first.
   cd envs/unified-dev.hera/
   spack env activate [-p] .

   # Edit the main config file for the environment and adjust the compiler matrix
   # to match the compilers available on your system, or a subset of them (see
   # note below for more information). Replace
   #    definitions:
   #    - compilers: ['%apple-clang', '%gcc', '%intel']
   # with the appropriate list of compilers for your system and desires, e.g.
   #    definitions:
   #    - compilers: ['%gcc', '%intel']
   emacs envs/unified-dev.hera/spack.yaml

   # Optionally edit config files (spack.yaml, packages.yaml compilers.yaml, site.yaml)
   emacs envs/unified-dev.hera/common/*.yaml
   emacs envs/unified-dev.hera/site/*.yaml

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

.. note::
  For platforms with multiple compilers in the site config, make sure that the correct compiler and corresponding MPI library are set correctly in ``envs/jedi-fv3.hera/site/packages.yaml`` before running ``spack concretize``. Also, check the output of ``spack concretize`` to make sure that the correct compiler is used (e.g. ``%intel-2022.0.1``). If not, edit ``envs/jedi-fv3.hera/site/compilers.yaml`` and remove the offending compiler. Then, remove ``envs/jedi-fv3.hera/spack.lock`` and rerun ``spack concretize``.

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
