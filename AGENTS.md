# AGENTS.md — spack-stack

Guidance for AI coding agents working in this repository. spack-stack is
spack-based distribution of software dependencies and packages supporting
a wide range of numerical weather prediction and data assimilation systems.

## Temporary AI policy

Refer to https://github.com/JCSDA/spack-stack/issues/2196

The spack-stack project, including its submodules spack and spack-packages, requires all GitHub contributions—including issues, pull requests, discussions, and comments—to be submitted by a real person.

Contributions that are developed with the assistance of large language models (LLMs) or AI agents are welcome, provided that a human author has reviewed and remains responsible for the language, code, and other proposed changes. Fully autonomous AI-generated contributions will be rejected. The spack-stack maintainers may also reject, at their sole discretion, contributions that contain excessive prose or otherwise indicate insufficient human review.

## Ground rules for agents

The policy above is binding. In practice:

- Every change is reviewed by a human before it becomes a pull request.
- Independent work is fine when directed; independently filing pull requests,
  issues or comments is not acceptable.
- Scope changes to the software intent, not the literal requirement. A goal
  like "make X build on site Y" warrants the smallest change that does it;
  surface wider findings to your human for discussion with maintainers rather
  than folding them into one large PR.
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
| 2 | Build procedure | Points to the Wiki and CI workflows; new-site vs existing-site paths |
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
target. On Windows use WSL, on macOS native installs are possible but some users
prefer a Linux VM via OrbStack (if the target environment is unclear, ask the user).

**Docs live in the GitHub Wiki, not the repo** — there is no `doc/` tree and
`.readthedocs.yml` is vestigial. If you are working on a site that already has a
config under `configs/sites/`, the `README.md` in that site's directory is often
worth reading first.

## 2. Build procedure

Wiki: [New Site Configs](https://github.com/JCSDA/spack-stack/wiki/New-Site-Configs) ·
[New and chained environments for existing sites](https://github.com/JCSDA/spack-stack/wiki/New-and-chained-environments-for-existing-sites) ·
[Supported Compilers](https://github.com/JCSDA/spack-stack/wiki/Supported-Compilers)

Read the Wiki pages above for details and explaination on the build procedure.
For a continuously tested record of the same procedure, read the CI workflows
in `.github/workflows/` (e.g. `ubuntu-ci-x86_64-gnu.yaml`): they create an env
from `--site linux.default`, derive the site config, concretize, install and
generate modules.

The **new-site** path is distinct from, and mostly a superset of, the
**existing-site** path: it adds deriving externals and compilers into the env's
`site/` scope (`spack external find` / `spack compiler find`) before
concretizing. If your site already has a config, skip those steps. **New
release** — read §7 first.

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
      < site/packages_<compiler>[-<ver>].yaml
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

**1. External `modules:` fail late** — any site whose externals use `modules:`
(all HPC, plus admin sites with vendor toolchains). Spack loads each external's
`modules:` at build time and raises `ModuleLoadError` if the module is not in
`$LOADEDMODULES` afterwards. Modules that are already loaded are accepted, so
preloading the toolchain or listing one module in two externals is fine. A
`ModuleLoadError` means the load really failed:

- Wrong name, or its directory was never `module use`d.
- A prereq is missing. Each `modules:` list must be self-sufficient and in
  prereq order, since spack loads externals in DAG order. If a list can't be
  made self-sufficient, drop `modules:` and rely on `prefix:` — many vendor
  packages (e.g. intel-oneapi-mkl) self-configure.
- Concretize never loads modules, so this surfaces mid-install and blames the
  wrong package. Probe cheaply:
  `spack build-env <mpi-using-spec> -- bash --norc --noprofile -c true`.

**2. Never re-run `spack external find` on a complete site config.** It
rediscovers declared packages and rewrites hand-curated entries. It derives new
configs; it does not refresh mature ones.

**3. A `require:` on a variant silently caps the version** — a variant that only
exists on some versions or build systems restricts you to those (`python ~crypt`
capped at 3.12; `cairo +pic` at 1.17.4). An error with an empty "required
because" chain is config-level, not recipe; a package that won't move means grep
the config for its *variants*, not its version. Scope them: `- spec: ~crypt` +
`when: '@:3.12'`.

**4. Every external needs `prefix:` or `modules:`** (and `buildable: false`).
With `modules:` alone spack infers the prefix from the modulefile; add `prefix:`
if it infers the wrong one. A `prefix:` only replaces that inference: the
`modules:` are still loaded at build time. Spack silently drops an external with neither and *builds* the package instead, which can then hit
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
`-- bash --norc --noprofile` for a shell in it (what `spack install` itself
uses; your rc files would otherwise pollute it), append `-c 'echo $CFLAGS'` to
check a flag reached the build, or `-c true` to test whether it assembles at all
(the cheap module probe). Highest-value, most underused command in spack.

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
| `ModuleLoadError` mid-install | missing `module use` or out-of-order prereqs in `modules:` (§5.1) |
| Hundreds of `incompatible pointer types` errors | clang16+/oneAPI promote to errors; `flag_handler` guarded only on `%gcc@14:` |
| configure: mandatory feature can't be enabled | version-gated `depends_on` left the dep out of the DAG |
| Variant set but feature missing | `requires(one_of)` group landed all-off |
| Package won't move; blamed packages look fine | config variant requirement caps it (§5.3) |
| Config edit does nothing | env snapshotted configs — edit `envs/<env>/{common,site}/` (§4) |
| Config edits keep reappearing | `external find` re-run on a complete site (§5.2) |
| Duplicate versions of one package | unversioned dep in two recipes; loose lower bound |
| Cryptic compiler errors early | redundant/empty compiler spec in `site/packages.yaml` |
| `KeyError: 'No spec with name X in Y'` on a system tool | external has neither `prefix:` nor `modules:` (§5.4) |
| External not detected by `external find` | hand-write the `externals:` block |
| Missing .so at runtime / others can't read the install | `util/ldd_check.py` / `check_permissions.sh` (§9) |
| Links Intel `libirc.so` | [libirc background](https://github.com/JCSDA/spack-stack/wiki/Intel-oneAPI-compilers-and-libirc.so) |

## 7. New releases (drift reconciliation)

Wiki: the per-release `Release-x.y.z` page (e.g.
[Release 2.2.0](https://github.com/JCSDA/spack-stack/wiki/Release-2.2.0)) and its `post-release-updates` companion.
Same procedure as §2; the work is absorbing drift in spack-stack, in spack itself, and in
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
It lives under `${SPACK_STACK_DIR}/cache/`, so every env in a checkout shares
it and each checkout has its own.

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
| `ldd_check.py [-i RE]` / `check_permissions.sh` | missing shared-lib deps under `$SPACK_ENV/install` / world-readability |
| `modules_config_check.py` | `modules_lmod.yaml` vs `modules_tcl.yaml` drift |
| `get_version_list.sh [ENV]` | markdown version table for a release Wiki page |
| `fetch_cargo_deps.py` / `fetch_go_deps.py` | pre-fetch Rust/Go deps for firewalled builds |

"Update the docs" splits two ways. Build procedure, release notes and site
listings go to the **Wiki** (clone `spack-stack.wiki.git`; pre-2.0 version
tables live in [Package Versions PreV2](https://github.com/JCSDA/spack-stack/wiki/Package-Versions-PreV2)). A single
machine's
concrete transcript goes in the `README.md` in that site's config dir, shipped
with the config it documents.
