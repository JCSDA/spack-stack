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

- NOAA Environmental Modeling Center (EMC)
- The UCAR Joint Center for Satellite Data Assimilation (JCSDA)
- The Earth Prediction Innovation Center (EPIC)

Each stakeholder will designate a small number of developers to assist
in spack-stack development by becoming a code manager of the
spack-stack repo.

### Code Managers

Organization | Code Manager(s)
-------------|----------------
NOAA EMC | Kyle Gerheiser, Hang Lei, Ed Hartnett
JCSDA | Dom Heinzeller

## Project Process

The spack-stack project will follow the proeesses outlined in this
document to allow all stakeholders to get the benefits they need from
spack-stack.

### Requesting a New Package

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
execution, package files can be temporarily housed in the spack-stack
repo, but all should be moved to the main spack repo as time permits.

### Installing on HPC Systems

The spack-stack stack must be installed on various NOAA and NCAR
systems. Each stakeholder will designiate programmers to install on
their own systems.

### Releases

Any stakeholder can perform a release at any time.

The release process:
* Add a new issue explaining the reason for the release, and to notify all other stakeholders.
* Designate any issues that must be fixed before release, and ensure their completion.
* Update the GitHub Release Notes.
* Perform the release on GitHub.
* Update the documentation.

### Tags

Sometimes tags are preferrable to releases. Tags can be added at any time. Tag process:
* Add a new issue documenting the reason for the tag.
* Tag the repo.

### Documentation

spack-stack is documented with its README.md and on readthedocs.

### Reporting Problems

All problems are reported as issues on the spack-stack GitHub site.

### Fixing Problems

Problems in stack-spack will be fixed by the code managers.

Problems in spack package files will be solved by programmers of the
organization which uses the package. Many packages are shared, in
which case the work will be shared by the code managers.

