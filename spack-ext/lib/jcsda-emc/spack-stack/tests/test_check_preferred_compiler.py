import shutil
import os

import pytest

import spack
import spack.environment as ev
from spack.llnl.util.filesystem import filter_file
import spack.main

spack_stack_cmd = spack.main.SpackCommand("stack")


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, ".spackstack")):
        return None

    return os.path.join(stack_dir, *paths)


test_dir = stack_path("envs", "unit-tests", "check-preferred-compiler")


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_check_preferred_compiler():
    if not test_dir:
        return

    os.makedirs(test_dir, exist_ok=True)
    env_root_dir = os.path.join(test_dir)

    env_name = "test1"
    env_dir = os.path.join(env_root_dir, env_name)
    module_dir = os.path.join(env_dir, "modules")
    if os.path.exists(env_dir):
        shutil.rmtree(env_dir)

    spack_stack_cmd("create", "env", "--dir", env_root_dir, "--name", env_name, "--compiler", "clang")

    # Create empty env
    env = ev.Environment(manifest_dir=env_dir)
    ev.activate(env)

    packages_definition = """
packages:
  gcc:
    externals:
    - spec: gcc@11.5.0 languages:='c,c++,fortran'
      prefix: /usr
      extra_attributes:
        compilers:
          c: /usr/bin/gcc
          cxx: /usr/bin/g++
          fortran: /usr/bin/gfortran
  llvm:
    externals:
    - spec: llvm@21.1.0
      prefix: /usr
      extra_attributes:
        compilers:
          c: /usr/bin/clang
          cxx: /usr/bin/clang++
          fortran: /usr/bin/flang-new
  mpi:
    buildable: false
  openmpi:
    externals:
    - spec: openmpi@5.0.8 ~internal-hwloc +two_level_namespace
      prefix: /usr
  zlib:
    prefer:
    - '%c=gcc'
  libszip:
    require:
    - '%c=gcc'
"""
    site_packages_yaml = os.path.join(env_dir, "site", "packages.yaml")
    if os.path.exists(site_packages_yaml):
        raise Exception("Not implemented: appending to existing {site_packages_yaml}")
    with open(site_packages_yaml, 'w') as f:
        f.write(packages_definition)

    cmd = spack.main.SpackCommand("add")
    cmd("gcc", "openmpi", "zlib", "libszip")

    cmd = spack.main.SpackCommand("concretize")
    cmd("--force", "--fresh")

    spack_stack_cmd("check-preferred-compiler")

    filter_file("%c=gcc", "%c=llvm", site_packages_yaml, string=True)

    with pytest.raises(Exception) as error:
        spack_stack_cmd("check-preferred-compiler")
    # There is only one compiler mismatch for libszip.
    # The concretizer chooses to use LLVM for zlib because
    # of the general compiler preference (common/packages.yaml),
    # i.e. it ignores the zlib-specific preference. The tool
    # check-preferred-compiler correctly reports a violation
    # of the hard requirement for libszip, but allows zlib
    # to be built with the default compiler instead of the soft req.
    assert "Detected 1 compiler mismatch" in str(error)
