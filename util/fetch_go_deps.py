#!/usr/bin/env spack-python
#
# Run this script in an active, concretized Spack environment to fetch Go
# dependencies and store them in $GOMODCACHE. You must either run it with
# 'spack-python' or have 'spack-python' in your $PATH. Ensure $GOMODCACHE has
# the same value when 'spack install' is run.
#
# For each spec that depends on 'go' and/or is specified by the user, it will
# attempt to use that spec's 'go' dependency to execute 'go mod download', but
# will fall back to searching for 'go' in $PATH if that dependency has not
# already been installed.
#
# Alex Richert, Apr 2025
#

import os
import argparse

from spack.environment import active_environment
from spack.error import SpackError
from spack.installer import PackageInstaller
from spack.spec import Spec
from spack.util.executable import Executable, which
from llnl.util.filesystem import working_dir

parser = argparse.ArgumentParser(
    description="Fetch Go dependencies for packages in a Spack environment"
)
parser.add_argument(
    "--spec", "-s",
    nargs="+",
    default=[],
    help="Additional specs for which to fetch go dependencies",
)
parser.add_argument(
    "--install-go",
    action="store_true",
    help="Install go dependency if not already installed",
)
parser.add_argument(
    "--only-listed", "-o",
    action="store_true",
    help="Only fetch user-provided specs (no auto-detection of go dependents)",
)

args = parser.parse_args()

# Load the current environment
env = active_environment()
if not env:
    raise SpackError("No active Spack environment")

gomodcache = os.getenv("GOMODCACHE")
if not gomodcache:
    raise SpackError("GOMODCACHE must be set")

user_specs = []
for spec_str in args.spec:
    try:
        user_specs.append(Spec(spec_str))
    except Exception as e:
        print(f"Warning: Invalid spec '{spec_str}': {e}")

# Find each spec that depends on 'go' or is in the user-specified package list
for spec in env.all_specs():
    if not spec.concrete:
        continue
     
    # Check if the package depends on go or is user specified
    is_user_specified = False
    for user_spec in user_specs:
        if spec.satisfies(user_spec):
            is_user_specified = True
            break
    if is_user_specified:
        fetch_it = True
    elif not args.only_listed:
        fetch_it = any(dep.name == 'go' for dep in spec.dependencies())
    else:
        fetch_it = False
    
    if fetch_it:
        print(f"Processing: {spec.name}@{spec.version}/{spec.dag_hash()}")
     
        # Check if package actually has a go dependency
        if 'go' not in spec:
            print(f"  Warning: {spec.name} does not have a 'go' dependency, skipping")
            continue
         
        pkg = spec.package
        pkg.do_stage()
     
        # Install go dependency if requested and not already installed
        go_dep = spec["go"]
        dep_go_path = os.path.join(go_dep.prefix.bin, "go")
     
        if not which(dep_go_path) and args.install_go:
            print(f"  Installing go dependency: {go_dep}")
            installer = PackageInstaller([go_dep.package])
            installer.install()
     
        # Now try to use the go dependency's go executable
        if which(dep_go_path):
            go_exe = Executable(dep_go_path)
        elif which("go"):
            go_exe = Executable("go")
        else:
            raise SpackError("Could not find 'go' executable")

        # Execute go mod download
        with working_dir(pkg.stage.source_path):
            if os.path.isfile("go.mod"):
                go_exe("mod", "download")
                print(f"  Successfully fetched dependencies for {spec.name}")
            else:
                print(f"  No go.mod for {spec.name}")
