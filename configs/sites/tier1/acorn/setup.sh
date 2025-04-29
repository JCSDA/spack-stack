## Load modules to avoid various issues with old Python versions
module load gcc/10.3.0 python/3.11.7

## Go, Rust repo setup for fetcher scripts
export GOMODCACHE=${SPACK_STACK_DIR}/cache/go
export CARGO_HOME=${SPACK_STACK_DIR}/cache/cargo
