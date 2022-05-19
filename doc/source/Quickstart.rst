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

   # Basic usage of create.py
   ./create.py -h

==============================
Create local environment
==============================

.. code-block:: console

   # See a list of sites and apps
   ./create.py environment -h

   # Create a pre-configured Spack environment in envs/<app>.<site>
   # (copies site-specific, application-specific, and common config files into the environment directory)
   ./create.py environment --site hera --app jedi-fv3 --name jedi-fv3.hera

   # Activate the newly created environment
   # Optional: decorate the command line prompt using -p
   #     Note: in some cases, this can mess up long lines in bash
   #     because color codes are not escaped correctly. In this
   #     case, use export SPACK_COLOR='never' first.
   spack env activate [-p] envs/jedi-fv3.hera

   # Optionally edit config files (spack.yaml, packages.yaml compilers.yaml, site.yaml)
   emacs envs/jedi-fv3.hera/spack.yaml
   emacs envs/jedi-fv3.hera/common/*.yaml
   emacs envs/jedi-fv3.hera/site/*.yaml

   # Process the specs and install
   # Note: both steps will take some time!
   spack concretize
   spack install

   # Create lua module files
   spack module lmod refresh

   # Create meta-modules for compiler, mpi, python
   ./meta_modules/setup_meta_modules.py

==============================
Create container
==============================

.. code-block:: console

   # See a list of preconfigured containers
   ./create.py container -h

   # Create container spack definition (spack.yaml) in directory envs/<spec>.<config>
   ./create.py container --config docker-ubuntu-gcc-openmpi --spec esmf

   # Descend into container environment directory
   cd envs/esmf.docker-ubuntu-gcc-openmpi

   # Optionally edit config file
   emacs spack.yaml

   # Docker: create Dockerfile and build container
   # See section "container" in spack.yaml for additional information
   spack containerize > Dockerfile
   docker build -t myimage .
   docker run -it myimage
