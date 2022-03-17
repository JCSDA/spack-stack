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
                 'modules.yaml', 'packages.yaml', 'repos.yaml', 'concretizer.yaml']

# Pass this value to --site for an empty config
empty_site = 'default'

def stack_path(*paths):
    return path.join(stack_dir, *paths)


def create_env_dir(name):
    # Create spack-stack/envs to hold envrionments, if it doesn't exist
    if not path.exists(stack_path('envs')):
        makedirs(stack_path('envs'))

    # Create env_dir
    env_dir = stack_path('envs', env_name)
    if not path.exists(env_dir):
        makedirs(env_dir)
        print("Created environment {} in {}".format(env_name, env_dir))
    else:
        sys.exit('Error: env {} already exists'.format(env_dir))

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
    for config_type in ['common', 'site']:
        config_dir = stack_path(env_dir, config_type)
        if path.isdir(config_dir):
            configs = list(filter(lambda f: f in valid_configs, listdir(config_dir)))
            configs = map(lambda conf: '  - {}/{}'.format(config_type, conf), configs)
            includes += configs
        
    includes.insert(0, 'include:') if includes else includes.insert(0, '')
    new_contents = contents.replace('@CONFIG_INCLUDES@', linesep.join(includes))

    with open(path.join(env_dir, 'spack.yaml'), "w") as f:
        f.write(new_contents)


def check_inputs(app, site):
    app_path = stack_path('configs', 'apps', app, 'spack.yaml')
    if not path.exists(app_path):
        sys.exit('Error: invalid app {}, "{}" does not exist'.format(app, app_path))

    if site == empty_site:
        return

    site_path = stack_path('configs', 'sites', site)
    if not path.exists(site_path):
        sys.exit('Error: invalid site {}, "{}" does not exist'.format(
            site, site_path))


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


description_text = '''
    Create a pre-configured Spack environment. Envrionments are created in spack-stack/envs/<env>.
'''

epilog_text = """
Example usage:
    source setup.sh
    ./create-env.py --site default --app ufs --name ufs-env
    spack env activate [-p] envs/ufs-env
    spack concretize
    spack install
"""
parser = argparse.ArgumentParser(description=description_text,
                                 epilog=epilog_text,
                                 formatter_class=RawTextHelpFormatter)

parser.add_argument('--site', type=str, required=False, nargs='?', const='default', help=site_help())
parser.add_argument('--app', type=str, required=True, help=app_help())
parser.add_argument('--name', type=str, required=False,
                    help='Optional name for env dir. Defaults to app.site name.')
parser.add_argument('--exclude-common-configs', required=False,
                    default=False, action='store_true', help='Ignore configs configs/common when creating environment')

args = parser.parse_args()

site = args.site
app = args.app
exclude_common_configs = args.exclude_common_configs
env_name = args.name if args.name else "{}.{}".format(app, site)

check_inputs(app, site)
env_dir = create_env_dir(env_name)
if not exclude_common_configs:
    copy_common_configs(env_dir)
if site != empty_site:
    copy_site_configs(site, env_dir)
copy_app_config(app, env_dir)
