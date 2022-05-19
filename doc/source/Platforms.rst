.. _Platforms:

*************************
Platforms
*************************

==============================
Pre-configured sites
==============================

Ready-to-use spack-stack installations are available on the following platforms:

**Note: this versions are for early testers - use at your own risk**

+-----------------------+---------------------------+------------------+
| System                | Maintained by (temporary) | jedi-ewok tested |
+=======================+===========================+==================+
| MSU Orion             | Dom Heinzeller            | yes              |
+-----------------------+---------------------------+------------------+
| NASA Discover         | Dom Heinzeller            | yes              |
+-----------------------+---------------------------+------------------+
| NCAR-Wyoming Cheyenne | Dom Heinzeller            | yes              |
+-----------------------+---------------------------+------------------+
| NOAA NCO WCOSS2       |                           |                  |
+-----------------------+---------------------------+------------------+
| NOAA RDHPCS Gaea      | Dom Heinzeller            | yes              |
+-----------------------+---------------------------+------------------+
| NOAA RDHPCS Hera      |                           |                  |
+-----------------------+---------------------------+------------------+
| NOAA RDHPCS Jet       |                           |                  |
+-----------------------+---------------------------+------------------+
| TACC Stampede2        | Dom Heinzeller            | install yes / not yet run |
+-----------------------+---------------------------+------------------+

+-----------------------+-------------------------------------------------------------------------------------------------------+
| System                | Location                                                                                              |
+=======================+=======================================================================================================+
| MSU Orion             | ``/work/noaa/gsd-hpcs/dheinzel/spack-stack-20220411-ewok-tmp``                                        |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NASA Discover         | ``/discover/swdev/jcsda/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.1/install``         |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NCAR-Wyoming Cheyenne | ``/glade/work/jedipara/cheyenne/spack-stack/spack-stack-v0.0.1/envs/jedi-all-intel-2022.0.2/install`` |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA NCO WCOSS2       |                                                                                                       |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Gaea      | ``/lustre/f2/pdata/esrl/gsd/spack-stack/spack-stack-v0.0.1``                                          |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Hera      |                                                                                                       |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| NOAA RDHPCS Jet       |                                                                                                       |
+-----------------------+-------------------------------------------------------------------------------------------------------+
| TACC Stampede2        | ``/work2/06146/tg854455/stampede2/spack-stack/spack-stack-0.0.1``                                     |
+-----------------------+-------------------------------------------------------------------------------------------------------+




For questions or problems, please consult the known issues in :numref:`Chapter %s <KnownIssues>`, the currently open GitHub `issues <https://github.com/noaa-emc/spack-stack/issues>`_ and `discussions <https://github.com/noaa-emc/spack-stack/discussions>`_ first.

==============================
Reference site configs
==============================

**MISSING**

==============================
Generating new site configs
==============================
Recommended: Start with an empty (default) site config. Then run ``spack external find`` to locate common external packages such as git, Perl, CMake, etc., and run ``spack compiler find`` to locate compilers in your path. Compilers or external packages with modules need to be added manually.

.. code-block:: console

   ./create.py environment --site default --app jedi-ufs --name jedi-ufs.mysite

   # Descend into site config directory
   cd envs/jedi-ufs.mysite/site

   # Find external packages and compilers, output the files here
   # (overwrites packages.yaml and compilers.yaml)
   SPACK_SYSTEM_CONFIG_PATH=`pwd` spack external find --all --scope system
   SPACK_SYSTEM_CONFIG_PATH=`pwd` spack compiler find --scope system

   # Optionally edit config files as above in the quickstart section

   # Optionally attempt to find additional packages by name,
   # for example: "spack external find wget"

It is also instructive to peruse the GitHub actions scripts in ``.github/workflows`` and ``.github/actions`` to see how automated spack-stack builds are configured for CI testing, as well as the existing site configs in ``configs/sites``.
