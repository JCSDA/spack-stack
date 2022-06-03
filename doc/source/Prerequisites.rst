..  _Prerequisites:

*******************************
Prerequisites
*******************************

==============================
Manual software installations
==============================

The following manual software installations may or may not be required as prerequisites, depending on the specific platform. For configurable/user systems, please consult Sect ...., for preconfigured systems please consult Section ... . Note that for preconfigured systems, the following one-off installations are only necessary for the maintainers of the preconfigured installations, users **do not** have to repeat any of these steps.

..  _Prerequisites_Git_LFS:

------------------------------
git-lfs
------------------------------

Building ``git-lfs`` with spack isn't straightforward as it requires ``go-bootstrap`` and ``go`` language support, which many compilers don't build correctly. We therefore require ``git-lfs`` as an external package. On many of the HPC systems, it is already available as a separate module or as part of a ``git`` module. On macOS and Linux, it can be installed using ``brew`` or other package managers (see :numref:`Sections %s <Platform_macOS>` and :numref:`%s <Platform_Linux>` for examples). :numref:`Section %s <MaintainersSection_Stampede2>` describes a manual installation of ``git-lfs`` on TACC Stampede, a Centos7 system.

..  _Prerequisites_Miniconda:

------------------------------
Miniconda
------------------------------

If required, miniconda can be used to provide a basic version of Python that spack-stack uses to support its Python packages.

In the following instructions, replace ``/work/noaa/gsd-hpcs/dheinzel/jcsda`` with the directory where your ``miniconda-3.9.7`` directory will be installed.

.. code-block:: console

   cd /work/noaa/gsd-hpcs/dheinzel/jcsda
   mkdir -p miniconda-3.9.7/src
   cd miniconda-3.9.7/src
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   sh Miniconda3-latest-Linux-x86_64.sh -u
   # Accept license agreement
   # Install in /work/noaa/gsd-hpcs/dheinzel/jcsda/miniconda-3.9.7
   # Do not have the installer initialize Miniconda3 by running conda init

Create modulefile ``/work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles/miniconda/3.9.7`` from template ``doc/modulefile_templates/miniconda`` and update ``MINICONDA_PATH`` in this file. Then:

.. code-block:: console

   module use /work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles
   module load miniconda/3.9.7
   which python3
   # make sure this points to the new miniconda install

Install two packages required for building Python modules with spack using ``conda``

.. code-block:: console

   eval "$(/work/noaa/gsd-hpcs/dheinzel/jcsda/miniconda-3.9.7/bin/conda shell.bash hook)"
   conda install -c conda-forge libpython-static
   conda install poetry
   # Test, successful if silent
   python3 -c "import poetry"
   # log out to forget about the conda environment

To use this installation of miniconda, the following needs to be done every time before installing packages with spack or before using the modules created by spack.

.. code-block:: console

   module use /work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles
   module load miniconda/3.9.7

..  _Prerequisites_Qt5:

------------------------------
qt (qt@5)
------------------------------

Building ``qt`` with spack isn't straightforward as it requires many libraries related to the graphical desktop that are often tied to the operating system, and which many compilers don't build correctly. We therefore require ``qt`` as an external package. On many of the HPC systems, it is already available as a separate module or provided by the operating system. On macOS and Linux, it can be installed using ``brew`` or other package managers (see :numref:`Sections %s <Platform_macOS>` and :numref:`%s <Platform_Linux>` for examples). 

On HPC systems without a sufficient Qt5 installation, we install it outside of spack with the default OS compiler and then point to it in the site's ``packages.yaml``. The following instructions install ``qt@5.15.3`` in ``/lustre/f2/pdata/esrl/gsd/spack-stack/qt-5.15.3``.

.. code-block:: console

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

.. note::
   The dependency on ``qt`` is introduced by ``ecflow``, which at present requires using ``qt@5`` - earlier or newer versions will not work.

.. note::
   When using an existing version provided by the operating system or as a module, one needs to check if all required components are installed. The ``ecflow`` installation will abort with an error message that a particular component of ``qt`` cannot be found.

..  _Prerequisites_Texlive:

------------------------------
Texlive (TeX/LaTeX)
------------------------------

Building ``texlive`` isn't straightforward as it has many dependencies. Since it is only used to generated documentation for ``spack-stack`` (and other projects), i.e. not to compile any code, it makes no sense to build it with ``spack``. We therefore require ``texlive`` or any other compatible TeX/LaTeX distribution as an external package.

On many of the HPC systems, it is already available as a separate module or as part of the default operating system. On macOS, the MacTeX distribution provides a full and easy-to-install TeX/LaTeX environment (see :numref:`Section %s <Platform_macOS>`). On Linux, ``texlive`` can be installed using the default package manager (see :numref:`Section %s <Platform_Linux>`).
