# Container Site

This site config is used to build the official Spack-stack containers. This new tier-1 container site superceedes the legacy spack-based container builds and orients the container builder around common configs and a common site definition. The motivation for this site is to have our shared containers more closely match sites with loadable modules and developer tools-pre installed.


# Building

This container is not a typical site config and is installed slightly differently to accomodate the use of a dockerfile. Please follow the instructions here to build it.

## Prerequisites
- Docker
- At least 100 GB of disk space for the build
- Sufficient RAM (8GB+ recommended)

## Quick Build

The build context is the spack-stack repository root.  The Dockerfile
copies the entire local checkout (including the submodules) into
the image, so any local changes to configs, templates, or spack-ext
are automatically reflected in the container.

```bash
docker build \
    -t spack-stack-gcc:local \
    -f "$(git rev-parse --show-toplevel)/configs/sites/tier1/container/Dockerfile.gcc" \
    --build-arg SPACK_STACK_TEMPLATE=unified-dev \
    --build-arg BUILD_JOBS=8 \
    "$(git rev-parse --show-toplevel)"  2>&1 | tee ${HOME}/log.docker_gcc


docker build \
    -t spack-stack-oneapi:local \
    -f "$(git rev-parse --show-toplevel)/configs/sites/tier1/container/Dockerfile.oneapi" \
    --build-arg SPACK_STACK_TEMPLATE=unified-dev \
    --build-arg BUILD_JOBS=8 \
    "$(git rev-parse --show-toplevel)" 2>&1 | tee ${HOME}/log.docker_oneapi
```

`BUILD_JOBS` is the number of make jobs per package. `config.yaml` sets
`concurrent_packages: 4`, so a build runs up to 4 x `BUILD_JOBS` jobs at once
(32 on a 16-core machine). A full `unified-dev` build takes about 4 hours on 16
cores and needs well over 100 GB of free disk for the build cache.

The `COPY` of the repository includes `.git` (`spack stack create env` records
the spack-stack and spack commit hashes), so staging or committing a change
invalidates the Docker cache from that layer on and starts the spack install
over.

## Image Contents

Both images are based on Ubuntu 26.04.

* **gcc**: gcc 14.3.0 and openmpi 5.0.10. Ubuntu 26.04's default gcc is 15.2,
  which is newer than spack-stack supports. The image installs gcc-14 next to
  it and makes it the default `gcc`/`g++`/`gfortran` with `update-alternatives`.
  Spack uses the `-14` binaries by full path.
* **oneapi**: Intel oneAPI 2026.1.1 compilers (icx/icpx/ifx), Intel MPI 2021.18
  and MKL 2026.1, installed from Intel's apt repository into `/opt/intel/oneapi`.
  The compilers are pinned to the gcc-14 toolchain with compiler flags (see
  `packages_oneapi.yaml` and the tier1/aws-ubuntu README). gcc 14.3.0 builds a
  few packages (cmake, rust, py-numpy, ...).

The site configs follow tier1/aws-ubuntu, which tracks the same Ubuntu LTS.
Differences: tcl modules (environment-modules) instead of Lmod, the
container-specific Python pins in `packages.yaml`, and build stages under
`/tmp` (not a tmpfs inside a container).

## Using the Container

The images are development images: they include the compilers, MPI, and the
spack-stack modules under `/opt/spack-software/modulefiles`. Every bash shell
sources `/etc/spack_container_rc.sh`, which puts the `Core` module directory on
`MODULEPATH` and defines `load_jedi_bundle_env`:

```bash
load_jedi_bundle_env    # stack-gcc + stack-openmpi (or the oneAPI meta-modules) and the JEDI modules
module list
```

To load modules by hand, start from the compiler and MPI meta-modules:

```bash
# gcc
module load stack-gcc/14.3.0 stack-openmpi/5.0.10
# oneapi
module load stack-intel-oneapi-compilers/2026.1.1 stack-intel-oneapi-mpi/2021.18
```

Load modules such as `py-cartopy` and `py-pyproj` **before** running `ecbuild`
on jedi-bundle: some tests record `PYTHONPATH` at configure time.

OpenMPI is set up to run as root and to oversubscribe, so MPI tests work with
the default `docker run`. Intel MPI uses `/dev/shm` for on-node communication,
and Docker's default of 64 MB is too small: 12-task jedi-bundle tests die with a
bus error. Run the oneAPI image with a larger `/dev/shm`, for example
`docker run --shm-size=16g ...`.
