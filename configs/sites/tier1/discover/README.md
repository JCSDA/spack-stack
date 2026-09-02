Discover (Tier 1 / GMAO SI Team)

---

## Table of Contents

- [Overview](#overview)
- [Clone spack-stack](#clone-spack-stack)
- [Setup spack-stack](#setup-spack-stack)
- [Using batch\_install.sh script](#using-batch_installsh-script)
  - [Help and dry-run](#help-and-dry-run)
  - [Roles and modes](#roles-and-modes)
  - [The -H flag](#the--h-flag)
  - [The -e flag](#the--e-flag)
  - [The -L / --disable-locks flag](#the--l---disable-locks-flag)
  - [The -s flag](#the--s-flag)
  - [The -a flag](#the--a-flag)
  - [The -p, -q, and --constraint flags](#the--p--q-and---constraint-flags)
  - [Typical workflow](#typical-workflow)
  - [Environment names](#environment-names)
  - [Loading the stack](#loading-the-stack)
- [Adding or Updating a Single Package](#adding-or-updating-a-single-package)
  - [Scenario A: Add an additional version](#scenario-a-add-an-additional-version)
  - [Scenario B: Replace an existing version](#scenario-b-replace-an-existing-version)
  - [Pushing to the build cache after manual changes](#pushing-to-the-build-cache-after-manual-changes)
- [Updating a Package Build Recipe](#updating-a-package-build-recipe)
- [Additional Options Reference](#additional-options-reference)
- [Debugging Package Builds](#debugging-package-builds)

---

## Overview

This configuration provides the Spack Stack setup for the Tier 1 GMAO SI Team installation on the NASA Discover supercomputer. It is maintained under the GMAO SI Team `/discover/nobackup/projects/gmao/SIteam/` space.

The site builds the `unified-dev` environment template with the following compilers:

- `gcc@=14.2.0`
- `gcc@=15.2.0`
- `oneapi@=2024.2.0`
- `oneapi@=2025.3.0`

Module files are managed with `lmod`. Shared caches are located under `/discover/nobackup/projects/gmao/SIteam/spack-stack/`.

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

Activate the base spack-stack environment from the root of the repository:

```bash
cd spack-stack-siteam
. ./setup.sh
```

> **Important:** You must run `. ./setup.sh` before running interactive Spack commands. The `batch_install.sh` script sources `setup.sh` internally, so this step is not required before calling it.

---

## Using batch_install.sh script

The `batch_install.sh` script automates environment creation, cache population, and the Spack installation pipeline. It is the recommended way to build or install the full stack on Discover.

### Help and dry-run

```bash
./util/gmao/batch_install.sh -h
```

Before running a full build, use the `-n` (dry-run) flag to preview exactly what the script would execute without making any changes:

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover -s -n
```

---

### Roles and modes

The script requires two key flags on every invocation:

- **`-r ROLE`** — either `dev` or `ops`
- **`-m MODE`** — either `build` or `install`

| Role + Mode | What it does |
|---|---|
| `-r dev -m build` | For SI Team developers with write access to the shared mirrors. Builds packages from source and writes results to the **default shared build cache**. |
| `-r dev -m install` | Installs packages from the shared build cache (no compilation) and generates module files. |
| `-r ops -m build` | For operational partners **without** write access to the shared mirrors. Builds packages and writes to a **custom build cache** specified with `-c BUILDCACHE_DIR`. Allows partners to maintain their own binary cache independently. |
| `-r ops -m install` | Installs packages from the shared build cache and generates module files. |

The `-m install` step is **required** to generate usable `lmod` module files. A `-m build` run alone does not produce modules.

---

### The -H flag

Always pass `-H discover` explicitly on Discover:

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover -s
```

Without `-H`, the script autodetects the hostname by stripping digits and the domain suffix from `$HOSTNAME`. On a node like `discover23`, this produces `discover` correctly — but if you are logged into a node whose name does not strip cleanly (or if you are on a `discover-gmao`-type node), explicit `-H` avoids any ambiguity.

---

### The -e flag

The `-e` flag tells the script to continue even if the environment directories already exist. Without it, the script exits with an error if any target environment directory is present.

- On the **very first run**, you do not need `-e` (the directories do not exist yet).
- On **every subsequent run** (rebuilds, retries, installs), you must pass `-e`.

---

### The -L / --disable-locks flag

The `-L` / `--disable-locks` flag creates a job-local Spack user configuration containing `config:locks:false`, so Spack's package workers inherit the setting without changing the environment YAML. It also sets `--concurrent-packages=1`. Per-package build parallelism is unchanged. Use it only to work around a filesystem lock failure such as `OSError: [Errno 37] No locks available`, and only when this is the sole process modifying the environment's install tree.

For example, an exclusive SLURM job retry for the oneAPI 2024.2.0 build can use:

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover -s \
  -C oneapi@=2024.2.0 -e -L
```

Do not use `-L` for normal shared-stack builds or when another Spack process might install, uninstall, or otherwise modify the same environment. Locks remain enabled by default.

---

### The -s flag

The `-s` flag submits the `spack install` step to the SLURM scheduler via `sbatch` rather than running it directly in your current shell. This is strongly recommended for full stack builds on Discover:

- Allocates a single node with 120 tasks
- Limits each Spack package build to 24 jobs; the full-node allocation provides isolation rather than maximum build parallelism
- Does not use `$TSE_TMPDIR`: its inode quota is insufficient for large packages such as Rust; build stages remain in the site-configured project-space cache
- Targets Milan nodes (`--constraint=mil`) by default
- Walltime: 8 hours
- Output is redirected to `spack.<hostname>.<env_name>.log` in the current directory

If the default account (`s1873`) is active, the job defaults to `--partition=preops --qos=benchmark`. Use `-p`, `-q`, and `--constraint` to override these. See `-a`, `-p`, `-q`, and `--constraint` below.

---

### The -a flag

Override the SLURM account (default: `s1873`):

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover -s -a <YOUR_ACCOUNT>
```

When the account is `s1873`, the job defaults to `--partition=preops --qos=benchmark`. For any other account, no partition or QOS flags are set by default. Use `-p` and `-q` to override.

---

### The -p, -q, and --constraint flags

Override the SLURM partition, QOS, and node constraint independently:

```bash
# Use a different partition
./util/gmao/batch_install.sh -r dev -m build -H discover -s -p compute

# Use a different QOS
./util/gmao/batch_install.sh -r dev -m build -H discover -s -q high

# Override the node constraint (default: mil for Milan nodes)
./util/gmao/batch_install.sh -r dev -m build -H discover -s --constraint=cas

# Override all three
./util/gmao/batch_install.sh -r dev -m build -H discover -s -p compute -q normal --constraint=sky
```

`-p` and `-q` also accept long-option forms (`--partition=`, `--qos=`). `--constraint` has no short form because `-c` and `-C` are already in use.

These flags override the site defaults regardless of the account. Useful when working under a non-`s1873` account that still has access to specific partitions, QOS levels, or node types.

---

### Typical workflow

The normal progression from a fresh clone to a fully installed, module-ready stack is three steps:

#### Step 1 — First run: build and populate caches

On the very first run, use `-u` to populate the bootstrap, source, and cargo mirrors. This requires `-r dev -m build`.

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover -s -u
```

- `-u`: Builds and populates the bootstrap mirror, source cache, and cargo mirror under `/discover/nobackup/projects/gmao/SIteam/spack-stack/`. Only needed once (or when the caches need to be refreshed).
- `-s`: Submits the install step to SLURM.
- No `-e` needed since the environment directories do not exist yet.

#### If one source fails while updating the cache

The `-u` source-cache update mirrors many packages concurrently. If one reachable Git source fails to mirror, fetch that concrete spec serially on the login node instead of sending an offline compute-node job without its source:

```bash
. ./setup.sh
spack -e envs/<build-environment> mirror create \
  -d /discover/nobackup/projects/gmao/SIteam/spack-stack/source-cache \
  <spec>
```

For example, `<spec>` can be `ioda-data@2.12.0`. After the command succeeds, resume `batch_install.sh` without `-u`. If the direct fetch also fails, investigate repository access or the package's source metadata before retrying.

#### Step 2 — Rebuild or retry runs

After the first run, the environment directories exist and the caches are populated. Drop `-u` and add `-e`:

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover -s -e
```

Use this if a build failed and you need to retry, or if you are iterating on the build configuration. The `-e` flag is required because the environment directories were created in Step 1.

#### Step 3 — Install from cache and generate modules

Once the build cache is ready, run in install mode to install from the cache and generate `lmod` module files:

```bash
./util/gmao/batch_install.sh -r dev -m install -H discover -s -e
```

This step is **required** to produce usable modules. The `-m build` steps above do not generate module files.

---

### Environment names

The script creates one environment per compiler under `envs/` (relative to the repository root, unless overridden with `-d`):

| Mode | Environment names created |
|---|---|
| `build` | `ue-gcc-14.2.0-build`, `ue-gcc-15.2.0-build`, `ue-oneapi-2024.2.0-build`, `ue-oneapi-2025.3.0-build` |
| `install` | `ue-gcc-14.2.0`, `ue-gcc-15.2.0`, `ue-oneapi-2024.2.0`, `ue-oneapi-2025.3.0` |

The `ue-` prefix comes from the `unified-dev` template used by this site.

---

### Loading the stack

After the `install` step completes, point your shell to the generated module files:

```bash
module use -a /path/to/spack-stack-siteam/envs/ue-gcc-15.2.0/install/modulefiles/Core
module load stack-gcc stack-openmpi
```

Replace `ue-gcc-15.2.0` with the appropriate environment name for your compiler of choice.

---

## Adding or Updating a Single Package

If the full stack is already installed and you need to add or change a single package — for example, someone needs `nco@5.3.8` but `nco@5.3.9` was built — it is easier to work inside the environment directly rather than re-running the full `batch_install.sh` pipeline.

First, activate spack-stack (required for interactive Spack commands) and activate the relevant environment:

```bash
. ./setup.sh
cd envs/ue-gcc-15.2.0
spack env activate -p .
```

### Scenario A: Add an additional version

If you want both `nco@5.3.9` and `nco@5.3.8` to coexist as separate modules:

1. Edit `spack.yaml` in the environment directory and add the additional spec:

   ```yaml
   specs:
   - nco@5.3.9
   - nco@5.3.8   # add this line
   ```

2. Re-concretize the environment:

   ```bash
   spack concretize 2>&1 | tee log.concretize
   ```

3. Install only the new package:

   ```bash
   spack install nco@5.3.8 2>&1 | tee log.install.nco
   ```

4. Refresh module files:

   ```bash
   spack module lmod refresh -y --delete-tree
   spack stack setup-meta-modules
   ```

5. Deactivate when done:

   ```bash
   spack env deactivate
   ```

### Scenario B: Replace an existing version

If you want to replace `nco@5.3.9` with `nco@5.3.8` (removing the old version):

1. Edit `spack.yaml` to change the spec:

   ```yaml
   specs:
   - nco@5.3.8   # was nco@5.3.9
   ```

2. Re-concretize:

   ```bash
   spack concretize 2>&1 | tee log.concretize
   ```

3. Install the new version:

   ```bash
   spack install nco@5.3.8 2>&1 | tee log.install.nco
   ```

4. Uninstall the old version:

   ```bash
   spack uninstall nco@5.3.9
   ```

5. Refresh module files:

   ```bash
   spack module lmod refresh -y --delete-tree
   spack stack setup-meta-modules
   ```

6. Deactivate when done:

   ```bash
   spack env deactivate
   ```

### Pushing to the build cache after manual changes

If you want the manually installed package to be available in the shared build cache for others to install from, push it after installation:

```bash
spack buildcache push -u local-binary
spack buildcache update-index local-binary
```

> **Warning:** This writes to the default shared build cache at `/discover/nobackup/projects/gmao/SIteam/spack-stack/build-cache`. Only do this if you have write access and intend to publish the change.

---

## Updating a Package Build Recipe

If a package needs a new version or checksum update (e.g., a new upstream release of `nco` or `cdo`), you can update the recipe and install the new version by hand without running the full pipeline.

1. Update the Spack package recipe (e.g., in `var/spack/repos/` or the upstream Spack packages repo) to add the new version and checksum.

2. Activate spack-stack (required for interactive Spack commands):

   ```bash
   . ./setup.sh
   ```

3. Activate the relevant environment:

   ```bash
   cd envs/ue-gcc-15.2.0
   spack env activate -p .
   ```

4. If the version spec in `spack.yaml` needs to change, edit it now.

5. Re-concretize:

   ```bash
   spack concretize 2>&1 | tee log.concretize
   ```

6. Install the updated package (Spack will only build what has changed):

   ```bash
   spack install <package>@<new_version> 2>&1 | tee log.install.<package>
   ```

7. Refresh module files:

   ```bash
   spack module lmod refresh -y --delete-tree
   spack stack setup-meta-modules
   ```

8. Deactivate:

   ```bash
   spack env deactivate
   ```

---

## Additional Options Reference

The following flags are less commonly used. The descriptions below reflect our best current understanding; confirm with the SI Team if you need to use them.

| Flag | Description |
|---|---|
| `-c BUILDCACHE_DIR` | Use a custom build cache directory. Required with `-r ops -m build` for operational partners who do not have write access to the shared mirrors. |
| `-d ENV_DIRS` | Override the default environment directory (default: `envs/` in the repo root). |
| `-C COMPILERS` | Comma-separated list of compilers to build (e.g., `gcc@=15.2.0,oneapi@=2025.3.0`). Overrides the site defaults. |
| `-p` / `--partition` | Override the SLURM partition. Defaults to `preops` when account is `s1873`, otherwise unset. |
| `-q` / `--qos` | Override the SLURM QOS. Defaults to `benchmark` when account is `s1873`, otherwise unset. |
| `--constraint` | Override the SLURM node constraint. Defaults to `mil` (Milan nodes). No short form (`-c`/`-C` are taken). |
| `-t` | Run tests for specific third-party dependencies after installation. The list of packages to test is hardcoded in `batch_install.sh`. |
| `-u` | Populate bootstrap, source, and cargo mirrors. Requires `-r dev -m build`. Only needed on first run or when refreshing caches. |
| `-L` / `--disable-locks` | Disable Spack install locks and serialize package installs for an isolated recovery run only. Per-package build parallelism is unchanged. Requires assurance that no other process is modifying the same install tree. |

---

## Debugging Package Builds

If a specific package fails to build, drop into Spack's build environment to debug it manually:

```bash
spack clean <package>
spack stage <package>
cd $(spack location -s <package>)
spack build-env <package> -- bash --norc --noprofile
```

This drops you into a clean bash shell with the exact environment variables, compiler wrappers, and dependencies loaded that Spack uses during the build.
