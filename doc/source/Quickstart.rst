.. _Quickstart:

*************************
Quickstart
*************************

.. code-block:: console

   git clone --recursive https://github.com/NOAA-EMC/spack-stack.git
   cd spack-stack

   # Ensure Python 3.7+ is available and the default before sourcing spack

   # Sources Spack from submodule and sets ${SPACK_STACK_DIR}
   source setup.sh

   # Basic usage of spack stack create
   spack stack create -h

.. note::

   We strongly recommend using external Python versions 3.8 or 3.9 with spack-stack due to numerous problems with Python 3.10 (see also :numref:`Section %s <KnownIssues>`).

=================================================
Using spack to create environments and containers
=================================================

------------------------
Create local environment
------------------------

The following instructions install a new spack environment on a pre-configured site (see :numref:`Section %s <Platforms_Preconfigured_Sites>` for a list of pre-configured sites and site-specific notes). Instructions for creating a new site config on an configurable system (i.e. a generic Linux or macOS system) can be found in :numref:`Section %s <Platform_New_Site_Configs>`.

.. code-block:: console

   # See a list of sites and apps
   spack stack create env -h

   # Create a pre-configured Spack environment in envs/<app>.<site>
   # (copies site-specific, application-specific, and common config files into the environment directory)
   spack stack create env --site hera --specs jedi-fv3-env --name jedi-fv3.hera

   # Activate the newly created environment
   # Optional: decorate the command line prompt using -p
   #     Note: in some cases, this can mess up long lines in bash
   #     because color codes are not escaped correctly. In this
   #     case, use export SPACK_COLOR='never' first.
   spack env activate [-p] envs/jedi-fv3.hera

   # Optionally edit config files (spack.yaml, packages.yaml compilers.yaml, site.yaml)
   emacs envs/jedi-fv3.hera/spack.yaml
   emacs envs/jedi-fv3.hera/packages.yaml
   emacs envs/jedi-fv3.hera/site/*.yaml

   # Process the specs and install
   # Note: both steps will take some time!
   spack concretize
   spack install [--verbose] [--fail-fast]

   # Create lua module files
   spack module lmod refresh

   # Create meta-modules for compiler, mpi, python
   spack stack setup-meta-modules

------------------------
Create container
------------------------

.. code-block:: console

   # See a list of preconfigured containers
   spack stack create container -h

   # Create container spack definition (spack.yaml) in directory envs/<spec>.<config>
   spack stack create container docker-ubuntu-gcc-openmpi --specs ufs-weather-model-env

   # Descend into container environment directory
   cd envs/ufs-weather-model.docker-ubuntu-gcc-openmpi

   # Optionally edit config file
   emacs spack.yaml

   # Docker: create Dockerfile and build container
   # See section "container" in spack.yaml for additional information
   spack containerize > Dockerfile
   docker build -t myimage .
   docker run -it myimage

------------------------
Extending environments
------------------------

Additional packages (and their dependencies) or new versions of packages can be added to existing environments. It is recommended to take a backup of the existing environment directory (e.g. using ``rsync``) or test this first as described in :numref:`Section %s <MaintainersSection_Testing_New_Packages>`, especially if new versions of packages are added that are themselves dependencies for other packages. In some cases, adding new versions of packages will require rebuilding large portions of the stack, for example if a new version of ``hdf5`` is needed. In this case, it is recommended to start over with an entirely new environment.

In the simplest case, a new package (and its basic dependencies) or a new version of an existing package that is not a dependency itself can be added as described in the following for a new version of ``ecmwf-atlas``.

1. Check if the package has any variants defined in the common (``env_dir/packages.yaml``) or site (``env_dir/site/packages.yaml``) package config and make sure that these are reflected
   correctly in the ``spec`` command:

.. code-block:: console

   spack spec ecmwf-atlas@0.29.0

2. Add package to environment specs:

.. code-block:: console

   spack add ecmwf-atlas@0.29.0

3. Run ``concretize`` step

.. code-block:: console

   spack concretize

4. Install

.. code-block:: console

   spack install [--verbose] [--fail-fast]

Further information on how to define variants for new packages, how to use these non-standard versions correctly as dependencies, ..., can be found in the `Spack Documentation <https://spack.readthedocs.io/en/latest>`_.

=================================================
Using a spack environment to compile and run code
=================================================

Spack environments are used by loading the modulefiles that generated at the end of the installation process. The ``spack`` command itself is not needed in this setup, hence the instructions for creating new environments (``source setup.sh`` etc.) can be ignored. The following is sufficient for loading the modules and using them to compile and run user code.

--------------------
Pre-configured sites
--------------------

For pre-configured sites, follow the instructions in :numref:`Section %s <Platforms_Preconfigured_Sites>` to set the basic environment.

.. note::
   Customizations of the user environment in `.bashrc`, `.bash_profile`, ..., that load certain modules automatically may interfere with the setup. It is highly advised to avoid "polluting" the standard environment, i.e. to keep the default environment as clean as possible, and create shell scripts that can be sourced to conveniently configure a user environment for a specific task instead.

Next, load the spack meta-modules directory into the module path using

.. code-block:: console

   module use $LOCATION/modulefiles/Core

where ``$LOCATION`` refers to the install location listed in the table in :numref:`Section %s <Platforms_Preconfigured_Sites>`. Loading the compiler meta-module will give access to the Python and MPI provider module and to packages that only depend on the compiler, not on the MPI provider. Loading the MPI meta-module will then add the MPI-dependent packages to the module path. Use ``module available`` to look for the exact names of the meta-modules.

.. code-block:: console

   module load stack-compiler-name/compiler-version
   module load stack-python-name/python-version
   module load stack-mpi-name/mpi-version

After that, list all available modules via ``module available``. For the environment packages described in Section :numref:`Section %s <Environments>`, convenience modules are created that can be loaded and that automatically load the required dependency modules.

.. note::
   When using ``lua`` modules, loading a different module will automatically switch the dependency modules. This is not the case for ``tcl`` modules. For the latter, it is recommended to start over with a clean shell and repeat the above steps.

-----------------------------------------
Configurable sites (generic macOS, Linux)
-----------------------------------------

The process for configurable sites is identical to that for pre-configured sites described above. ``$LOCATION`` in this case needs to be replaced with the install directory for the spack packages, which by default is subdirectory ``install`` in the environment directory.
