# spack-stack Project Charter

## Introduction

spack-stack is a project which allows sysadmins and users to install
correct versions of the many dependent packages that are required to
build the Unified Forecast System (UFS) and other models.

spack-stack relies on the open-source [spack
project](https://github.com/spack/spack). Spack uses package
configuration files to manage the building and dependencies of each
package in the stack. (For example, the spack netcdf-c package file
manages the installation of the netCDF C library.)

All package configuration files used by spack-stack are maintained in
the main spack repository, making them available for all
users. spack-spack is a thin shell on spack which contains necessary
configuration files for our HPC systems, and some utilities which aid
in installing the large number of packages managed by spack-stack.

## Stakeholders

- The NOAA Environmental Modeling Center (EMC)
- The UCAR Joint Center for Satellite Data Assimilation (JCSDA)
- The Earth Prediction Innovation Center (EPIC)
- The U.S. Naval Research Laboratory (NRL)

Each stakeholder will designate a small number of developers to assist
in spack-stack development by becoming a code manager of the
spack-stack repo.

### Code Managers

Organization | Code Manager(s)
-------------|----------------
NOAA EMC | Alex Richert, Hang Lei, Ed Hartnett
JCSDA | Steve Herbener, TBD
EPIC | Cam Book, Natalie Perlin, Ratko Vasic
NRL | Dom Heinzeller, Sarah King

## Project Process

The spack-stack project will follow the processes outlined in this
document to allow all stakeholders to get the benefits they need from
spack-stack.

### Requesting a New Package, fork management

New packages must be requested as a GitHub issue. There is a template
with relevant questions that must be answered.

New packages must have a working package configuration file in
spack. If not present, it must be added - if present, it must be
examined and tested for correctness. It must be maintained with each
new release of the package. Some package files are quite simple,
others are very complex and take more work.

Developing and maintaining the spack package file for each package is
the responsibility of the organization that has requested that
package. In the case of packages used by all organizations (like
netcdf-c), the work of maintaining the spack package file is shared.

Spack package files should be pushed to the spack main repository, not
held within the spack-stack project. For quick development and
execution, package files can be temporarily housed in the the spack
fork used by spack-stack, but all should be moved to the main spack
repo as time permits.

Regular updates of our spack submodule (a fork of the authoritative repo)
are necessary to keep the code in sync and simplify the process of
sending updates in our fork to upstream.

### Installing on HPC Systems

The spack-stack stack must be installed on various NOAA, NCAR, NASA,
and other HPC systems. Each stakeholder will designate developers to
install on their systems (see https://spack-stack.readthedocs.io/en/latest/PreConfiguredSites.html).

### Releases

Any stakeholder can perform a release at any time.

The release process:
* Create a GitHub issue explaining the reason for the release, and to notify all other stakeholders.
* Unless it is a patch release (increasing the z in x.y.z,), create a project board for the release at https://github.com/JCSDA/spack-stack/projects.
* Designate any issues that must be fixed before release by assigning it to the epic and the project board, and ensure their completion.
* Install the release tags (or the final version of the release branches to allow for last-minute site config updates) on all supported platforms.
* Update the documentation and create release tags for the spack-stack repo and the spack submodule.
* Update the GitHub Release Notes.
* Perform the release on GitHub.

### Tags

Sometimes tags are preferrable to releases. Tags can be added at any time. Tag process:
* Add a new issue documenting the reason for the tag.
* Tag the spack-stack repo.

### Documentation

spack-stack is documented with its README.md and [Spack Documentation
on readthedocs](https://spack-stack.readthedocs.io/en/latest/#).

### Reporting Problems

All problems are reported as issues on the spack-stack GitHub site.

### Fixing Problems

Problems in stack-spack will be fixed by the code managers.

Problems in spack package files will be solved by programmers of the
organization which uses the package. Many packages are shared, in
which case the work will be shared by the code managers.

## Requesting updates to spack-stack

### Directory structure of spack-stack installations

#### Directory structure of spack-stack installs

/path/to/spack-stack/spack-stack-x.y.z/envs/ue-compiler-name-compiler-version/install/compiler-name/compiler-version/package-name-version-hash

_Example_
/Users/heinzell/prod/spack-stack-1.4.0/envs/ue-apple-clang-13.1.6/install/apple-clang/13.1.6/netcdf-c-4.9.2-vrrvi2u

#### Auto-generated modules structure (no MPI dependency)

/path/to/spack-stack/spack-stack-x.y.z/envs/ue-compiler-name-compiler-version/install/modulefiles/compiler-name/compiler-version/package-name/package-version[.lua]

_Example_
/Users/heinzell/prod/spack-stack-1.4.0/envs/ue-apple-clang-13.1.6/install/modulefiles/apple-clang/13.1.6/sfcio/1.4.1.lua

####  Auto-generated modules structure (MPI dependency)

/path/to/spack-stack/spack-stack-x.y.z/envs/ue-compiler-name-compiler-version/install/modulefiles/mpi-name/mpi-version/compiler-name/compiler-version/package-name/package-version[.lua]

_Example_
/Users/heinzell/prod/spack-stack-1.4.0/envs/ue-apple-clang-13.1.6/install/modulefiles/openmpi/4.1.5/apple-clang/13.1.6/hdf5/1.14.0.lua

#### Important points to remember 

1. For readability reasons, we do not append hashes to auto-generated modulenames
   (what is the difference between `hdf5/1.14.0-a736dsk` and `hdf5/1.14.0-1pz83nx` ???)
2. Duplicate module names are errors
2. "Convenience" modules (e.g. `module load ufs-weather-model-env`) are built for one
   specific version of each package at the time the spack-stack environment is installed first

#### Impact

Within the same environment, there can be no more than one version of a library
iff (=if and only if) it has downstream dependencies and not all of them get
updated to newer versions at the same time.

_Example_
`hdf5@1.14.0 + netcdf-c@4.6.0` does not work with `hdf5@1.14.1-2 + netcdf-c@4.6.0` because auto-generated module name for netcdf is `netcdf/4.6.0`

_Sole exception_
`esmf@8.4.2 + mapl@2.35.2` works with `esmf@8.5.0 + mapl@2.35.2` because auto-generated module name for mapl is `mapl/2.35.2-esmf-8.5.0`

#### Also to consider
Our spack environments are large and complex. Adding more and more packages to the same environment between releases increases the risk of spack concretization errors (rebuilding existing libraries against new dependencies, unintended updates to existing libraries, duplicate packages, …)

Spack-stack unified environments serve multiple applications at the same time: `ufs-weather-model`, `ufs-srw-app`, `skylab` (`jedi-fv3`, `soca`, `ewok`), `jedi-mpas`, `jedi-neptune`, `jedi-um`, `jedi-ufs`, etc. - for each of these, developers may potentially request several package installations “between releases”.

### Handling library updates for applications
We need to consider two types of installations: test installations and official updates

#### Test installations
Test installations can be requested as part of issues (which should be mandatory for pull requests anyway). These can be more frequent than official updates.
Issues can be in the application (e.g. `ufs-weather-model` repo) or in spack-stack, clearly describing the need and with a reasonable timeline.

Test installations are limited to one platform at a time (depending on the developer’s needs). The installers for that platform (see table in https://spack-stack.readthedocs.io/en/1.4.1/PreConfiguredSites.html) are responsible for installing it.

Test installations are made outside the official spack-stack release environment using chained environments (if possible, otherwise completely new install trees), never in the official environments. This currently requires the developer to add an additional module use statement, as in the example below. The spack-stack developers are working on a solution to make the upstream modules available to the chained environment to make life easier for the users.

```
module use /path/to/separate/spack-stack-1.4.1-testing/envs/fms-2023.02-chained/install/modulefiles/openmpi/4.1.6/gcc/11.3.1
module load fms/2023.02
```
The advantage is that it is obvious to the developer, the reviewers and the code managers that a library update in a PR is not officially rolled out everywhere yet. Further, there is no risk to corrupt official spack-stack installations with frequent test installs. 

#### Official updates / patch releases
Official updates should be limited in frequency and are only allowed after full acceptance testing (see test installations above).

Updates that will generate module duplicates require a completely new spack-stack installation. Making these kinds of updates between releases should be the absolute exception when it is really urgent (critical bugs or security issues). We roll out a new spack-stack release every three months anyway!

Official updates need to be made consistently across all platforms. There shall never be a situation when an official spack-stack installation on one platform differs from the others in their packages, package configurations, etc. (unless required by and encoded in spack-stack itself).

Since official updates require coordination across all platforms, the timeline for these installs must be more generous than for test installs.

## Lifetime of spack-stack installations
Regular, full releases of spack-stack are made every three months around the end of February, May, August, and November.

spack-stack developers are committed to maintaining a rolling stock of the last four releases, i.e. one year's worth of spack-stack releases. Under special circumstances (e.g. operational implementations that require long-term support, long-running official retrospectives), selected releases may be kept longer. Maintenance in this context refers to addressing bugs or recompiling in the event of an intrusive update to the system. Adding new functionality or new packages is in general limited to the current and future releases. Modifications to past releases that do not impact existing installations, such as the addition of chained environments/custom Spack repositories, or new templates or site configurations, may be considered on a case-by-case basis."

Developers in need of a long-term installation for their personal experiments are required to install spack-stack themselves - the spack-stack developers are available for support during the original installation. spack-stack developers cannot assist with updating old spack-stack installations from individuals in case they stop working (e.g. due to HPC OS/compiler updates).
