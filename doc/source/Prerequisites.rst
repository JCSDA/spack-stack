..  _Prerequisites:

Prerequisites
*******************************

==============================
Manual software installations
==============================

The following manual software installations may or may not be required as prerequisites, depending on the specific platform. For configurable/user systems, please consult :numref:`Section %s <Platforms_Preconfigured_Sites>`, for preconfigured systems please consult :numref:`Section %s <Platform_New_Site_Configs>`. Note that for preconfigured systems, the following one-off installations are only necessary for the maintainers of the preconfigured installations, users **do not** have to repeat any of these steps.

..  _Prerequisites_Git_LFS:

------------------------------
git-lfs
------------------------------

Building ``git-lfs`` with spack isn't straightforward as it requires ``go-bootstrap`` and ``go`` language support, which many compilers don't build correctly. We therefore require ``git-lfs`` as an external package. On many of the HPC systems, it is already available as a separate module or as part of a ``git`` module. On macOS and Linux, it can be installed using ``brew`` or other package managers (see :numref:`Sections %s <Platform_macOS>` and :numref:`%s <Platform_Linux>` for examples). :numref:`Section %s <MaintainersSection_Frontera>` describes a manual installation of ``git-lfs`` on TACC Frontera, a Centos7.9 system.

..  _Prerequisites_Miniconda:

------------------------------
Miniconda
------------------------------

If required, miniconda can be used to provide a basic version of Python that spack-stack uses to support its Python packages. A Bash script is provided to bootstrap the Miniconda installation and create a default directory layout.

.. code-block:: console

   cd spack-stack/bootstrap
   ./bootstrap.sh -p ${prefix}

Which runs the following commands

.. code-block:: console

   eval "$(/work/noaa/gsd-hpcs/dheinzel/jcsda/miniconda-3.9.12/bin/conda shell.bash hook)"
   conda install -c conda-forge libpython-static
   conda install poetry
   # Test, successful if silent
   python3 -c "import poetry"
   # log out to forget about the conda environment

..  _Prerequisites_Qt5:

------------------------------
qt (qt@5)
------------------------------

Building ``qt`` with spack isn't straightforward as it requires many libraries related to the graphical desktop that are often tied to the operating system, and which many compilers don't build correctly. We therefore require ``qt`` as an external package. On many of the HPC systems, it is already available as a separate module or provided by the operating system. On macOS and Linux, it can be installed using ``brew`` or other package managers (see :numref:`Sections %s <Platform_macOS>` and :numref:`%s <Platform_Linux>` for examples). 

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

..  _Prerequisites_ecFlow:

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

Create modulefile ``/discover/swdev/jcsda/spack-stack/modulefiles/ecflow/5.8.4`` from template ``doc/modulefile_templates/ecflow`` and update ``ECFLOW_PATH`` in this file.

.. note::
   For certain Cray systems, for example NRL's Narwhal or NOAA's Gaea, the following modifications are necessary: After extracting the ecflow tarball, edit ``ecFlow-5.8.4-Source/build_scripts/boost_build.sh`` and remove the following lines:

.. code-block:: console

   if [ "$PE_ENV" = INTEL ] ; then
      tool=intel
   fi
   if [ "$PE_ENV" = CRAY ] ; then
      tool=cray
   fi

   Further on Narwhal, the ``cmake`` command for ``ecbuild`` must be told to use the GNU compilers:

.. code-block:: console

   CC=gcc CXX=g++ FC=gfortran cmake .. -DCMAKE_INSTALL_PREFIX=/path/to/ecflow/installation 2>&1 | tee log.cmake

..  _Prerequisites_Texlive:

------------------------------
Texlive (TeX/LaTeX)
------------------------------

Building ``texlive`` isn't straightforward as it has many dependencies. Since it is only used to generated documentation for ``spack-stack`` (and other projects), i.e. not to compile any code, it makes no sense to build it with ``spack``. We therefore require ``texlive`` or any other compatible TeX/LaTeX distribution as an external package.

On many of the HPC systems, it is already available as a separate module or as part of the default operating system. On macOS, the MacTeX distribution provides a full and easy-to-install TeX/LaTeX environment (see :numref:`Section %s <Platform_macOS>`). On Linux, ``texlive`` can be installed using the default package manager (see :numref:`Section %s <Platform_Linux>`).
