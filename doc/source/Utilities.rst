.. _Utilities:

Miscellaneous utilities
*************************

.. _Duplicate_Checker:

------------------------------
show_duplicate_packages.py
------------------------------

The utility located at util/show_duplicate_packages.py parses the output of ``spack concretize`` and detects duplicates. Usage is as follows:

.. code-block:: console

   spack concretize | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py
   # - OR -
   spack concretize |& tee log.concretize
   ${SPACK_STACK_DIR}/util/show_duplicate_packages.py log.concretize

The ``-d`` option shows only a list of the duplicates, as opposed to the default behavior, which is to show a print-out of all packages with colorized duplicates. In any case, the identification of any duplicates will yield a return code of 1. The ``-i`` option can be invoked multiple times to skip specific package names. The ``-c`` option can be used to ignore duplicates associated with different compilers; in an environment with, say, GCC and Intel copies of any given package, those two copies of a package will not be reported as duplicates.

.. _Permissions_Checker:

------------------------------
check_permissions.sh
------------------------------

The utility located at util/check_permissions.sh can be run inside any spack-stack environment directory intended for multiple users (i.e., on an HPC or cloud platform). It will return errors if the environment directory is inaccessible to non-owning users and groups (i.e., if o+rx not set), as well as if any directories or files have permissions that make them inaccessible to other users.

.. _LDD_Checker:

------------------------------
ldd_check.py
------------------------------

The utils/ldd_check.py utility should be run for new installations to ensure that no shared library or executable that uses shared libraries is missing a shared library dependency. If the script returns a warning for a given file, this may indicate that Spack's RPATH substitution has not been properly applied. In some instances, missing library dependencies may not indicate a problem, such as a library that is intended to be found through $LD_LIBRARY_PATH after, say, a compiler or MPI environment module is loaded. Though these paths should probably also be RPATH-ified, such instances of harmless missing dependencies may be ignored with ldd_check.py's ``--ignore`` option by specifying a Python regular expression to be excluded from consideration (see example below), or can be permanently whitelisted by modifying the ``whitelist`` variable at the top of the ldd_check.py script itself (in which case please submit a PR). The script searches the 'install/' subdirectory of a given path and runs ``ldd`` on all shared objects. The base path to be search can be specified as a lone positional argument, and by default is the current directory. In practice, this should be ``$SPACK_ENV`` for the environment in question.

.. code-block:: console

   cd $SPACK_ENV && ../../utils/ldd_check.py
   # - OR -
   utils/ldd_check.py $SPACK_ENV --ignore '^libfoo.+' # check for missing shared dependencies, but ignore missing libfoo*

.. _Acorn_Utilities:

------------------------------
Acorn utilities
------------------------------
The util/acorn/ directory provides scripting for spack-stack builds through PBS Pro on Acorn. To use them, copy them into the directory of the Spack environment you wish to build, set the number of nodes to use (make sure ``#PBS -l select=X`` and ``mpiexec -n X`` use the same value for ``X``), and run ``qsub build.pbs``. Note that the temporary directory specification uses a soft link where the referent location depends on the node (this is to avoid compiling directly on LFS, which frequently fails when working with small files as when cloning git repositories). For parallel installations on Acorn, 2-6 is a reasonable range for the number of nodes (MPI proc analogs), and 6-8 is a reasonable number for the number of threads (note that for ``#PBS -l ncpus=Y`` in build.pbs, ``Y`` should match the ``-j`` argument for ``spack install`` in spackinstall.sh).
