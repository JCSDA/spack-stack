..  _KnownIssues:

Known Issues
*******************************

==============================
General
==============================

1. First call to ``spack concretize`` fails with ``[Errno 2] No such file or directory: ... .json``

   This can happen when ``spack concretize`` is called the very first time in a new spack-stack clone, during which the boostrapping (installation of ``clingo``) is done first. Simply rerunning the command should solve the problem.

2. Build errors with Python 3.10

   These build errors have been addressed, it should now be possible to use Python 3.10. Please report errors to the spack-stack developers and, if applicable, to the spack developers.

3. Issues starting/finding ``ecflow_server`` due to a mismatch of hostnames
   On some systems, ``ecflow_server`` gets confused by multiple hostnames, e.g. ``localhost`` and ``MYORG-L-12345``. The ``ecflow_start.sh`` script reports the hostname it wants to use. This name (or both) must be in ``/etc/hosts`` in the correct address line, often the loopback address (``127.0.0.1``).

4. Installation of duplicate packages ``ecbuild``, ``hdf5``
   One reason for this is an external ``cmake@3.20`` installation, which confuses the concretizer when building a complex environment such as the ``skylab-dev`` or ```jedi-ufs-all`` environment. For certain packages (and thus their dependencies), a newer version than ``cmake@3.20`` is required, for others ``cmake@3.20`` works, and spack then thinks that it needs to build two identical versions of the same package with different versions of ``cmake``. The solution is to remove any external ``cmake@3.20`` package (and best also earlier versions) in the site config and run the concretization step again. Another reason on Ubuntu 20 is the presence of external ``openssl`` packages, which should be removed before re-running the concretization step.

==============================
NASA Discover
==============================

1. Timeout when fetching software during spack installs.

   Discover's connection to the outside world can be very slow and spack sometimes aborts with fetch timeouts. Try again until it works, sometimes have to wait for a bit.

==============================
NOAA Parallel Works
==============================

1. With the default module path, spack will detect the system as Cray, therefore one needs to remove it when building or using spack environments

2. ``libxml2`` won't untar during the ``spack install`` step, because of an issue with the filesystem. This can be avoided by making ``libxml2`` an external package

3. The ``/contrib`` filesystem can be very, very slow

==============================
NOAA RDHPCS Gaea
==============================

1. Random "permission denied" errors during the spack install phase

   If random errors during the spack install phase occur related to "permission denied" when building packages, edit ``envs/env_name/config.yaml`` and comment out the lines ``build_stage`` and ``test_stage``.

2. Random "git-lfs not found" errors during the spack install phase

   If random errors during the spack install phase occur related to "git-lfs not found" when building packages (e.g. crtm), simply load the module and try again (``module load git-lfs``).

==============================
UW (Univ. of Wisconsin) S4
==============================

1. Compiler errors when using too many threads for parallel builds

   Using more than two threads when running ``make`` (e.g. ``make -j4``) can lead to compiler errors like the following:

.. code-block:: console

   [94%] Linking CXX executable test_ufo_parameters
   icpc: error #10106: Fatal error in /home/opt/intel/oneapi/2022.1/compiler/2022.0.1/linux/bin/intel64/../../bin/intel64/mcpcom, terminated by kill signal
   ...

==============================
macOS
==============================

1. Error ``invalid argument '-fgnu89-inline' not allowed with 'C++'``

   This error occurs on macOS Monterey with ``mpich-3.4.3`` installed via Homebrew when trying to build the jedi bundles that use ``ecbuild``. The reason was that the C compiler flag ``-fgnu89-inline`` from ``/usr/local/Cellar/mpich/3.4.3/lib/pkgconfig/mpich.pc`` was added to the C++ compiler flags by ecbuild. The solution was to set ``CC=mpicc FC=mpif90 CXX=mpicxx`` when calling ``ecbuild`` for those bundles. Note that it is recommended to install ``mpich`` or ``openmpi`` with spack-stack, not with Homebrew.

2. Installation of ``poetry`` using ``pip3`` or test with ``python3`` fails

   This can happen when multiple versions of Python were installed with Homebrew and ``pip3``/``python3`` point to different versions. Run ``brew doctor`` and check if there are issues with Python not being properly linked. Follow the instructions given by ``brew``, if applicable.

3. Error ``AttributeError: Can't get attribute 'Mark' on <module 'ruamel.yaml.error' from ...`` when running ``spack install``

   Some users are seeing this with Python 3.10 installed via Homebrew on macOS. Run ``export | grep SPACK_PYTHON`` to verify the Python version used, then run ``brew list`` to check if there are alternative Python versions available. Manually setting ``SPACK_PYTHON`` to a different version, for example via ``export SPACK_PYTHON=/usr/local/bin/python3.9``, solves the problem.

4. Errors handling exceptions on macOS.

   A large number of errors related to handling exceptions thrown by applications was found when using default builds or Homebrew installations of ``mpich`` or ``openmpi``, which use flat namespaces. With our spack version, ``mpich`` and ``openmpi`` are installed with a ``+two_level_namespace`` option that fixes the problem.

5. Errors such as ``Symbol not found: __cg_png_create_info_struct``

   Can happen when trying to use the raster plotting scripts in ``fv3-jedi-tools``. In that case, exporting ``DYLD_LIBRARY_PATH=/usr/lib/:$DYLD_LIBRARY_PATH`` can help. If ``git`` commands fail after this, you might need to verify where ``which git`` points to (Homebrew vs module) and unload the ``git`` module.

6. Error building MET 10.1.1.20220419 build error on macOS Monterey 12.1
   See https://github.com/NOAA-EMC/spack-stack/issues/316. Note that this error does not occur in the macOS CI tests.
