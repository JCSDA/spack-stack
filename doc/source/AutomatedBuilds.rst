================
Automated builds
================

.. _AutomatedBuildWorkflow:

Workflow
*************************

The spack-stack repository now contains scripts for implementing scheduled, automated building, unit testing, and build caching of packages. These scripts live under utils/weekly_build/. They download their own copy of spack-stack (the develop branch, by default) and build one or more environments under that directory structure, which may be transient or reused.

Script failures are detected by non-zero exit codes.

The list of packages to be unit tested is stored in the ``$PACKAGES_TO_TEST`` variable in ShellSetup.sh. As unit testing needs are identified, this list should be updated to be as comprehensive as possible based on https://github.com/JCSDA/spack-stack/wiki/Automated-testing-and-building#unit-testing-requirements.

.. _AutomatedBuildAddPlatform:

Overview of implementing on a new platform
******************************************

Use a clean environment. Do NOT run setup.sh in the directory containing the build scripts (util/weekly_build/) to be run. Nothing in spack-stack outside of the build scripts is needed to get the automated build workflow running, as the workflow will take care of download a copy of spack-stack to be used for doing the automated builds themselves.

-------------------------------
Platform-specific configuration
-------------------------------

The ShellSetup.sh script points to a script in the sites/ subdirectory based on the site name as set by the third argument of each build script (stored and used as ``$PLATFORM`` throughout the scripts). Note that a number of variables and functions can be set or overridden here:
 - ``$COMPILERS``: Space-delimited list of compilers to be built against on a given system.
 - ``$TEMPLATES``: Space-delimited list of templates to install. Default is 'unified-env'.
 - ``$PACKAGES_TO_TEST``: Space-delimited list of packages for which units tests should be run.
 - ``$PACKAGES_TO_INSTALL``: Space-delimited list of packages to be installed. For many systems it can be left empty so as to install the entire Unified Environment.
 - ``alert_cmd()``: This function should be set for each system. It is invoked when any step fails (non-zero exit code somewhere in the workflow), and so can be used to send emails, post to Slack or GitHub, etc.
 - ``spack_wrapper()``: This function runs the Spack command, where the first argument is a log file name. It should not typically need to be redefined by platform.
 - ``spack_install_wrapper()``: This function determines the means by which the ``spack`` command is invoked for the install steps, and can be overridden for each platform. If testing and installation will be performed outside of a batch scheduler, i.e., directly on a login node, then the default can probably be used. However, overriding this function allows, for instance, for job schedulers to be invoked (srun, qsub, etc.), as well as for parallel installations to be performed. Note that the first argument is a log file name, so custom versions of this function will most likely need to use ``shift`` to properly access the remaining arguments.
 - ``$INSTALL_OPTS``: Additional ``spack install`` flags to be supplied to ``spack_install_wrapper()``.
 - ``$TEST_<APPNAME>``: Set this variable to ON in order to enable the corresponding test under util/weekly_build/apptests/.
 - ``$BUILD_CACHE``: Name of or path to (beginning with '\file://') build cache directory. Defaults to 'local-binary' mirror defined in site's mirrors.yaml.
 - ``$SOURCE_CACHE``: Name of or path to (beginning with '\file://') source cache directory. Defaults to 'local-source' mirror defined in site's mirrors.yaml.
 - ``$PADDED_LENGTH``: Padded length setting for Spack build cache generation. It should be as long as possible without the build failing.
 - ``$KEEP_WEEKLY_BUILD_DIR``: Set to 'YES' to use a persistent directory structure for automated builds.

------------------------------
Setting up weekly builds: cron
------------------------------

Prior to running, obtain a current copy of the build scripts by cloning the spack-stack repository to the platform of interest (/path/to/spack-stack-auto-build/).

If /path/to/spack-stack is the local spack-stack root directory containing spack-stack-x.y.z installations, run ``mkdir -p /path/to/spack-stack/weekly_build/logs``.

In crontab, add:

.. code-block:: console

   0 1 * * SUN /path/to/spack-stack-auto-build/util/weekly_build/SpackStackBuildCache_AllSteps.sh $(date +\%y\%m\%d) /path/to/spack-stack/weekly_build acorn > /path/to/spack-stack/weekly_build/logs/cron.$(date +\%y\%m\%d).out 2>&1
