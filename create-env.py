#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
from argparse import RawTextHelpFormatter

# Get directory of this script
stack_dir = os.path.dirname(os.path.realpath(__file__))

def stack_path(*paths):
    return os.path.join(stack_dir, *paths)

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
    cd envs/ufs-env
    spack end create -d .
    spack env activate .
    spack install
"""

parser = argparse.ArgumentParser(description=description_text,
    epilog=epilog_text,
    formatter_class=RawTextHelpFormatter)

parser.add_argument('--site', type=str, required=True, help = site_help())
parser.add_argument('--app', type=str, required=True, help = app_help())
parser.add_argument('--name', type=str, required=False, help = 'Optional name for env dir. Defaults to site name.')

args = parser.parse_args()

site = args.site
app = args.app
env_name = args.name if args.name else site

# Create spack-stack/envs to hold envrionments, if it doesn't exist
if not os.path.exists(stack_path('envs')):
    os.makedirs(stack_path('envs'))

site_config = stack_path('configs', 'sites', site, 'site.yaml')
app_config = stack_path('configs', 'apps', app, 'spack.yaml')

common_configs = []
for common_config in ['config.yaml', 'modules.yaml', 'packages.yaml']:
    common_configs.append(stack_path('configs', 'common', common_config))

configs_to_copy = [site_config] + [app_config] + common_configs

# Check if files exist before copying them
for config in configs_to_copy:
    if not os.path.exists(config):
        sys.exit('Error: file "{}" does not exist'.format(config))

# Create env_dir after checking if source files exist
env_dir = stack_path('envs', env_name)
if not os.path.exists(env_dir):
    os.makedirs(env_dir)
else:
    sys.exit('Error: env {0} already exists'.format(env_dir))

for config in configs_to_copy:
    shutil.copy2(config, env_dir)
