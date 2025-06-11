.. _Utilities:

Miscellaneous utilities
*************************

.. _Duplicate_Checker:

------------------------------
show_duplicate_packages.py
------------------------------

The utility located at util/show_duplicate_packages.py parses ``spack.lock`` and detects duplicates. Usage is as follows:

.. code-block:: console

   # In an active environment ($SPACK_ENV set), after concretization:
   ${SPACK_STACK_DIR}/util/show_duplicate_packages.py

In any case, the identification of any duplicates will yield a return code of 1. The ``-i`` option can be invoked multiple times to skip specific package names.

.. _Permissions_Checker:

------------------------------
check_permissions.sh
------------------------------

The utility located at ``util/check_permissions.sh`` can be run inside any spack-stack environment directory intended for multiple users (i.e., on an HPC or cloud platform). It will return errors if the environment directory is inaccessible to non-owning users and groups (i.e., if o+rx not set), as well as if any directories or files have permissions that make them inaccessible to other users.

.. _LDD_Checker:

------------------------------
ldd_check.py (Linux only)
------------------------------

The ``util/ldd_check.py`` utility should be run for new installations to ensure that no shared library or executable that uses shared libraries is missing a shared library dependency. If the script returns a warning for a given file, this may indicate that Spack's RPATH substitution has not been properly applied. In some instances, missing library dependencies may not indicate a problem, such as a library that is intended to be found through $LD_LIBRARY_PATH after, say, a compiler or MPI environment module is loaded. Though these paths should probably also be RPATH-ified, such instances of harmless missing dependencies may be ignored with ldd_check.py's ``--ignore`` option by specifying a Python regular expression to be excluded from consideration (see example below), or can be permanently whitelisted by modifying the ``whitelist`` variable at the top of the ldd_check.py script itself (in which case please submit a PR). The script searches the 'install/' subdirectory of a given path and runs ``ldd`` on all shared objects. The base path to be search can be specified as a lone positional argument, and by default is the current directory. In practice, this should be ``$SPACK_ENV`` for the environment in question. This utility is available for Linux only.

.. code-block:: console

   cd ${SPACK_ENV} && ../../util/ldd_check.py
   # - OR -
   util/ldd_check.py $SPACK_ENV --ignore '^libfoo.+' # check for missing shared dependencies, but ignore missing libfoo*

.. _Libirc_Checker:

------------------------------
check_libirc.sh (Linux only)
------------------------------

The ``util/check_libirc.sh`` utility should be run for new installations with Intel oneAPI (``icx``, ``icpx``, ``ifort`` or ``ifx``). In an active environment after a successful ``spack install``, execute the following command to check if any of the shared libraries or executables is linked to ``libirc.so``. See https://github.com/JCSDA/spack-stack/issues/1436 for some background context and why we want need to avoid ``libirc.so``. If ``libirc.so`` is linked to a shared library or executable in a spack-stack environment, please create an issue in the spack-stack GitHub repository (https://github.com/JCSDA/spack-stack/issues). For downstream applications, see the spack-stack wiki (https://github.com/JCSDA/spack-stack/wiki/Intel-oneAPI-compilers-and-libirc.so).

.. code-block:: console

   cd ${SPACK_ENV} && ../../util/check_libirc.sh
   # - OR -
   cd ${SPACK_STACK_DIR} && ./check_libirc.sh

.. _Parallel_Install:

------------------------------
parallel_install.sh
------------------------------

The util/parallel_install.sh utility runs parallel installations by launching multiple ``spack install`` instances as backgrounded processes. It can be run as an executable or sourced; the latter option will cause the launched jobs to be associated with the current shell environment. It takes the number of ``spack install`` instances to launch and the number of threads per instance as arguments, in that order, and accepts optional arguments which are applied to each ``spack install`` instance. For instance, ``util/parallel_install.sh 4 8 --fail-fast`` will run four instances of ``spack install -j8 --fail-fast &``. Output files are automatically saved under the current Spack environment directory, ``$SPACK_ENV``.

.. note::
   The parallel_install.sh utility runs all installation instances on a single node, therefore be respectful of other users and of system usage policies, such as computing limits on HPC login nodes.

.. _Fetch_Cargo_Dependencies:
-------------------------------------
fetch_cargo_deps.py / install_rust.sh
-------------------------------------

This utility downloads Rust/Cargo package dependencies and stores them in a local directory for later use during ``spack install``. This is required for installing on systems that do no have access to the internet during the ``spack install`` phase and complements other mirrors such as the spack source mirror.

Run this script in an active, concretized Spack environment to fetch Rust dependencies and store them in ``${CARGO_HOME}. You must either run it with ``spack-python`` or have ``spack-python`` in your ``${PATH}``. Ensure ``${CARGO_HOME}`` has the same value when ``spack install`` is run. For each spec that is a CargoPackage or a PythonPackage with a rust dependency, the script will attempt to fetch all of its cargo dependencies using ``cargo`` if available in the user's environment, but will fall back to installing ``cargo``/``rustup`` from the internet using ``install_rust.sh`` (located in in the same directory as this script).

.. _Fetch_Go_Dependencies:

----------------
fetch_go_deps.py
----------------

The ``fetch_go_deps.py`` utility prefetches Go dependencies, storing them in a local directory for later use during ``spack install``. This is required for installing on systems that do no have access to the internet during the ``spack install`` phase and complements other mirrors such as the spack source mirror. The ``$GOMODCACHE`` variable must be set, and the utility must be run in an active, concretized environment. It will fetch Spack packages of type GoPackage, and fetch all dependencies based on the dependency listings found in those packages. The utilities will attempt to use each package's ``go`` dependency, in which case these utilities must be run after ``go`` is installed. It will revert to using system-installed ``go`` if available.

.. _Acorn_Utilities:

------------------------------
Acorn utilities
------------------------------
The util/acorn/ directory provides scripting for spack-stack builds through PBS Pro on Acorn. To use them, copy them into the directory of the Spack environment you wish to build, set the number of nodes to use (make sure ``#PBS -l select=X`` and ``mpiexec -n X`` use the same value for ``X``), and run ``qsub build.pbs``. Note that the temporary directory specification uses a soft link where the referent location depends on the node (this is to avoid compiling directly on LFS, which frequently fails when working with small files as when cloning git repositories). For parallel installations on Acorn, 2-6 is a reasonable range for the number of nodes (MPI proc analogs), and 6-8 is a reasonable number for the number of threads (note that for ``#PBS -l ncpus=Y`` in build.pbs, ``Y`` should match the ``-j`` argument for ``spack install`` in spackinstall.sh).
