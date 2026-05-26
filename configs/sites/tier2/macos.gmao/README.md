Default macOS for GMAO

---

## Table of Contents

- [Overview](#overview)
- [Brew Packages Required](#brew-packages-required)
- [Clone spack-stack](#clone-spack-stack)
- [Setup spack-stack](#setup-spack-stack)
- [Using batch\_install.sh script](#using-batch_installsh-script)
  - [First run](#first-run)
  - [Subsequent builds](#subsequent-builds)
  - [Installing from build caches](#installing-from-build-caches)
  - [Loading the stack](#loading-the-stack)
- [Building the stack by hand](#building-the-stack-by-hand)
  - [Create Environments](#create-environments)
  - [Activate the Environment](#activate-the-environment)
  - [Concretize the Environment](#concretize-the-environment)
  - [Create Source Cache](#create-source-cache)
  - [Pre-Fetch Cargo Dependencies](#pre-fetch-cargo-dependencies)
  - [Install Packages](#install-packages)
  - [Update Module Files](#update-module-files)
  - [Deactivate the Environment](#deactivate-the-environment)
- [Debugging Package Builds](#debugging-package-builds)

---

## Overview

This configuration provides a generalized Spack Stack setup for GMAO users on macOS using Homebrew. It serves as a generic Tier 2 site `macos.gmao` that dynamically detects your Homebrew installation prefix.

---

## Brew Packages Required

You must have `brew` installed and the following packages available. (Note: compilers like NAG or Intel are installed out-of-band and configured separately).

```bash
brew install coreutils
brew install gcc@15
brew install flang
brew install git
brew install lmod
brew install wget
brew install bash
brew install tcsh
brew install cmake
brew install openssl
brew install rust
```

---

## Clone spack-stack

Use the appropriate branch or tag:

### Fixed Tag - JCSDA

```bash
git clone --recurse-submodules https://github.com/JCSDA/spack-stack.git -b x.y.z spack-stack-x.y.z
```

### Development - JCSDA

```bash
git clone --recurse-submodules https://github.com/JCSDA/spack-stack.git -b develop spack-stack-dev
```

### Development - SI Team

```bash
git clone --recurse-submodules https://github.com/GMAO-SI-Team/spack-stack.git -b develop spack-stack-siteam
```

---

## Setup spack-stack

Activate the base spack-stack environment:

```bash
cd spack-stack-dev
. ./setup.sh
```

---

## Using batch_install.sh script

The `batch_install.sh` script automates the creation of environments (e.g., `gcc` and `clang` builds), populating your Spack bootstrap caches, and running the Spack installation pipeline.

### Usage help

```bash
./util/gmao/batch_install.sh -h
```

### Compiler Selection and Auto-Detection

By default, `batch_install.sh` builds the `gcc@=15.2.0` stack. 

The script will automatically detect your currently active version of Apple Clang (e.g. `apple-clang@21.0.0`) and substitute it into the templates. If the NAG Fortran compiler (`nagfor`) is found in your `PATH`, the script will automatically detect its version as well and add it to the build queue (e.g., `nag@=7.2.7243`). 

If your NAG compiler is installed in a non-standard location and not in your `PATH`, you can explicitly provide its path using the `-N` flag:

```bash
./util/gmao/batch_install.sh -N /path/to/your/nag/bin/nagfor -r dev -m build -H macos.gmao -e
```

If you want to explicitly override the compilers built by the script entirely, use the `-C` flag with a comma-separated list of Spack compiler specs:

```bash
./util/gmao/batch_install.sh -C "gcc@=15.2.0,nag@=7.2.7243" -r dev -m build -H macos.gmao -e
```

*Note: For every compiler you specify, you must have a corresponding `packages_<compiler_name>-<version>.yaml.template` file in this site directory.*

### First run (Building Bootstrap and Source Caches)

When you first run the script on a new machine, you need to use the `-u` option. This tells Spack to build the bootstrap mirror and source caches locally before attempting to register them.

```bash
./util/gmao/batch_install.sh -r dev -m build -H macos.gmao -u -e
```

- `-r dev -m build`: Sets the developer mode and tells Spack to build the environments.
- `-H macos.gmao`: Overrides hostname detection. This is required to force the script to use this specific generic macOS site, avoiding issues where VPNs or routers mask the real hostname.
- `-u`: Updates and populates the bootstrap/source caches.
- `-e`: Allows continuing builds in existing environments (prevents the script from failing if the environment directories were just created).

### Subsequent builds

Once the initial caches are set up, you can run builds without the `-u` flag:

```bash
./util/gmao/batch_install.sh -r dev -m build -H macos.gmao -e
```

### Installing from build caches

If you are just installing environments using already populated build caches (the typical workflow for users after the initial maintainer setup), use `-m install`:

```bash
./util/gmao/batch_install.sh -r dev -m install -H macos.gmao -e
```

### Generating `.yaml.generated` files
`batch_install.sh` uses `.yaml.template` files in the `macos.gmao` site directory to dynamically detect the path to your Brew installation, your active `apple-clang` version, and your NAG compiler, creating `.yaml.generated` files on the fly. 
To prevent cluttering the site configuration directory, the script writes these generated files directly to `configs/sites/tier2/macos.gmao/`, injects them directly into the target environment's `site/` directory during creation, and then automatically cleans up the temporary files from the configurations directory.

### Loading the stack

Once the installation and module generation are complete, you can point your shell to the newly built modules. OpenMPI is built specifically with `~two_level_namespace` to support flat namespace linking required by GEOS. 

To ensure executables (like MAPL tests) running under macOS System Integrity Protection (SIP) can properly resolve runtime paths (RPATHs) when using compilers like NAG, the `macos.gmao` site-level `modules.yaml` configuration explicitly permits exporting `DYLD_LIBRARY_PATH` and `DYLD_FALLBACK_LIBRARY_PATH` variables into your environment when loading modules.

Depending on which compiler you built, you will need to add the correct `install/modulefiles/Core` directory to your `module use` path.

#### Loading the GCC Stack

```bash
module use -a /path/to/spack-stack/envs/ge-gcc-15.2.0-build/install/modulefiles/Core
module load stack-gcc stack-openmpi geos-gcm-env
```

#### Loading the NAG Stack

```bash
module use -a /path/to/spack-stack/envs/ge-nag-7.2.7243-build/install/modulefiles/Core
module load stack-nag stack-openmpi geos-gcm-env
```

---

## Building the stack by hand

If you prefer to run the Spack commands manually instead of using `batch_install.sh`, you can still follow these steps. However, it's highly recommended to use `batch_install.sh` because it automatically handles dynamic template substitution (e.g., for Homebrew paths, `apple-clang` versions, and NAG compiler versions) that you will otherwise need to do manually with `sed`.

If you choose to do this manually, you must first run `sed` over the `*.yaml.template` files and create the `.yaml.generated` files. 

### Create Environments

You only need to create each environment once. Our `macos.gmao` site configurations use `.yaml.template` files which are dynamically processed into `.yaml.generated` files.

#### GCC Environment

```bash
spack stack create env --name ge-gcc-15.2.0 --template geos-dev --site macos.gmao --compiler=gcc-15.2.0
```

#### NAG Environment

```bash
spack stack create env --name genag-nag-7.2.7243 --template geos-dev-nag --site macos.gmao --compiler=nag-7.2.7243
```

---

### Activate the Environment

Navigate to the environment directory you wish to work on. For example, if you built the GCC stack:

```bash
cd envs/ge-gcc-15.2.0-build
spack env activate -p .
```

> **Note:** If you are building or debugging a different compiler stack, be sure to `cd` into that specific environment directory instead (e.g., `envs/ge-nag-7.2.7243-build` or `envs/ge-clang-22.1.3-build`).

> **Important:** Run this in *every* terminal where you plan to run Spack commands for this environment.

---

### Concretize the Environment

```bash
spack concretize 2>&1 | tee log.concretize ; bell
```

*(Optional `bell` helper: `bell() { tput bel ; printf "\nFinished at: " ; date; }`)*

---

### Create Source Cache

This downloads all source tarballs for your concretized environment to prevent network timeouts during the build:

```bash
spack mirror create -a -d $HOME/spack-stack-mirrors/spack-source-mirror
```

> ⚠️ **Do not run this outside an activated environment.**
> Otherwise, Spack will attempt to mirror **every** known package and version in the registry.

---

### Pre-Fetch Cargo Dependencies

Rust packages frequently require network access during the build. Pre-fetch their dependencies to the cargo mirror:

```bash
export CARGO_HOME=$HOME/spack-stack-mirrors/spack-cargo-mirror
../../util/fetch_cargo_deps.py
```

> ⚠️ **Set `CARGO_HOME` in your environment before running `spack install`.**

---

### Install Packages

```bash
export CARGO_HOME=$HOME/spack-stack-mirrors/spack-cargo-mirror
spack install -j 6 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install ; bell
```

> **Note:** You may need to re-run this command if a package fails due to an intermittent network issue or parallel build race condition.

---

### Update Module Files

After installation completes, regenerate the Lmod module tree and meta-modules:

```bash
spack module lmod refresh -y --delete-tree ; bell
spack stack setup-meta-modules
```

---

### Deactivate the Environment

```bash
spack env deactivate
```

---

## Debugging Package Builds

If a specific package fails to build, you can drop into Spack's build environment to debug it manually:

```bash
spack clean <package>
spack stage <package>
cd $(spack location -s <package>)
spack build-env <package> -- bash --norc --noprofile
```

This drops you into a clean bash shell with the exact environment variables, compiler wrappers, and dependencies loaded that Spack uses during the build.

