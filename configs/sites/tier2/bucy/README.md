# Bucy

Bucy is an RHEL 8.10 x86_64 Tier 2 site using Lmod. The first configuration
builds `geos-dev` for GCC, Intel oneAPI, and LLVM Flang, and `geos-dev-nag`
for NAG. Compiler and MPI installations are external site software; Spack
builds the scientific stack and generates the user-facing Lmod modules.

The initial compiler matrix is:

- `gcc@=15.2.0` with OpenMPI 5.0.4
- `gcc@=16.1.0` with OpenMPI 5.0.10
- `oneapi@=2024.2.0` with Intel MPI 2021.13
- `oneapi@=2025.3.0` with Intel MPI 2021.17
- `nag@=7.2.43` with the patched OpenMPI 5.0.3
- `llvm@=22.1.0` with OpenMPI 5.0.10
- `llvm@=23.1.0` with OpenMPI 5.0.10

The NAG license is not stored in this repository. Before building
`geos-dev-nag`, ensure `NAG_KUSARI_FILE` points to the site license, or load
the site NAG module that sets it:

```bash
export NAG_KUSARI_FILE=/ford1/share/gmao_SIteam/nag/nag.key
```

---

## Using batch_install.sh script

On Bucy the `batch_install.sh` script runs in its one-step `local` mode: it builds directly into the final environment, generates modules, and writes to the shared build cache. There is no batch scheduler on Bucy, so `-s`, `-r`, `-p`, `-q`, `--constraint`, and `-a` do not apply.

### Help and dry-run

```bash
./util/gmao/batch_install.sh -h
```

Preview what the script would do without making any changes:

```bash
./util/gmao/batch_install.sh -m local -H bucy -n
```

### The -H flag

Always pass `-H bucy` explicitly. Without it, the script autodetects the site from `$HOSTNAME`; explicit `-H` avoids any ambiguity.

### First run

On the very first run, use `-u` to populate the bootstrap, source, and cargo mirrors:

```bash
./util/gmao/batch_install.sh -m local -H bucy -u
```

### The -e flag

On every subsequent run (rebuilds, retries), pass `-e` so the script continues in the existing environment directories instead of exiting with an error:

```bash
./util/gmao/batch_install.sh -m local -H bucy -e
```

### Selecting compilers and templates

Use `-C` to build only some compilers and `-T` to build only some templates (both comma-separated). By default all compilers in the matrix above are built with the `geos-dev` and `geos-dev-nag` templates (`geos-dev-nag` only applies to NAG):

```bash
./util/gmao/batch_install.sh -m local -H bucy -e -C gcc@=15.2.0,oneapi@=2024.2.0 -T geos-dev
```

### Other useful flags

- `-d ENV_DIRS`: override the environment directory (default: `envs/` in the repo root).
- `-c BUILDCACHE_DIR`: use a custom build cache instead of the shared one.
- `-o` / `--concretize-only`: stop after concretization.
- `-L` / `--disable-locks`: disable Spack install locks and serialize package installs; only for an isolated recovery run when no other process modifies the install tree.
- `-t`: run tests for specific third-party dependencies after installation.
- `--datestamp` / `--suffix=LABEL`: see below.
- `--with-ai`: add `ai-env` (py-torch + `jedi-base-env`) to newly created environments; expensive, off by default.

### Environment names

Environments are created directly under `envs/` (not `envs/bucy`), one per compiler, named `<prefix>-<compiler>-<version>`, e.g. `ge-gcc-15.2.0`, `ge-oneapi-2024.2.0`, `ge-nag-7.2.43`. The `ge-` prefix comes from the `geos-dev` and `geos-dev-nag` templates.

To keep an environment others may be using from being replaced, tag its name
with `--datestamp` (appends `-YYYYMMDD`) and/or `--suffix=LABEL` (appends
`-LABEL`), e.g. `./util/gmao/batch_install.sh -m local -H bucy --datestamp --suffix=swelltest`
gives `ge-gcc-15.2.0-YYYYMMDD-swelltest`. Both are off by default. Use the same options together with `-e` to continue a tagged environment.

---

## Site configuration notes

The shared installation, source, bootstrap, and cache locations are under
`/ford1/share/gmao_SIteam/spack-stack`. Tcl module generation is intentionally
not enabled in this first pass; it can be added after the Lmod hierarchy is
validated.

Compilers are not defined in a `compilers.yaml`; each is declared as an
external package (`gcc`, `llvm`, `intel-oneapi-compilers`, `nag`) in the
matching `packages_<compiler>.yaml`, together with its MPI external. The
OpenMPI externals list their variants explicitly (`~internal-hwloc
+two_level_namespace` is required by `configs/common/packages.yaml`, although
these builds actually use the bundled hwloc). `packages.yaml` sets the target
to `x86_64_v3`, declares the RHEL 8 system build tools (autoconf, automake,
gmake, and so on) as externals, and forces the system `tar`, because
`tar@1.35` fails to build against the system libacl headers.

Environments are created directly under `envs/` (not `envs/bucy`).
