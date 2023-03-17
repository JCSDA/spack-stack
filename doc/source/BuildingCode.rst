.. _BuildingCode:

Building code with spack-stack
**************************************************

The following tutorial assumes you have a functioning spack-stack environment local to your system. This environment is provided on platforms described in `Section %s <Preconfigured_Sites>`. If you intend to run spack-stack on your developer machine or on a new platform, you can create an environment using the steps described in `Section %s <NewSiteConfigs>`.


.. _Preconfigured_Sites_UseSpackStack:

=================================================
Using a spack environment to compile and run code
=================================================

Spack environments are used by loading the modulefiles that generated at the end of the installation process. The ``spack`` command itself is not needed in this setup, hence the instructions for creating new environments (``source setup.sh`` etc.) can be ignored. The following is sufficient for loading the modules and using them to compile and run user code.

.. note::
   Customizations of the user environment in `.bashrc`, `.bash_profile`, ..., that load modules automatically may interfere with environment setup or updates. It is highly advised to avoid "polluting" the standard environment. If you frequently reuse the same module set, you should put your setup procedure into a shell script that can be sourced as needed.

--------------------
Pre-configured sites
--------------------

For pre-configured sites, follow the instructions in :numref:`Section %s <Preconfigured_Sites_Preconfigured_Sites>` to set the basic environment.



Next, load the spack meta-modules directory into the module path using

.. code-block:: console

   module use $LOCATION/modulefiles/Core

where ``$LOCATION`` refers to the install location listed in the table in :numref:`Section %s <Preconfigured_Sites_Preconfigured_Sites>`. Loading the compiler meta-module will give access to the Python and MPI provider module and to packages that only depend on the compiler, not on the MPI provider. Loading the MPI meta-module will then add the MPI-dependent packages to the module path. Use ``module available`` to look for the exact names of the meta-modules.

.. code-block:: console

   module load stack-compiler-name/compiler-version
   module load stack-python-name/python-version
   module load stack-mpi-name/mpi-version

After that, list all available modules via ``module available``. For the environment packages described in Section :numref:`Section %s <Environments>`, convenience modules are created that can be loaded and that automatically load the required dependency modules.

.. note::
   When using ``lua`` modules, loading a different module will automatically switch the dependency modules. This is not the case for ``tcl`` modules. For the latter, it is recommended to start over with a clean shell and repeat the above steps.