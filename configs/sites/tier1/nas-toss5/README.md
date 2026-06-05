# How to Build **spack-stack** at NAS on TOSS5

This guide documents how to build **spack-stack** on NASA NAS TOSS5 systems. The previous install process used three stages across compute and login nodes, but recent testing shows installation can now be done directly on a compute node.

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

NAS login nodes and compute nodes have different constraints:

- **Login nodes**:
  - Have internet access
  - Limited to **2 processes**

- **Compute nodes** (Turin):
  - No internet access
  - Allow parallel builds

Use login nodes for setup steps that require internet access (e.g., concretization, mirroring sources, pre-fetching Cargo dependencies), then run installation on a compute node.

The install step itself is now a single compute-node command.

---

## Machines Required

You will need:

- **A login node**
  Used for setup steps that require internet access.

- **A Turin compute node**
  Used for package installation with higher parallelism.

---

## Clone spack-stack

Use the appropriate branch or tag:

```bash
git clone --recurse-submodules https://github.com/JCSDA/spack-stack.git -b spack-stack-2.1.0 spack-stack-2.1.0
```

---

## Obtain an Interactive Compute Node

NAS login nodes allow only **2 processes**, so use:

```bash
qsub -I -V -X -l select=1:ncpus=128:mpiprocs=128:model=tur_ath -l walltime=12:00:00 -W group_list=s1873 -m b -N Interactive
```

This gives a **Turin** compute node for up to 12 hours.

---

## Setup spack-stack

Run on a **login node with internet**:

```bash
cd spack-stack-2.1.0
. setup.sh
```

---

## Create Environments

You only need to create each environment once.

### oneAPI - ifx Environment

```bash
spack stack create env --name ue-oneapi-2025.3.0 --template unified-dev --site nas-toss5 --compiler=oneapi-2025.3.0
cd envs/ue-oneapi-2025.3.0
```

### oneAPI - ifort Environment

```bash
spack stack create env --name ue-oneapi-2024.2.0 --template unified-dev --site nas-toss5 --compiler=oneapi-2024.2.0
cd envs/ue-oneapi-2024.2.0
```

### GCC Environment

```bash
spack stack create env --name ue-gcc-14.2.1 --template unified-dev --site nas-toss5 --compiler=gcc-14.2.1
cd envs/ue-gcc-14.2.1
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

## Create Source Cache (LOGIN NODE ONLY)

This downloads all source tarballs for your environment:

```bash
spack mirror create -a -d /swbuild/gmao_SIteam/spack-stack/source-cache
```

> ⚠️ **Do not run this outside an activated environment.**
> Otherwise Spack will attempt to mirror **every** known package/version.

---

## Pre-Fetch Cargo Dependencies (LOGIN NODE ONLY)

Rust packages frequently require network access during build. Pre-fetch their dependencies:

```bash
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-mirror
../../util/fetch_cargo_deps.py
```

> ⚠️ **Set `CARGO_HOME` on compute nodes** before running `spack install`.

---

## Install Packages (COMPUTE NODE)

Run installation on a **compute node**:

```bash
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-mirror
spack install -j 16 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install ; bell
```

This replaces the former compute → login → compute install sequence.

> **Note:** You may need to re-run this command multiple times. Some builds fail intermittently but succeed on retry.

---

## Update Module Files

After installation completes, run:

```bash
spack module tcl refresh -y --delete-tree ; bell
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

---

## Deprecated: Legacy Three-Step Install

> ⚠️ **Deprecated:** Keep this only as historical reference. Prefer the single compute-node install above.

Older workflows used three stages:

1. Compute node: build dependencies for Rust-related Python packages and ecFlow.
2. `athfe` login node: build `py-cryptography`, `py-maturin`, `py-rpds-py`, and `ecflow` with `-j 2`.
3. Compute node: run full `spack install` to finish remaining packages.

Typical commands were:

```bash
# Step 1 (compute node)
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-mirror
spack install -j 16 --verbose --fail-fast --show-log-on-error --no-check-signature \
  --only dependencies py-cryptography py-maturin py-rpds-py ecflow 2>&1 | tee log.install.deps-for-rust-and-ecflow ; bell

# Step 2 (athfe login node)
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-mirror
spack install -j 2 -p 1 --verbose --fail-fast --show-log-on-error --no-check-signature \
  py-cryptography py-maturin py-rpds-py ecflow 2>&1 | tee log.install.rust-and-ecflow ; bell

# Step 3 (compute node)
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-mirror
spack install -j 16 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install.after-cargo ; bell
```

---
