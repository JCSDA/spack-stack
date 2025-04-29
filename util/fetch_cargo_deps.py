#!/usr/bin/env spack-python
#
# Run this script in an active, concretized Spack environment to fetch Rust
# dependencies and store them in $CARGO_HOME. You must either run it with
# 'spack-python' or have 'spack-python' in your $PATH. Ensure $CARGO_PATH has
# the same value when 'spack install' is run.
#
# For each spec that is a CargoPackage, it will attempt to use that spec's
# 'rust' dependency to execute 'cargo fetch', but will fall back to searching
# $PATH if that dependency has not already been installed.
#
# Alex Richert, Apr 2025
#

import os

from spack.environment import active_environment
from spack.build_systems.cargo import CargoPackage
from spack.package_base import PackageBase
from spack.util.executable import Executable, which
from llnl.util.filesystem import working_dir
from spack.store import find
from spack.error import SpackError

# Load the current environment
env = active_environment()
if not env:
    raise SpackError("No active Spack environment")

cargo_home = os.getenv("CARGO_HOME")
if not cargo_home:
    raise SpackError("CARGO_HOME must be set")

# Find each spec that is a CargoPackage
#  and fetch its dependencies to $CARGO_HOME
for spec in env.all_specs():
    if not spec.concrete:
        continue
    pkg_cls = spec.package.__class__
    if issubclass(pkg_cls, CargoPackage):
        print(f"Found spec with CargoPackage: {spec.name}@{spec.version}/{spec.dag_hash()}")
    else:
        continue
    pkg = spec.package
    pkg.do_stage()

    # 'replace' is due to https://github.com/spack/spack/issues/50079
    dep_cargo_path = os.path.join(spec["rust"].prefix.bin, "cargo").replace("/bin/bin/", "/bin/")
    if which(dep_cargo_path):
        cargo_exe = Executable(dep_cargo_path)
    elif which("cargo"):
        cargo_exe = Executable("cargo")
    else:
        raise SpackError("Could not find 'cargo' executable")

    with working_dir(pkg.stage.source_path):
        cargo_exe("fetch")
