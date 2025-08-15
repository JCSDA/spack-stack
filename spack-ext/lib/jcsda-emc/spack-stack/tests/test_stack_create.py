import os
import re
import shutil

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
        #sites = {}
        sites = []
        _, tiers, _ = next(os.walk(site_path))
        for tier in tiers:
            _, tier_sites, _ = next(os.walk(stack_path("configs", "sites", tier)))
            for site in tier_sites:
                _, _, files_in_site_dir = next(os.walk(stack_path("configs", "sites", tier, site)))
                compilers = []
                for file in files_in_site_dir:
                    if file.startswith("packages_") and file.endswith(".yaml"):
                        compilers.append(file.replace("packages_", "").replace(".yaml", ""))
                sites.append([site, compilers])
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
    stack_create(
        "create",
        "env",
        "--template",
        template,
        "--dir",
        test_dir,
        "--compiler",
        "gcc"
    )


@pytest.mark.extension("stack")
@pytest.mark.parametrize("site", all_sites())
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_sites(site):
    if not site:
        return
    name = site[0]
    compilers = site[1]
    # Assign dummy gcc compiler for sites without packages_*.yaml
    if not compilers:
        compilers = ["gcc"]
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    for compiler in compilers:
        stack_create(
            "create",
            "env",
            "--site",
            name,
            "--dir",
            test_dir,
            "--compiler",
            compiler
        )


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
        test_dir
    )


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_modules():
    stack_create(
        "create",
        "env",
        "--site",
        "hera",
        "--name",
        "modulesys_test",
        "--dir",
        test_dir,
        "--compiler",
        "gcc"
    )
    modules_yaml_path = os.path.join(test_dir, "modulesys_test", "common", "modules.yaml")
    with open(modules_yaml_path, "r") as f:
        modules_yaml_txt = f.read()
    assert "%s:" % "lmod" in modules_yaml_txt
    assert "%s:" % "tcl" not in modules_yaml_txt


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_compilers():
    for compiler in ["gcc-13.2.1", "oneapi-2025.1.0"]:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        stack_create(
            "create",
            "env",
            "--site",
            "blackpearl",
            "--name",
            "compiler_test",
            "--dir",
            test_dir,
            "--compiler",
            compiler
        )
        legacy_compiler_name, compiler_version = (
            lambda m: (compiler[:m.start()], compiler[m.start()+1:]) if m else (compiler, ''))(re.search(r'-(?=\d)', compiler)
        )
        if legacy_compiler_name in spack.aliases.LEGACY_COMPILER_TO_BUILTIN.keys():
            builtin_compiler_name = spack.aliases.LEGACY_COMPILER_TO_BUILTIN[legacy_compiler_name]
        else:
            builtin_compiler_name = legacy_compiler_name
        site_packages_yaml_path = os.path.join(test_dir, "compiler_test", "site", "packages.yaml")
        with open(site_packages_yaml_path, "r") as f:
            site_packages_yaml = f.read()
        assert f"{builtin_compiler_name}@{compiler_version}" in site_packages_yaml
        common_packages_yaml_path = os.path.join(test_dir, "compiler_test", "common", "packages.yaml")
        with open(common_packages_yaml_path, "r") as f:
            common_packages_yaml = f.read()
        assert f"%{legacy_compiler_name}" in common_packages_yaml


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_upstream():
    base_env = os.path.join(test_dir, "base_env/install/")
    os.makedirs(os.path.join(base_env, ".spack-db/"), exist_ok=True)
    base_env_spack_yaml_path = os.path.realpath(os.path.join(base_env, "../spack.yaml"))
    f_base_env = open(base_env_spack_yaml_path, "w")
    f_base_env.write("spack:\n  dummytag: dummyvalue")
    f_base_env.close()
    stack_create(
        "create",
        "env",
        "--site",
        "hera",
        "--name",
        "chainedA",
        "--dir",
        test_dir,
        "--compiler",
        "gcc",
        "--upstream",
        base_env,
    )
    spack_yaml_path = os.path.join(test_dir, "chainedA", "spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml_txt = f.read()
    assert f"install_tree: {base_env}" in spack_yaml_txt
    assert (
        "repos: [$env/envrepo]" not in spack_yaml_txt
    ), "--modify-pkg functionality modified spack.yaml without being called"


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_layered_upstreams():
    os.makedirs(os.path.join(test_dir, "chainedA/install/.spack-db/"))
    os.makedirs(os.path.join(test_dir, "base_env/envrepo/"))
    os.makedirs(os.path.join(test_dir, "chainedA/envrepo/"))
    f_base_env_envrepo_file_path = os.path.join(test_dir, "base_env/envrepo/file")
    f_chainedA_envrepo_file_path = os.path.join(test_dir, "chainedA/envrepo/file")
    f_base_env_envrepo_file = open(f_base_env_envrepo_file_path, "w")
    f_chainedA_envrepo_file = open(f_chainedA_envrepo_file_path, "w")
    f_base_env_envrepo_file.write("bad")
    f_chainedA_envrepo_file.write("good")
    f_base_env_envrepo_file.close()
    f_chainedA_envrepo_file.close()
    stack_create(
        "create",
        "env",
        "--site",
        "hera",
        "--name",
        "chainedB",
        "--dir",
        test_dir,
        "--compiler",
        "gcc",
        "--upstream",
        os.path.join(test_dir, "chainedA/install/")
    )
    spack_yaml_path = os.path.join(test_dir, "chainedB", "spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml_txt = f.read()
    assert "/base_env/install/" in spack_yaml_txt
    assert "/chainedA/install/" in spack_yaml_txt
    file_path = os.path.join(test_dir, "chainedB/envrepo/file")
    with open(file_path, "r") as f:
        assert "good" in f.read()


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
        "--compiler",
        "gcc",
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
        test_dir, "modifypkg_test/envrepo/packages/ufs_weather_model_env/package.py"
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
        "--env-dir", env_dir, "location", "--package-dir", "ufs_weather_model_env", output=str
    ).strip()
    assert custom_ufswm_path == os.path.join(
        ufswm_spack_path, "package.py"
    ), "Incorrect ufs-weather-model-env location in modifypkg_test"
    netcdfc_spack_path = spack_cmd(
        "--env-dir", env_dir, "location", "--package-dir", "netcdf_c", output=str
    ).strip()
    print("DH DEBUG 1:", os.path.join(spack.config.get("repos")['builtin'], "packages/netcdf_c"))
    print("DH DEBUG 2:", netcdfc_spack_path)
    assert (
        os.path.join(spack.config.get("repos")['builtin'].replace("${SPACK_STACK_DIR}", os.getenv("SPACK_STACK_DIR")), "packages/netcdf_c") == netcdfc_spack_path
    ), "Incorrect netcdf-c location in modifypkg_test"
