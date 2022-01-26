#!/usr/bin/env python3

import os
import shutil
import sys

this_script_dir=os.path.realpath(os.path.split(__file__)[0])
base_dir=os.path.realpath(os.path.join(this_script_dir, '..'))
spack_dir=os.path.join(base_dir,'spack')
print(this_script_dir)
print(base_dir)
print(spack_dir)

sys.path.append(os.path.join(spack_dir, 'lib/spack/external'))
sys.path.append(os.path.join(spack_dir, 'lib/spack'))

import spack.config
import spack.environment

#Todo: get from spack env status
# Get environment 
env_dir=os.getenv('SPACK_ENV')
if not env_dir:
    raise Exception("No active spack environment")


env = spack.environment.Environment(env_dir)
print(env)
spack.environment.environment.activate(env)
#spack.config.get()

### MAIN CONFIG
main_config = spack.config.get('config')
install_dir = main_config['install_tree']['root']
if not os.path.isabs(install_dir):
    install_dir = os.path.realpath(os.path.join(env_dir, install_dir))
else:
    install_dir = os.path.realpath(install_dir)
module_dir = main_config['module_roots']['lmod']
if not os.path.isabs(module_dir):
    module_dir = os.path.realpath(os.path.join(env_dir, module_dir))
else:
    module_dir = os.path.realpath(module_dir)
#print(main_config)
print(install_dir)
print(module_dir)

### PACKAGE CONFIG
package_config = spack.config.get('packages')
#print(package_config)
#print(package_config['all'])
compiler_list = package_config['all']['compiler']
mpi_list = package_config['all']['providers']['mpi']
if len(compiler_list)>1 or len(mpi_list)>1:
    raise Exception("Currently not supported: More than one compiler or mpi provider per environment")
print(compiler_list)
print(mpi_list)
try:
    (stack_compiler_name, stack_compiler_version) = compiler_list[0].split('@')
except ValueError:
    stack_compiler_name = compiler_list[0]
    stack_compiler_version = None
try:
    (stack_mpi_name, stack_mpi_version) = mpi_list[0].split('@')
except ValueError:
    stack_mpi_name = mpi_list[0]
    stack_mpi_version = None
print(stack_compiler_name)
print(stack_compiler_version)
print(stack_mpi_name)
print(stack_mpi_version)

### MODULE CONFIG
module_config = spack.config.get('modules')
print(module_config)
core_compilers = module_config['default']['lmod']['core_compilers']
print(core_compilers)

for compiler in compiler_list:
    if compiler in core_compilers:
        raise Exception("Currently not supported: compiler used for environment is in list of core compilers")

meta_module_dir = os.path.join(module_dir, 'Core')
if os.path.isdir(meta_module_dir):
    # DH*
    shutil.rmtree(meta_module_dir)
    #raise Exception("Directory {} must not exist".format(meta_module_dir))
    # *DH
os.makedirs(meta_module_dir)
print(meta_module_dir)

substitutes = {
    'MODULELOADS'   : '',
    'MODULEPREREQS' : '',
    'MODULEPATH'    : '',
    'CC'            : '',
    'CXX'           : '',
    'F77'           : '',
    'FC'            : '',
    'COMPFLAGS'     : '',
    'ENVVARS'       : '',
    }

# Create compiler module
compiler_lua_template = os.path.join(this_script_dir, 'templates/compiler.lua'.format(stack_compiler_name))

compiler_config = spack.config.get('compilers')
#print(compiler_config)
for compiler in compiler_config:
    print(compiler)
    (compiler_name, compiler_version) = compiler['compiler']['spec'].split('@')
    compiler_lua_dir = os.path.join(meta_module_dir, 'stack-compiler-'+compiler_name)
    compiler_lua_file = os.path.join(compiler_lua_dir, compiler_version + '.lua')
    print(compiler_name, compiler_version, compiler_lua_file)
    if stack_compiler_name==compiler_name:
        if not stack_compiler_version:
            stack_compiler_version = compiler_version
        if stack_compiler_version==compiler_version:
            print("FOUND MY COMPILER!")
            print(compiler)
            # Compiler environment variables; names are lowercase in spack
            substitutes['CC'] = compiler['compiler']['paths']['cc']
            substitutes['CXX'] = compiler['compiler']['paths']['cxx']
            substitutes['F77'] = compiler['compiler']['paths']['f77']
            substitutes['FC'] = compiler['compiler']['paths']['fc']
            # Compiler flags; names are lowercase in spack
            for flag_name in compiler['compiler']['flags']:
                flag_values = compiler['compiler']['flags'][flag_name]
                print(flag_name, flag_values)
                substitutes['COMPFLAGS'] += 'setenv("{}", "{}")\n'.format(flag_name.upper(), flag_values)
            # Existing non-spack modules to load
            for module in compiler['compiler']['modules']:
                substitutes['MODULELOADS'] += 'load({})\n'.format(module)
                substitutes['MODULEPREREQS'] += 'prereq({})\n'.format(module)
            # Environment variables; case-sensitive in spack
            if compiler['compiler']['environment']:
                # prepend_path
                if 'prepend_path' in compiler['compiler']['environment'].keys():
                    for env_name in compiler['compiler']['environment']['prepend_path']:
                        env_values = compiler['compiler']['environment']['prepend_path'][env_name]
                        print(env_name, env_values)
                        substitutes['ENVVARS'] += 'prepend_path("{}", "{}")\n'.format(env_name, env_values)
                # set
                if 'set' in compiler['compiler']['environment'].keys():
                    for env_name in compiler['compiler']['environment']['set']:
                        env_values = compiler['compiler']['environment']['set'][env_name]
                        print(env_name, env_values)
                        substitutes['ENVVARS'] += 'setenv("{}", "{}")\n'.format(env_name, env_values)
            # Extra rpaths - not supported
            if compiler['compiler']['extra_rpaths']:
                raise Exception("Support for extra_rpaths not yet implemented")
            print(substitutes)

            # Spack compiler module hierarchy
            substitutes['MODULEPATH'] = os.path.join(module_dir, stack_compiler_name, stack_compiler_version)
            if not os.path.isdir(substitutes['MODULEPATH']):
                raise Exception("Compiler module path {} does not exist".format(substitutes['MODULEPATH']))

            with open(compiler_lua_template) as f:
                module_content = f.read()
            print ('Content TMP: "{}"'.format(module_content))

            for key in substitutes.keys():
                module_content = module_content.replace("@{}@".format(key), substitutes[key])

            print ('Content NEW: "{}"'.format(module_content))
            if not os.path.isdir(compiler_lua_dir):
                os.makedirs(compiler_lua_dir)
            with open(compiler_lua_file, 'w') as f:
                f.write(module_content)
            raise Exception("Wrote {}".format(compiler_lua_file))