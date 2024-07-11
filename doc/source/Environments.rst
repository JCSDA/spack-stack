.. _Environments:

Constructing Environments
*************************

This section describes the environments (environment specs) defined in ``spack/var/spack/repos/jcsda-emc-bundles/packages``, additional packages available in the JCSDA/NOAA-EMC spack fork, as well as pre-defined application templates and container recipes.

Environments can be constructed in two ways in spack-stack:

1. Start with an empty template, ``spack stack create env --template=empty --compiler=<compiler>`` or just ``spack stack create env --compiler=<compiler>`` without specifying a template.

    - Configure the environment as shown in :numref:`Sections %s <NewSiteConfigs>`.

    - Ensure that <compiler> corresponds to a valid compiler for the site. Examples are ``gcc``, ``intel``, ``apple-clang``, ``oneapi``.

    - Add spack packages (also referred to as ``specs``) to the environment using ``spack add``. These packages can be virtual environments described in :numref:`Section %s <EnvironmentsVirtualPackages>` below, or individual packages, e.g. ``esmf`` or ``atlas``. Examples:

        .. code-block:: console

           spack add netcdf-c@4.7.4
           spack add ufs-weather-model-env
           spack add ufs-weather-model-env@1.0.0 +debug
           spack add ewok-env
           spack add mapl@2.12.3 +debug ^esmf@8.3.0 +debug
           spack add mapl@2.12.3 +debug ^esmf@8.3.0 +debug
           ...

2. Use a non-empty template to automatically populate the environment with a vetted combination of packages. See :numref:`Section %s <EnvironmentsTemplates>` for a description of the available templates. Note that additional packages can be added to the templated environment as in the previous step after activating the environment. Example:

    .. code-block:: console

       spack stack create env --template=skylab-1.0.0 --compiler=<compiler>
       ...
       cd envs/env-name
       spack env activate .
       ...
       spack add jedi-tools-env@1.0.0

.. _EnvironmentsAdditionalPackages:

-------------------
Additional packages
-------------------

Packages that are available in the JCSDA/NOAA-EMC spack fork, but not (yet) in the authoritative spack repository are defined in ``spack-ext/repos/spack-stack/packages/``. Users are encouraged to run ``spack info <packagename>`` or open the files in an ASCII editor for more information.

.. _EnvironmentsVirtualPackages:

----------------
Virtual packages
----------------

The purpose of virtual packages is to provide a convenient collection of packages for a given application. These packages are also defined in ``spack-ext/repos/spack-stack/packages/``. Users are encouraged to run ``spack info <packagename>`` or open the files in an ASCII editor for more information.

.. _EnvironmentsTemplates:

---------
Templates
---------

Templates are vetted combinations of packages, i.e. these have been tested to build together. Templates are defined in ``configs/templates/``. Users are encouraged to inspect these templates in an ASCII editor for more information.
