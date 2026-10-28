# AGENTS.md — spack-stack

Guidance for AI coding agents working in this repository. spack-stack is
spack-based distribution of software dependencies and packages supporting
a wide range of numerical weather prediction and data assimilation systems.

## Ground rules for agents

- Every change is reviewed by a human before it becomes a pull request.
- Independent work is fine when directed; independently filing pull requests
  and bugs is not acceptable.
- No tool attribution (`Co-Authored-By`, "Generated with…") anywhere.
- Submodule pins (`spack/`, `repos/builtin/`) stay put unless moving them is the
  task.
- Follow the output discipline in §3. Streaming spack output will overwhelm your
  context window and end the session.
- Run `spack dependents <spec>` before anything destructive —
  `spack uninstall --dependents` can take down half an env.

## Contents

| § | Section | TL;DR |
|---|---|---|
| 1 | Orientation | Repo map, submodules, recipe paths, where docs live |
| 2 | Build procedure | The 7-step spine; admin vs non-admin prerequisites |
| 3 | Output discipline | tee output to logs and background-run for verbose and slow commands like concretize and install |
| 4 | Configuration model | Configs are snapshotted; merge precedence; promotion |
| 5 | Sharp edges | The traps that waste days |
| 6 | Debugging | Error extraction → build-env → lock queries → symptom table |
| 7 | New releases | Reconciling spack / spack-stack / machine drift |
| 8 | Caches | Staging scratch vs binary build-cache mirrors |
| 9 | Utilities and docs | `util/` catalog; Wiki vs in-repo READMEs |

## 1. Orientation

Wiki: [Preconfigured Sites](https://github.com/JCSDA/spack-stack/wiki/Preconfigured-Sites) (tier1) ·
[Configurable Sites](https://github.com/JCSDA/spack-stack/wiki/Configurable-Sites) (tier2)

- `configs/common/` — cross-site defaults, including per-compiler
  `packages_<compiler>.yaml`.
- `configs/sites/tier{1,2}/<site>/` — machine configs. **tier1** = preconfigured,
  supported, often operational HPC; **tier2** = configurable/research. Orthogonal
  to the admin/non-admin split in §2.
- `configs/templates/<template>/spack.yaml` — spec sets (`unified-dev` is the big
  one). The list drifts; trust the directory.
- `spack/`, `repos/builtin/` — submodules (jcsda forks, branch
  `spack-stack-dev`). Recipes at
  `repos/builtin/repos/spack_repo/builtin/packages/<name>/package.py`, with
  hyphens→underscores and leading digits prefixed `_` (`py-numpy` → `py_numpy`,
  `7zip` → `_7zip`).
- `spack-ext/` — the `spack stack` extension. `util/` — helpers (§9). `envs/` —
  created environments, untracked.

`source setup.sh` in every fresh shell before anything else. Linux is the primary
target; on Windows use WSL, on macOS prefer a Linux VM.

**Docs live in the GitHub Wiki, not the repo** — there is no `doc/` tree and
`.readthedocs.yml` is vestigial. Per-site transcripts are the `README.md` inside
each site config dir; `tier2/aws-ubuntu2404/README.md` is the best **admin**
one, and it *derives* its site config from `--site linux.default`, which is the
canonical new-site pattern. For the **HPC** shape read `tier2/frontera/` — the
yaml is the documentation.

## 2. Build procedure

Wiki: [New Site Configs](https://github.com/JCSDA/spack-stack/wiki/New-Site-Configs) ·
[New and chained environments for existing sites](https://github.com/JCSDA/spack-stack/wiki/New-and-chained-environments-for-existing-sites) ·
[Supported Compilers](https://github.com/JCSDA/spack-stack/wiki/Supported-Compilers)

Which steps you need: **new site** — all. **New env on a site that already has a
config** — 1–2 then 5–7. **New release** — read §7 first.

### Step 0 — Prerequisites (the admin / non-admin fork)

Work out which you are first (`whoami`, `sudo -v`, is there already a `module`
system?). On shared/HPC systems, missing prerequisites are the sysadmins' to
provide — request them, don't shadow-install.

**Admin** — you provide build tooling, compilers, a module system and any vendor
toolchain; follow the aws-ubuntu2404 README. Two things bite: spack's Lua
modulefiles need **Lmod ≥ 7.0** and **Ubuntu's packaged lmod does not qualify**;
and for vendor compilers, build one combined `intel-oneapi-full-env/<ver>`
module, load it while deriving config, then **`module purge` before
`spack install`** (§5.1).

**Non-admin / HPC** — never build a compiler. Declare the existing system modules
as externals (`buildable: false` + `modules: [...]`, plus `all: providers: mpi:`
and `mpi: buildable: false`). Copy an existing HPC site dir.

### Steps 1–7 — The spine

```bash
set -o pipefail

# 1. Clone at the RIGHT ref (release/X.Y for reproducible builds, develop for latest)
git clone -b <ref> --recurse-submodules https://github.com/jcsda/spack-stack.git
cd spack-stack && source setup.sh

# 2. Create the environment (SNAPSHOTS configs — see §4)
#    New site? use --site linux.default and derive the real config in step 3.
spack stack create env --site <site> --template <template> \
    --name <env-name> --compiler <gcc|oneapi|intel|apple-clang>
cd envs/<env-name> && spack env activate -p .

# 3. NEW SITES ONLY — derive externals/compilers into the env's site/ scope.
# - Compilers: Multiple versions of site compilers are often found. Edit the
#   `site/packages.yaml` to ensure that exactly one external compiler of each
#   target type is available. For example, if targeting gcc-13, eliminate
#   external references to gcc11, 12, and 14.
# - Vendor MPI libraries often fail to auto-detect and must be hand written as an
#   external in `site/packages.yaml`.
unset SPACK_DISABLE_LOCAL_CONFIG
export SPACK_SYSTEM_CONFIG_PATH="$(pwd)/site"
spack external find --scope system --exclude python --exclude cmake ...  # site-specific
spack compiler find --scope system
export SPACK_DISABLE_LOCAL_CONFIG=true && unset SPACK_SYSTEM_CONFIG_PATH

# 4. Configure MPI provider, preferences, pins
spack config add "packages:all:providers:mpi:[openmpi@5.0.8]"   # example — use the site's MPI

# 5. Concretize and sanity-check — ALWAYS tee (§3)
spack concretize --fresh 2>&1 | tee log.concretize
${SPACK_STACK_DIR}/util/show_duplicate_packages.py   # -i <pkg> IGNORES known dups
spack stack check-preferred-compiler

# 6. Install — hours long; run in background, inspect the log file (§3)
spack install --fail-fast -j <N> 2>&1 | tee log.install

# 7. Modules
spack module lmod refresh          # or tcl; add --upstream-modules for chained envs
spack stack setup-meta-modules     # generates the stack-<compiler>/stack-<mpi> modules
```

## 3. Output discipline (critical for agents)

Some spack commands emit enormous output. Never stream a concretize or install
log into your context.

Always `2>&1 | tee log.<step>` for every long command, and do not accept
the full output into your context.

Start every shell with `set -o pipefail`. A pipeline returns its *last*
element's status, so without it `cmd | tee log` returns tee's `0` and a
failed build reports success to the harness (this also improves behavior
when chaining commands with `&&` or catching failures with `set -e`).

More notes on context discipline:
 * `spack install` - Takes hours, run in the background. On failure, verify
   with `tail -n 40 log.install`. When a spack install fails it will prefix
   failure log lines with `> ` to make them easier to grep out of the long log.
 * Do not `cat` a generated `packages.yaml` or `spack.lock`; grep them or read
   line ranges. Note that `spack.lock` is a large one-line JSON object. There
   is advice in §6 on querying this file.
 * `show_duplicate_packages.py` output is small — read it fully. `-i <pkg>`
   **ignores** a package; it is NOT a focus flag. `unified-dev` intentionally
   duplicates some, so the canonical check is
   `show_duplicate_packages.py -i fms -i crtm -i crtm-fix -i esmf -i mapl -i py-cython`.

```bash
# Find and deduplicate errors from an install log.
grep -E "^> .*error:" log.install | sed 's/^> //' | sort | uniq -c | sort -rn | head
```

## 4. Configuration model

Wiki: [Configuration Files And Templates](https://github.com/JCSDA/spack-stack/wiki/Configuration-Files-And-Templates)

`spack stack create env` **snapshots** configs: it *copies* `configs/common/` and
`configs/sites/<site>/` into `envs/<name>/{common,site}/`. Editing `configs/`
afterwards does nothing to an existing env. Iterate by editing the env's copies
AND keeping `configs/` in sync (that is what gets committed); `diff` them before
re-concretizing.

Merge precedence, low → high (higher wins):

```
common/*.yaml
  < common/packages_<compiler>.yaml
    < site/*.yaml
      < site/packages_<compiler>.yaml
        < the env's own spack.yaml   (template contents + create-env/config-add writes)
```

Included scopes sit below their includer, and earlier `include:` entries beat
later ones. A **double colon** (`enable::`, `mpi::`) *replaces* the
lower-precedence value instead of merging. `spack config blame packages` answers
"which scope set this?" with file:line.

**Promotion** — once an env builds cleanly its `site/` scope *is* the draft site
config. Copy `envs/<env>/site/*.yaml` into `configs/sites/tier{1,2}/<site>/`,
**fold in anything that lives only in the env `spack.yaml`** (everything added
via `spack config add`, or it is lost), rename to match a sibling site, and
re-run `create env` from a clean checkout to confirm it reproduces the env.

## 5. Sharp edges

**1. The `LOADEDMODULES` trap** — any site whose externals use `modules:` (all
HPC, plus admin sites with vendor toolchains). Spack judges a module load by
whether `$LOADEDMODULES` *changed*, not by exit status. So:

- Never `module load` the vendor toolchain in the shell running `spack install`:
  an already-loaded module reads as a *failed* load — `ModuleLoadError` for a
  module that loads fine by hand. `module use` the directory, purge, let spack
  load.
- No module may appear in two externals' `modules:` lists in one DAG; the second
  load is a no-op and errors. Each list must also be self-sufficient and in
  prereq order, since spack loads externals in DAG order. When those two collide,
  drop `modules:` from the dependent external and rely on `prefix:` — many vendor
  packages (e.g. intel-oneapi-mkl) self-configure.
- It fails *late* and blames the wrong thing (concretize never loads modules).
  Probe cheaply: `spack build-env <mpi-using-spec> -- true`.

**2. Never re-run `spack external find` on a complete site config.** It
rediscovers declared packages and rewrites hand-curated entries. It derives new
configs; it does not refresh mature ones.

**3. A `require:` on a variant silently caps the version** — a variant that only
exists on some versions or build systems restricts you to those (`python ~crypt`
capped at 3.12; `cairo +pic` at 1.17.4). An error with an empty "required
because" chain is config-level, not recipe; a package that won't move means grep
the config for its *variants*, not its version. Scope them: `- spec: ~crypt` +
`when: '@:3.12'`.

**4. Every external needs `prefix:`** (and `buildable: false`). Spack silently
drops one that lacks it and *builds* the package instead, which can then hit
recipe bugs — a prefix-less `tar` died with
`KeyError: 'No spec with name xz in tar@1.35'`.

**5. `spack spec <pkg>` is not your env.** Standalone it is a fresh,
unconstrained solve. Query `spack.lock` instead (§6).

## 6. Debugging

Wiki: [Known Issues](https://github.com/JCSDA/spack-stack/wiki/Known-Issues) — check it before any deep dive.

Triage: concretize failure → `==> Error:` near the end of `log.concretize`, no
`spack.lock` written (usually §5.3/§5.5 or duplicates, below). Install failure →
`log.install`. Module-generation tracebacks from `meta_modules.py` are env/config
mismatches and say so.

Extract the error with the `> `-prefix histogram from §3, then:

```bash
spack logs <spec>              # full build log, decompressed — works for failed builds
spack location -i <spec>       # install prefix; -b = build dir while stage survives
spack dependents <spec>        # blast radius before uninstalling anything
spack find -c                  # includes concretized-but-not-installed specs
spack install --only=package <spec>       # rebuild just this node
spack install -u <phase> <spec>           # stop after configure/build/...
```

Each install prefix has a `.spack/` with `spack-build-env.txt` (every env var —
ground truth for "what CC/CFLAGS did it *really* use?"),
`spack-configure-args.txt`, `archived-files/spack-src/config.log` and `spec.json`.

**`spack build-env`** reconstructs a package's exact build environment (recipe
`setup_build_environment`, external `modules:`, all of it) without building:
`-- bash` for a shell in it, `-- bash -c 'echo $CFLAGS'` to check a flag reached
the build, `-- true` to test whether it assembles at all (the cheap module-trap
probe). Highest-value, most underused command in spack.

**Editing a recipe changes its hash**: `py_compile` it,
`spack uninstall -y --dependents <pkg>`, then `spack concretize --fresh --force`,
or spack rebuilds the old hash.

**Interrogate `spack.lock`** — it is what will actually be built. The query that
matters most is "who pulled in each copy of this duplicated package":

```bash
python3 - <<'EOF'
import json
cs = json.load(open('spack.lock'))['concrete_specs']
target = 'py-versioneer'
for h, s in cs.items():
    if s['name'] != target: continue
    print(s['version'], sorted({f"{p['name']}@{p['version']}" for p in cs.values()
          for d in p.get('dependencies', []) if d.get('hash') == h}))
EOF
```

**Duplicates** usually come from a dep declared with no version bound in two
recipes; fix with a *loose lower bound* (`require: ['@5.18:']`), never an exact
pin. Structural ones (two recipes pinning exact, different versions) can't be
fixed — stop them *cascading* by pinning the flexible middle package to one side.

**Read the recipe** (path rules in §1): grep `conflicts(`, `depends_on(.*when=`
(version-gated deps — an old version can concretize *without* a dep it needs),
`requires(` (all-or-nothing variant groups), and `flag_handler` /
`setup_build_environment` — an `env.set("CFLAGS", ...)` in the latter
**replaces** whatever `flag_handler` computed, which is why a config-level
`cflags=` can appear to do nothing.

### Symptom table

| Symptom | Likely cause |
|---|---|
| `ModuleLoadError` but it loads by hand | preloaded module, or two externals list it (§5.1) |
| Hundreds of `incompatible pointer types` errors | clang16+/oneAPI promote to errors; `flag_handler` guarded only on `%gcc@14:` |
| configure: mandatory feature can't be enabled | version-gated `depends_on` left the dep out of the DAG |
| Variant set but feature missing | `requires(one_of)` group landed all-off |
| Package won't move; blamed packages look fine | config variant requirement caps it (§5.3) |
| Config edit does nothing | env snapshotted configs — edit `envs/<env>/{common,site}/` (§4) |
| Config edits keep reappearing | `external find` re-run on a complete site (§5.2) |
| Duplicate versions of one package | unversioned dep in two recipes; loose lower bound |
| Cryptic compiler errors early | redundant/empty compiler spec in `site/packages.yaml` |
| `KeyError: 'No spec with name X in Y'` on a system tool | external missing `prefix:` (§5.4) |
| External not detected by `external find` | hand-write the `externals:` block |
| Links `libirc.so` / missing .so / others can't read | `util/check_libirc.sh` / `ldd_check.py` / `check_permissions.sh` |

## 7. New releases (drift reconciliation)

Wiki: the per-release `Release-x.y.z` page (e.g.
[Release 2.1.1](https://github.com/JCSDA/spack-stack/wiki/Release-2.1.1)) and its `post-release-updates` companion.

Same spine; the work is absorbing drift in spack-stack, in spack itself, and in
the machine. Clone fresh at the release branch — never `git pull` an old tree
across a major bump, since submodule pins must land together. Read the release's
Wiki page and its `post-release-updates` page first, then re-derive externals and
compilers on the actual machine rather than trusting the old
`site/packages.yaml`.

Watch two things. An MPI version appears in at least three places that must
agree: `providers:`, the external's `spec:`/`modules:`, and the README's
`module load stack-<mpi>/<ver>`. And expect spack's compiler-as-dependency model
(`gcc@13.3.0 languages:='c,c++,fortran'` plus `extra_attributes: compilers:`,
per-language `%c=oneapi %fortran=gcc` conflicts, empty compiler specs now
near-fatal).

Trust the old README for the *shape* of a build; re-derive every *value*.

## 8. Caches — two different things

Wiki: [Spack Mirrors](https://github.com/JCSDA/spack-stack/wiki/Spack-Mirrors) — also covers air-gapped installs and
cargo/go mirrors.

**Staging cache** (`config.yaml`: `build_stage`, `source_cache`, `misc_cache`) —
where spack unpacks and compiles. Pure scratch; `spack clean -a` purges it.
**The paths are absolute**, so two working trees on one machine share them —
don't run concurrent builds without repointing.

**Binary build cache** (`mirrors.yaml`, `binary: true`) — relocatable prebuilt
packages that skip recompiles, pushed with `spack buildcache push` and reused
automatically when the mirror is present.

On an ephemeral machine put both under `/tmp`: this is build acceleration, not
storage. A cache that must survive the machine is a shared mount or `s3://`
mirror — a deliberate infra decision, never a silent default.

## 9. Utilities and docs

Wiki: [Utilities](https://github.com/JCSDA/spack-stack/wiki/Utilities)

| Script (`util/`) | Purpose |
|---|---|
| `show_duplicate_packages.py [-i PKG ...]` | duplicate versions in `spack.lock`; `-i` **ignores** (§3) |
| `parallel_install.sh N M [args]` | N parallel installs × M jobs each; source it |
| `ldd_check.py` / `check_libirc.sh` / `check_permissions.sh` | unresolved libs / leaked Intel `libirc.so` ([background](https://github.com/JCSDA/spack-stack/wiki/Intel-oneAPI-compilers-and-libirc.so)) / world-readability |
| `modules_config_check.py` | `modules_lmod.yaml` vs `modules_tcl.yaml` drift |
| `get_version_list.sh [ENV]` | markdown version table for a release Wiki page |
| `fetch_cargo_deps.py` / `fetch_go_deps.py` | pre-fetch Rust/Go deps for firewalled builds |

"Update the docs" splits two ways. Build procedure, release notes and site
listings go to the **Wiki** (clone `spack-stack.wiki.git`; pre-2.0 version
tables live in [Package Versions PreV2](https://github.com/JCSDA/spack-stack/wiki/Package-Versions-PreV2)). A single
machine's
concrete transcript goes in the `README.md` in that site's config dir, shipped
with the config it documents.
