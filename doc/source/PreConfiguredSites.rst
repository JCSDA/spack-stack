.. _Preconfigured_Sites:

Pre-configured sites
*************************

Directory ``configs/sites`` contains site configurations for several HPC systems, as well as minimal configurations for macOS and Linux. The macOS and Linux configurations are **not** meant to be used as is, as user setups and package versions vary considerably. Instructions for adding this information can be found in :numref:`Section %s <NewSiteConfigs>`.

Pre-configured sites are split into two categories: Tier 1 with officially support spack-stack installations (see :numref:`Section %s <Preconfigured_Sites_Tier1>`), and Tier 2 (sites with configuration files that were tested or contributed by others in the past, but that are not officially supported by the spack-stack team; see :numref:`Section %s <Preconfigured_Sites_Tier2>`).

.. _Preconfigured_Sites_Tier1:
=======================================================
Officially supported spack-stack installations (tier 1)
=======================================================

Ready-to-use spack-stack installations are available on the following, fully supported platforms. This version supports the JEDI Skylab release 4 of March 2023, and can be used for testing spack-stack with other applications (e.g. the UFS Weather Model, the UFS Short Range Weather Application, and the EMC Global Workflow). Amazon Web Services AMI are available on request in the US East 1 or 2 regions.

+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| System                                                     | Maintainers                   | Location                                                                                                     |
+============================================================+===============================+==============================================================================================================+
| MSU Orion Intel/GNU                                        | Cam Book / Dom Heinzeller     | ``/work/noaa/epic-ps/role-epic-ps/spack-stack/spack-stack-1.3.0/envs/unified-env``                           |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NASA Discover Intel/GNU                                    | Dom Heinzeller / ???          | ``/gpfsm/dswdev/jcsda/spack-stack/spack-stack-1.3.0/envs/unified-env``                                       |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NAVY HPCMP Narwhal Intel                                   | Dom Heinzeller / ???          | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.3.0/envs/unified-env-intel-2021.4.0``                    |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NAVY HPCMP Narwhal GNU                                     | Dom Heinzeller / ???          | ``/p/app/projects/NEPTUNE/spack-stack/spack-stack-1.3.0/envs/unified-env-gcc-10.3.0``                        |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Casper Intel                                  | Dom Heinzeller / ???          | ``/glade/work/epicufsrt/contrib/spack-stack/spack-stack-1.3.0-casper/envs/unified-env``                      |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne Intel/GNU                            | Cam Book / Dom Heinzeller     | ``/glade/work/epicufsrt/contrib/spack-stack/spack-stack-1.3.0/envs/unified-env``                             |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA Parallel Works (AWS, Azure, Gcloud) Intel/GNU?        | Mark Potts / Cam Book         | **will be supported soon**                                                                                   |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA Acorn Intel                                           | Hang Lei / ???                | **will be supported soon**                                                                                   |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea (C3/C4)                                   | Dom Heinzeller / ???          | ``/lustre/f2/dev/wpo/role.epic/contrib/spack-stack/spack-stack-1.3.0/envs/unified-env``                      |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera Intel/GNU                                 | Mark Potts / Dom Heinzeller   | ``/scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.3.0/envs/unified-env``                          |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet Intel/GNU                                  | Cam Book / Dom Heinzeller     | ``/mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.3.0/envs/unified-env``                          |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| UW (Univ. of Wisc.) S4 Intel/GNU                           | Dom Heinzeller / Mark Potts   | ``/data/prod/jedi/spack-stack-1.3.0/envs/unified-env``                                                       |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| Amazon Web Services Parallelcluster Ubuntu 20.04 Intel/GNU | Dom Heinzeller / ???          | ``/mnt/experiments-efs/skylab-v4/spack-stack-1.3.0/envs/unified-env``                                        |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+
| Amazon Web Services AMI Red Hat 8 GNU                      | Dom Heinzeller / ???          | ``/home/ec2-user/spack-stack/spack-stack-1.3.0/envs/unified-env``                                            |
+------------------------------------------------------------+-------------------------------+--------------------------------------------------------------------------------------------------------------+

For questions or problems, please consult the known issues in :numref:`Section %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/noaa-emc/spack-stack/issues>`_ and `discussions <https://github.com/noaa-emc/spack-stack/discussions>`_ first.

.. _Preconfigured_Sites_Orion:

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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/epic-ps/role-epic-ps/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.0.2
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.7
   module available

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /work/noaa/epic-ps/role-epic-ps/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/10.2.0
   module load stack-openmpi/4.0.4
   module load stack-python/3.9.7
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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.0.1
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.9.7
   module available

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /gpfsm/dswdev/jcsda/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.3
   module load stack-python/3.9.7
   module available

.. _Preconfigured_Sites_Narwhal:

------------------------------
NAVY HPCMP Narwhal
------------------------------

With Intel, the following is required for building new spack environments and for using spack to build and run software. Don't use ``module purge`` on Narwhal!

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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading the above modules.

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.3.0/envs/unified-env-intel-2021.4.0/install/modulefiles/Core
   module load stack-intel/2021.4.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.9.7

With GNU, the following is required for building new spack environments and for using spack to build and run software.  Don't use ``module purge`` on Narwhal!

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

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading the above modules.

.. code-block:: console

   module use /p/app/projects/NEPTUNE/spack-stack/spack-stack-1.3.0/envs/unified-env-gcc-10.3.0/install/modulefiles/Core
   module load stack-gcc/10.3.0
   module load stack-cray-mpich/8.1.14
   module load stack-python/3.9.7

.. _Preconfigured_Sites_Casper:

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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow.

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/spack-stack-1.3.0-casper/envs/unified-env/install/modulefiles/Core
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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow.

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/19.1.1.217
   module load stack-intel-mpi/2019.7.217
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /glade/work/epicufsrt/contrib/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/10.1.0
   module load stack-openmpi/4.1.1
   module load stack-python/3.9.12
   module available

.. _Preconfigured_Sites_Acorn:

-------------------------------
NOAA Acorn (WCOSS2 test system)
-------------------------------

.. note::
   ``spack-stack-1.3.0`` is not yet supported on this platform, but will be added on develop later.

On WCOSS2 OpenSUSE sets `CONFIG_SITE` which causes libraries to be installed in `lib64`, breaking the `lib` assumption made by some packages.

CONFIG_SITE should be set to empty in `compilers.yaml`. Don't use ``module purge`` on Acorn!

.. note::
   ``spack`` software installations are maintained by NCO on this platform.

.. _Preconfigured_Sites_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

.. note::
   ``spack-stack-1.3.0`` is not yet supported on this platform, but will be added on develop later.

The following is required for building new spack environments and for using spack to build and run software. The default module path needs to be removed, otherwise spack detect the system as Cray. It is also necessary to add ``git-lfs`` and some other utilities to the search path.

.. code-block:: console

   module unuse /opt/cray/craype/default/modulefiles
   module unuse /opt/cray/modulefiles
   export PATH="${PATH}:/contrib/spack-stack/apps/utils/bin"
   module use /contrib/spack-stack/modulefiles/core
   module load miniconda/3.9.7
   module load mysql/8.0.31

.. _Preconfigured_Sites_Gaea:

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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /lustre/f2/dev/wpo/role.epic/contrib/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.3.0
   module load stack-cray-mpich/7.7.11
   module load stack-python/3.9.12
   module available

.. warning::
   Is the following still true???

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
   module use /scratch1/NCEPDEV/jcsda/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load ecflow/5.5.3
   module load mysql/8.0.31

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/9.2.0
   module load stack-openmpi/3.1.4
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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.1
   module load stack-python/3.9.12
   module available

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /mnt/lfs4/HFIP/hfv3gfs/role.epic/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
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

For ``spack-stack-1.3.0`` with Intel, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /data/prod/jedi/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2021.5.0
   module load stack-intel-oneapi-mpi/2021.5.0
   module load stack-python/3.9.12
   module unuse /opt/apps/modulefiles/Compiler/intel/non-default/22
   module unuse /opt/apps/modulefiles/Compiler/intel/22
   module available

Note the two `module unuse` commands, that need to be run after the stack metamodules are loaded. Loading the Intel compiler meta module loads the Intel compiler module provided by the sysadmins, which adds those two directories to the module path. These contain duplicate libraries that are not compatible with our stack, such as ``hdf4``.

For ``spack-stack-1.3.0`` with GNU, load the following modules after loading miniconda and ecflow:

.. code-block:: console

   module use /data/prod/jedi/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core

   module load stack-gcc/9.3.0
   module load stack-mpich/4.0.1
   module load stack-python/3.9.12
   module available

------------------------------------------------
Amazon Web Services Parallelcluster Ubuntu 20.04
------------------------------------------------

Access to the JCSDA-managed AWS Parallel Cluster is not available to the public. The following instructions are for JCSDA core staff and in-kind contributors.

For ``spack-stack-1.3.0`` with Intel, run the following commands/load the following modules:

.. code-block:: console

   module purge
   ulimit -s unlimited
   source /opt/intel/oneapi/compiler/2022.1.0/env/vars.sh
   module use /mnt/experiments-efs/skylab-v4/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-intel/2022.1.0
   module load stack-intel-oneapi-mpi/2021.6.0
   module load stack-python/3.10.8
   module available

For ``spack-stack-1.3.0`` with Intel, run the following commands/load the following modules:

   module purge
   ulimit -s unlimited
   module use /mnt/experiments-efs/skylab-v4/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/9.4.0
   module load stack-openmpi/4.1.4
   module load stack-python/3.10.8
   module available

-----------------------------
Amazon Web Services Red Hat 8
-----------------------------

For ``spack-stack-1.3.0`` use a c6i.4xlarge instance or similar with AMI "skylab-4.0.0-redhat8" (ami-098a3fdd801055c14 in region us-east-1, ami-039759644cac741eb in region us-east-2). After logging in, run:

.. code-block:: console

   ulimit -s unlimited
   scl enable gcc-toolset-11 bash
   module use /home/ec2-user/spack-stack/spack-stack-1.3.0/envs/unified-env/install/modulefiles/Core
   module load stack-gcc/11.2.1
   module load stack-openmpi/4.1.4
   module load stack-python/3.10.8
   module available

.. _Preconfigured_Sites_Tier2:
=============================
Pre-configured sites (tier 2)
=============================

Tier 2 sites are sites with configuration files that were tested or contributed by others in the past, but that are not officially supported by the spack-stack team. The configuration files for these sites may not be up to date or functional.

------------------------------
NOAA RDHPCS Gaea (C5)
------------------------------

.. note::
   ``spack-stack-1.3.0`` is currently not supported on this platform and may be added in the near future.

The following is required for building new spack environments and for using spack to build and run software. Don't use ``module purge`` on Gaea!

.. code-block:: console

   module load PrgEnv-intel/8.3.3
   module load intel/2022.0.2
   module load cray-mpich/8.1.16
   module load python/3.9.12

------------------------------
TACC Frontera
------------------------------

.. note::
   ``spack-stack-1.3.0`` is currently not supported on this platform and may be added in the near future.

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

   git clone --recursive https://github.com/NOAA-EMC/spack-stack.git
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
   spack env activate [-p] envs/unified-dev.hera

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

   # Process/concretize the specs
   spack concretize

   # Optional step for systems with a pre-configured spack mirror, see below.

   # Install the environment, recommended to always use --source
   # to install the source code with the compiled binary package
   spack install --source [--verbose] [--fail-fast]

   # Create lua module files
   spack module lmod refresh

   # Create meta-modules for compiler, mpi, python
   spack stack setup-meta-modules

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