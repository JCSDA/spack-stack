.. _Add_Test_Packages:

Adding Test Packages (Chained Environments)
********************************************

Releases of spack-stack are deployed quarterly on supported platforms. Between releases, additional packages may be installed using Spack's *environment chaining* capabilities. This mechanism allows parts of the stack to be replaced and a new *chained environment* created while leaving the base release environment untouched.

What a "Chained Environment" Means
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A *chained environment* is a Spack environment ("downstream") that builds on top of one or more existing environments ("upstream"). Instead of creating a standalone installation, the downstream environment reuses the install tree(s) of previously deployed environments. The upstream environment provides a fully configured collection of packages and modulefiles, which the downstream environment can incorporate without rebuilding them.

In a chained environment, users may override specific packages (for example, to test a newer version) or add new packages on top of those supplied by the upstream stack. Because the downstream environment references the upstream installation without modifying it, the result is a chain of environments: the new environment extends or customizes the existing software stack while preserving the stability and integrity of the base installation.

Setting Up the Spack-Stack Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install an additional environment within an official spack-stack installation space, change into the appropriate spack-stack root directory and run: ``. setup.sh`` before proceeding with the steps below. To create a chained environment in a personal space outside an official installation, it is recommended that you use the same *spack-stack release* as the one providing the upstream environment.

For example, if you are targeting an environment installed under *spack-stack-1.4.1/*, clone and check out the matching release branch:

.. code-block:: console

   git clone --recurse-submodules -b  release/1.4.1 https://github.com/jcsda/spack-stack spack-stack-1.4.1


Then, in the newly created spack-stack directory:

.. code-block:: console

   . setup.sh

and proceed with environment creation.

Example: Creating a "netcdf-test" Chained Environment on Hera
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The example below demonstrates creating a ``netcdf-test`` chained environment on Hera using an existing GCC-based upstream environment. In this example, a newer version of NetCDF-C is built with the Intel compiler along with all dependencies required by the UFS Weather Model.

It is recommended to use one or more meta-modules (e.g., ``ufs-weather-model-env``) rather than individual packages. Meta-modules ensure that all required modulefiles from the upstream environment are made available in the downstream environment when:

.. code-block:: console

   spack module lmod refresh --upstream-modules


is invoked. Make sure to use the same compiler family as the upstream environment unless you intentionally override it and rebuild all dependent packages.

.. code-block:: console

   spack stack create env --name netcdf-test --template empty --site hera --compiler gcc \
      --upstream /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.4.1/envs/ue-gcc/install \
     [--upstream /path/to/second/install] [--modify-pkg netcdf-c]

   cd envs/netcdf-test
   spack env activate .


Upstream Environment Declaration in spack.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a chained environment is created, it includes an ``upstreams``: section at the end of its ``spack.yaml.`` This section records the name of each upstream environment and the location of its install tree. For example:

.. code-block:: console

   upstreams:
     my-base-env:
       install_tree: /full/path/to/spack-stack/envs/my-base-env/install

This configuration instructs Spack to reuse packages already installed in the upstream environment unless overridden in the downstream environment. Multiple upstream environments may be listed; Spack will search them in order during concretization.

Adding Packages After Creating the Chained Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the chained environment has been created and activated, additional packages may be added either:

 * directly from the command line, or
 * by editing spack.yaml.

*(i) Adding Packages from the Command Line*

For example, the following command adds the ufs-weather-model-env meta-environment and requests a new version of NetCDF-C:

.. code-block:: console

   spack add ufs-weather-model-env%intel ^netcdf-c@4.9.2

*(ii) Adding Packages by Editing spack.yaml*

Users may alternatively edit ``spack.yaml`` (and configuration files under ``./site/`` and ``./common/``, if needed) in the same way as for a base environment installation. This approach is useful when adding multiple packages or making broader specification adjustments.

Example of ``specs``: entry:

.. code-block:: console

   specs:
     - ufs-weather-model-env%intel ^netcdf-c@4.9.2
     - netcdf-fortran@4.6.1 %intel
     - nco@5.0.6 %intel

Concretization and Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After adding new packages using method (i) or (ii), proceed with concretization and installation. Use the ``--upstream-modules`` flag when refreshing **Lmod** modulefiles:

.. code-block:: console

   spack concretize 2>&1 | tee log.concretize
   spack install 2>&1 | tee log.install
   spack module lmod refresh --upstream-modules
   spack stack setup-meta-modules

Using the Chained Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use the chained environment, access it in the same way as a regular spack-stack installation: add the directory returned by ``spack stack setup-meta-modules`` (ending in */modulefiles/Core*) to your ``$MODULEPATH``.

This ensures that the correct combination of upstream and downstream modulefiles is available, while avoiding conflicts.

Do not add the *upstream environment’s* module directory directly to ``$MODULEPATH``.


.. note::
   The ``--upstream`` option for the ``spack stack create env`` command adds a specified Spack/spack-stack installation path as an upstream environment in the resulting ``spack.yaml``, and may be invoked multiple times. The command will *warn but not fail* if an invalid directory is provided. If the path does not exist, check for typos and ensure you are using the correct system path from the table in :numref:`Section %s <Preconfigured_Sites>`.

.. note::
   The ``--modify-pkg`` option for the ``spack stack create env`` command should be used by spack-stack maintainers when a package recipe needs to be modified for between-release deployments (i.e., chained environments within an official release). This option creates a separate custom Spack repository under ``$SPACK_ENV/envrepo/``, updates the environment’s repo configuration automatically, and prevents accidental modifications to the upstream installation.

.. note::
   Additional guidance and cautions on chaining Spack environments can be found in the `Spack documentation <https://spack.readthedocs.io/en/latest/chain.html?highlight=chaining%20spack%20installations>`_. In particular, avoid deleting modulefiles or dependencies from the upstream environment.

