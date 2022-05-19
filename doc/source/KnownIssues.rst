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
Site XYZ
==============================

**MISSING**