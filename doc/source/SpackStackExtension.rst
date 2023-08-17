.. _SpackStackExtension:

Extension of spack command in spack-stack
*****************************************

This section describes the ``spack stack`` extension of the ``spack`` command, which simplifies the installation process. As for any other ``spack`` command, help is available with ``spack stack -h``. The ``spack stack`` extension has two subcommands, explained in the following.

.. code-block:: console

   spack stack [create|setup-meta-modules]

The ``spack stack create`` command creates a new environment or a new container (add ``-h`` for each of them for help):

.. code-block:: console

   spack stack create [env|ctr] 

The full list of options for creating environments is:

.. code-block:: console

   spack stack create env [--template TEMPLATE] [--specs [SPECS [SPECS ...]]] [--name NAME] [--dir DIR] [--overwrite] [--packages PACKAGES] [--site SITE] [--prefix PREFIX] [--envs-file ENVS_FILE] [--upstream UPSTREAM]

Here, ``TEMPLATE`` corresponds to a pre-defined list of specs (see :numref:`Section %s <EnvironmentsTemplates>`), ``SITE`` to a pre-configured or a configurable site (see :numref:`Section %s <Preconfigured_Sites>`). For all other options, consult the output of ``spack stack create env -h``.

The full list of options for creating containers is:

.. code-block:: console

   spack stack create ctr [--template TEMPLATE] [--name NAME] [--dir DIR] [--overwrite] [--packages PACKAGES] container

``TEMPLATE`` is identical to creating environments, and ``container`` corresponds to a pre-defined container recipe (see :numref:`Section %s <EnvironmentsContainers>`). For all other options, consult the output of ``spack stack create ctr -h``.

Following a successful creation of an environment (not a container), and the generation of the ``spack`` ``lmod/tcl`` module files via ``spack module [lmod|tcl] refresh``, the meta modules for compiler, Python interpreter and MPI library are generated with

.. code-block:: console

   spack stack setup-meta-modules

This step completes the environment generation and outputs a ``Core`` directory to screen that must be added to the module path (``module use .../Core``) as shown in :numref:`Section %s <UsingSpackEnvironments>`.