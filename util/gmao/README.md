GMAO Spack-Stack Utilities

---

## Table of Contents

- [Overview](#overview)
- [batch\_install.sh](#batch_installsh)
- [monitor\_install.py](#monitor_installpy)

---

## Overview

This directory contains GMAO SI Team utility scripts for building and managing spack-stack environments.

---

## batch_install.sh

The primary script for building and installing spack-stack environments. It automates environment creation, cache population, and the Spack installation pipeline across all GMAO-supported sites.

### Usage

```
batch_install.sh -r <ROLE> -m <MODE> [-d <ENV_DIRS>] [-c <BUILDCACHE_DIR>] [-H <HOSTNAME>]
```

Run with `-h` for full usage:

```bash
./util/gmao/batch_install.sh -h
```

### Key flags

| Flag | Description |
|---|---|
| `-r ROLE` | Role: `dev` (SI Team developers with write access to shared mirrors, writes to default build cache) or `ops` (operational partners without write access, requires `-c` to specify their own build cache). |
| `-m MODE` | Mode: `build` (compile + populate build cache) or `install` (install from cache + generate modules). |
| `-H HOSTNAME` | Override hostname autodetection. Usually required (e.g. `-H discover-gmao`, `-H macos.gmao`). |
| `-s` | Submit the install step to the batch scheduler (SLURM/PBS) instead of running interactively. |
| `-e` | Continue if environment directories already exist. Required on all runs after the first. |
| `-u` | Populate bootstrap, source, and cargo mirrors. Requires `-r dev -m build`. First run only. |
| `-o` / `--concretize-only` | Stop after concretization; do not proceed to install. Useful for inspecting solver output before committing to a full build. |
| `-a ACCOUNT` | Override the scheduler account (default: `s1873`). |
| `-n` | Dry-run: print what would be executed without running anything. |
| `-p` / `--partition` | Override SLURM partition. **NCCS hosts only** (discover, discover-gmao). |
| `-q` / `--qos` | Override SLURM QOS. **NCCS hosts only** (discover, discover-gmao). |
| `--constraint` | Override SLURM node constraint (e.g. `--constraint=mil`). **NCCS hosts only**. No short form. |
| `-c BUILDCACHE_DIR` | Custom build cache path. Required with `-r ops -m build`. |
| `-d ENV_DIRS` | Override the default environment directory. |
| `-C COMPILERS` | Comma-separated compiler list, overrides site defaults. |
| `-N NAGFOR_PATH` | Path to `nagfor` executable for NAG compiler detection (macOS only). |
| `-t` | Run tests for hardcoded third-party packages after installation. |

### Supported sites

The script detects the current site from `$HOSTNAME` (stripping digits and domain), or you can override with `-H`:

| Site key | System |
|---|---|
| `discover` | NASA NCCS Discover (JCSDA account/partition) |
| `discover-gmao` | NASA NCCS Discover (GMAO SI Team account/partition) |
| `nas` | NASA NAS Pleiades (TOSS 4) |
| `nas-toss5` | NASA NAS Pleiades (TOSS 5) |
| `macos.gmao` | macOS with Homebrew (GMAO SI Team) |
| `bucy` | RHEL 8.10 host with shared GMAO SI Team software |

### Site-specific READMEs

For detailed workflow instructions for each site, see:

- `configs/sites/tier2/discover-gmao/README.md` — Discover GMAO workflow
- `configs/sites/tier2/macos.gmao/README.md` — macOS GMAO workflow
- `configs/sites/tier2/bucy/README.md` — Bucy workflow

---

## monitor_install.py

A Python script that monitors a spack install log file and reports progress with a progress bar. Useful for watching a build submitted via `-s` without having to tail the raw log.

### Usage

```bash
# Monitor a live log from its current end (attach to a running build)
python3 util/gmao/monitor_install.py <logfile>

# Monitor a live log from the beginning of the file
python3 util/gmao/monitor_install.py -f <logfile>

# Read the full log, print a progress report, then exit
python3 util/gmao/monitor_install.py -r <logfile>
```

The log file is the `.log` file written by `batch_install.sh -s`, named:

```
spack.<hostname>.<env_name>.log
```

For example, after running:

```bash
./util/gmao/batch_install.sh -r dev -m build -H discover-gmao -s -e
```

The log files will be named `spack.discover-gmao.ge-gcc-15.2.0-build.log`, etc. in the current directory.

### Options

| Flag | Description |
|---|---|
| `-f` / `--from-start` | Scan from the beginning of the file rather than tailing live. |
| `-r` / `--report` | Read full file, print progress summary, then exit (non-interactive). |
| `-t SECONDS` / `--timeout` | Seconds of log inactivity before exiting live mode (default: 300). |

### Exit conditions (live mode)

The script exits automatically when:
- All packages are installed (progress counter reaches total)
- A spack error is detected in the log
- No new log output for `--timeout` seconds (default: 5 minutes)

---
