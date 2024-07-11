.. _CreatingEnvironment:

Creating and installing new environments
****************************************

The following instructions are a simplified version of the instructions found in :numref:`Sections %s <NewSiteConfigs_macOS>` and :numref:`%s <NewSiteConfigs_Linux>`, and should work for systems where spack-stack already has a site configuration, or where minimal configuration is necessary. For more detailed instructions, including how to generate new site configurations and more details of when and how to use external packages, see :numref:`Sections %s <NewSiteConfigs_macOS>` and :numref:`%s <NewSiteConfigs_Linux>`. To chain a new Spack environment to an existing one, such as to test a new package version based on dependencies already installed in the upstream environment, see :numref:`%s <Add_Test_Packages>`.

Note that items in "<>" should be replaced with the appropriate values (site names, etc.), and items in '[]' are optional. *<site name>* and *<template name>* must match the names of directories found under 'configs/sites/' and 'configs/templates/', respectively; *<environment name>* is a user-chosen name for the Spack environment. *<path to spack-stack directory>* is the root directory created by cloning the spack-stack GitHub repository, which contains 'configs/', 'doc/', 'setup.sh', 'util/', etc.

.. code-block:: console

   # To generate a new spack-stack directory structure, run 'git clone --recurse-submodules https://github.com/JCSDA/spack-stack',
   # optionally with, e.g., '-b release/1.4.1' to specify the version

   . <path to spack-stack directory>/setup.sh

   spack stack create env --site <site name> --template <template name> --name <environment name> --compiler <compiler>

   cd ${SPACK_STACK_DIR}/envs/<environment name>/

   spack env activate .

   # If not using an existing site configuration, you may wish to modify config files and/or populate them using commands
   # such as 'spack external find' and 'spack compiler find'.
   # See https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html

   spack concretize 2>&1 | tee log.concretize

   spack install [--verbose] [--fail-fast] 2>&1 | tee log.install

   spack module lmod refresh

   spack stack setup-meta-modules

.. note::
   Depending on the site configuration, ``tcl`` may be used instead of ``lmod`` modules. Check ``envs/<environment name>/site/modules.yaml`` and replace ``lmod`` with ``tcl`` if necessary in ``spack module lmod refresh``.
