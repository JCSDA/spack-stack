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

The NAG license is not stored in this repository. Before building
`geos-dev-nag`, ensure `NAG_KUSARI_FILE` points to the site license, or load
the site NAG module that sets it:

```bash
export NAG_KUSARI_FILE=/ford1/share/gmao_SIteam/nag/nag.key
```

For a direct local build, use:

```bash
./util/gmao/batch_install.sh -m local -H bucy -u
```

The shared installation, source, bootstrap, and cache locations are under
`/ford1/share/gmao_SIteam/spack-stack`. Tcl module generation is intentionally
not enabled in this first pass; it can be added after the Lmod hierarchy is
validated.
