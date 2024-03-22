..  _KnownIssues:

Known Issues
*******************************

==============================
General
==============================

1. ``gcc@13`` (``gcc``, ``g++``, ``gfortran``) and ``apple-clang@15`` (``clang``, ``clang++``) not yet supported

   Our software stack doesn't build with ``gcc@13`` yet. This is also true when combining the LLVM or Apple ``clang`` compiler with ``gfortran@13``. We also don't support the latest release of ``apple-clang@15`` with Xcode 15.3 yet, and with Xcode 15.0 a workaround is described in :numref:`Section %s <NewSiteConfigs>`.

2. Build errors for ``mapl@2.35.2`` with ``mpich@4.1.1``

   This problem is described in https://github.com/JCSDA/spack-stack/issues/608.

3. Issues starting/finding ``ecflow_server`` due to a mismatch of hostnames

   On some systems, ``ecflow_server`` gets confused by multiple hostnames, e.g. ``localhost`` and ``MYORG-L-12345``. The ``ecflow_start.sh`` script reports the hostname it wants to use. This name (or both) must be in ``/etc/hosts`` in the correct address line, often the loopback address (``127.0.0.1``).

4. Installation of duplicate packages ``ecbuild``, ``hdf5``

   One reason for this is an external ``cmake@3.20`` installation, which confuses the concretizer when building a complex environment such as the ``skylab-dev`` or ```unified-dev`` environment. For certain packages (and thus their dependencies), a newer version than ``cmake@3.20`` is required, for others ``cmake@3.20`` works, and spack then thinks that it needs to build two identical versions of the same package with different versions of ``cmake``. The solution is to remove any external ``cmake@3.20`` package (and best also earlier versions) in the site config and run the concretization step again. Another reason on Ubuntu 20 is the presence of external ``openssl`` packages, which should be removed before re-running the concretization step.

5. Installation of duplicate package ``nco``

   We tracked this down to multiple versions of ``bison`` being used. The best solution is to remove external ``bison`` versions earlier than 3.8 from the site config (``packages.yaml``).

6. Installing/using graphical applications after switching user using ``sudo su``

   When using a role account to install spack-stack, it is sometimes necessary to run graphical applications such as the ``qt`` online installer. The following website describes in detail how this can be done: https://www.thegeekdiary.com/how-to-set-x11-forwarding-export-remote-display-for-users-who-switch-accounts-using-sudo/

7. ``==> Error: the key "core_compilers" must be set in modules.yaml`` during ``spack module [lmod|tcl] refresh``

   This error usually indicates that the wrong module type is used in the ``spack module ... refresh`` command. For example, the system is configured for ``lmod``, but the command used is ``spack module tcl refresh``.

==============================
MSU Hercules
==============================

1. ``wgrib2@2.0.8`` doesn't build on Hercules, use ``wgrib2@3.1.1`` instead.

==============================
NASA Discover
==============================

1. Timeout when fetching software during spack installs.

   Discover's connection to the outside world can be very slow and spack sometimes aborts with fetch timeouts. Try again until it works, sometimes have to wait for a bit.

2. ``configure: error: cannot guess build type; you must specify one`` when building ``freetype`` or other packages that use configure scripts

   This can happen if a spack install is started in a ``screen`` session, because Discover puts the temporary data in directories like ``/gpfsm/dnb33/tdirs/login/discover13.29716.dheinzel``, which get wiped out after some time. Without ``screen``, this problem doesn't occur.

3. Insufficient diskspace when building ``py-pytorch``

   This is because ``py-pytorch`` uses directory ``~/.ccache`` during the build, and the user's home directories have small quotas set. This problem can be avoided by creating a symbolic link from the home directory to a different place with sufficient quota: ``rm -fr ~/.ccache && ln -sf /path/to/dot_ccache_pytorch/ ~/.ccache``. It's probably a good idea to revert this hack after a successful installation.

==============================
NOAA Parallel Works
==============================

1. With the default module path, spack will detect the system as Cray, therefore one needs to remove it when building or using spack environments

2. ``libxml2`` won't untar during the ``spack install`` step, because of an issue with the filesystem. This can be avoided by making ``libxml2`` an external package

3. The ``/contrib`` filesystem can be very, very slow

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
NAVY HPCMP Narwhal
==============================

1. On Narwhal (like on any other Cray), the spack build environment depends on the currently loaded modules. It is therefore necessary to build separate environments for different compilers while having the correct modules for that setup loaded.

2. ``mapl@2.35.2`` does not build on Narwhal, see https://github.com/JCSDA/spack-stack/issues/524. When using the ``unified-dev`` template, one has to manually remove ``jedi-ufs-env`` and ``ufs-weather-model-env`` from the environment's ``spack.yaml``.

==============================
NAVY HPCMP Nautilus
==============================

1. ``wgrib2@2.0.8`` doesn't build on Nautilus, use ``wgrib2@3.1.1`` instead.

==============================
macOS
==============================

1. Error ``invalid argument '-fgnu89-inline' not allowed with 'C++'``

   This error occurs on macOS Monterey with ``mpich-3.4.3`` installed via Homebrew when trying to build the jedi bundles that use ``ecbuild``. The reason was that the C compiler flag ``-fgnu89-inline`` from ``/usr/local/Cellar/mpich/3.4.3/lib/pkgconfig/mpich.pc`` was added to the C++ compiler flags by ecbuild. The solution was to set ``CC=mpicc FC=mpif90 CXX=mpicxx`` when calling ``ecbuild`` for those bundles. Note that it is recommended to install ``mpich`` or ``openmpi`` with spack-stack, not with Homebrew.

2. Installation of ``gdal`` fails with error ``xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance``.

   If this happens, install the full ``Xcode`` application in addition to the Apple command line utilities, and switch ``xcode-select`` over with ``sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`` (change the path if you installed Xcode somewhere else).

3. Error ``AttributeError: Can't get attribute 'Mark' on <module 'ruamel.yaml.error' from ...`` when running ``spack install``

   Some users are seeing this with Python 3.10 installed via Homebrew on macOS. Run ``export | grep SPACK_PYTHON`` to verify the Python version used, then run ``brew list`` to check if there are alternative Python versions available. Manually setting ``SPACK_PYTHON`` to a different version, for example via ``export SPACK_PYTHON=/usr/local/bin/python3.9``, solves the problem.

4. Errors handling exceptions on macOS.

   A large number of errors related to handling exceptions thrown by applications was found when using default builds or Homebrew installations of ``mpich`` or ``openmpi``, which use flat namespaces. With our spack version, ``mpich`` and ``openmpi`` are installed with a ``+two_level_namespace`` option that fixes the problem.

5. Errors such as ``Symbol not found: __cg_png_create_info_struct``

   Can happen when trying to use the raster plotting scripts in ``fv3-jedi-tools``. In that case, exporting ``DYLD_LIBRARY_PATH=/usr/lib/:$DYLD_LIBRARY_PATH`` can help. If ``git`` commands fail after this, you might need to verify where ``which git`` points to (Homebrew vs module) and unload the ``git`` module.

6. ``apple-clang@15.0.0`` not yet supported

   Building with ``apple-clang@15.0.0`` is under development and should be working soon. In the meantime, please use ``apple-clang@14.x`` or older versions.

==============================
Ubuntu
==============================

1. The lmod version in Ubuntu 22.04 LTS breaks spack modules.

   Ubuntu 22.04 LTS will install lmod 6.6 from official apt repositories. Module files authored by spack use the `depends_on` directive that was introduced in lmod 7.0. The new site config instructions in :numref:`Section %s <NewSiteConfigs_Linux>` circumvent the issue by using `tcl/tk` environment modules. If you attempt to use lmod 6.6 you will get the following error:

   .. code-block:: console

      $ module load stack-python
      Lmod has detected the following error:  Unable to load module: python/3.10.8
      /home/ubuntu/spack-stack-1.3.1/envs/skylab-4/install/modulefiles/gcc/11.3.0/python/3.10.8.lua : [string "-- -*- lua -*-..."]:16: attempt to call global 'depends_on' (a nil value)
