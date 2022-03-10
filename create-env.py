#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
from argparse import RawTextHelpFormatter

# Get directory of this script
stack_dir = os.path.dirname(os.path.realpath(__file__))

# Get a path
def stack_path(*paths):
    return os.path.join(stack_dir, *paths)

# Append individual system configs into 'site.yaml'
def create_site_config(site, env_dir):
    site_dir = stack_path('configs', 'sites', site)
    site_configs = os.listdir(site_dir)
    new_site_config = stack_path(env_dir, 'site.yaml')
    with open(new_site_config, 'w') as f:
        for config in site_configs:
            if config in valid_configs:
                with open(os.path.join(site_dir, config)) as tmp:
                    f.write(tmp.read())
                    f.write(os.linesep)

def create_env_dir(name):
    # Create spack-stack/envs to hold envrionments, if it doesn't exist
    if not os.path.exists(stack_path('envs')):
        os.makedirs(stack_path('envs'))

    # Create env_dir
    env_dir = stack_path('envs', env_name)
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
        print("Created environment {} in {}".format(env_name, env_dir))
    else:
        sys.exit('Error: env {} already exists'.format(env_dir))

    return env_dir

def copy_common_configs(env_dir):
    common_dir = stack_path('configs', 'common')
    common_configs = os.listdir(common_dir)
    for config in common_configs:
        shutil.copy2(os.path.join(common_dir, config), env_dir)

def copy_app_config(env_dir):
    app_config = stack_path('configs', 'apps', app, 'spack.yaml')
    shutil.copy2(app_config, env_dir)

def check_inputs(app, site):
    app_path = stack_path('configs', 'apps', app, 'spack.yaml')
    if not os.path.exists(app_path):
        sys.exit('Error: invalid app {}, "{}" does not exist'.format(app, app_path))

    site_path = stack_path('configs', 'sites', site)
    if not os.path.exists(site_path):
        sys.exit('Error: invalid site {}, "{}" does not exist'.format(site, site_path))

def site_help():
    _, site_dirs, _ = next(os.walk(stack_path('configs', 'sites')))
    help_string = 'Pre-configured platform, or "default" for an empty site.yaml.' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for site in site_dirs:
        help_string += '\t' + site + os.linesep
    return help_string

def app_help():
    _, app_dirs, _ = next(os.walk(stack_path('configs', 'apps')))
    help_string = 'Application environment to build.' + os.linesep
    help_string += 'Available options are: ' + os.linesep
    for app in app_dirs:
        help_string += '\t' + app + os.linesep
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

valid_configs = ['compilers.yaml', 'config.yaml', 'mirrors.yaml', 
    'modules.yaml', 'packages.yaml', 'repos.yaml']

parser = argparse.ArgumentParser(description=description_text,
    epilog=epilog_text,
    formatter_class=RawTextHelpFormatter)

parser.add_argument('--site', type=str, required=True, help = site_help())
parser.add_argument('--app', type=str, required=True, help = app_help())
parser.add_argument('--name', type=str, required=False, help = 'Optional name for env dir. Defaults to app.site name.')
parser.add_argument('--exclude-common-configs', required=False, 
    default = False, action='store_true', help='Ignore configs configs/common when creating environment')

args = parser.parse_args()

site = args.site
app = args.app
exclude_common_configs = args.exclude_common_configs
env_name = args.name if args.name else "{}.{}".format(app, site)

check_inputs(app, site)
env_dir = create_env_dir(env_name)
if not exclude_common_configs:
    copy_common_configs(env_dir)
copy_app_config(env_dir)
create_site_config(site, env_dir)
