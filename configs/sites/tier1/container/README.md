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
    --build-arg BUILD_JOBS=10 \
    "$(git rev-parse --show-toplevel)"  2>&1 | tee ${HOME}/log.docker_gcc


docker build \
    -t spack-stack-oneapi:local \
    -f "$(git rev-parse --show-toplevel)/configs/sites/tier1/container/Dockerfile.oneapi" \
    --build-arg SPACK_STACK_TEMPLATE=unified-dev \
    --build-arg BUILD_JOBS=10 \
    "$(git rev-parse --show-toplevel)" 2>&1 | tee ${HOME}/log.docker_oneapi
```
