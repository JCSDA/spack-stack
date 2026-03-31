import shutil
import os

import pytest

import spack
import spack.environment as ev
import spack.main

spack_stack_cmd = spack.main.SpackCommand("stack")


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, ".spackstack")):
        return None

    return os.path.join(stack_dir, *paths)


test_dir = stack_path("envs", "unit-tests", "setup-meta-modules")


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_setup_meta_modules():
    if not test_dir:
        return

    os.makedirs(test_dir, exist_ok=True)
    env_root_dir = os.path.join(test_dir)

    env_name = "test1"
    env_dir = os.path.join(env_root_dir, env_name)
    module_dir = os.path.join(env_dir, "modules")
    if os.path.exists(env_dir):
        shutil.rmtree(env_dir)

    spack_stack_cmd("create", "env", "--dir", env_root_dir, "--name", env_name, "--compiler", "gcc")

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
  mpi:
    buildable: false
  openmpi:
    externals:
    - spec: openmpi@5.0.8 ~internal-hwloc +two_level_namespace
      prefix: /usr
"""
    site_packages_yaml = os.path.join(env_dir, "site", "packages.yaml")
    if os.path.exists(site_packages_yaml):
        raise Exception("Not implemented: appending to existing {site_packages_yaml}")
    with open(site_packages_yaml, 'w') as f:
        f.write(packages_definition)

    cmd = spack.main.SpackCommand("concretize")
    cmd("--force", "--fresh")

    cmd = spack.main.SpackCommand("install")
    cmd("--add", "--no-cache", "gcc", "openmpi")

    cmd = spack.main.SpackCommand("module")
    cmd("tcl", "refresh", "--yes")

    spack_stack_cmd("setup-meta-modules")

    expected_comp_meta_module = os.path.join(module_dir, "Core", "stack-gcc", "11.5.0")
    assert(
        os.path.exists(expected_comp_meta_module),
        f"Expected module {expected_comp_meta_module} not found"
    )

    expected_mpi_meta_module = os.path.join(module_dir, "gcc", "11.5.0", "stack-openmpi", "5.0.8")
    assert(
        os.path.exists(expected_mpi_meta_module),
        f"Expected module {expected_mpi_meta_module} not found"
    )

    # Test "view: true"
    cmd = spack.main.SpackCommand("env")
    cmd("view", "enable")
    cmd("view", "regenerate")

    spack_stack_cmd("setup-meta-modules")

    expected_venv_meta_module = os.path.join(module_dir, "Core", "stack-venv", "default")

    assert(
        os.path.exists(expected_venv_meta_module),
        f"Expected module {expected_venv_meta_module} not found"
    )

    # Test explicitly configured view
    view_config = """view:
    myview:
      root: views/myview
"""
    env_yaml = os.path.join(env_dir, "spack.yaml")
    with open(env_yaml, "r") as f:
        content = f.read()
    content = content.replace("view: true", view_config)
    with open(env_yaml, "w") as f:
        f.write(content)

    cmd("view", "regenerate")

    expected_venv_meta_module = os.path.join(module_dir, "Core", "stack-venv", "myview")

    assert(
        os.path.exists(expected_venv_meta_module),
        f"Expected module {expected_venv_meta_module} not found"
    )
