import os
import shutil

import pytest

import spack
import spack.main
import spack.util.spack_yaml as syaml

from spack.extensions.stack.stack_env import compiler_name_and_version_from_string

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
    env_name = "modulesys_test"
    stack_create(
        "create",
        "env",
        "--site",
        "hera",
        "--name",
        env_name,
        "--dir",
        test_dir,
        "--compiler",
        "gcc"
    )
    spack_yaml_path = os.path.join(test_dir, env_name, "spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml = syaml.load_config(f)

    includes = spack_yaml["spack"]["include"]

    # For site 'hera', we expect 'lmod' to be used.
    # This should result in 'modules_lmod.yaml' being included.
    assert os.path.join("common", "modules_lmod.yaml") in includes
    assert os.path.join("common", "modules_tcl.yaml") not in includes


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_compilers():
    for compiler in ["gcc-13.2.1", "oneapi-2024.2.1", "gcc"]:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

        env_name = "compiler_test"
        stack_create(
            "create",
            "env",
            "--site",
            "blackpearl",
            "--name",
            env_name,
            "--dir",
            test_dir,
            "--compiler",
            compiler
        )

        spack_yaml_path = os.path.join(test_dir, env_name, "spack.yaml")
        with open(spack_yaml_path, "r") as f:
            spack_yaml = syaml.load_config(f)

        includes = spack_yaml["spack"]["include"]

        # Check for common compiler-specific package file, which sets compiler preference.
        # This is equivalent to the old test's check on common/packages.yaml.
        compiler_name, _ = compiler_name_and_version_from_string(compiler)
        expected_common_include = os.path.join("common", f"packages_{compiler_name}.yaml")
        common_config_path = stack_path("configs", "common", f"packages_{compiler_name}.yaml")
        if common_config_path and os.path.exists(common_config_path):
            assert expected_common_include in includes

        # Check for site-specific compiler file, which defines the compiler.
        # This is equivalent to the old test's check on site/packages.yaml.
        # This file is optional, so we only assert its inclusion if the source file exists.
        site_config_file = f"packages_{compiler}.yaml"
        site_configs_dir = None
        # This logic to find the site dir is a bit fragile but necessary for a thorough test.
        for tier in ["tier1", "tier2"]:
            d = stack_path("configs", "sites", tier, "blackpearl")
            if d and os.path.isdir(d):
                site_configs_dir = d
                break

        if site_configs_dir:
            site_config_path = os.path.join(site_configs_dir, site_config_file)
            if os.path.exists(site_config_path):
                assert os.path.join("site", site_config_file) in includes


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_upstream():
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # 1. Set up a base environment to be used as an upstream
    base_env_dir = os.path.join(test_dir, "base_env")
    base_env_install = os.path.join(base_env_dir, "install")
    os.makedirs(os.path.join(base_env_install, ".spack-db/"))
    with open(os.path.join(base_env_dir, "spack.yaml"), "w") as f:
        f.write("spack:\n  upstreams: {}\n")

    # 2. Create a new environment that uses the base environment as an upstream
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
        base_env_install,
    )

    # 3. Assertions
    spack_yaml_path = os.path.join(test_dir, "chainedA", "spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml_txt = f.read()

    base_env_install_realpath = os.path.realpath(base_env_install)
    assert base_env_install_realpath in spack_yaml_txt
    assert (
        "repos: [$env/envrepo]" not in spack_yaml_txt
    ), "--modify-pkg functionality modified spack.yaml without being called"


@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_layered_upstreams():
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # 1. Set up base_env
    base_env_dir = os.path.join(test_dir, "base_env")
    base_env_install_path = os.path.join(base_env_dir, "install")
    os.makedirs(os.path.join(base_env_install_path, ".spack-db"))
    with open(os.path.join(base_env_dir, "spack.yaml"), "w") as f:
        f.write("spack:\n  specs: {}\n")
    os.makedirs(os.path.join(base_env_dir, "envrepo"))
    with open(os.path.join(base_env_dir, "envrepo", "file"), "w") as f:
        f.write("bad")

    # 2. Set up chainedA env, pointing to base_env
    chainedA_dir = os.path.join(test_dir, "chainedA")
    if os.path.exists(chainedA_dir):
        shutil.rmtree(chainedA_dir)
    base_env_install_realpath = os.path.realpath(base_env_install_path)
    stack_create(
        "create", "env", "--site", "hera", "--name", "chainedA",
        "--dir", test_dir, "--compiler", "gcc",
        "--upstream", base_env_install_path
    )
    chainedA_install_path = os.path.join(chainedA_dir, "install")
    os.makedirs(os.path.join(chainedA_install_path, ".spack-db"))
    with open(os.path.join(chainedA_dir, "envrepo", "file"), "w") as f:
        f.write("good") # nearer upstream should take precedence

    # 3. Create chainedB env using chainedA as upstream
    chainedB_dir = os.path.join(test_dir, "chainedB")
    if os.path.exists(chainedB_dir):
        shutil.rmtree(chainedB_dir)
    chainedA_install_realpath = os.path.realpath(chainedA_install_path)
    stack_create(
        "create", "env", "--site", "hera", "--name", "chainedB",
        "--dir", test_dir, "--compiler", "gcc",
        "--upstream", chainedA_install_realpath
    )

    # 4. Assertions
    spack_yaml_path = os.path.join(chainedB_dir, "spack.yaml")
    with open(spack_yaml_path, "r") as f:
        spack_yaml_txt = f.read()
    assert base_env_install_realpath in spack_yaml_txt
    assert chainedA_install_realpath in spack_yaml_txt
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
    assert (
        os.path.join(spack.config.get("repos")['builtin'].replace("${SPACK_STACK_DIR}", os.getenv("SPACK_STACK_DIR")), "packages/netcdf_c") == netcdfc_spack_path
    ), "Incorrect netcdf-c location in modifypkg_test"

@pytest.mark.extension("stack")
@pytest.mark.filterwarnings("ignore::UserWarning")
def test_treatwarningsaserrors():
    with pytest.raises(Exception, match="packages_fj.yaml not found"):
        stack_create(
            "create",
            "env",
            "--site",
            "blueback",
            "--name",
            "treatwarningsaserrors_test",
            "--dir",
            test_dir,
            "--compiler",
            "fj",
            "--treat-warnings-as-errors"
        )
