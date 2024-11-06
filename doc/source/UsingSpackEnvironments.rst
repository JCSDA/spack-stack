.. _UsingSpackEnvironments:

Using spack-stack environments
******************************

The following tutorial assumes you have a functioning spack-stack environment installed local to your system. This environment is provided on platforms described in :numref:`Section %s <Preconfigured_Sites>`. If you intend to run spack-stack on your developer machine or on a new platform, you can create an environment using the steps described in :numref:`Section %s <NewSiteConfigs>`.

There are three steps in setting up a usable development environment.
The first is to load the spack-stack environment and the second is to create a python virtual environment that is based on the python executable included within the spack-stack installation.
The reason for the python virtual environment is to ensure that python based applications are utilizing the spack-stack python modules in a consistent manner.
The third step is to configure your build system to use the python virtual environment created in the second step.

When using a spack-stack environment please utilize the spack-stack installed python modules as much as possible to help maintain the consistency mentioned above.
Note that after loading the spack-stack environment, all of the spack-stack installed python modules have been added to :code:`PYTHONPATH` so they are immediately accessable in your spack-stack based python virtual environment.

Load the spack-stack environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Create and activate a python virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is important that the creation of the python virtual environment be based on the python executable from the spack-stack installation.
This ensures consistency for python applications between the python executable and the spack-stack installed python packages (eg., numpy).
Without this consistency, it is easy for the wrong underlying library versions to get dynamically loaded and cause problems with applications crashing.

After the :code:`module load stack-python-name/python-version` command is run, the environment variable :code:`python_ROOT` will be set to the path where the spack-stack installed python version is located.
The :code:`python_ROOT` variable can be used to ensure that you get the proper virtual environment set as shown here:

.. code-block:: console

    ${python_ROOT}/bin/python3 -m venv <path-to-python-virtual-env>

Once the virtual environment is set, it must be activated:

.. code-block:: console

   source <path-to-python-virtual-env>/bin/activate

and after activation the spack-stack python executable will be the first one in your PATH.
The implication of this is that you should activate the python virtual enviroment as the last step in setting up your environment to ensure that the path to the virtual environment python remains first in your PATH. Here is an example of the whole process:

.. code-block:: console

    # start from clean slate
    module purge

    # load the base packages from the spack-stack environment
    module use $SPACK_STACK_GNU_ENV/install/modulefiles/Core
    module load stack-gcc/12.2.0
    module load stack-openmpi/4.1.4
    module load stack-python/3.11.7

    # load the additional environments required for your
    # target application
    module load jedi-fv3-env
    module load ewok-env
    module load soca-env

    # Create and activate the spack-stack based python
    # virtual environment
    # Note that you only need to create the virtual environment
    # the first time. Once created you only need to activate
    # the virtual environment.
    cd $HOME/projects/jedi
    ${python_ROOT}/bin/python3 -m venv jedi_py_venv # first time only
    source jedi_py_venv/bin/activate

Configure build system to utilize the python virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configuring your application build system to use the python virtual environment will continue the goal of consistency mentioned above where all python scripts and packages within the target application are based on the spack-stack built python executable and packages.

There are a variety of build systems in use, and CMake is quite commonly used so CMake will be used as an example for this step.
The CMake variable :code:`Python3_FIND_STRATEGY` can be used in conjunction with the python virtual environment to direct CMake to find and use the desired python virtual environment.
By default CMake chooses the latest python installation regardless of which comes first in your PATH.
By setting :code:`Python3_FIND_STRATEGY=LOCATION`, CMake will instead find and use the first python installation found in your PATH.
This is the reason for making the spack-stack based python virtual environment first in PATH in the step above.

:code:`Python3_FIND_STRATEGY` can be set in two ways: the first in the project's top-level CMakeLists.txt file and the second on the cmake (or ecbuild) command line.
Here are examples of both methods:

.. code-block:: console

   # In CMakeLists.txt
   set( Python3_FIND_STRATEGY LOCATION )

.. code-block:: console

   # On the command line
   cmake -DPython3_FIND_STRATEGY=LOCATION ...


