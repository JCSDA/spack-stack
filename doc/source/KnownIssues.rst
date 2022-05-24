..  _KnownIssues:

*******************************
Known Issues
*******************************

==============================
General
==============================

1. First call to ``spack concretize`` fails with ``[Errno 2] No such file or directory: ... .json``

   This can happen when ``spack concretize`` is called the very first time in a new spack-stack clone, during which the boostrapping (installation of ``clingo``) is done first. Simply rerunning the command should solve the problem.

==============================
NOAA RDHPCS Gaea
==============================

1. Random "permission denied" errors during the spack install phase

   If random errors during the spack install phase occur related to "permission denied" when building packages, edit ``envs/env_name/config.yaml`` and comment out the lines ``build_stage`` and ``test_stage``.

2. Random "git-lfs not found" errors during the spack install phase

   If random errors during the spack install phase occur related to "git-lfs not found" when building packages (e.g. crtm), simply load the module and try again (``module load git-lfs``).
