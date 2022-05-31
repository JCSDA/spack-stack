..  _KnownIssues:

*******************************
Known Issues
*******************************

==============================
General
==============================

1. First call to ``spack concretize`` fails with ``[Errno 2] No such file or directory: ... .json``

   This can happen when ``spack concretize`` is called the very first time in a new spack-stack clone, during which the boostrapping (installation of ``clingo``) is done first. Simply rerunning the command should solve the problem.

==============================
NOAA RDHPCS Gaea
==============================

1. Random "permission denied" errors during the spack install phase

   If random errors during the spack install phase occur related to "permission denied" when building packages, edit ``envs/env_name/config.yaml`` and comment out the lines ``build_stage`` and ``test_stage``.

2. Random "git-lfs not found" errors during the spack install phase

   If random errors during the spack install phase occur related to "git-lfs not found" when building packages (e.g. crtm), simply load the module and try again (``module load git-lfs``).

==============================
macOS
==============================

1. Error `invalid argument '-fgnu89-inline' not allowed with 'C++'`

   This error occurs on macOS Monterey with ``mpich-3.4.3`` installed via Homebrew when trying to build the jedi bundles that use ``ecbuild``. The reason was that the C compiler flag ``-fgnu89-inline`` from ``/usr/local/Cellar/mpich/3.4.3/lib/pkgconfig/mpich.pc`` was added to the C++ compiler flags by ecbuild. The solution was to set ``CC=mpicc FC=mpif90 CXX=mpicxx`` when calling ``ecbuild`` for those bundles. Note that it is recommended to install ``mpich`` or ``openmpi`` with spack-stack, not with Homebrew.

2. Installation of ``poetry`` using ``pip3`` or test with ``python3`` fails

   This can happen when multiple versions of Python were installed with Homebrew and ``pip3``/``python3`` point to different versions. Run ``brew doctor`` and check if there are issues with Python not being properly linked. Follow the instructions given by ``brew``, if applicable.

3. Errors handling exceptions on macOS. A large number of errors related to handling exceptions thrown by applications was found when using default builds or Homebrew installations of ``mpich`` or ``openmpi``, which use flat namespaces. With our spack version, ``mpich`` and ``openmpi`` are installed with a ``+two_level_namespace`` option that fixes the problem.
