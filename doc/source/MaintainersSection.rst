.. _MaintainersSection:

*************************
Maintainers Section
*************************

==============================
Pre-configuring sites
==============================

------------------------------
TACC Stampede2
------------------------------

Several packages need to be installed as a one-off before spack can be used.

``/work2/06146/tg854455/stampede2/spack-stack/spack-stack-0.0.1``

Intel oneAPI compilers
   The latest version of the Intel compiler on Stampede2 is 19.1.1, and the default modulefile created by the system administrators ties it to `gcc-9.1.0`. The way the module file has been written is incompatible with spack. We therefore recommend installing the latest Intel oneAPI compiler suite (Intel oneAPI Base and HPC Toolkits). The following instructions install Intel oneAPI 2022.2 in ``/work2/06146/tg854455/stampede2/spack-stack``.

.. code-block:: console

   wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18679/l_HPCKit_p_2022.2.0.191.sh
   wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18673/l_BaseKit_p_2022.2.0.262.sh
   # Customize the installations to install in /work2/06146/tg854455/stampede2/spack-stack/intel-oneapi-2022.2
   sh l_BaseKit_p_2022.2.0.262.sh
   sh l_HPCKit_p_2022.2.0.191.sh

git-lfs
   The following instructions install ``git-lfs`` in ``/work2/06146/tg854455/stampede2/spack-stack/git-lfs-1.2.1``. Version 1.2.1 is the Centos7 default version.

.. code-block:: console

   module purge
   cd /work2/06146/tg854455/stampede2/spack-stack/
   mkdir -p git-lfs-1.2.1/src
   cd git-lfs-1.2.1/src
   wget --content-disposition https://packagecloud.io/github/git-lfs/packages/el/7/git-lfs-1.2.1-1.el7.x86_64.rpm/download.rpm
   rpm2cpio git-lfs-1.2.1-1.el7.x86_64.rpm | cpio -idmv
   mv usr/* ../

   Create modulefile ``/work2/06146/tg854455/stampede2/spack-stack/modulefiles/git-lfs/1.2.1`` from template ``doc/modulefile_templates/git-lfs`` and update ``GITLFS_PATH`` in this file.

==============================
Testing new packages
==============================

 (chaining spack installations)
 
 https://spack.readthedocs.io/en/latest/chain.html?highlight=chaining%20spack%20installations
 
 