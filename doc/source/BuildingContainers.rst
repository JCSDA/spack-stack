.. _BuildingContainers:


Creating Containers
********************

=================
Container recipes
=================

Container recipes are self-contained except that at container creation time (``spack stack create ctr ...``) package information from the common ``packages.yaml`` (or a manually provided version) is added to the ``packages:`` section, and specs are added in the section ``specs`` from the specs file provided as an argument. Container recipes are defined in ``configs/containers``, and specs are defined in ``configs/containers/specs``.

**WORK IN PROGRESS**


-----------------------
Container build example
-----------------------

It is important to know that container builds do not allow for multiple versions of the same package (e.g., ``fms@2022.01`` and ``fms@release-jcsda``), which needs to be taken into account when creating the specs in ``configs/containers/specs/*.yaml``.

.. code-block:: console

   # See a list of preconfigured containers
   spack stack create ctr -h

   # Create container spack definition (spack.yaml) in directory envs/<container-config>
   spack stack create ctr --container=docker-ubuntu-gcc-openmpi --specs=jedi-ci

   # Descend into container environment directory
   cd envs/docker-ubuntu-gcc-openmpi

   # Docker: create Dockerfile and build container
   # See section "container" in spack.yaml for additional information
   spack containerize > Dockerfile
   docker build -t myimage .
   docker run -it myimage
