#!/usr/bin/env python3

import argparse
import os
import sys
import shutil

parser = argparse.ArgumentParser(description='Create a pre-configured Spack env folder.')
parser.add_argument('site', help = 'Pre-configured platforms (hera, orion, cheyenne, etc).')
parser.add_argument('app', help = 'Which app env to build (ufs, jedi).')
parser.add_argument('name', help = 'Optional name for env dir. Defaults to site name.')

args = parser.parse_args()

site = args.site
app = args.app
env_name = args.name

# spack-stack/envs
stack_dir = os.path.dirname(os.path.realpath(__file__))
env_dir = os.path.join(stack_dir, 'envs', env_name)

if not os.path.exists(os.path.join(stack_dir, 'envs')):
    os.makedirs(os.path.join(stack_dir, 'envs'))

if not os.path.exists(env_dir):
    os.makedirs(env_dir)
else:
    sys.exit('env {0} already exists'.format(env_dir))

site_config = os.path.join(stack_dir, 'configs', 'sites', site, 'site.yaml')
app_config = os.path.join(stack_dir, 'configs', 'apps', app, 'spack.yaml')

common_configs = []
for common_config in ['config.yaml', 'modules.yaml', 'packages.yaml']:
    common_configs.append(os.path.join(stack_dir, 'configs', 'common', common_config))

configs_to_copy = [site_config] + [app_config] + common_configs

for config in configs_to_copy:
    shutil.copy2(config, os.path.join(env_dir, ))
