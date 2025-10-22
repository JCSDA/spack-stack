#!/usr/bin/env spack-python

import argparse

parser = argparse.ArgumentParser(description="Your script description")

parser.add_argument('-n', '--no-scheduler', action='store_true', help="Run installation on local node (no job scheduler)")
parser.add_argument('-s', '--skip-go-rust-handling', action='store_true', help="Skip handling of Go/Rust dep fetching when using parallel job scheduler")
parser.add_argument('-c', '--concretize-args', type=str, help="Concretize arguments (provide a single string)")
parser.add_argument('-i', '--install-args', type=str, help="Install arguments (provide a single string)")
parser.add_argument('-r', '--redeploy-existing', action='store_true', help="Redeploy existing deployments")

parser.add_argument('deployments', nargs='*', help="List of deployments to apply (default is all)")

args = parser.parse_args()

import collections
from datetime import datetime
import logging
import os
import subprocess
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

nowdate = datetime.now().strftime("%Y%m%d-%H%M")
logdir = os.path.join(spack_stack_dir, "deploy_logs")
os.makedirs(logdir, exist_ok=True)

def get_env_dir_basename(deployment):
    base = deployment["template"]
    base = base.replace("unified-dev", "ue")
    base = base.replace("-dev", "")
    return "-".join([base, deployment["compiler"]])

def deployment_already_exists(env_dir_basename, args):
    path_to_check = os.path.join(spack_stack_dir, "envs", env_dir_basename)
    return os.path.isdir(path_to_check)

def is_deployment_requested(env_dir_basename, deployment, args):
    if deployment["template"] in args.deployments:
        return True
    if deployment["template"] + "/" + deployment["compiler"] in args.deployments:
        return True
    if args.redeploy_existing:
        return True
    return not deployment_already_exists(env_dir_basename, args)

def get_create_env_settings(env_dir_basename, deployment, deployments):
    config_dict = {}
    config_dict["site"] = "acorn"
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

def run_batch_install(batch_config, deployment, env_dir_full_path, specs_str, logfile, logfilepath, suffix=".batch_install"):
    if "walltime" in deployment:
        walltime = deployment["walltime"]
    elif "default_walltime" in batch_config:
        walltime = batch_config["default_walltime"]
    else:
        assert False, "Set deployment-specific walltime or batch_config:default_walltime" 
    cmd = [
        "qsub",
        "-o", logfilepath + suffix,
        "-e", logfilepath + suffix,
        "-A", batch_config["account"],
        "-q", batch_config["queue"],
        "-l", "walltime=" + walltime + ",select=1:ncpus=12",
        "-V", "-Wblock=true", "--",
        which("spack").path, "--env", env_dir_full_path,
        "install", "--concurrent-packages", "3", "--jobs", "4",
    ]
    cmd.extend(specs_str)
    subprocess.run(cmd, stdout=logfile, stderr=logfile, check=True)

# Load deployments.yaml configuration
print("Loading deployments.yaml")
script_directory = os.path.dirname(os.path.abspath(__file__))
deployments_yaml_path = os.path.join(script_directory, "deployments.yaml")
with open(deployments_yaml_path, "r") as f:
    deployments_yaml = yaml.safe_load(f)

# Generate deployments object, including iterating over compilers
deployments = collections.OrderedDict()

for _deployment in deployments_yaml["deployments"]:
    for _compiler in _deployment["compilers"]:
        deployment = _deployment.copy()
        del(deployment["compilers"])
        deployment["compiler"] = _compiler
        env_dir_basename = get_env_dir_basename(deployment)
        deployments[env_dir_basename] = deployment
        print(f"Registered deployment: {deployment['template']}/{deployment['compiler']} ({env_dir_basename})")

print("="*30)

# Create and install each deployment
for env_dir_basename, deployment in deployments.items():
    if not is_deployment_requested(env_dir_basename, deployment, args):
        print(f"Skipping existing deployment: {deployment['template']}/{deployment['compiler']} ({env_dir_basename})")
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
    logfile = open(logfilepath, "a")
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

    # Concretize environment
    concretize_args = SimpleNamespace(
        test = False, ###
        quiet = False,
        fresh = True, ###
        force = True,
    )
    print(f"... concretizing ...")
    with redirect_stdout(logfile), redirect_stderr(logfile):
        concretize(None, concretize_args)

    # Fetch packages
    if "packages_to_install" in deployment:
        specs_str = deployment["packages_to_install"]
    else:
        specs_str = []
    fetch_args = SimpleNamespace(
        missing = True,
        no_checksum = False,
        dependencies = bool(specs_str),
        specs = specs_str,
    )
    print(f"... fetching packages ...")
    with redirect_stdout(logfile), redirect_stderr(logfile):
        fetch(None, fetch_args)

    # Install packages
    print("... installing" + (" specs: " +" ".join(specs_str) if specs_str else "") + " ...")
    logfile.flush()
    if args.no_scheduler:
        specs = env.all_matching_specs(*specs_str)
        env.install_specs(specs)
    else:
        if not args.skip_go_rust_handling:
            run_batch_install(deployments_yaml["batch_config"], deployment, env_dir_full_path, ["rust", "go"], logfile, logfilepath, suffix=".rustgo")
            logfile.flush()
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
            logfile.flush()
            subprocess.run(
                os.path.join(spack_stack_dir, "util", "fetch_go_deps.py"),
                env=shell_env,
                stdout=logfile,
                stderr=logfile,
                check=True,
                text=True,
            )
            logfile.flush()
        run_batch_install(deployments_yaml["batch_config"], deployment, env_dir_full_path, specs_str, logfile, logfilepath)
        logfile.flush()

    # Generate modules
    print(f"... writing package modules ...")
    subprocess.run(
        ["spack", "-e", env_dir_full_path, "module", "lmod", "refresh", "--yes-to-all", "--upstream-modules"],
        stdout=logfile,
        stderr=logfile,
        check=True,
        text=True,
    )
    logfile.flush()

    # Meta modules
    print(f"... writing metamodules ...")
    setup_meta_modules()

    logfile.close()

    print(f"... done.")
