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
   module use module use /work/noaa/da/jedipara/spack-stack/modulefiles
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

qt (qt@5)
   The default ``qt@5`` in ``/usr`` is incomplete and thus insufficient for building ``ecflow``. After loading/unloading the modules as shown below, refer to 
   :numref:`Section %s <Prerequisites_Qt5>` to install ``qt@5.15.3`` in ``/scratch1/NCEPDEV/jcsda/jedipara/spack-stack/qt-5.15.3``.

.. code-block:: console

   module purge
   module use /scratch1/NCEPDEV/jcsda/jedipara/spack-stack/modulefiles
   module load miniconda/3.9.12
   # Need a newer gcc compiler than the default OS compiler gcc-4.8.5
   module load gnu/9.2.0

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

5. Create modulefiles - do not create the meta modules

.. code-block:: console

    spack module [lmod|tcl] refresh

6. Do *not* run the `spack stack setup-meta-modules` script. *** MAYBE ***

To use the chained spack environment, first load the usual modules from the upstream spack environment. Then add the full path to the newly created modules manually, for example:

.. code-block:: console

    module use /path/to/spack-stack-1.0.0/envs/jedi-ufs-chain-test/install/modulefiles/openmpi/4.1.3/apple-clang/13.1.6

Load the newly created modules 
and meta modules as usual. Note that the call to `spack stack setup-meta-modules` is only required to update the automatic ``tcl/tk`` environment modules.



Note. Spack find doesn't show the packages installed in upstream, unfortunately.

**DOM WORK IN PROGRESS**  Note that it is not necessary to create the meta modules. Simply add the directory to which the new modules a???A? HOW ABOUT TCL????

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

Python packages can be added in various ways:

1. Using ``python setup.py install --prefix=$MY_INSTALL_TREE ...`` or ``python3 -m pip install --no-deps --prefix=$MY_INSTALL_TREE ...``. The ``--no-deps`` options is very important, because ``pip`` may otherwise attempt to install dependencies that already exist in spack-stack. These dependencies are not only duplicates, they may also be different versions and/or compiled with different compilers/libraries (because they are wheels). This approach requires adding the appropriate subdirectories of ``$MY_INSTALL_TREE`` to the different search paths, as shown above.

2. Using Python virtual environments. Two important flags need to be passed to the command that creates the environment ``--system-site-packages`` and ``--without-pip``. After activating the environment, packages can be installed using `python3 -m pip` without having to specify ``--no-deps`` or ``--prefix``, and without having to manually modify ``PATH``, ``PYTHONPATH``, etc.

.. code-block:: console

   python3 -m venv --system-site-packages --without-pip $MY_INSTALL_TREE
   source $MY_INSTALL_TREE/bin/activate
   python3 -m pip install ...

.. note::
   Users are equally strongly advised to not use ``conda`` or ``miniconda`` in combination with Python modules provided by spack-stack, as well as not installing packages other than ``poetry`` in the basic ``miniconda`` installation for spack-stack (if using such a setup).
