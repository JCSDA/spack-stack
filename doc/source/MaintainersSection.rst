.. _MaintainersSection:

Maintainers/Developers Section
******************************

==============================
Manual software installations
==============================

The following manual software installations may or may not be required as prerequisites, depending on the specific platform. For configurable/user systems, please consult :numref:`Section %s <Preconfigured_Sites>`, for preconfigured systems please consult :numref:`Section %s <NewSiteConfigs>`. Note that for preconfigured systems, the following one-off installations are only necessary for the maintainers of the preconfigured installations, users **do not** have to repeat any of these steps.

..  _MaintainersSection_Git_LFS:

------------------------------
git-lfs
------------------------------

Building ``git-lfs`` with spack isn't straightforward as it requires ``go-bootstrap`` and ``go`` language support, which many compilers don't build correctly. We therefore require ``git-lfs`` as an external package. On many of the HPC systems, it is already available as a separate module or as part of a ``git`` module. On macOS and Linux, it can be installed using ``brew`` or other package managers (see :numref:`Sections %s <NewSiteConfigs_macOS>` and :numref:`%s <NewSiteConfigs_Linux>` for examples). :numref:`Section %s <MaintainersSection_Frontera>` describes a manual installation of ``git-lfs`` on TACC Frontera, a Centos7.9 system.

..  _MaintainersSection_Miniconda:

------------------------------
Miniconda (legacy)
------------------------------

miniconda can be used to provide a basic version of Python that spack-stack uses to support its Python packages. This is not recommended on configurable systems (user workstations and laptops using GNU compiler) where Python gets installed by spack. But any system using Intel compilers with spack-stack will need an external Python to build ecflow with Python bindings (because ecflow requires a boost serialization function that does **not** work with Intel, a known yet ignored bug), and then both Python and ecflow are presented to spack as external packages. Often, it is possible to use the default (OS) Python if new enough (3.9+), or a module provided by the system administrators. If none of this works, use the following instructions to install a basic Python interpreter using miniconda:

The following is for the example of ``miniconda_ver="py39_4.12.0"`` (for which ``python_ver=3.9.12``) and ``platform="MacOSX-x86_64"`` or ``platform="Linux-x86_64"``

.. code-block:: console

   cd /path/to/top-level/spack-stack/
   mkdir -p miniconda-${python_ver}/src
   cd miniconda-${python_ver}/src
   wget https://repo.anaconda.com/miniconda/Miniconda3-${miniconda_ver}-${platform}.sh
   sh Miniconda3-${miniconda_ver}-${platform}.sh -u -b -p /path/to/top-level/spack-stack/miniconda-${python_ver}
   eval "$(/path/to/top-level/spack-stack/miniconda-${python_ver}/bin/conda shell.bash hook)"
   conda install -y -c conda-forge libpython-static

After the successful installation, create modulefile ``/path/to/top-level/spack-stack/modulefiles/miniconda/${python_ver}`` from template ``doc/modulefile_templates/miniconda`` and update ``MINICONDA_PATH`` and the Python version in this file.

..  _MaintainersSection_Qt5:

------------------------------
qt (qt@5)
------------------------------

Building ``qt`` with spack isn't straightforward as it requires many libraries related to the graphical desktop that are often tied to the operating system, and which many compilers don't build correctly. We therefore require ``qt`` as an external package. On many of the HPC systems, it is already available as a separate module or provided by the operating system. On macOS and Linux, it can be installed using ``brew`` or other package managers (see :numref:`Sections %s <NewSiteConfigs_macOS>` and :numref:`%s <NewSiteConfigs_Linux>` for examples). 

On HPC systems without a sufficient Qt5 installation, we install it outside of spack with the default OS compiler and then point to it in the site's ``packages.yaml``. The following instructions install ``qt@5.15.2`` in ``/discover/swdev/jcsda/spack-stack/qt-5.15.2/5.15.2/gcc_64``.

.. code-block:: console

   mkdir -p /discover/swdev/jcsda/spack-stack/qt-5.15.2/src
   cd /discover/swdev/jcsda/spack-stack/qt-5.15.2/src
   wget --no-check-certificate http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run
   chmod u+x qt-unified-linux-x64-online.run
   ./qt-unified-linux-x64-online.run

Sign into qt, select customized installation, choose qt@5.15.2 only (uncheck all other boxes) and set install prefix to ``/discover/swdev/jcsda/spack-stack/qt-5.15.2``. After the successful installation, create modulefile ``/discover/swdev/jcsda/spack-stack/modulefiles/qt/5.15.2`` from template ``doc/modulefile_templates/qt`` and update ``QT_PATH`` in this file.

.. note::
   The dependency on ``qt`` is introduced by ``ecflow``, which at present requires using ``qt@5`` - earlier or newer versions will not work.

.. note::
   On air-gapped systems, the above method may not work (we have not encountered such a system so far).

.. note::
   If ``./qt-unified-linux-x64-online.run`` fails to start with the error ``qt.qpa.xcb: could not connect to display`` and a role account is being used, follow the procedure described in https://www.thegeekdiary.com/how-to-set-x11-forwarding-export-remote-display-for-users-who-switch-accounts-using-sudo to export the display. A possible warning ``xauth:  file /ncrc/home1/role.epic/.Xauthority does not exist`` can be ignored, since this file gets created by the ``xauth`` command.

..  _MaintainersSection_ecFlow:

------------------------------
ecFlow (with GUI and Python)
------------------------------

Building ``ecFlow`` with spack is pretty tricky, because it requires functions from the ``boost`` serialization library that do not build cleanly with the Intel classic compilers (see https://github.com/USCiLab/cereal/issues/606 for a description of the problem of Intel with json cereal). When using the Intel compilers on HPC systems, it is therefore necessary to build ``ecFlow`` with the GNU compilers, preferably the same version that is used as the C++ backend for Intel, outside of spack-stack and make it available as a module. The build of ``ecFlow`` described below links against this ``boost`` library statically, therefore it does not interfere with ``boost`` built by spack-stack for other applications. ``ecFlow`` also uses ``Python3`` and ``qt5``.

.. note::
   Installing ``ecFlow`` with ``conda``, ``brew``, etc. is not recommended, since these install a number of packages as dependencies (e.g. ``numpy``, dynamically-linked ``boost``) that may interfere with the spack software stack.

After loading the required modules for this system (typically the same ``gcc`` used as backend for Intel or for GNU spack-stack builds, ``cmake``, ``qt5``, ``Python3``), follow these instructions to install ecFlow with the graphical user interface (GUI) and Python3 API. See also https://confluence.ecmwf.int/display/ECFLOW/ecflow5.

The following instructions are for Discover (see :numref:`Section %s <MaintainersSection_Discover>` for the required modules).

.. code-block:: console

   mkdir -p /lustre/f2/pdata/esrl/gsd/spack-stack/ecflow-5.8.4/src
   cd /lustre/f2/pdata/esrl/gsd/spack-stack/ecflow-5.8.4/src
   wget https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-5.8.4-Source.tar.gz?api=v2
   wget https://boostorg.jfrog.io/artifactory/main/release/1.78.0/source/boost_1_78_0.tar.gz
   mv ecFlow-5.8.4-Source.tar.gz\?api\=v2 ecFlow-5.8.4-Source.tar.gz
   tar -xvzf boost_1_78_0.tar.gz
   tar -xvzf ecFlow-5.8.4-Source.tar.gz
   export WK=/lustre/f2/pdata/esrl/gsd/spack-stack/ecflow-5.8.4/src/ecFlow-5.8.4-Source
   export BOOST_ROOT=/lustre/f2/pdata/esrl/gsd/spack-stack/ecflow-5.8.4/src/boost_1_78_0

   # Build static boost (to not interfere with spack-stack boost)
   cd $BOOST_ROOT
   ./bootstrap.sh 2>&1 | tee bootstrap.log
   $WK/build_scripts/boost_build.sh 2>&1 | tee boost_build.log

   # Build ecFlow
   cd $WK
   mkdir build
   cd build
   cmake .. -DCMAKE_INSTALL_PREFIX=/lustre/f2/pdata/esrl/gsd/spack-stack/ecflow-5.8.4 2>&1 | tee log.cmake
   make -j4 2>&1 | tee log.make
   make install 2>&1 | tee log.install

Create modulefile ``/lustre/f2/pdata/esrl/gsd/spack-stack/modulefiles/ecflow/5.8.4`` from template ``doc/modulefile_templates/ecflow`` and update ``ECFLOW_PATH`` in this file.

.. note::
   For Cray systems, for example NRL's Narwhal, NOAA's Gaea C4/C5, or NCAR's Derecho, the following modifications are necessary: After extracting the ecflow tarball, edit ``ecFlow-5.8.4-Source/build_scripts/boost_build.sh`` and remove the following lines:

.. code-block:: console

   if [ "$PE_ENV" = INTEL ] ; then
      tool=intel
   fi
   if [ "$PE_ENV" = CRAY ] ; then
      tool=cray
   fi

.. note::
   Further on Narwhal, the ``cmake`` command for ``ecbuild`` must be told to use the GNU compilers:

.. code-block:: console

   CC=gcc CXX=g++ FC=gfortran cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/ecflow/installation 2>&1 | tee log.cmake

.. note::
   Further, on Gaea C5, one needs to pass the correct ``python3`` executable to the ``cmake`` command:

.. code-block:: console

   cmake .. -DPython3_EXECUTABLE=`which python3` -DCMAKE_INSTALL_PREFIX=/path/to/ecflow/installation 2>&1 | tee log.cmake

.. note::
   Finally, on Derecho (or any other system with ``gcc@12.2.0``), one needs to patch file ``ecflow-5.8.4/src/ecFlow-5.8.4-Source/ACore/src/Passwd.cpp`` by adding ``#include <ctime>`` below line ``#include "Passwd.hpp"`` before running ``make``.

..  _MaintainersSection_MySQL:

------------------------------
MySQL (server and client)
------------------------------

We do not build ``mysql`` with spack, since it depends on specific versions of the ``boost`` library and C++ standards that make our large environments very complicated and often don't build on older systems. Instead, we identify the default ``glibc`` of the system, obtain the binary tarball from the `MySQL Community Downloads <https://dev.mysql.com/downloads/mysql/>`_  page and make it available to spack as an external package. The following instructions are for Orion:

1. Check the glibc version by executing ``ldd --version``

.. code-block:: console

   ldd (GNU libc) 2.17

2. Download and unpack the correct tarball, in this case option "Linux - Generic (glibc 2.17) (x86, 64-bit), Compressed TAR Archive Minimal Install 8.0.31"

.. code-block:: console

   cd /work/noaa/da/role-da/spack-stack/
   mkdir -p mysql-8.0.31/src
   cd mysql-8.0.31/src
   wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz
   tar -xvf mysql-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz
   # This moves the content of directory "mysql-8.0.31-linux-glibc2.17-x86_64-minimal" one level up, next to the "src" directory
   mv mysql-8.0.31-linux-glibc2.17-x86_64-minimal/* ..
   rmdir mysql-8.0.31-linux-glibc2.17-x86_64-minimal

3. Create modulefile ``/work/noaa/da/role-da/spack-stack/modulefiles/mysql/8.0.31`` from template ``doc/modulefile_templates/mysql`` and update ``MYSQL_PATH`` in this file.

..  _MaintainersSection_Texlive:

------------------------------
Texlive (TeX/LaTeX)
------------------------------

Building ``texlive`` isn't straightforward as it has many dependencies. Since it is only used to generated documentation for ``spack-stack`` (and other projects), i.e. not to compile any code, it makes no sense to build it with ``spack``. We therefore require ``texlive`` or any other compatible TeX/LaTeX distribution as an external package.

On many of the HPC systems, it is already available as a separate module or as part of the default operating system. On macOS, the MacTeX distribution provides a full and easy-to-install TeX/LaTeX environment (see :numref:`Section %s <NewSiteConfigs_macOS>`). On Linux, ``texlive`` can be installed using the default package manager (see :numref:`Section %s <NewSiteConfigs_Linux>`).


.. _Preconfigured_Sites_SpackMirror:

=========================================================
Optional step for sites with a preconfigured spack mirror
=========================================================

To check if a mirror is configured, look for ``local-source`` in the output of

.. code-block:: bash

   spack mirror list

If a mirror exists, add new packages to the mirror. Here, ``/path/to/mirror`` is the location from the above list command without the leading ``file://``

.. code-block:: bash

   spack mirror create -a -d /path/to/mirror

If this fails with ``git lfs`` errors, check the site config for which module to load for ``git lfs`` support. Load the module, then run the ``spack mirror add`` command, then unload the module and proceed with the installation.

==============================
Pre-configuring sites
==============================

.. _MaintainersSection_Preface:

------------------------------
Preface/general instructions
------------------------------

Preconfigured sites are defined through spack configuration files in the spack-stack directory ``configs/sites``, for example ``configs/sites/orion``. All files in the site-specific subdirectory will be copied into the environment into ``envs/env-name/site``. Site-specific configurations consist of general definitions (``config.yaml``), packages (``packages.yaml``), compilers (``compilers.yaml``), modules (``modules.yaml``), mirrors (``mirrors.yaml``) etc. These configurations overwrite the common configurations that are copied from ``configs/common`` into ``envs/env-name/common``.

The instructions below are platform-specific tasks that only need to be done once and can be reused for new spack environments. To build new environments on preconfigured platforms, follow the instructions in :numref:`Section %s <Preconfigured_Sites_ExtendingEnvironments>`.

Note that, for official installations of new environments on any supported platform, the ``spack install`` command should be invoked with the ``--source`` and ``--verbose`` arguments, i.e.:

.. code-block:: console
    
   spack install --source --verbose

.. _MaintainersSection_Orion:

------------------------------
MSU Orion
------------------------------

On Orion, it is necessary to change the default ``umask`` from ``0027`` to ``0022`` so that users not in the group of the role account can still see and use the software stack. This can be done by running ``umask 022`` after logging into the role account.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`. Note that the default/system ``qt@5`` can be used on Orion.

.. code-block:: console

   module purge
   module use /work/noaa/da/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.7
   module load cmake/3.22.1
   module load gcc/10.2.0

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/work/noaa/da/role-da/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_Hercules:

------------------------------
MSU Hercules
------------------------------

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library, using an available ``Qt5`` installation. After loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>` to install ``ecflow`` in ``/work/noaa/epic/role-epic/spack-stack/hercules/ecflow-5.8.4``. NOTE: do NOT include the ``Qt5`` module dependency in the ``ecflow`` modulefile, as it is only needed at build time (and causes issues with zlib/tar if the depedency is kept in the modulefile). 

.. code-block:: console

   module purge
   module load qt/5.15.8

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/work/noaa/epic-ps/role-epic-ps/spack-stack/mysql-8.0.31-hercules``.

openmpi
  need to load qt so to get consistent zlib (or just load zlib directly, check qt module)

.. code-block:: console

   module purge
   module load zlib/1.2.13
   module load ucx/1.13.1
   ./configure \
       --prefix=/work/noaa/epic/role-epic/spack-stack/hercules/openmpi-4.1.5/gcc-11.3.1  \
       --with-ucx=$UCX_ROOT \
       --with-zlib=$ZLIB_ROOT
   make VERBOSE=1 -j4
   make check
   make install

.. _MaintainersSection_Discover:

------------------------------
NASA Discover
------------------------------

On Discover, ``miniconda``, ``qt``, ``ecflow``, and ``mysql`` need to be installed as a one-off before spack can be used. When using the GNU compiler, it is also necessary to build your own ``openmpi`` or other MPI library, which requires adapting the installation to the network hardware and ``slurm`` scheduler.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <MaintainersSection_Qt5>` to install ``qt@5.15.2`` in ``/discover/swdev/jcsda/spack-stack/qt-5.15.2``.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`.

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
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/discover/swdev/jcsda/spack-stack/mysql-8.0.31``. Note that the ``glibc`` version on Discover is 2.22, which works with the latest available ``glibc`` version for the ``mysql`` server ``2.17``.

.. _MaintainersSection_Narwhal:

------------------------------
NAVY HPCMP Narwhal
------------------------------

On Narwhal, ``git-lfs``, ``qt``, ``ecflow``, and ``mysql`` need to be installed as a one-off before spack can be used.

git-lfs
   The following instructions install ``git-lfs`` in ``/p/app/projects/NEPTUNE/spack-stack/git-lfs-2.10.0``. Version 2.10.0 is the default version for Narwhal. First, download the ``git-lfs`` RPM on a system with full internet access (e.g., Cheyenne) using ``wget https://download.opensuse.org/repositories/openSUSE:/Leap:/15.2/standard/x86_64/git-lfs-2.10.0-lp152.1.2.x86_64.rpm`` and copy this file to ``/p/app/projects/NEPTUNE/spack-stack/git-lfs-2.10.0/src``. Then switch to Narwhal and run the following commands. 

   .. code-block:: console

      cd /p/app/projects/NEPTUNE/spack-stack/git-lfs-2.10.0/src
      rpm2cpio git-lfs-2.10.0-lp152.1.2.x86_64.rpm | cpio -idmv
      mv usr/* ../

   Create modulefile ``/p/app/projects/NEPTUNE/spack-stack/modulefiles/git-lfs/2.10.0`` from template ``doc/modulefile_templates/git-lfs`` and update ``GITLFS_PATH`` in this file.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <MaintainersSection_Qt5>` to install ``qt@5.15.2`` in ``/p/app/projects/NEPTUNE/spack-stack/qt-5.15.2``.

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
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>` to install ``ecflow`` in ``/p/app/projects/NEPTUNE/spack-stack/ecflow-5.8.4``. Ensure to follow the extra instructions in that section for Narwhal.

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
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/p/app/projects/NEPTUNE/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_Nautilus:

------------------------------
NAVY HPCMP Nautilus
------------------------------

On Nautilus, ``mysql`` and ``ecflow`` need to be installed as a one-off before spack can be used.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>` to install ``ecflow`` in ``/p/app/projects/NEPTUNE/spack-stack/ecflow-5.8.4``.

.. code-block:: console

   module purge

   module load slurm
   module load amd/aocc/4.0.0
   module load amd/aocl/aocc/4.0

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/p/app/projects/NEPTUNE/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_Casper:

------------------------------
NCAR-Wyoming Casper
------------------------------

Casper is co-located with Cheyenne and shares the parallel filesystem ``/glade`` and more with it. It is, however, a different operating system with a somewhat different software stack. spack-stack was installed on Casper after it was installed on Cheyenne, and prerequisites from Cheyenne were reused where possible (``miniconda``, ``qt``, ``ecflow``, ``mysql``). See below for information on how to install these packages.

.. _MaintainersSection_Cheyenne:

------------------------------
NCAR-Wyoming Cheyenne
------------------------------

On Cheyenne, there are problems with newer versions of the Intel compiler/MPI library when trying to run MPI jobs with just one task (``mpiexec -np 1``) - for JEDI, job hangs forever in a particular MPI communication call in oops. This is why an older version Intel 19 is used here and on Casper.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Because of the workaround for the compilers, the ``miniconda`` module should be placed in ``/glade/work/jedipara/cheyenne/spack-stack/misc``. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to :numref:`Section %s <MaintainersSection_Qt5>` to install ``qt@5.15.2`` in ``/glade/work/jedipara/cheyenne/spack-stack/qt-5.15.2``. Because of the workaround for the compilers, the ``qt`` module should be placed in ``/glade/work/jedipara/cheyenne/spack-stack/misc``.

.. code-block:: console

   module purge
   export LMOD_TMOD_FIND_FIRST=yes
   module load gnu/10.1.0

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`. Because of the workaround for the compilers, the ``qt`` module should be placed in ``/glade/work/jedipara/cheyenne/spack-stack/misc``. Also, because of the dependency on ``miniconda``, that module must be loaded automatically in the ``ecflow`` module (similar to ``qt@5.15.2``).

.. code-block:: console

   module purge
   export LMOD_TMOD_FIND_FIRST=yes
   module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
   module load gnu/10.1.0
   module load miniconda/3.9.12
   module load qt/5.15.2
   module load cmake/3.18.2

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/glade/work/jedipara/cheyenne/spack-stack/mysql-8.0.31``.

openmpi

.. code-block:: console

    module purge
    export LMOD_TMOD_FIND_FIRST=yes
    module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/misc
    module load gnu/10.1.0

   ./configure \
       --prefix=/glade/work/epicufsrt/contrib/spack-stack/openmpi-4.1.5 \
       --without-verbs \
       --with-ucx=/glade/u/apps/ch/opt//ucx/1.12.1 \
       --disable-wrapper-runpath \
       --with-tm=/opt/pbs \
       --enable-mca-no-build=btl-uct \
       2>&1 | tee log.config
   make VERBOSE=1 -j2
   make check
   make install

.. _MaintainersSection_Derecho:

------------------------------
NCAR-Wyoming Derecho
------------------------------

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>` to install ``ecflow`` in ``/lustre/desc1/scratch/epicufsrt/contrib/ecflow-5.8.4``. Be sure to follow the extra instructions for Derecho in that section.

.. code-block:: console

   module purge
   export LMOD_TMOD_FIND_FIRST=yes
   module load gcc/12.2.0
   module load cmake/3.26.3

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/lustre/desc1/scratch/epicufsrt/contrib/mysql-8.0.33``.

.. _MaintainersSection_WCOSS2:

------------------------------
NOAA NCO WCOSS2
------------------------------

**WORK IN PROGRESS**

.. _MaintainersSection_Parallel_Works:

----------------------------------------
NOAA Parallel Works (AWS, Azure, Gcloud)
----------------------------------------

See ``configs/sites/noaa-aws/README.md``. These instructions are identical for all three vendors.

.. _MaintainersSection_Gaea:

------------------------------
NOAA RDHPCS Gaea C4
------------------------------

On Gaea, ``miniconda``, ``qt``, ``ecflow``, and ``mysql`` need to be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment. Use the following workaround to avoid the terminal being spammed by error messages about missing version information (``/bin/bash: /lustre/f2/pdata/esrl/gsd/spack-stack/miniconda-3.9.12/lib/libtinfo.so.6: no version information available (required by /lib64/libreadline.so.7)``):

.. code-block:: console

   cd /lustre/f2/pdata/esrl/gsd/spack-stack/miniconda-3.9.12/lib
   mv libtinfow.so.6.3 libtinfow.so.6.3.conda.original
   ln -sf /lib64/libtinfo.so.6 libtinfow.so.6.3

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <MaintainersSection_Qt5>` to install ``qt@5.15.2`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.2``.

.. code-block:: console

   module unload intel cray-mpich cray-python darshan PrgEnv-intel
   module load gcc/10.3.0
   module load PrgEnv-gnu/6.0.5

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, `qt5`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`. Because of the dependency on ``miniconda``, that module must be loaded automatically in the ``ecflow`` module (similar to ``qt@5.15.2``).  Ensure to follow the extra instructions in that section for Gaea.

   module unload intel cray-mpich cray-python darshan PrgEnv-intel
   module load gcc/10.3.0
   module load PrgEnv-gnu/6.0.5
   module load cmake/3.20.1
   module use /lustre/f2/pdata/esrl/gsd/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load qt/5.15.2

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/mysql-8.0.31``.

.. _MaintainersSection_GaeaC5:

------------------------------
NOAA RDHPCS Gaea C5
------------------------------

On Gaea C5, ``miniconda``, ``qt``, ``ecflow``, and ``mysql`` need to be installed as a one-off before spack can be used.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to :numref:`Section %s <MaintainersSection_Qt5>` to install ``qt@5.15.2`` in ``/lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/qt-5.15.2``. :numref:`Section %s <MaintainersSection_Qt5>` describes how to export the X windows environment in order to install ``qt@5`` using the role account.

.. code-block:: console

   module unload intel-classic cray-mpich PrgEnv-intel
   module load gcc/10.3.0
   module load PrgEnv-gnu/8.3.3

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `qt5` and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`. Because of the dependency on ``miniconda``, that module must be loaded automatically in the ``ecflow`` module (similar to ``qt@5.15.2-c5``).  Ensure to follow the extra instructions in that section for Gaea C5 in ``/lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/ecflow-5.8.4``.
  
   Ensure to follow the extra instructions in that section for Gaea.

.. code-block:: console

   module unload intel-classic cray-mpich PrgEnv-intel
   module load gcc/10.3.0
   module load PrgEnv-gnu/8.3.3
   module load python/3.9.12

   module use /lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/modulefiles
   module load qt/5.15.2

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/lustre/f2/dev/wpo/role.epic/contrib/spack-stack/c5/mysql-8.0.31``.

.. _MaintainersSection_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

On Hera, ``miniconda`` and ``mysql`` must be installed as a one-off before spack can be used. When using the GNU compiler, it is also necessary to build your own ``openmpi`` or other MPI library.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/scratch1/NCEPDEV/global/spack-stack/apps/mysql-8.0.31``. Since Hera cannot access the MySQL community URL, the tarball needs to be downloaded on a different machine and then copied over.

openmpi
   It is easier to build and test ``openmpi`` manually and use it as an external package, instead of building it as part of spack-stack. These instructions were used to build the ``openmpi@4.1.5`` MPI library with ``gcc@9.2.0`` as referenced in the Hera site config. After the installation, create modulefile `openmpi/4.1.5` using the template ``doc/modulefile_templates/openmpi``. Note the site-specific module settings at the end of the template, this will likely be different for other HPCs.

.. code-block:: console

   module purge
   module load gnu/9.2.0
   ./configure \
       --prefix=/scratch1/NCEPDEV/jcsda/jedipara/spack-stack/openmpi-4.1.5 \
       --with-pmi=/apps/slurm/default \
       --with-lustre
   make VERBOSE=1 -j4
   make check
   make install

Hera sits behind the NOAA firewall and doesn't have access to all packages on the web. It is therefore necessary to create a spack mirror on another platform (e.g. Cheyenne). This can be done as described in section :numref:`Section %s <MaintainersSection_spack_mirrors>` for air-gapped systems.

.. _MaintainersSection_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

Note that the ``target`` architecture for Jet must be set to ``core2`` to satisfy differences between the various Jet partitions and ensure that installations run on the front-end nodes (xjet-like) will function on the other partitions.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

.. code-block:: console

   module use /lfs4/HFIP/hfv3gfs/spack-stack/modulefiles
   module load miniconda/3.9.12
   # Need a newer gcc compiler than the default OS compiler gcc-4.8.5
   module load gnu/9.2.0
   
mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/lfs4/HFIP/hfv3gfs/role.epic/apps/mysql-8.0.31``. Since Jet cannot access the MySQL community URL, the tarball needs to be downloaded on a different machine and then copied over.


.. _MaintainersSection_Frontera:

------------------------------
TACC Frontera
------------------------------

Several packages need to be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation in ``/work2/06146/USERNAME/frontera/spack-stack/miniconda-3.9.12`` and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`.

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
   Follow the instructions in :numref:`Section %s <MaintainersSection_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

ecflow
  ``ecFlow`` must be built manually using the GNU compilers and linked against a static ``boost`` library. After installing `miniconda`, and loading the following modules, follow the instructions in :numref:`Section %s <MaintainersSection_ecFlow>`.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.12
   module load gcc/9.3.0

mysql
  ``mysql`` must be installed separately from ``spack`` using a binary tarball provided by the MySQL community. Follow the instructions in :numref:`Section %s <MaintainersSection_MySQL>` to install ``mysql`` in ``/data/prod/jedi/spack-stack/mysql-8.0.31``.

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
   cd envs/air_gapped_mirror_env/
   spack env activate .
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

Chaining spack-stack installations is a powerful way to test adding new packages without affecting the existing packages. The idea is to define one or more upstream spack installations that the environment can use as dependencies. This is described in detail in :numref:`Section %s <Add_Test_Packages>`.

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
