.. _Preconfigured_Sites:

Pre-configured sites
*************************

Directory ``configs/sites`` contains site configurations for several HPC systems, as well as minimal configurations for macOS and Linux. The macOS and Linux configurations are **not** meant to be used as is, as user setups and package versions vary considerably. Instructions for adding this information can be found in :numref:`Section %s <NewSiteConfigs>`.

Pre-configured sites are split into two categories: Tier 1 with officially supported spack-stack installations (see :numref:`Section %s <Preconfigured_Sites_Tier1>`), and Tier 2 (sites with configuration files that were tested or contributed by others in the past, but that are not officially supported by the spack-stack team; see :numref:`Section %s <Preconfigured_Sites_Tier2>`).

=============================================================
Officially supported spack-stack 1.5.0 installations (tier 1)
=============================================================

Ready-to-use spack-stack 1.5.0 installations are available on the following, fully supported platforms. This version supports the JEDI Skylab release 5 of June 2023, and the UFS Weather Model of July 2023. It can also be used for testing spack-stack with other UFS applications (e.g. the UFS Short Range Weather Application, and the EMC Global Workflow). Amazon Web Services AMI are available in the US East 1 or 2 regions.

+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| Organization        | System                           | Compilers       | Location                                                                                                | Maintainers                   |
+=====================+==================================+=================+=========================================================================================================+===============================+
| **HPC platforms**                                                                                                                                                                                                  |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Hercules^*                       | GCC, Intel      | ``/work/noaa/epic/role-epic/spack-stack/hercules/spack-stack-1.5.0/envs/unified-env``                   | Cam Book / Dom Heinzeller     |
| MSU                 +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Orion                            | GCC, Intel      | ``/work/noaa/epic/role-epic/spack-stack/orion/spack-stack-1.5.0/envs/unified-env``                      | Cam Book / Dom Heinzeller     |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| NASA                | Discover                         | GCC, Intel      | ``/gpfsm/dswdev/jcsda/spack-stack/spack-stack-1.5.0/envs/unified-env``                                  | Dom Heinzeller / ???          |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Casper                           | Intel           | ``/glade/work/epicufsrt/contrib/spack-stack/casper/spack-stack-1.4.1/envs/unified-env``                 | Dom Heinzeller / ???          |
|                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| NCAR-Wyoming        | Cheyenne                         | GCC, Intel      | ``/glade/work/epicufsrt/contrib/spack-stack/cheyenne/spack-stack-1.4.1/envs/unified-env``               | Cam Book / Dom Heinzeller     |
|                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Derecho^**                       | Intel           | ``/lustre/desc1/scratch/epicufsrt/contrib/spack-stack/spack-stack-dev-20230814/envs/unified-en2``       | Mark Potts / Dom Heinzeller   |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| NOAA (NCEP)         | Acorn                            | Intel           | ``/lfs/h1/emc/nceplibs/noscrub/spack-stack/spack-stack-1.4.1/envs/unified-env``                         | Hang Lei / Alex Richert       |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Gaea C4                          | Intel           | ``/lustre/f2/dev/wpo/role.epic/contrib/spack-stack/spack-stack-1.4.1-c4/envs/unified-env``              | Dom Heinzeller / ???          |
|                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Gaea C5                          | Intel           | ``/lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/spack-stack-dev-20230717/envs/unified-env``       | Dom Heinzeller / ???          |
| NOAA (RDHPCS)       +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Hera                             | GCC, Intel      | ``/scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.4.1/envs/unified-env``                     | Mark Potts / Dom Heinzeller   |
|                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Jet                              | GCC, Intel      | ``/mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.4.1/envs/unified-env``                     | Cam Book / Dom Heinzeller     |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Narwhal                          | Intel           | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.5.0/envs/unified-env-intel-2021.4.0``               | Dom Heinzeller / Sarah King   |
|                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Narwhal                          | GCC             | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.5.0/envs/unified-env-gcc-10.3.0``                   | Dom Heinzeller / Sarah King   |
| U.S. Navy (HPCMP)   +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Nautilus                         | Intel^*         | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.5.0/envs/unified-env``                              | Dom Heinzeller / Sarah King   |
|                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Nautilus                         | AOCC            | *currently not supported*                                                                               | Dom Heinzeller / Sarah King   |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | S4                               | Intel           | ``/data/prod/jedi/spack-stack/spack-stack-1.5.0/envs/unified-env``                                      | Dom Heinzeller / Mark Potts   |
| Univ. of Wisconsin  +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | S4                               | GCC             | *currently not supported*                                                                               | Dom Heinzeller / Mark Potts   |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| **Cloud platforms**                                                                                                                                                                                                |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | AMI Red Hat 8                    | GCC             | ``/home/ec2-user/spack-stack/spack-stack-1.4.0/envs/unified-env``                                       | Dom Heinzeller / ???          |
+                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| Amazon Web Services | Parallelcluster JCSDA R&D        |                 | ``/mnt/experiments-efs/skylab-v6/spack-stack-1.5.0/envs/unified-env``                                   | Dom Heinzeller / ???          |
+                     +----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
|                     | Parallelcluster JCSDA ROMEX      |                 | ``/mnt/experiments-efs/ROMEX/spack-stack-1.5.0/envs/unified-env``                                       | Dom Heinzeller / ???          |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+
| NOAA (RDHPCS)       | RDHPCS Cloud (Parallel Works)^** | Intel           | ``/contrib/spack-stack/spack-stack-dev-20230816/envs/unified-env``                                      | Mark Potts / Cam Book / Dom H |
+---------------------+----------------------------------+-----------------+---------------------------------------------------------------------------------------------------------+-------------------------------+

^* This system uses a different wgrib2 version 3.1.1 than the default 2.0.8.

For questions or problems, please consult the known issues in :numref:`Section %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/jcsda/spack-stack/issues>`_ and `discussions <https://github.com/jcsda/spack-stack/discussions>`_ first.

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
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/orion/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.0.2
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.10.8
   module available

For ``spack-stack-1.5.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/orion/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/10.2.0
   module load stack-openmpi/4.0.4
   module load stack-python/3.10.8
   module available

------------------------------
MSU Hercules
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work/noaa/epic/role-epic/spack-stack/hercules/modulefiles
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with Intel, load the following modules after loading mysql and ecflow:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/hercules/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.9.0
   module load stack-intel-oneapi-mpi/2021.9.0
   module load stack-python/3.10.8
   module available

For ``spack-stack-1.5.0`` with GNU, load the following modules after loading mysql and ecflow:

.. code-block:: console

   module use /work/noaa/epic/role-epic/spack-stack/hercules/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/11.3.1
   module load stack-openmpi/4.1.5
   module load stack-python/3.10.8
   module available

.. _Preconfigured_Sites_Discover:

------------------------------
NASA Discover
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.0.1
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.10.8
   module available

For ``spack-stack-1.5.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.3
   module load stack-python/3.10.8
   module available

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
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with Intel, load the following modules after loading the above modules.

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.5.0/envs/unified-env-intel-2021.4.0/install/modulefiles/Core
   module load stack-intel/2021.4.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.10.8

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
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with GNU, load the following modules after loading the above modules.

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.5.0/envs/unified-env-gcc-10.3.0/install/modulefiles/Core
   module load stack-gcc/10.3.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.10.8

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
   module load penguin/openmpi/4.1.5rc2/intel

   module use /p/app/projects/NEPTUNE/spack-stack/modulefiles
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with Intel, load the following modules after loading the above modules.

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-openmpi/4.1.5rc2
   module load stack-python/3.10.8

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
   module load mysql/8.0.31

.. note::

   ``spack-stack-1.5.0`` is not yet supported with the Arm clang/flang compilers. Use Intel instead.

.. note::

   There are still problems launching the ecflow GUI, although the package is installed.

.. _Preconfigured_Sites_Casper:

------------------------------
NCAR-Wyoming Casper
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   export LMOD_TMOD_FIND_FIRST=yes
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
   module load miniconda/3.9.12
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.4.1`` with Intel, load the following modules after loading miniconda and ecflow.

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/casper/spack-stack-1.4.1/envs/unified-env/install/modulefiles/Core
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2019.7.217
   module load stack-python/3.9.12
   module available

.. _Preconfigured_Sites_Cheyenne:

---------------------
NCAR-Wyoming Cheyenne
---------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   export LMOD_TMOD_FIND_FIRST=yes
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
   module load miniconda/3.9.12
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.4.1`` with Intel, load the following modules after loading miniconda, ecflow and mysql.

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/cheyenne/spack-stack-1.4.1/envs/unified-env
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2019.7.217
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.4.1`` with GNU, load the following modules after loading miniconda, ecflow and mysql.

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/cheyenne/spack-stack-1.4.1/envs/unified-env
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.1
   module load stack-python/3.9.12
   module available

.. _Preconfigured_Sites_Derecho:

--------------------
NCAR-Wyoming Derecho
--------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   # ignore that the sticky module ncarenv/... is not unloaded
   export LMOD_TMOD_FIND_FIRST=yes
   # Temporary, until CISL created the module tree for the newest Intel compilers
   module use /lustre/desc1/scratch/epicufsrt/contrib/modulefiles_extra
   module use /lustre/desc1/scratch/epicufsrt/contrib/modulefiles
   module load ecflow/5.8.4
   module load mysql/8.0.33

For ``spack-stack-develop`` as of 2023/08/25 with Intel, load the following modules after loading ecflow and mysql:

.. code-block:: console

   module use /lustre/desc1/scratch/epicufsrt/contrib/spack-stack/spack-stack-dev-20230825/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.10.0
   module load stack-cray-mpich/8.1.25
   module load stack-python/3.10.10
   module available

.. note::
   CISL restricts the amount of memory available for processes on the login nodes. For example, it is impossible to compile JEDI with even one task (``make -j1``) with the Intel compiles in release mode (``-O2``). We therefore recommend compiling on compute nodes using interactive jobs, if possible.

.. _Preconfigured_Sites_Acorn:

-------------------------------
NOAA Acorn (WCOSS2 test system)
-------------------------------

For spack-stack-1.4.1, the meta modules are in ``/lfs/h1/emc/nceplibs/noscrub/spack-stack/spack-stack-1.4.1/envs/unified-env/install/modulefiles/Core``.

On WCOSS2 OpenSUSE sets ``CONFIG_SITE`` which causes libraries to be installed in ``lib64``, breaking the ``lib`` assumption made by some packages. Therefore, ``CONFIG_SITE`` should be set to empty in ``compilers.yaml``. Also, don't use ``module purge`` on Acorn!

When installing an official ``spack-stack`` on Acorn, be mindful of umask and group ownership, as these can be finicky. The umask value should be 002, otherwise various files can be assigned to the wrong group. In any case, running something to the effect of ``chgrp nceplibs <spack-stack dir> -R`` and ``chmod o+rX <spack-stack dir> -R`` after the whole installation is done is a good idea.

Due to a combined quirk of Cray and Spack, the ``PrgEnv-gnu`` and ``gcc`` modules must be loaded when `ESMF` is being installed with ``gcc``.

As of spring 2023, there is an inconsistency in ``libstdc++`` versions on Acorn between the login and compute nodes. It is advisable to compile on the compute nodes, which requires running ``spack fetch`` prior to installing through a batch job.

Note that certain packages, such as recent versions of `py-scipy`, cannot be compiled on compute nodes because their build systems require internet access.

.. note::
   System-wide ``spack`` software installations are maintained by NCO on this platform. The spack-stack official installations use those installations for some dependencies.

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
   module load mysql/8.0.31
   module load git-lfs/2.4.1

For ``spack-stack-dev-20230816`` with Intel, load the following modules after loading miniconda, mysql and ecflow:

.. code-block:: console

   module use /contrib/spack-stack/spack-stack-dev-20230816/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.3.0
   module load stack-intel-oneapi-mpi/2021.3.0
   module load stack-python/3.10.8
   module available

.. _Preconfigured_Sites_Gaea:

------------------------------
NOAA RDHPCS Gaea C4
------------------------------

The following is required for building new spack environments and for using spack to build and run software. Make sure to log into a C4 head node, and don't use ``module purge`` on Gaea!

.. code-block:: console

   module unload intel
   module unload cray-mpich
   module unload cray-python
   module unload darshan
   module use /lustre/f2/pdata/esrl/gsd/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.4.1`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /lustre/f2/dev/wpo/role.epic/contrib/spack-stack/spack-stack-1.4.1-c4/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.0.2
   module load stack-cray-mpich/7.7.20
   module load stack-python/3.9.12
   module available

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE

.. _Preconfigured_Sites_Gaea_C5:

------------------------------
NOAA RDHPCS Gaea C5
------------------------------

The following is required for building new spack environments and for using spack to build and run software. Make sure to log into a C5 head node, and don't use ``module purge`` on Gaea!

.. code-block:: console

   module load PrgEnv-intel/8.3.3
   module load intel-classic/2023.1.0
   module load cray-mpich/8.1.25
   module load python/3.9.12

   module use /lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/modulefiles
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-20230717`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/spack-stack-dev-20230717/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2023.1.0
   module load stack-cray-mpich/8.1.25
   module load stack-python/3.9.12
   module -t available

.. note::

   The recent update to ``spack-stack-dev-20230717`` was required on Gaea C5 due to a bug in the Intel compilers used in ``spack-stack-1.4.1``.

.. note::
   On Gaea C5, running ``module available`` without the option ``-t`` leads to an error: ``/usr/bin/lua5.3: /opt/cray/pe/lmod/lmod/libexec/Spider.lua:568: stack overflow``

.. note::
   On Gaea C5, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE

.. _Preconfigured_Sites_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /scratch1/NCEPDEV/jcsda/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.5.3
   module load mysql/8.0.31

For ``spack-stack-1.4.1`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.4.1/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.4.1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.4.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/9.2.0
   module load stack-openmpi/4.1.5
   module load stack-python/3.9.12
   module available

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
   module load mysql/8.0.31

For ``spack-stack-1.4.1`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.4.1/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.4.1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.4.1/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/9.2.0
   module load stack-openmpi/3.1.4
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
   module load mysql/8.0.31

For ``spack-stack-1.5.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /data/prod/jedi/spack-stack/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.10.8
   module unuse /opt/apps/modulefiles/Compiler/intel/non-default/22
   module unuse /opt/apps/modulefiles/Compiler/intel/22
   module available

Note the two `module unuse` commands, that need to be run after the stack metamodules are loaded. Loading the Intel compiler meta module loads the Intel compiler module provided by the sysadmins, which adds those two directories to the module path. These contain duplicate libraries that are not compatible with our stack, such as ``hdf4``.

.. note::

   There is currently no support for GNU on S4, because recent updates to ``hdf5`` require a newer version of ``mpich`` (or other MPI library) than available on the system.

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

Access to the JCSDA-managed AWS Parallel Clusters is not available to the public. The following instructions are for JCSDA core staff and in-kind contributors.

For ``spack-stack-1.5.0`` with Intel on the JCSDA R&D cluster (``hpc6a.48xlarge`` instances), run the following commands/load the following modules:

.. code-block:: console

   module purge
   ulimit -s unlimited
   source /opt/intel/oneapi/compiler/2022.1.0/env/vars.sh
   module use /mnt/experiments-efs/skylab-v6/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.1.0
   module load stack-intel-oneapi-mpi/2021.6.0
   module load stack-python/3.10.8
   module available

For ``spack-stack-1.5.0`` with GNU on the JCSDA R&D cluster (``hpc6a.48xlarge`` instances), run the following commands/load the following modules:

   module purge
   ulimit -s unlimited
   module use /mnt/experiments-efs/skylab-v6/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/9.4.0
   module load stack-openmpi/4.1.4
   module load stack-python/3.10.8
   module available

.. note::

   Users reported problems with parallel applications using GNU+OpenMPI in earlier versions of spack-stack. This may still be the case for ``spack-stack-1.5.0``. We recommend using the well-tested Intel setup.

For ``spack-stack-1.5.0`` with Intel on the JCSDA ROMEX cluster (``c6i.32xlarge`` instances), run the following commands/load the following modules:

.. code-block:: console

   module purge
   ulimit -s unlimited
   source /opt/intel/oneapi/compiler/2022.1.0/env/vars.sh
   module use /mnt/experiments-efs/ROMEX/spack-stack-1.5.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.1.0
   module load stack-intel-oneapi-mpi/2021.6.0
   module load stack-python/3.10.8
   module available

.. note::

   There is no GNU option for the ROMEX cluster.

-----------------------------
Amazon Web Services Red Hat 8
-----------------------------

Use a c6i.4xlarge instance or similar with AMI "skylab-5.0.0-redhat8" (ami-02324faac94a9cac9 in region us-east-1, ami-038d9beca351f9005 in region us-east-2).

For ``spack-stack-1.4.0``, run:

.. code-block:: console

   ulimit -s unlimited
   scl enable gcc-toolset-11 bash
   module use /home/ec2-user/spack-stack/spack-stack-1.4.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/11.2.1
   module load stack-openmpi/4.1.5
   module load stack-python/3.10.8
   module available

-----------------------------
Amazon Web Services Ubuntu 20
-----------------------------

Use a c6i.4xlarge instance or similar with AMI "skylab-5.0.0-ubuntu20" (ami-09a8c9d3775feafcf in region us-east-1, ami-03e47cdb4ced34d7e in region us-east-2).

For ``spack-stack-1.4.0``, run:

.. code-block:: console

   ulimit -s unlimited
   module use /home/ubuntu/spack-stack/spack-stack-1.4.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/10.3.0
   module load stack-openmpi/4.1.5
   module load stack-python/3.10.8
   module available

.. _Preconfigured_Sites_Tier2:

=============================
Pre-configured sites (tier 2)
=============================

Tier 2 sites are sites with configuration files that were tested or contributed by others in the past, but that are not officially supported by the spack-stack team. The configuration files for these sites may not be up to date or functional.

------------------------------
TACC Frontera
------------------------------

.. note::
   ``spack-stack-1.4.0`` is currently not supported on this platform and may be added in the near future.

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work2/06146/tg854455/frontera/spack-stack/modulefiles
   module load miniconda/3.9.12
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
