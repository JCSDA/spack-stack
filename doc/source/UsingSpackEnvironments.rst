.. _UsingSpackEnvironments:

Using spack-stack environments
******************************

The following tutorial assumes you have a functioning spack-stack environment installed local to your system. This environment is provided on platforms described in :numref:`Section %s <Preconfigured_Sites>`. If you intend to run spack-stack on your developer machine or on a new platform, you can create an environment using the steps described in :numref:`Section %s <NewSiteConfigs>`.

Spack environments are used by loading the modulefiles generated at the end of the installation process. These modules control the unix environment and allow CMake, ecbuild, and other build toolchains to resolve the version of software intended for the compilation task. The ``spack`` command itself is not needed in this setup, hence the instructions for creating new environments (``source setup.sh`` etc.) can be ignored. The following is sufficient for loading the modules, allowing them to be used while compiling and running user code.

.. note::
   Customizations of the user environment in `.bashrc`, `.bash_profile`, ..., that load modules automatically may interfere with environment setup or updates. It is highly advised to avoid "polluting" the standard environment. If you frequently reuse the same module set, you should put your setup procedure into a shell script that can be sourced as needed.

Load the spack meta-modules directory into the module path using a value for ``$LOCATION`` from the table in :numref:`Section %s <Preconfigured_Sites_Tier1>`. If you created your own site config and spack-stack environment, use the install directory noted in the last step of the setup procedure. The meta-module does not update your environment and only informs your module tool of the location of a new set of modules.

.. code-block:: console

   module use $LOCATION/modulefiles/Core

If you run ``module available`` now, you will see only one option; the compiler. Loading the compiler meta-module will give access to the Python and MPI provider module and access to other packages that only depend on the compiler, not on the MPI provider or the Python provider. Loading the MPI meta-module will then add the MPI-dependent packages to the module path, and so on.

.. code-block:: console

   module load stack-compiler-name/compiler-version
   module load stack-python-name/python-version
   module load stack-mpi-name/mpi-version

Now list all available modules via ``module available``. You may be required to load additional packages depending on your build target's requirements, but now you have loaded a basic spack environment and you are ready to build. For the environment packages described in Section :numref:`Section %s <Environments>`, convenience modules are created that, when loaded, will automatically load the required dependency modules.

.. note::
   When using ``lua`` modules, loading a different module will automatically switch the dependency modules. This is not the case for ``tcl`` modules. For the latter, it is recommended to start over with a clean shell and repeat the above steps.
