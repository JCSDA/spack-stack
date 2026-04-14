Alderaan is one of @mathomp4's development systems (Mac Studio)

---

## Table of Contents

- [Overview](#overview)
- [Machines Required](#machines-required)
- [Clone spack-stack](#clone-spack-stack)
- [Obtain an Interactive Compute Node](#obtain-an-interactive-compute-node)
- [Setup spack-stack](#setup-spack-stack)
- [Create Environments](#create-environments)
  - [oneAPI - ifx Environment](#oneapi---ifx-environment)
  - [oneAPI - ifort Environment](#oneapi---ifort-environment)
  - [GCC Environment](#gcc-environment)
- [Activate the Environment](#activate-the-environment)
- [Concretize the Environment](#concretize-the-environment)
- [Create Source Cache (LOGIN NODE ONLY)](#create-source-cache-login-node-only)
- [Pre-Fetch Cargo Dependencies (LOGIN NODE ONLY)](#pre-fetch-cargo-dependencies-login-node-only)
- [Install Packages (COMPUTE NODE)](#install-packages-compute-node)
- [Update Module Files](#update-module-files)
- [Deactivate the Environment](#deactivate-the-environment)
- [Debugging Package Builds](#debugging-package-builds)
- [Deprecated: Legacy Three-Step Install](#deprecated-legacy-three-step-install)

---

## Overview

---

## Brew Packages Required

You must have `brew` installed and the following packages available:

```
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

```bash
git clone --recurse-submodules https://github.com/GMAO-SI-Team/spack-stack.git -b geos-testing spack-stack-dev
```

---

## Setup spack-stack

```bash
cd spack-stack-dev
. ./setup.sh
```

---

## Create Environments

You only need to create each environment once.

### GCC Environment

```bash
spack stack create env --name ge-gcc-15.2.0 --template geos-dev --site alderaan --compiler=gcc-15.2.0
cd envs/ge-gcc-15.2.0
```

### Flang Environment

```bash
spack stack create env --name ge-clang-22.1.3 --template geos-dev --site alderaan --compiler=clang-22.1.3
cd envs/ge-clang-22.1.3
```

---

## Activate the Environment

```bash
spack env activate .
```

> **Important:** Run this in *every* terminal where you plan to run Spack commands.

---

## Concretize the Environment

Run on a **login node** (internet required for bootstrapping Clingo and other tools):

```bash
spack concretize 2>&1 | tee log.concretize ; bell
```

### Optional `bell` helper

```bash
bell() { tput bel ; printf "\nFinished at: " ; date; }
```

---

## Create Source Cache

This downloads all source tarballs for your environment:

```bash
spack mirror create -a -d /Users/mathomp4/prod/spack-source-mirror
```

> ⚠️ **Do not run this outside an activated environment.**
> Otherwise Spack will attempt to mirror **every** known package/version.

---

## Pre-Fetch Cargo Dependencies (LOGIN NODE ONLY)

Rust packages frequently require network access during build. Pre-fetch their dependencies:

```bash
export CARGO_HOME=/Users/mathomp4/prod/spack-cargo-mirror
../../util/fetch_cargo_deps.py
```

> ⚠️ **Set `CARGO_HOME` before running `spack install`.**

---

## Install Packages

```bash
export CARGO_HOME=/Users/mathomp4/prod/spack-cargo-mirror
spack install -j 6 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install ; bell
```

> **Note:** You may need to re-run this command multiple times. Some builds fail intermittently but succeed on retry.

---

## Update Module Files

After installation completes, run:

```bash
spack module lmod refresh -y --delete-tree ; bell
spack stack setup-meta-modules
```

---

## Deactivate the Environment

```bash
spack env deactivate
```

---

## Debugging Package Builds

```bash
spack clean
spack stage <package>
spack build-env <package> -- bash --norc --noprofile
```

This drops you into a clean build environment with the package’s full compiler/runtime environment loaded.

