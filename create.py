#!/usr/bin/env python3

import argparse
from operator import index
import os
from os import listdir, path, makedirs, linesep
import sys
import shutil
from argparse import RawTextHelpFormatter

# Get directory of this script
stack_dir = path.dirname(path.realpath(__file__))

# Possible spack configuration files
valid_configs = ['compilers.yaml', 'config.yaml', 'mirrors.yaml',
                 'modules.yaml', 'packages.yaml', 'concretizer.yaml']

# Pass this value to --site for an empty config
empty_site = 'default'

def stack_path(*paths):
    return path.join(stack_dir, *paths)


def create_env_dir(env_name):
    # Create spack-stack/envs to hold envrionments, if it doesn't exist
    if not path.exists(stack_path('envs')):
        makedirs(stack_path('envs'))

    # Create env_dir
    env_dir = stack_path('envs', env_name)
    if not path.exists(env_dir):
        makedirs(env_dir)
        print("Created {} in {}".format(env_name, env_dir))
    else:
        sys.exit('Error: {} already exists'.format(env_dir))

    return env_dir


def copy_common_configs(env_dir):
    common_dir = stack_path('configs', 'common')
    common_configs = listdir(common_dir)
    shutil.copytree(common_dir, path.join(env_dir, 'common'))


def copy_site_configs(site, env_dir):
    site_dir = stack_path('configs', 'sites', site)
    shutil.copytree(site_dir, path.join(env_dir, 'site'))


def copy_app_config(app, env_dir):
    app_config = stack_path('configs', 'apps', app, 'spack.yaml')
    with open(app_config, "r") as f:
        contents = f.read()

    includes = []
    for config_type in ['site', 'common']:
        config_dir = stack_path(env_dir, config_type)
        if path.isdir(config_dir):
            configs = list(filter(lambda f: f in valid_configs, listdir(config_dir)))
            configs = map(lambda conf: '  - {}/{}'.format(config_type, conf), configs)
            includes += configs
    includes.insert(0, 'include:') if includes else includes.insert(0, '')
    new_contents = contents.replace('@CONFIG_INCLUDES@', linesep.join(includes))

    with open(path.join(env_dir, 'spack.yaml'), "w") as f:
        f.write(new_contents)


def copy_container_config(container, spec, env_dir):
    container_config = stack_path('configs', 'containers', container + '.yaml')
    with open(container_config, "r") as f:
        contents = f.read()

    common_package_config = stack_path('configs', 'common', 'packages.yaml')
    with open(common_package_config, "r") as f:
        common_package_contents = f.read()
    # Replace double colons in common_package_contents with single colons
    # due to a bug in spack that replaces '::' with ':":"' during concretization
    common_package_contents = common_package_contents.replace('::', ':')

    new_contents = contents.replace('@PACKAGE_CONFIG@', common_package_contents)
    new_contents = new_contents.replace('@SPEC@', spec)
    with open(path.join(env_dir, 'spack.yaml'), "w") as f:
        f.write(new_contents)


def check_inputs(app=None, site=None, container=None):
    if app:
        app_path = stack_path('configs', 'apps', app, 'spack.yaml')
        if not path.exists(app_path):
            sys.exit('Error: invalid app {}, "{}" does not exist'.format(app, app_path))
    if site:
        if not site == empty_site:
            site_path = stack_path('configs', 'sites', site)
            if not path.exists(site_path):
                sys.exit('Error: invalid site {}, "{}" does not exist'.format(
                    site, site_path))
    if container:
        container_path = stack_path('configs', 'containers', container + '.yaml')
        if not path.exists(container_path):
            sys.exit('Error: invalid container config {}, "{}" does not exist'.format(
                container, container_path))

def site_help():
    _, site_dirs, _ = next(os.walk(stack_path('configs', 'sites')))
    help_string = 'Pre-configured platform, or "default" for an empty site.yaml.' + linesep
    help_string += 'Defaults to "default" if no arg is given' + linesep
    help_string += 'Available options are: ' + linesep
    for site in site_dirs:
        help_string += '\t' + site + linesep
    return help_string


def app_help():
    _, app_dirs, _ = next(os.walk(stack_path('configs', 'apps')))
    help_string = 'Application environment to build.' + linesep
    help_string += 'Available options are: ' + linesep
    for app in app_dirs:
        help_string += '\t' + app + linesep
    return help_string


def config_help():
    _, _, configs = next(os.walk(stack_path('configs', 'containers')))
    help_string = 'Pre-configured container.' + linesep
    help_string += 'Available options are: ' + linesep
    for config in configs:
        help_string += '\t' + config + linesep
    return help_string


def spec_help():
    help_string = 'Any valid spack spec, e.g. "wget" or "jedi-ufs-bundle-env".' + linesep
    return help_string

description_text = '''
    Create a pre-configured Spack environment or container in spack-stack/envs/<env>.
'''

epilog_text = """
Example usage:
    source setup.sh
    # Option 1: To create a local environment
    ./create.py environment --site default --app ufs [--name ufs-env] [--exclude-common-configs]
    spack env activate [-p] envs/ufs-env
    spack concretize
    spack install
    # Option 2: create a container
    ./create.py container --site docker-ubuntu-gcc --app jedi-ufs
    cd envs/jedi-ufs.docker-ubuntu-gcc
    spack containerize > Dockerfile
    docker build -t myimage .
    docker run -it myimage
"""
parser = argparse.ArgumentParser(description=description_text,
                                 epilog=epilog_text,
                                 formatter_class=RawTextHelpFormatter)
subparsers = parser.add_subparsers(help='help for subcommand', dest='subcommand')

env_parser = subparsers.add_parser('environment', help='Create local environment')
env_parser.add_argument('--site', type=str, required=False, nargs='?', default='default', help=site_help())
env_parser.add_argument('--app', type=str, required=True, help=app_help())
env_parser.add_argument('--name', type=str, required=False,
                    help='Optional name for env dir. Defaults to app.site name.')
env_parser.add_argument('--exclude-common-configs', required=False,
                    default=False, action='store_true', help='Ignore configs configs/common when creating environment')

con_parser = subparsers.add_parser('container', help='Create container')
con_parser.add_argument('--config', type=str, required=True, help=config_help())
con_parser.add_argument('--spec', type=str, required=True, help=spec_help())

args = parser.parse_args()

create_env = False
create_con = False
if args.subcommand == 'environment':
    create_env = True
elif args.subcommand == 'container':
    create_con = True
else:
    parser.print_help()
    sys.exit(-1)

if create_env:
    site = args.site
    app = args.app
    exclude_common_configs = args.exclude_common_configs
    env_name = args.name if args.name else "{}.{}".format(app, site)

    check_inputs(app=app, site=site)
    env_dir = create_env_dir(env_name)
    if not exclude_common_configs:
        copy_common_configs(env_dir)
    copy_site_configs(site, env_dir)
    copy_app_config(app, env_dir)
else:
    container = args.config
    spec = args.spec

    check_inputs(container=container)
    env_name = "{}.{}".format(spec, container) 
    env_dir = create_env_dir(env_name)
    copy_container_config(container, spec, env_dir)