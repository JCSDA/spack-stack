#!/usr/bin/env spack-python

import argparse

parser = argparse.ArgumentParser(description="Your script description")

parser.add_argument('-n', '--no-scheduler', action='store_true', help="Run installation on local node (no job scheduler)")
parser.add_argument('-x', '--skip-go-rust-handling', action='store_true', help="Skip handling of Go/Rust dep fetching when using parallel job scheduler")
parser.add_argument('-r', '--redeploy-existing', action='store_true', help="Redeploy existing deployments (default is skip existing env dirs)")
parser.add_argument('-s', '--site', type=str, help='Site name override')
parser.add_argument('-u', '--until', choices=("create", "concretize", "validate", "fetch", "install"), help='Carry out steps up to and including')

parser.add_argument('deployments', nargs='*', help="List of deployments to apply (default is all; specify template+compiler with, e.g., 'unified-dev%%oneapi@2024.2.1')")

args = parser.parse_args()

import collections
from datetime import datetime
import logging
import os
import socket
import subprocess
import sys
import yaml
from contextlib import redirect_stdout, redirect_stderr
from types import SimpleNamespace

logging.basicConfig(level=logging.CRITICAL)

import spack.extensions
spack.extensions.load_extension("stack")
from spack.extensions.stack.cmd.stack_cmds.create import *
from spack.extensions.stack.meta_modules import setup_meta_modules
import spack.environment
from spack.cmd.concretize import concretize
from spack.cmd.fetch import fetch
from spack.cmd.module import module
from spack import modules
from spack.util.executable import which

spack_stack_dir = os.getenv("SPACK_STACK_DIR")

sys.path.append(os.path.join(spack_stack_dir, "util"))
from show_duplicate_packages import show_duplicate_packages

nowdate = datetime.now().strftime("%Y%m%d-%H%M")
logdir = os.path.join(spack_stack_dir, "deploy_logs")
os.makedirs(logdir, exist_ok=True)

def get_site_and_tier(deployment={}):
    if args.site:
        return args.site, "tier1"
    if "site" in deployment:
        return deployment["site"], "tier1"
    fqdn = socket.getfqdn()
    if "acorn.wcoss2" in fqdn:
        return "acorn", "tier1"

def get_env_dir_basename(deployment):
    base = deployment["template"]
    base = base.replace("unified-dev", "ue")
    base = base.replace("-dev", "")
    return "-".join([base, deployment["compiler"]])

def deployment_already_exists(env_dir_basename, args):
    path_to_check = os.path.join(spack_stack_dir, "envs", env_dir_basename)
    return os.path.isdir(path_to_check)

def is_deployment_requested(env_dir_basename, deployment, args):
    template = deployment["template"]
    template_and_compiler = deployment["template"] + "%" + deployment["compiler"]
    if args.deployments and (template not in args.deployments) and (template_and_compiler not in args.deployments):
        return False
    if template in args.deployments:
        return True
    if template_and_compiler in args.deployments:
        return True
    if args.redeploy_existing:
        return True
    return not deployment_already_exists(env_dir_basename, args)

def get_create_env_settings(env_dir_basename, deployment, deployments):
    config_dict = {}
    config_dict["site"] = get_site_and_tier(deployment=deployment)[0]
    config_dict["template"] = deployment["template"]
    config_dict["dir"] = os.path.join(spack_stack_dir, "envs")
    config_dict["name"] = env_dir_basename
    if "upstreams" in deployment:
        upstream_full_paths = []
        for upstream_template in deployment["upstreams"]:
            for _candidate_upstream in deployments.values():
                if (_candidate_upstream["template"] == upstream_template) and (_candidate_upstream["compiler"] == deployment["compiler"]):
                    upstream_basename = get_env_dir_basename(_candidate_upstream)
                    upstream_full_path = os.path.join(spack_stack_dir, "envs", upstream_basename, "install")
                    upstream_full_paths.append([upstream_full_path])
                    break
        config_dict["upstreams"] = upstream_full_paths
    config_dict["compiler"] = deployment["compiler"]

    return config_dict

def run_batch_install(batch_config, deployment, env_dir_full_path, logfile, logfilepath, packages_to_install=[], suffix=".batch_install"):
    if "walltime" in deployment:
        walltime = deployment["walltime"]
    elif "default_walltime" in batch_config:
        walltime = batch_config["default_walltime"]
    else:
        assert False, "Set deployment-specific walltime or batch_config:default_walltime" 

    if batch_config["scheduler"] == "pbspro":
        cmd = [
            "qsub",
            "-o", logfilepath + suffix,
            "-e", logfilepath + suffix,
            "-A", batch_config["account"],
            "-q", batch_config["queue"],
            "-l", "walltime=" + walltime + ",select=1:ncpus=12",
            "-V", "-Wblock=true", "--",
            which("spack").path, "--env", env_dir_full_path,
            "install", "--fail-fast", "--show-log-on-error",
            "--concurrent-packages", "4", "--jobs", "4",
        ]
    else:
        assert False, "batch_config:scheduler must be pbspro"
    if packages_to_install:
        cmd.extend(packages_to_install)
    logfile.write("Launching batch job:\n%s\n" % " ".join(cmd))
    subprocess.run(cmd, stdout=logfile, stderr=logfile, check=True)

assert not os.getenv("SPACK_ENV"), "$SPACK_ENV is set. Reconsider your choices."

# Load deployments.yaml configuration
site, tier = get_site_and_tier()
deployments_yaml_path = os.path.join(spack_stack_dir, "configs", "sites", tier, site, "deployments.yaml")
with open(deployments_yaml_path, "r") as f:
    deployments_yaml = yaml.safe_load(f)
print(f"Loading deployments.yaml for site {site}")

# Generate deployments object, including iterating over compilers
deployments = collections.OrderedDict()

for _deployment in deployments_yaml["deployments"]:
    for _compiler in _deployment["compilers"]:
        deployment = _deployment.copy()
        del(deployment["compilers"])
        deployment["compiler"] = _compiler
        if "packages_to_install" not in deployment:
            deployment["packages_to_install"] = []
        if "only_concretize_requested_packages" not in deployment:
            deployment["only_concretize_requested_packages"] = False
        env_dir_basename = get_env_dir_basename(deployment)
        deployments[env_dir_basename] = deployment
        print(f"  Registered deployment: {deployment['template']}/{deployment['compiler']} ({env_dir_basename})")

print("="*30)

# Create and install each deployment
for env_dir_basename, deployment in deployments.items():
    if not is_deployment_requested(env_dir_basename, deployment, args):
        print(f"Skipping deployment: {deployment['template']}/{deployment['compiler']} ({env_dir_basename})")
        continue
    print("="*30)
    # Create env based on config
    stack_settings = get_create_env_settings(env_dir_basename, deployment, deployments)
    env_dir_full_path = os.path.join(spack_stack_dir, "envs", env_dir_basename)
    if os.path.isdir(env_dir_full_path) and args.redeploy_existing:
        backup_dir_full_path = os.path.join(spack_stack_dir, "envs", env_dir_basename + "_bkp")
        assert not os.path.isdir(backup_dir_full_path), f"Backup dir {backup_dir_full_path} already exists"
        print(f"Moving {env_dir_full_path}\n  to {backup_dir_full_path}")
        os.rename(env_dir_full_path, backup_dir_full_path)
    logfilepath = os.path.join(logdir, nowdate + f".{deployment['template']}.{deployment['compiler']}.log")
    print(f"Log file: {logfilepath}")
    logfile = open(logfilepath, "a", buffering=1)
    logfile.write(str(deployment) + "\n")
    logfile.write(str(stack_settings) + "\n")
    print(f"Creating environment for {deployment['template']}/{deployment['compiler']}")
    print(f"  at {env_dir_full_path} ...")
    # Use equivalent of 'spack stack create env'
    stack_env = StackEnv(**stack_settings)
    stack_env.write()
    stack_env.check_umask()
    env = spack.environment.Environment(env_dir_full_path)
    spack.environment.activate(env)

    # Filter out unwanted packages before concretization
    if deployment["only_concretize_requested_packages"]:
        for root_spec in env.roots():
            if root_spec.name not in deployment["packages_to_install"]:
                env.remove(root_spec)
        env.write()

    if args.until == "create":
        spack.environment.deactivate()
        logfile.close()
        continue

    # Concretize environment
    print(f"... concretizing ...")
    with redirect_stdout(logfile), redirect_stderr(logfile):
        with env.write_transaction():
            concretized_specs = env.concretize()
            env.write()
        spack.environment.display_specs([concrete for _, concrete in concretized_specs])

    if args.until == "concretize":
        spack.environment.deactivate()
        logfile.close()
        continue

    print("... validating concretization ...")
    # Check for duplicate packages
    with open(os.path.join(env_dir_full_path, "spack.lock"), "r") as f:
        json_to_check = f.read()
    ignore_list = [] if "duplicates_to_ignore" not in deployment else deployment["duplicates_to_ignore"]
    ret = show_duplicate_packages(json_to_check, ignore_list=ignore_list)
    assert ret==0, "Duplicates found! Check spack.lock/show_duplicate_packages.py"

    # Fail if there packages that shouldn't be built with GCC are built with GCC:
    all_compilers = set()
    for spec in env.all_specs():
        for language in ("c", "cxx", "fortran"):
            if language not in spec: continue
            compiler_name = spec[language].name
            all_compilers.add(compiler_name)
            if "allowed_gcc_packages" in deployment:
                is_legal = not (compiler_name == "gcc" and spec.name not in deployment["allowed_gcc_packages"])
                assert is_legal, f"spec '{spec.name}/{spec.dag_hash()}' to be built with GCC but not in 'allowed_gcc_packages'!"

    if args.until == "validate":
        spack.environment.deactivate()
        logfile.close()
        continue

    # Fetch packages
    print(f"... fetching packages ...")
    for spec in env.all_specs():
        logfile.write(f"Fetching {spec.name}@{spec.version}/{spec.dag_hash(length=7)}\n")
        with redirect_stdout(logfile), redirect_stderr(logfile):
            spec.package.do_fetch()

    if args.until == "fetch":
        spack.environment.deactivate()
        logfile.close()
        continue

    # Install packages
    print("... installing", end="")
    if deployment["packages_to_install"]:
        print(" specs: " +" ".join(deployment["packages_to_install"]), end="")
    print(" ...")
    if args.no_scheduler:
        specs = env.all_matching_specs(*(" ".join(deployment["packages_to_install"])))
        env.install_specs(specs)
    else:
        logfile.write("Starting install jobs via job scheduler...\n")
        if not args.skip_go_rust_handling:
            run_batch_install(deployments_yaml["batch_config"], deployment, env_dir_full_path, logfile, logfilepath, packages_to_install=["rust", "go"], suffix=".rustgo")
            shell_env = os.environ.copy()
            shell_env["SPACK_ENV"] = env_dir_full_path
            subprocess.run(
                os.path.join(spack_stack_dir, "util", "fetch_cargo_deps.py"),
                env=shell_env,
                stdout=logfile,
                stderr=logfile,
                check=True,
                text=True,
            )
            subprocess.run(
                os.path.join(spack_stack_dir, "util", "fetch_go_deps.py"),
                env=shell_env,
                stdout=logfile,
                stderr=logfile,
                check=True,
                text=True,
            )
        run_batch_install(deployments_yaml["batch_config"], deployment, env_dir_full_path, logfile, logfilepath, packages_to_install=deployment["packages_to_install"])

    if args.until == "install":
        spack.environment.deactivate()
        logfile.close()
        continue

    # Generate modules
    print(f"... writing package modules ...")
    subprocess.run(
        ["spack", "--env", env_dir_full_path, "module", "lmod", "refresh", "--yes-to-all", "--upstream-modules"],
        stdout=logfile,
        stderr=logfile,
        check=True,
        text=True,
    )
    # Also generate a modules dir with a flat structure, i.e., everything is under Core with no metamodules
    cfg_hierarchy = "modules:default:lmod:hierarchy::[]"
    cfg_compilers = "modules:default:lmod:core_compilers::[%s]" % ",".join(all_compilers)
    cfg_root = "modules:default:roots:lmod:$env/modules_flat"
    subprocess.run(
        [
            "spack", "--env", env_dir_full_path,
            "--config", cfg_hierarchy,
            "--config", cfg_compilers,
            "--config", cfg_root,
            "module", "lmod", "refresh", "--yes-to-all"
        ]
    )

    # Meta modules
    print(f"... writing metamodules ...")
    setup_meta_modules()

    # Close this deployment's logfile and zero out spack.environment's stored config info
    spack.environment.deactivate()
    logfile.close()

    print(f"... done.")
