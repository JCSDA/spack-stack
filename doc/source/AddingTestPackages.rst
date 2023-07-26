.. _Add_Test_Packages:

Adding test packages (chaining environments)
********************************************

Releases of spack-stack are deployed quarterly on supported platforms. Between releases, additional packages may be installed through the following steps, which make use of Spack's environment chaining capabilities. This allows parts of the stack to be replaced while leaving the release environment untouched.

To install in an additional environment within an official spack-stack space, simply ``cd`` into the appropriate spack-stack root directory and run ``. setup.sh`` before continuing to the following steps. To create a chained environment in a personal space outside of an official installation, it is recommended that you use the same spack-stack release as the one from which you wish to use an upstream environment. For instance, if you are targeting an environment installed under ``spack-stack-1.4.1/``, then use ``git clone --recurse-submodules https://github.com/jcsda/spack-stack -b release/1.4.1`` to set up your installation, then in the newly created spack-stack directory run ``. setup.sh`` and proceed with the following steps. The following steps install a hypothetical new version of NetCDF C on Hera that also rebuilds all of its dependencies for the UFS Weather Model.

.. code-block:: bash

    spack stack create env --name netcdf-test --template empty --site hera --upstream /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.4.1/envs/unified-env/install [--upstream /path/to/second/install]
    cd envs/netcdf-test
    spack env activate .
    spack add ufs-weather-model-env%intel ^netcdf-c@5.0.0
    spack concretize | tee log.concretize
    spack install | tee log.install
    spack module lmod refresh --upstream-modules
    spack stack setup-meta-modules

To use the environment, access it in the same way as a regular spack-stack installation, i.e., add the directory provided by ``spack stack setup-meta-modules`` ending with '/modulefiles/Core' to your MODULEPATH variable. This will give access to the upstream modules needed while avoiding package conflicts; do not use the upstream environment in ``$MODULEPATH`` directly.
