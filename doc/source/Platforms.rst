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
   This version supports the JEDI Skylab release 3 of December 2022, and can be used for testing spack-stack with other applications (e.g. the UFS Weather Model). Amazon Web Services AMI are available in the US East 1 or 2 regions.

+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| System                                                   | Maintainers               | Location                                                                                                           |
+==========================================================+===========================+====================================================================================================================+
| MSU Orion Intel/GNU (**TEMPORARY**)                      | Dom Heinzeller            | ``/work2/noaa/da/role-da/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install``                           |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NASA Discover Intel/GNU (**TEMPORARY**)                  | Dom Heinzeller            | ``/gpfsm/dnb55/projects/p01/s2127/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install``                  |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NAVY HPCMP Narwhal Intel                                 | Dom Heinzeller            | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-2021.4.0/install``                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NAVY HPCMP Narwhal GNU (**TEMPORARY LOCATION**)          | Dom Heinzeller            | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-test-20230214/envs/skylab-dev-gnu-10.3.0-libsci-22.08.1.1/install``|
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Casper                                      | Dom Heinzeller            | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-19.1.1.217-casper/install``     |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne Intel/GNU (**TEMPORARY**)          | Dom Heinzeller            | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install``        |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA Parallel Works (AWS, Azure, Gcloud)                 |                           | not yet supported - coming soon                                                                                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea (C3/C4)                                 | Dom Heinzeller            | ``/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-2021.3.0/install``                  |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea (C5)                                    | Alex Richert / Dom Heinzeller | not yet supported - coming soon                                                                                |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera Intel                                   | Hang Lei / Dom Heinzeller | ``/scratch1/NCEPDEV/global/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-2021.5.0/install``                   |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera GNU                                     | Hang Lei / Dom Heinzeller | ``/scratch1/NCEPDEV/global/spack-stack/spack-stack-v1/envs/skylab-3.0.0-gnu-9.2.0/install``                        |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet Intel                                    |                           | not yet supported - coming soon                                                                                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet GNU                                      |                           | not yet supported - coming soon                                                                                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| TACC Frontera Intel                                      |                           | not yet supported - coming soon                                                                                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| TACC Frontera GNU                                        |                           | not yet supported - coming soon                                                                                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| UW (Univ. of Wisc.) S4 Intel/GNU (**TEMPORARY LOCATION**)| Dom Heinzeller            | ``/data/prod/jedi/spack-stack/spack-stack-feature-mysql-testing/envs/unified-4.0.0-rc1/install``                   |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| Amazon Web Services AMI Parallelcluster Ubuntu 20.04 GNU | Dom Heinzeller            | not yet supported - coming soon                                                                                    |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+
| Amazon Web Services AMI Red Hat 8 GNU                    | Dom Heinzeller            | ``/home/ec2-user/spack-stack-v1/envs/skylab-3.0.0-gcc-11.2.1/install``                                             |
+----------------------------------------------------------+---------------------------+--------------------------------------------------------------------------------------------------------------------+

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
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work2/noaa/da/role-da/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-intel/2022.0.2
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.7
   module available

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work2/noaa/da/role-da/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install/modulefiles/Core
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
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /gpfsm/dnb55/projects/p01/s2127/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-intel/2022.0.1
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.9.7
   module available

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /gpfsm/dnb55/projects/p01/s2127/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.3
   module load stack-python/3.9.7
   module available

.. _Platforms_Narwhal:

------------------------------
NAVY HPCMP Narwhal
------------------------------

With Intel, the following is required for building new spack environments and for using spack to build and run software:

.. code-block:: console

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

For ``spack-stack-1.2.0``/``skylab-3.0.0`` with Intel, load the following modules after loading the above modules.

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-2021.4.0/install/modulefiles/Core
   module load stack-intel/2021.4.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.9.7

With GNU, the following is required for building new spack environments and for using spack to build and run software:

.. code-block:: console

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

For ``spack-stack-1.2.0``/``skylab-3.0.0`` with GNU, load the following modules after loading the above modules. **Note: temporary location!**

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-test-20230214/envs/skylab-dev-gnu-10.3.0-libsci-22.08.1.1/install/modulefiles/Core
   module load stack-gcc/10.3.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.9.7

.. _Platforms_Casper:

-------------------
NCAR-Wyoming Casper
-------------------

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   export LMOD_TMOD_FIND_FIRST=yes
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
   module load miniconda/3.9.12
   module load ecflow/5.8.4
   module load mysql/8.0.31

For ``spack-stack-1.2.0``/``skylab-3.0.0`` with Intel, load the following modules after loading miniconda and ecflow.

.. code-block:: console

   module use /glade/work/jedipara/cheyenne/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-19.1.1.217-casper/install/modulefiles/Core
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2019.7.217
   module load stack-python/3.9.12
   module available

.. _Platforms_Cheyenne:

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

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with Intel, load the following modules after loading miniconda and ecflow. Note that there are problems with newer versions of the Intel compiler/MPI library when trying to run MPI jobs with just one task (``mpiexec -np 1``) - for JEDI, job hangs forever in a particular MPI communication call in oops.

.. code-block:: console

   module use /glade/work/jedipara/cheyenne/spack-stack/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2019.7.217
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /glade/work/jedipara/cheyenne/spack-stack/spack-stack-feature-r2d2-mysql/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.1
   module load stack-python/3.9.12
   module available

.. _Platforms_Acorn:

-------------------------------
NOAA Acorn (WCOSS2 test system)
-------------------------------

.. note::
   ``spack-stack-1.2.0``/``skylab-3.0.0`` is currently not supported on this platform and will be added in the near future.

On WCOSS2 OpenSUSE sets `CONFIG_SITE` which causes libraries to be installed in `lib64`, breaking the `lib` assumption made by some packages.

CONFIG_SITE should be set to empty in `compilers.yaml`.

.. note::
   ``spack`` software installations are maintained by NCO on this platform.

.. _Platforms_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

.. note::
   ``spack-stack-1.2.0``/``skylab-3.0.0`` is currently not supported on this platform and will be added in the near future.

The following is required for building new spack environments and for using spack to build and run software. The default module path needs to be removed, otherwise spack detect the system as Cray. It is also necessary to add ``git-lfs`` and some other utilities to the search path.

.. code-block:: console

   module unuse /opt/cray/craype/default/modulefiles
   module unuse /opt/cray/modulefiles
   export PATH="${PATH}:/contrib/spack-stack/apps/utils/bin"
   module use /contrib/spack-stack/modulefiles/core
   module load miniconda/3.9.7
   module load mysql/8.0.31

.. _Platforms_Gaea:

------------------------------
NOAA RDHPCS Gaea (C3/C4)
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
   module load mysql/8.0.31

For ``spack-stack-1.2.0``/``skylab-3.0.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-2021.3.0/install/modulefiles/Core
   module load stack-intel/2021.3.0
   module load stack-cray-mpich/7.7.11
   module load stack-python/3.9.12
   module available

.. note::
   On Gaea, a current limitation is that any executable that is linked against the MPI library (``cray-mpich``) must be run through ``srun`` on a compute node, even if it is run serially (one process). This is in particular a problem when using ``ctest`` for unit testing created by the ``ecbuild add_test`` macro. A workaround is to use the `cmake` cross-compiling emulator for this:

.. code-block:: console

   cmake -DCMAKE_CROSSCOMPILING_EMULATOR="/usr/bin/srun;-n;1" -DMPIEXEC_EXECUTABLE="/usr/bin/srun" -DMPIEXEC_NUMPROC_FLAG="-n" PATH_TO_SOURCE

------------------------------
NOAA RDHPCS Gaea (C5)
------------------------------

.. note::
   ``spack-stack-1.2.0``/``skylab-3.0.0`` is currently not supported on this platform and will be added in the near future.

The following is required for building new spack environments and for using spack to build and run software. Don't use ``module purge`` on Gaea!

.. code-block:: console

   module load PrgEnv-intel/8.3.3
   module load intel/2022.0.2
   module load cray-mpich/8.1.16
   module load python/3.9.12


.. _Platforms_Hera:

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

For ``spack-stack-1.2.0``/``skylab-3.0.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /scratch1/NCEPDEV/global/spack-stack/spack-stack-v1/envs/skylab-3.0.0-intel-2021.5.0/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.2.0``/``skylab-3.0.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /scratch1/NCEPDEV/global/spack-stack/spack-stack-v1/envs/skylab-3.0.0-gnu-9.2.0/install/modulefiles/Core
   module load stack-gcc/9.2.0
   module load stack-openmpi/3.1.4
   module load stack-python/3.9.12
   module available

Note that on Hera, a dedicated node exists for ``ecflow`` server jobs (``hecflow01``). Users starting ``ecflow_server`` on the regular login nodes will see their servers being killed every few minutes, and may be barred from accessing the system.

.. _Platforms_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

.. note::
   ``spack-stack-1.2.0``/``skylab-3.0.0`` is currently not supported on this platform and will be added in the near future.

**WORK IN PROGRESS**

------------------------------
TACC Frontera
------------------------------

.. note::
   ``spack-stack-1.2.0``/``skylab-3.0.0`` is currently not supported on this platform and will be added in the near future.

The following is required for building new spack environments and for using spack to build and run software.

.. code-block:: console

   module purge
   module use /work2/06146/tg854455/frontera/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.8.4

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

For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /data/prod/jedi/spack-stack/spack-stack-feature-mysql-testing/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.9.12
   module unuse /opt/apps/modulefiles/Compiler/intel/non-default/22
   module unuse /opt/apps/modulefiles/Compiler/intel/22
   module available

Note the two `module unuse` commands, that need to be run after the stack metamodules are loaded. Loading the Intel compiler meta module loads the Intel compiler module provided by the sysadmins, which adds those two directories to the module path. These contain duplicate libraries that are not compatible with our stack, such as ``hdf4``.


For ``spack-stack-1.3.0-rc1``/``unified-4.0.0-rc1`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /data/prod/jedi/spack-stack/spack-stack-feature-mysql-testing/envs/unified-4.0.0-rc1/install/modulefiles/Core
   module load stack-gcc/9.3.0
   module load stack-mpich/4.0.1
   module load stack-python/3.9.12
   module available

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

.. note::
   ``spack-stack-1.2.0``/``skylab-3.0.0`` is currently not supported on this platform and will be added in the near future.

**COMING SOON**

-----------------------------
Amazon Web Services Red hat 8
-----------------------------

For ``spack-stack-1.2.0``/``skylab-3.0.0``, use a c6i.2xlarge instance or similar with AMI "skylab-3.0.0-redhat8" (ami-0b7ee6595f9f79860), available on request in us-east-1. After logging in, run:

.. code-block:: console

   scl enable gcc-toolset-11 bash
   module use /home/ec2-user/spack-stack-v1/envs/skylab-3.0.0-gcc-11.2.1/install/modulefiles/Core
   module load stack-gcc/11.2.1
   module load stack-openmpi/4.1.4
   module load stack-python/3.9.13
   module available
