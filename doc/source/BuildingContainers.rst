.. _BuildingContainers:


Creating Containers
********************

=================
Container recipes
=================

Container recipes are self-contained except that at container creation time (``spack stack create ctr ...``) package information from the common ``packages.yaml`` (or a manually provided version) is added to the ``packages:`` section, and specs are added in the section ``specs`` as defined in the template (default is an empty template with no specs.) Container recipes are defined in ``configs/containers``. Currently available container recipes can be found in ``configs/containers/``.

**WORK IN PROGRESS**


-----------------------
Container build example
-----------------------

In this example, a container is created with an empty template, and specs are added manually. It is also possible to start with a different template, but it is important to know that container builds do not allow for multiple versions of the same package (e.g., ``fms@2022.01`` and ``fms@release-jcsda``), therefore not all templates will work (one can remove certain specs from the build, as long as this does not impact the usability of the container).

.. code-block:: console

   # See a list of preconfigured containers
   spack stack create ctr -h

   # Create container spack definition (spack.yaml) in directory envs/<container-config>
   spack stack create ctr docker-ubuntu-gcc-openmpi --template=empty

   # Descend into container environment directory
   cd envs/docker-ubuntu-gcc-openmpi

   # Edit config file and add the required specs in section "specs:"
   emacs spack.yaml

   # Docker: create Dockerfile and build container
   # See section "container" in spack.yaml for additional information
   spack containerize > Dockerfile
   docker build -t myimage .
   docker run -it myimage
