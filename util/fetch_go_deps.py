#!/usr/bin/env spack-python
#
# Run this script in an active, concretized Spack environment to fetch Go
# dependencies and store them in $GOMODCACHE. You must either run it with
# 'spack-python' or have 'spack-python' in your $PATH. Ensure $GOMODCACHE has
# the same value when 'spack install' is run.
#
# For each spec that is a GoPackage, it will attempt to use that spec's 'go'
# dependency to execute '', but will fall back to searching $PATH if that
# dependency has not already been installed.
#
# Alex Richert, Apr 2025
#

import os

from spack.environment import active_environment
from spack.build_systems.go import GoPackage
from spack.package_base import PackageBase
from spack.util.executable import Executable, which
from llnl.util.filesystem import working_dir
from spack.store import find
from spack.error import SpackError

# Load the current environment
env = active_environment()
if not env:
    raise SpackError("No active Spack environment")

gomodcache = os.getenv("GOMODCACHE")
if not gomodcache:
    raise SpackError("GOMODCACHE must be set")

# Find each spec that is a GoPackage
#  and fetch its dependencies to $GOMODCACHE
for spec in env.all_specs():
    if not spec.concrete:
        continue
    pkg_cls = spec.package.__class__
    if issubclass(pkg_cls, GoPackage):
        print(f"Found spec with GoPackage: {spec.name}@{spec.version}/{spec.dag_hash()}")
    else:
        continue
    pkg = spec.package
    pkg.do_stage()

    dep_go_path = os.path.join(spec["go"].prefix.bin, "go")
    if which(dep_go_path):
        go_exe = Executable(dep_go_path)
    elif which("go"):
        go_exe = Executable("go")
    else:
        raise SpackError("Could not find 'go' executable")

    with working_dir(pkg.stage.source_path):
        go_exe("mod", "download")
