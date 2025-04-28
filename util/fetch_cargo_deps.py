#!/usr/bin/env spack-python
#
# Run this script in an active, concretized Spack environment to fetch Rust
# dependencies and store them in $CARGO_HOME. You must either run it with
# 'spack-python' or have 'spack-python' in your $PATH. Ensure $CARGO_HOME has
# the same value when 'spack install' is run.
#
# For each spec that is a CargoPackage or a PythonPackage with a rust dependency,
# it will attempt to fetch all of its cargo dependencies using 'cargo' if available
# in the user's environment, but will fall back to installing cargo/rustup from the
# internet using install_rust.sh (located in in the same directory as this script).
#
# Created by Alex Richert, April 2025
# Modified by Dom Heinzeller, April 2025
#

import shutil
import sys
import os

this_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

from spack.environment import active_environment
from spack.build_systems.cargo import CargoPackage
from spack.build_systems.python import PythonPackage
from spack.package_base import PackageBase
from spack.util.executable import Executable, which
from llnl.util.filesystem import working_dir
from spack.store import find
from spack.error import SpackError

# Load the current environment
env = active_environment()
if not env:
    raise SpackError("No active Spack environment")

default_path = os.getenv("PATH")

spack_stack_dir = os.getenv("SPACK_STACK_DIR")
if not spack_stack_dir:
    raise SpackError("SPACK_STACK_DIR must be set")

cargo_home = os.getenv("CARGO_HOME")
if not cargo_home:
    raise SpackError("CARGO_HOME must be set")
if not os.path.isdir(cargo_home):
    os.makedirs(cargo_home)

# Find each spec that is a CargoPackage or a PythonPackage with a
# rust/rust-bootstrap dependency and fetch its dependencies to $CARGO_HOME
for spec in env.all_specs():
    if not spec.concrete:
        continue
    pkg_cls = spec.package.__class__
    
    rust_spec = None
    if issubclass(pkg_cls, CargoPackage):
        for dep in spec.dependencies():
            if "rust" in dep.name:
                rust_spec = dep
                break
        if not rust_spec:
            raise SpackError(f"Could not find rust dependency for CargoPackage {spec.name}")
        print(f"Found CargoPackage {spec.name}@{spec.version}/{spec.dag_hash()} with rust dependency {rust_spec.name}")
    elif issubclass(pkg_cls, PythonPackage):
        for dep in spec.dependencies():
            if "rust" in dep.name:
                rust_spec = dep
                break
        if not rust_spec:
            continue
        print(f"Found PythonPackage {spec.name}@{spec.version}/{spec.dag_hash()} with rust dependency {rust_spec.name}")
    else:
        continue
    pkg = spec.package
    pkg.do_stage()

    if which("cargo"):
        cargo_exe = Executable("cargo")
    else:
        # cargo/rustup
        cargo_path = os.path.join(cargo_home, "bin", "cargo")
        print(f"Checking for {cargo_path} ...")
        if which(cargo_path):
            print(f"  ... found {cargo_path}")
        else:
            print("  ... not found, installing cargo/rustup from remote")
            cargo_install = Executable(os.path.join(this_dir, "install_rust.sh"))
            cargo_install_cache_path = os.path.join(spack_stack_dir, "cache", "rust-install")
            if os.path.isdir(cargo_install_cache_path):
                shutil.rmtree(cargo_install_cache_path)
            os.makedirs(cargo_install_cache_path)
            cargo_install(cargo_install_cache_path)
            shutil.rmtree(cargo_install_cache_path)
        # cargo-wrapper
        cargo_wrapper = os.path.join(cargo_home, "bin", "cargo-wrapper")
        print(f"Checking for {cargo_wrapper} ...")
        if which(cargo_wrapper):
            print(f"  ... found {cargo_wrapper}")
        else:
            print("  ... not found, creating {{cargo_wrapper}}")
            with open(cargo_wrapper, "w") as f:
                f.write(f"""#!/usr/bin/env bash
        
export PATH="{cargo_home}/bin:{default_path}"
export RUSTUP_HOME="{cargo_home}/rustup"
{cargo_path} $@
""")
            os.chmod(cargo_wrapper, 0o744)
        cargo_exe = Executable(cargo_wrapper)

    for root, dirs, files in os.walk(pkg.stage.source_path):
        if "Cargo.toml" in files:
            with working_dir(root):
                cargo_exe("fetch")
