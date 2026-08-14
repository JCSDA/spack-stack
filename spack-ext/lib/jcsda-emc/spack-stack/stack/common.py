#!/usr/bin/env python3

# Terminal colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Colored log levels
INFO_LABEL = "INFO: "
ERROR_LABEL = "\033[91mERROR:\033[0m "

# Aliases to shorten module paths for tcl modules. These aliases must match
# the compiler and MPI name translations in configs/common/modules_tcl.yaml
ALIASES = {
    "none" : "none",
    # Compilers
    "gcc" : "gcc",
    "intel-oneapi-compilers-classic" : "intel",
    "intel-oneapi-compilers" : "oneapi",
    "llvm" : "llvm",
    "nvhpc" : "nvhpc",
    # MPI
    "cray-mpich" : "cray-mpich",
    "intel-oneapi-mpi" : "impi",
    "mpich" : "mpich",
    "mpt" : "mpt",
    "openmpi" : "openmpi",
}


def get_preferred_compiler(config):
    """Determine the preferred compiler by looking at
    packages:
      fortran:
        prefer:
        - COMPILER_NAME (gcc, intel-oneapi-compilers, llvm, ..)
    """
    try:
        preferred_compilers = config.get("packages")["fortran"]["prefer"]
    except:
        raise Exception(
            """Unable to detect preferred compiler from environment.
            Does the environment have the config entry 'packages:fortran:prefer?'"""
        )
    if len(preferred_compilers)>1:
        raise Exception(f"Invalid value for packages:fortran:prefer is {preferred_compilers}")
    preferred_compiler = preferred_compilers[0]
    return preferred_compiler
