import os

import pytest

import spack
import spack.main

stack_create = spack.main.SpackCommand("stack")


# Find spack-stack directory assuming this Spack instance
# is a submodule of spack-stack.
def stack_path(*paths):
    stack_dir = os.path.dirname(spack.paths.spack_root)

    if not os.path.exists(os.path.join(stack_dir, ".spackstack")):
        return None

    return os.path.join(stack_dir, *paths)


test_dir = stack_path("envs", "unit-tests", "stack-create")


def all_templates():
    template_path = stack_path("configs", "templates")
    if template_path:
        _, templates, _ = next(os.walk(template_path))
        return list(templates)
    else:
        return None


def all_sites():
    site_path = stack_path("configs", "sites")
    if site_path:
        sites = []
        _, tiers, _ = next(os.walk(site_path))
        for tier in tiers:
            _, tier_sites, _ = next(os.walk(stack_path("configs", "sites", tier)))
            sites += list(tier_sites)
        return sites
    else:
        return None


def all_containers():
    container_path = stack_path("configs", "containers")
    if container_path:
        _, _, containers = next(os.walk(container_path))
        # Exclude files like "README.md"
        containers = [x for x in containers if x.endswith(".yaml")]
        return containers
    else:
        return None


def all_specs():
    specs_path = stack_path("configs", "containers", "specs")
    if specs_path:
        _, _, specs = next(os.walk(specs_path))
        # Exclude files like "README.md"
        specs = [x for x in specs if x.endswith(".yaml")]
        return specs
    else:
        return None


@pytest.mark.extension("stack")
@pytest.mark.parametrize("template", all_templates())
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_apps(template):
    if not template:
        return
    stack_create("create", "env", "--template", template, "--dir", test_dir, "--overwrite")


@pytest.mark.extension("stack")
@pytest.mark.parametrize("site", all_sites())
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_sites(site):
    if not site:
        return
    stack_create("create", "env", "--site", site, "--dir", test_dir, "--overwrite")


@pytest.mark.extension("stack")
@pytest.mark.parametrize("container", all_containers())
@pytest.mark.parametrize("spec", all_specs())
# @pytest.mark.filterwarnings("ignore::UserWarning")
def test_containers(container, spec):
    if not container or not spec:
        return
    container_wo_ext = os.path.splitext(container)[0]
    spec_wo_ext = os.path.splitext(spec)[0]
    stack_create(
        "create",
        "ctr",
        "--container",
        container_wo_ext,
        "--spec",
        spec_wo_ext,
        "--dir",
        test_dir,
        "--overwrite",
    )


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_modulesys():
    modsystems = {"lmod", "tcl"}
    for modulesys in modsystems:
        stack_create(
            "create",
            "env",
            "--site",
            "hera",
            "--name",
            "modulesys_test",
            "--dir",
            test_dir,
            "--overwrite",
            "--modulesys",
            modulesys,
        )
    modules_yaml_path = os.path.join(test_dir, "modulesys_test", "common", "modules.yaml")
    with open(modules_yaml_path, "r") as f:
        modules_yaml_txt = f.read()
    assert "%s:" % modulesys in modules_yaml_txt
    assert "%s:" % list(modsystems.difference(modulesys))[0] not in modules_yaml_txt


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_upstream():
    stack_create(
        "create",
        "env",
        "--site",
        "hera",
        "--name",
        "upstream_test",
        "--dir",
        test_dir,
        "--overwrite",
        "--upstream",
        "/test/path/to/upstream/env",
    )
    spack_yaml_path = os.path.join(test_dir, "upstream_test", "spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml_txt = f.read()
    assert "install_tree: /test/path/to/upstream/env" in spack_yaml_txt
    assert (
        "repos: [$env/envrepo]" not in spack_yaml_txt
    ), "--modify-pkg functionality modified spack.yaml without being called"


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_modifypkg():
    stack_create(
        "create",
        "env",
        "--site",
        "hera",
        "--name",
        "modifypkg_test",
        "--dir",
        test_dir,
        "--overwrite",
        "--modify-pkg",
        "hdf5",
        "--modify-pkg",
        "ufs-weather-model-env",
    )
    env_dir = os.path.join(test_dir, "modifypkg_test")
    spack_yaml_path = os.path.join(test_dir, "modifypkg_test/spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml_txt = f.read()
    assert "repos: [$env/envrepo]" in spack_yaml_txt, "--modify-pkg did not update spack.yaml"
    custom_hdf5_path = os.path.join(test_dir, "modifypkg_test/envrepo/packages/hdf5/package.py")
    assert os.path.exists(
        custom_hdf5_path
    ), "'--modify-pkg hdf5' failed to create custom package.py"
    custom_ufswm_path = os.path.join(
        test_dir, "modifypkg_test/envrepo/packages/ufs-weather-model-env/package.py"
    )
    assert os.path.exists(
        custom_ufswm_path
    ), "'--modify-pkg ufs-weather-model-env' failed to create custom package.py"
    spack_cmd = spack.util.executable.which("spack")
    hdf5_spack_path = spack_cmd(
        "--env-dir", env_dir, "location", "--package-dir", "hdf5", output=str
    ).strip()
    assert custom_hdf5_path == os.path.join(
        hdf5_spack_path, "package.py"
    ), "Incorrect hdf5 location in modifypkg_test"
    ufswm_spack_path = spack_cmd(
        "--env-dir", env_dir, "location", "--package-dir", "ufs-weather-model-env", output=str
    ).strip()
    assert custom_ufswm_path == os.path.join(
        ufswm_spack_path, "package.py"
    ), "Incorrect ufs-weather-model-env location in modifypkg_test"
    netcdfc_spack_path = spack_cmd(
        "--env-dir", env_dir, "location", "--package-dir", "netcdf-c", output=str
    ).strip()
    assert (
        os.path.join(spack.paths.packages_path, "packages/netcdf-c") == netcdfc_spack_path
    ), "Incorrect netcdf-c location in modifypkg_test"
