import logging
import os
import shutil
from sys import platform

import llnl.util.tty as tty

from spack.extensions.stack.container_env import StackContainer
from spack.extensions.stack.stack_env import StackEnv, stack_path

description = "Create spack-stack environment (environment or container)"
section = "spack-stack"
level = "long"

default_env_name = "default"
default_env_path = stack_path("envs")


def default_site():
    if platform == "linux" or platform == "linux2":
        return "linux.default"
    elif platform == "darwin":
        return "macos.default"


def site_help():
    help_string = f'Pre-configured platform, or "{default_site()}" if no arg is given'
    help_string += os.linesep
    help_string += "Available options are: "
    help_string += os.linesep
    _, tiers, _ = next(os.walk(stack_path("configs", "sites")))
    for tier in tiers:
        help_string += "\t" + tier + os.linesep
        _, tier_sites, _ = next(os.walk(stack_path("configs", "sites", tier)))
        for site in list(tier_sites):
            help_string += "\t\t" + site + os.linesep
    return help_string


def template_help():
    _, template_dirs, _ = next(os.walk(stack_path("configs", "templates")))
    help_string = 'Environment template, default is "empty"' + os.linesep
    help_string += "Available options are: " + os.linesep
    for template in template_dirs:
        help_string += "\t" + template + os.linesep
    return help_string


def container_config_help():
    _, _, container_configs = next(os.walk(stack_path("configs", "containers")))
    # Exclude files like "README.md"
    container_configs = [x for x in container_configs if x.endswith(".yaml")]
    help_string = "Pre-configured container." + os.linesep
    help_string += "Available options are: " + os.linesep
    for config in container_configs:
        help_string += "\t" + config.rstrip(".yaml") + os.linesep
    return help_string


def container_specs_help():
    _, _, specs_lists = next(os.walk(stack_path("configs", "containers", "specs")))
    help_string = "List of specs to build in container." + os.linesep
    help_string += "Available options are: " + os.linesep
    for specs_list in specs_lists:
        help_string += "\t" + specs_list.rstrip(".yaml") + os.linesep
    return help_string


def setup_ctr_parser(subparser):
    """create container-specific parsing options"""

    subparser.add_argument("--container", required=True, help=container_config_help())

    subparser.add_argument("--specs", required=True, help=container_specs_help())

    subparser.add_argument(
        "--dir",
        type=str,
        required=False,
        default=default_env_path,
        help="Environment will be placed in <dir>/container/."
        " Default is {}/container/.".format(default_env_path),
    )


def setup_env_parser(subparser):
    """create environment-specific parsing options"""

    subparser.add_argument(
        "--dir",
        type=str,
        required=False,
        default=default_env_path,
        help="Environment will be placed in <dir>/<env-name>/.\n"
        "Default is {}/<env-name>/.".format(default_env_path),
    )

    subparser.add_argument(
        "--name",
        type=str,
        required=False,
        default=None,
        help="Environment name, defaults to <template>.<site>.<compiler>",
    )

    subparser.add_argument(
        "--template",
        type=str,
        required=False,
        dest="template",
        default="empty",
        help=template_help(),
    )

    subparser.add_argument(
        "--upstream",
        nargs="*",
        action="append",
        help="Include upstream environment (/path/to/spack-stack-x.y.z/envs/unified-env/install)",
    )

    subparser.add_argument(
        "--site", type=str, required=False, default=default_site(), help=site_help()
    )

    subparser.add_argument(
        "--prefix",
        type=str,
        required=False,
        default=None,
        help="Install prefix for spack packages and modules (not the spack environment).",
    )

    subparser.add_argument(
        "--modify-pkg",
        action="append",
        help="Modify selected package and place in an environment-specific repository",
    )

    subparser.add_argument(
        "--compiler",
        type=str,
        required=True,
        default=None,
        help="""Compiler to use. Must be a supported compiler for this site.""",
    )


def setup_create_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="env_type")

    env_parser = sp.add_parser("env", help="Create local Spack environment")
    ctr_parser = sp.add_parser("ctr", help="Create container.")

    setup_env_parser(env_parser)

    setup_ctr_parser(ctr_parser)


def container_create(args):
    """Create pre-configured container"""

    container = StackContainer(args.container, args.dir, args.specs)

    env_dir = container.env_dir
    if os.path.exists(env_dir):
        raise Exception("Env: {} already exists".format(env_dir))

    container.write()
    tty.msg("Created container {}".format(env_dir))


def dict_from_args(args):
    dict = {}
    dict["site"] = args.site
    dict["template"] = args.template
    dict["name"] = args.name
    dict["install_prefix"] = args.prefix
    dict["dir"] = args.dir
    dict["upstreams"] = args.upstream
    dict["modifypkg"] = args.modify_pkg
    dict["compiler"] = args.compiler

    return dict


def env_create(args):
    """Create pre-configured Spack environment.

    Args: args

    Returns:

    """

    stack_settings = dict_from_args(args)
    stack_env = StackEnv(**stack_settings)

    env_dir = stack_env.env_dir()
    if os.path.exists(env_dir):
        raise Exception("Environment: {} already exists".format(env_dir))

    logging.debug("Creating environment from command-line args")
    stack_env = StackEnv(**stack_settings)
    stack_env.write()
    stack_env.check_umask()
    tty.msg("Created environment {}".format(env_dir))


def stack_create(parser, args):
    if args.env_type == "env":
        env_create(args)
    elif args.env_type == "ctr":
        container_create(args)
