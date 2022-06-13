.. _Environments:

*************************
Constructing Environments
*************************

This section describes the environments (environment specs) defined in ``spack/var/spack/repos/jcsda-emc-bundles/packages``, additional packages available in the JCSDA/NOAA-EMC spack fork, as well as pre-defined application templates and container recipes.

Environments can be constructed in two ways in spack-stack:

1. Start with an empty template, ``spack stack create env --template=empty`` or just ``spack stack create env`` without specifying a template.

    - Configure the environment as shown in :numref:`Sections %s <Quickstart>` and :numref:`%s <Platforms>`.

    - Add spack packages (also referred to as ``specs``) to the environment using ``spack add``. These packages can be virtual environments described in :numref:`Section %s <EnvironmentsVirtualEnvironments>` below, or individual packages, e.g. ``esmf`` or ``atlas``. Examples:

        .. code-block:: console

           spack add netcdf-c@4.7.4
           spack add ufs-weather-model-env
           spack add ufs-weather-model-env@1.0.0 +debug
           spack add jedi-ewok-env +solo +r2d2 +ewok 
           spack add mapl@2.12.3 +debug ^esmf@8.3.0 +debug
           spack add mapl@2.12.3 +debug ^esmf@8.3.0 +debug
           ...

2. Use a non-empty template to automatically populate the environment with a vetted combination of packages. See :numref:`Section %s <EnvironmentsTemplates>` for a description of the available templates. Note that additional packages can be added to the templated environment as in the previous step after activating the environment. Example:

    .. code-block:: console

       spack stack create env --template=skylab-1.0.0
       ...
       spack env activate envs/env-name
       ...
       spack add jedi-tools-env@1.0.0

.. _EnvironmentsAdditionalPackages:

-------------------
Additional packages
-------------------

Packages that are available in the JCSDA/NOAA-EMC spack fork, but not (yet) in the authoritative spack repository are defined in ``spack/var/spack/repos/jcsda-emc/packages/``. Users are encouraged to run ``spack info <packagename>`` or open the files in an ASCII editor for more information.

**WORK IN PROGRESS**

**AUTOMATICALLY GENERATE A TABLE WITH NAME AND DESCRIPTION BASED ON THE FILE NAME AND THE DOXSTRING? IF WE DO THAT, ALSO UPDATE THE SECTION ON GENERATING DOCUMENTATION WITH THE NECESSARY DETAILS**

**For now, check the contents of ``spack/var/spack/repos/jcsda-emc/packages/`` yourself, sorry. Also, run ``spack info ecmwf-atlas``, for example, to obtain further information on the package.**

.. _EnvironmentsVirtualPackages:

----------------
Virtual packages
----------------

The purpose of virtual packages is to provide a convenient collection of packages for a given application. These packages are defined in ``spack/var/spack/repos/jcsda-emc-bundles/packages/``. Currently available virtual packages are:

**WORK IN PROGRESS**

**AUTOMATICALLY GENERATE A TABLE WITH NAME AND DESCRIPTION BASED ON THE FILE NAME AND THE DOXSTRING? IF WE DO THAT, ALSO UPDATE THE SECTION ON GENERATING DOCUMENTATION WITH THE NECESSARY DETAILS**

**For now, check the contents of ``spack/var/spack/repos/jcsda-emc-bundles/packages/`` yourself, sorry. Also, run ``spack info jedi-ewok-env``, for example, to obtain further information on the package.**

.. _EnvironmentsTemplates:

---------
Templates
---------

Templates are vetted combinations of packages, i.e. these have been tested to build together. Templates are defined in ``configs/templates/``. Currently available templates are:

**WORK IN PROGRESS**

**AUTOMATICALLY GENERATE A TABLE WITH NAME AND DESCRIPTION BASED ON THE FILE NAME AND THE SPECS IN THE TEMPLATE? IF WE DO THAT, ALSO UPDATE THE SECTION ON GENERATING DOCUMENTATION WITH THE NECESSARY DETAILS**

**For now, check the contents of ``configs/templates/`` yourself, sorry.**

.. _EnvironmentsContainers:

-----------------
Container recipes
-----------------

Container recipes are self-contained except that at container creation time (``spack stack create ctr ...``) package information from the common ``packages.yaml`` (or a manually provided version) is added to the ``packages:`` section, and specs are added in the section ``specs`` as defined in the template (default is an empty template with no specs.) Container recipes are defined in ``configs/containers``. Currently available container recipes are:

**WORK IN PROGRESS**

**AUTOMATICALLY GENERATE A TABLE WITH NAME AND DESCRIPTION BASED ON THE FILE NAME AND ... WHAT ELSE? IF WE DO THAT, ALSO UPDATE THE SECTION ON GENERATING DOCUMENTATION WITH THE NECESSARY DETAILS**

**For now, check the contents of ``configs/containers/`` yourself, sorry.**
