# How to Build **spack-stack** at NAS

This guide documents how to build **spack-stack** on NASA NAS systems, where login nodes have internet access but are CPU-restricted, while compute nodes allow parallel builds but have *no* internet access. Several packages (Rust/Cargo, ecFlow, CRTM) require special handling due to these constraints.

---

## Table of Contents

- [Overview](#overview)
- [Machines Required](#machines-required)
- [Clone spack-stack](#clone-spack-stack)
- [Obtain an Interactive Compute Node](#obtain-an-interactive-compute-node)
- [Setup spack-stack](#setup-spack-stack)
- [Create Environments](#create-environments)
  - [oneAPI Environment](#oneapi-environment)
  - [GCC Environment](#gcc-environment)
- [Activate the Environment](#activate-the-environment)
- [Concretize the Environment](#concretize-the-environment)
- [Create Source Cache (LOGIN NODE ONLY)](#create-source-cache-login-node-only)
- [Pre-Fetch Cargo Dependencies (LOGIN NODE ONLY)](#pre-fetch-cargo-dependencies-login-node-only)
- [Install Packages](#install-packages)
  - [Step 1 — Dependencies of Rust codes and ecFlow (COMPUTE NODE)](#step-1--dependencies-of-rust-codes-and-ecflow-compute-node)
  - [Step 2 — Rust codes and ecFlow (AFE LOGIN NODE)](#step-2--rust-codes-and-ecflow-afe-login-node)
  - [Step 3 — Remaining Packages (COMPUTE NODE)](#step-3--remaining-packages-compute-node)
  - [Packages Requiring Internet](#packages-requiring-internet)
- [Update Module Files](#update-module-files)
- [Deactivate the Environment](#deactivate-the-environment)
- [Debugging Package Builds](#debugging-package-builds)

---

## Overview

Due to NAS system architecture and network restrictions:

- **Login nodes**:  
  - Have internet  
  - Limited to **2 processes**  
  - `pfe` nodes use **Sandy Bridge** (too old for x86_64_v3 builds)

- **Compute nodes** (Milan / Rome):  
  - No internet  
  - Allow parallel builds  

Some packages (Cargo/Rust, ecFlow, CRTM) require internet or newer CPU features, so the install is broken into multiple steps across different node types.

---

## Machines Required

You will need:

- **An `afe01` login node**  
  Supports x86_64_v3 binaries → required for building Rust packages and ecFlow.

- **A Rome or Milan compute node**  
  Used for the main installation with multiple cores.

---

## Clone spack-stack

Use the appropriate branch or tag:

```bash
git clone --recurse-submodules https://github.com/JCSDA/spack-stack.git \
    -b spack-stack-2.0.0 spack-stack-2.0.0
```

---

## Obtain an Interactive Compute Node

NAS login nodes allow only **2 processes**, so use:

```bash
qsub -I -V -X \
    -l select=1:ncpus=128:mpiprocs=128:model=rom_ait \
    -l walltime=12:00:00 \
    -W group_list=s1873 \
    -m b \
    -N Interactive
```

This gives a **Rome** compute node for up to 12 hours. 

For a **Milan** node, change `model=rom_ait` to `model=mil_ait` and run the `qsub` command on a Milan-capable login node (e.g., `afe02`).

---

## Setup spack-stack

Run on a **login node with internet**:

```bash
cd spack-stack-2.0.0
. setup.sh
```

---

## Create Environments

You only need to create each environment once.

### oneAPI Environment

```bash
spack stack create env --name ue-oneapi-2024.2.0 \
    --template unified-dev --site nas --compiler=oneapi-2024.2.0
cd envs/ue-oneapi-2024.2.0
```

### GCC Environment

```bash
spack stack create env --name ue-gcc-13.2.0 \
    --template unified-dev --site nas --compiler=gcc-13.2.0
cd envs/ue-gcc-13.2.0
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
spack mirror create -a \
    -d /swbuild/gmao_SIteam/spack-stack/source-cache
```

> ⚠️ **Do not run this outside an activated environment.**  
> Otherwise Spack will attempt to mirror **every** known package/version.

---

## Pre-Fetch Cargo Dependencies (LOGIN NODE ONLY)

Rust packages frequently require network access during build. Pre-fetch their dependencies:

```bash
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
../../util/fetch_cargo_deps.py
```

> ⚠️ **You must also set `CARGO_HOME` on compute nodes** before building.

---

## Install Packages

Installation requires three stages:

| Step | Node Type | Why |
|------|-----------|-----|
| Step 1 | Compute | Build dependencies in parallel, avoids CPU limits |
| Step 2 | `afe` login | Needed for x86_64_v3 Python and internet access |
| Step 3 | Compute | Finish main installation at high parallelism |

---

### Step 1 — Dependencies of Rust codes and ecFlow (COMPUTE NODE)

```bash
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
spack install -j 16 --verbose --fail-fast --show-log-on-error \
    --no-check-signature \
    --only dependencies py-cryptography py-maturin py-rpds-py ecflow \
    2>&1 | tee log.install.deps-for-rust-and-ecflow ; bell
```

---

### Step 2 — Rust codes and ecFlow (AFE LOGIN NODE)

`pfe` nodes use Sandy Bridge CPUs, which **cannot run** spack-stack’s x86_64_v3 Python interpreter → results in `Illegal instruction`.

So this must be done on **afe**:

```bash
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
spack install -j 2 -p 1 --verbose --fail-fast --show-log-on-error \
    --no-check-signature \
    py-cryptography py-maturin py-rpds-py ecflow \
    2>&1 | tee log.install.rust-and-ecflow ; bell
```

NAS limits login nodes to 2 processes, hence `-j 2`.

---

### Step 3 — Remaining Packages (COMPUTE NODE)

```bash
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
spack install -j 16 --verbose --fail-fast --show-log-on-error \
    --no-check-signature \
    2>&1 | tee log.install.after-cargo ; bell
```

> **Note:** You may need to re-run this command multiple times. Some builds fail intermittently but succeed on retry.

---

### Packages Requiring Internet (AFE LOGIN NODE)

If you encounter another package that insists on network access:

```bash
spack install -j 2 --verbose --fail-fast --show-log-on-error \
    --no-check-signature <package> \
    |& tee log.install.<package> ; bell
```

Again, this must be done on an **afe** login node because of the CPU architecture.

Once built, return to the compute node and resume the full installation.

---

## Update Module Files (AFE LOGIN NODE)

After installation completes, on an **afe** login node run:

```bash
spack module tcl refresh -y --delete-tree ; bell
spack stack setup-meta-modules
```

Apparently, spack modulefile generation might use code that spack built for `x86_64_v3`.

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


