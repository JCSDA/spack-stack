.. _MaintainersSection:

*************************
Maintainers Section
*************************

==============================
Pre-configuring sites
==============================

------------------------------
NASA Discover
------------------------------

On Discover, ``miniconda`` and ``qt`` need to be installed as a one-off before spack can be used.

miniconda
   Follow the instructions in section **MISSING** to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. Because installing ``qt`` is complex and has a lot of OS (``X11``) dependencies, we install it outside of spack with the default OS compiler and then point to it in Gaea's ``packages.yaml``. The following instructions install ``qt@5.15.3`` in ``/gpfsm/dswdev/jcsda/spack-stack//qt-5.15.3``.

.. code-block:: console

   module purge
   module use /discover/swdev/jcsda/spack-stack/modulefiles
   module load miniconda/3.9.7
   module load comp/gcc/10.1.0

   cd /gpfsm/dswdev/jcsda/spack-stack/
   mkdir -p qt-5.15.3/src
   cd qt-5.15.3/src
   git clone git://code.qt.io/qt/qt5.git
   cd qt5/
   git fetch --tags
   git checkout v5.15.3-lts-lgpl
   perl init-repository
   git submodule update --init --recursive
   cd ..
   mkdir qt5-build
   cd qt5-build/
   ../qt5/configure -opensource -nomake examples -nomake tests -prefix /discover/swdev/jcsda/spack-stack/qt-5.15.3 -skip qtdocgallery -skip qtwebengine 2>&1 | tee log.configure
   gmake -j4 2>&1 | tee log.gmake
   gmake install 2>&1 | tee log.install

------------------------------
NOAA RDHPCS Gaea
------------------------------

On Gaea, ``qt`` needs to be installed as a one-off before spack can be used.

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. Because installing ``qt`` is complex and has a lot of OS (``X11``) dependencies, we install it outside of spack with the default OS compiler and then point to it in Gaea's ``packages.yaml``. The following instructions install ``qt@5.15.3`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.3``.

.. code-block:: console

   module unload intel cray-mpich cray-python darshan
   module load cray-python/3.7.3.2
   cd /lustre/f2/pdata/esrl/gsd/spack-stack
   mkdir -p qt-5.15.3/src
   cd qt-5.15.3/src
   git clone git://code.qt.io/qt/qt5.git
   cd qt5
   git fetch --tags
   git checkout v5.15.3-lts-lgpl
   perl init-repository
   git submodule update --init --recursive
   cd ..
   mkdir qt5-build
   cd qt5-build
   ../qt5/configure -opensource -nomake examples -nomake tests -prefix /lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.3 -skip qtdocgallery -skip qtwebengine 2>&1 | tee log.configure
   gmake -j4 2>&1 | tee log.gmake
   gmake install 2>&1 | tee log.install

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
   Follow the instructions in section **MISSING** to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

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

------------------------------
UW (Univ. of Wisconsin) S4
------------------------------

miniconda
   Follow the instructions in section **MISSING** to create a basic ``miniconda`` installation and associated modulefile for working with spack. Don't forget to log off and back on to forget about the conda environment.

==============================
Testing new packages
==============================

 (chaining spack installations)
 
 https://spack.readthedocs.io/en/latest/chain.html?highlight=chaining%20spack%20installations
 
 