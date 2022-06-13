.. _MaintainersSection:

******************************
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

.. _MaintainersSection_Discover:

------------------------------
NASA Discover
------------------------------

On Discover, ``miniconda`` and ``qt`` need to be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.3`` in ``/discover/swdev/jcsda/spack-stack/qt-5.15.3``.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7
   # Need a newer gcc compiler than the default OS compiler gcc-4.8.5
   module load comp/gcc/10.1.0

.. _MaintainersSection_Cheyenne:

------------------------------
NCAR-Wyoming Cheyenne
------------------------------

On Cheyenne, a workaround is needed to avoid the modules provided by CISL take precedence over the spack modules. The default module path for compilers is removed, the module path is set to a different location and that location is then loaded into the module environment. If new compilers or MPI libraries are
added to ``/glade/u/apps/ch/modulefiles/default/compilers`` by CISL, the spack-stack maintainers need to make the corresponding changes in ``/glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers``. See :numref:`Section %s <Platforms_Cheyenne>` for details.

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

On Gaea, ``qt`` needs to be installed as a one-off before spack can be used.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.3`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.3``.

.. code-block:: console

   module unload intel cray-mpich cray-python darshan
   module load cray-python/3.7.3.2

.. _MaintainersSection_Hera:

------------------------------
NOAA RDHPCS Hera
------------------------------

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

.. _MaintainersSection_Jet:

------------------------------
NOAA RDHPCS Jet
------------------------------

**WORK IN PROGRESS**

.. _MaintainersSection_Stampede2:

------------------------------
TACC Stampede2
------------------------------

Several packages need to be installed as a one-off before spack can be used.

Intel oneAPI compilers
   The latest version of the Intel compiler on Stampede2 is 19.1.1, and the default modulefile created by the system administrators ties it to `gcc-9.1.0`. The way the module file has been written is incompatible with spack. We therefore recommend installing the latest Intel oneAPI compiler suite (Intel oneAPI Base and HPC Toolkits). The following instructions install Intel oneAPI 2022.2 in ``/work2/06146/tg854455/stampede2/spack-stack``.

.. code-block:: console

   wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18679/l_HPCKit_p_2022.2.0.191.sh
   wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18673/l_BaseKit_p_2022.2.0.262.sh
   # Customize the installations to install in /work2/06146/tg854455/stampede2/spack-stack/intel-oneapi-2022.2
   sh l_BaseKit_p_2022.2.0.262.sh
   sh l_HPCKit_p_2022.2.0.191.sh

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

git-lfs
   The following instructions install ``git-lfs`` in ``/work2/06146/tg854455/stampede2/spack-stack/git-lfs-1.2.1``. Version 1.2.1 is the Centos7 default version.

.. code-block:: console

   module purge
   cd /work2/06146/tg854455/stampede2/spack-stack/
   mkdir -p git-lfs-1.2.1/src
   cd git-lfs-1.2.1/src
   wget --content-disposition https://packagecloud.io/github/git-lfs/packages/el/7/git-lfs-1.2.1-1.el7.x86_64.rpm/download.rpm
   rpm2cpio git-lfs-1.2.1-1.el7.x86_64.rpm | cpio -idmv
   mv usr/* ../

   Create modulefile ``/work2/06146/tg854455/stampede2/spack-stack/modulefiles/git-lfs/1.2.1`` from template ``doc/modulefile_templates/git-lfs`` and update ``GITLFS_PATH`` in this file.

.. _MaintainersSection_S4:

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

miniconda
   Follow the instructions in :numref:`Section %s <Prerequisites_Miniconda>` to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.3`` in ``/data/prod/jedi/spack-stack/qt-5.15.3``.

.. code-block:: console

   module purge
   module use /data/prod/jedi/spack-stack/modulefiles
   module load miniconda/3.9.7
   # Need a newer gcc compiler than the default OS compiler gcc-4.8.5
   export PATH=/data/prod/hpc-stack/gnu/9.3.0/bin:$PATH
   export LD_LIBRARY_PATH=/data/prod/hpc-stack/gnu/9.3.0/lib64:$LD_LIBRARY_PATH
   export CPATH=/data/prod/hpc-stack/gnu/9.3.0/include:$CPATH

.. _MaintainersSection_Testing_New_Packages:

==============================
Testing new packages
==============================

--------------------------------
Using spack to test/add packages
--------------------------------

The simplest case of adding new packages that are available in spack-stack is described in :numref:`Section %s <QuickstartExtendingEnvironments>`. As mentioned there, it is advised to take a backup of the spack environment (and install directories if outside the spack environment directory tree). It is also possible to chain spack installations, which means creating a test environment that uses installed packages and modulefiles from another (e.g. authoritative) spack environment and build the packages to be tested in isolation.

**WORK IN PROGRESS**

More details and a few words of caution can be found in the  `Spack documentation <https://spack.readthedocs.io/en/latest/chain.html?highlight=chaining%20spack%20installations>`_

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

Python packages can be added using ``python setup.py install --prefix=...`` or ``python3 -m pip install --no-deps --prefix=...``. The ``--no-deps`` options is very important, because ``pip`` may otherwise attempt to install dependencies that already exist in spack-stack. These dependencies are not only duplicates, they may also be different versions and/or compiled with different compilers/libraries (because they are wheels).

