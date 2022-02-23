#!/usr/bin/env python3

import logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
import os
import shutil
import sys

# Get basic directory information
logging.info("Configuring basic directory information ...")
this_script_dir=os.path.realpath(os.path.split(__file__)[0])
base_dir=os.path.realpath(os.path.join(this_script_dir, '..'))
spack_dir=os.path.join(base_dir,'spack')
logging.info("  ... script directory: {}".format(this_script_dir))
logging.info("  ... base directory: {}".format(base_dir))
logging.info("  ... spack directory: {}".format(spack_dir))

# Import spack python modules
logging.info("Importing spack python modules ...")
sys.path.append(os.path.join(spack_dir, 'lib/spack/external'))
sys.path.append(os.path.join(spack_dir, 'lib/spack'))
import spack.config
import spack.environment

# Templates for creating compiler modules
COMPILER_TEMPLATES = {
    'lmod': os.path.join(this_script_dir, 'templates/compiler.lua'),
    'tcl': os.path.join(this_script_dir, 'templates/compiler'),
    }
MPI_TEMPLATES = {
    'lmod': os.path.join(this_script_dir, 'templates/mpi.lua'),
    'tcl': os.path.join(this_script_dir, 'templates/mpi'),
    }
PYTHON_TEMPLATES = {
    'lmod': os.path.join(this_script_dir, 'templates/python.lua'),
    'tcl': os.path.join(this_script_dir, 'templates/python')
    }
MODULE_FILE_EXTENSION = {
    'lmod': '.lua',
    'tcl': '',
    }

SUBSTITUTES_TEMPLATE = {
    'MODULELOADS'   : '',
    'MODULEPREREQS' : '',
    'MODULEPATH'    : '',
    'CC'            : '',
    'CXX'           : '',
    'F77'           : '',
    'FC'            : '',
    'COMPFLAGS'     : '',
    'ENVVARS'       : '',
    'MPICC'         : '',
    'MPICXX'        : '',
    'MPIF77'        : '',
    'MPIFC'         : '',
    'MPIROOT'       : '',
    'PYTHONROOT'    : '',
    }

########################################################################

def setenv_command(module_choice, key, value):
    if module_choice == 'lmod':
        return 'setenv("{}", "{}")\n'.format(key, value)
    else:
        return 'setenv {{{}}} {{{}}}\n'.format(key, value)

def prepend_path_command(module_choice, key, value):
    if module_choice == 'lmod':
        return 'prepend_path("{}", "{}")\n'.format(key, value)
    else:
        return 'prepend-path {{{}}} {{{}}}\n'.format(key, value)

def module_load_command(module_choice, module):
    if module_choice == 'lmod':
        return 'load("{}")\n'.format(module)
    else:
        return """if {{ [ module-info mode load ] && ![ is-loaded {0} ] }} {{
    module load {0}
}}\n""".format(module)

def module_prereq_command(module_choice, module):
    if module_choice == 'lmod':
        return 'prereq("{}")\n'.format(module)
    else:
        return ''

# Find currently active spack environment, activate here
logging.info("Configuring active spack environment ...")
env_dir=os.getenv('SPACK_ENV')
if not env_dir:
    raise Exception("No active spack environment")
env = spack.environment.Environment(env_dir)
spack.environment.environment.activate(env)
logging.info("  ... environment directory: {}".format(env_dir))

# Parse spack main config from environment
logging.info("Parsing spack environment main config ...")
main_config = spack.config.get('config')
install_dir = main_config['install_tree']['root']
if not os.path.isabs(install_dir):
    install_dir = os.path.realpath(os.path.join(env_dir, install_dir))
else:
    install_dir = os.path.realpath(install_dir)
logging.info("  ... install directory: {}".format(install_dir))

# Parse spack package config from environment
logging.info("Parsing spack environment package config ...")
package_config = spack.config.get('packages')
compiler_list = package_config['all']['compiler']
mpi_list = package_config['all']['providers']['mpi']
#
#if len(compiler_list)>1 or len(mpi_list)>1:
#    raise Exception("Currently not supported: More than one compiler or mpi provider per environment")
#
compiler_names = []
for compiler in compiler_list:
    try:
        (compiler_name, compiler_version) = compiler.split('@')
    except ValueError:
        raise Exception("No version provided for compiler '{}'".format(compiler))
    logging.info("  ... stack compiler: {}@{}".format(compiler_name, compiler_version))
    compiler_names.append(compiler_name)
#
mpi_names = []
for mpi in mpi_list:
    try:
        (mpi_name, mpi_version) = mpi.split('@')
    except ValueError:
        raise Exception("No version provided for mpi library '{}'".format(mpi))
    logging.info("  ... stack mpi library: {}@{}".format(mpi_name, mpi_version))
    mpi_names.append(mpi_name)

# Parse spack module config from environment
logging.info("Parsing spack environment modules config ...")
module_config = spack.config.get('modules')

# Check which modules are used - tcl or lmod (can only be one)
if len(module_config['default']['enable'])>1:
    raise Exception("Can use either lmod or tcl modules, not both")
module_choice = module_config['default']['enable'][0]
logging.info("  ... configured to use {} modules".format(module_choice))

module_dir = main_config['module_roots'][module_choice]
if not os.path.isabs(module_dir):
    module_dir = os.path.realpath(os.path.join(env_dir, module_dir))
else:
    module_dir = os.path.realpath(module_dir)
logging.info("  ... module directory: {}".format(module_dir))

core_compilers = module_config['default'][module_choice]['core_compilers']
logging.info("  ... core compilers: {}".format(core_compilers))
# Check that none of the compilers used for the stack is a core compiler
for compiler in compiler_list:
    if compiler in core_compilers:
        raise Exception("Currently not supported: compiler used for environment is in list of core compilers")

# Prepare meta module directory
logging.info("Preparing meta module directory ...")
meta_module_dir = os.path.join(module_dir, 'Core')
if os.path.isdir(meta_module_dir):
    # DH*
    shutil.rmtree(meta_module_dir)
    #raise Exception("Directory {} must not exist".format(meta_module_dir))
    # *DH
os.makedirs(meta_module_dir)
logging.info("  ... meta module directory : {}".format(meta_module_dir))

# Create compiler modules
logging.info("Creating compiler modules ...")
compiler_config = spack.config.get('compilers')
for compiler in compiler_config:
    if compiler['compiler']['spec'] in compiler_list:
        (compiler_name, compiler_version) = compiler['compiler']['spec'].split('@')
        logging.info("  ... configuring stack compiler {}@{}".format(compiler_name, compiler_version))
        compiler_module_dir = os.path.join(meta_module_dir, 'stack-'+compiler_name)
        compiler_module_file = os.path.join(compiler_module_dir, compiler_version + MODULE_FILE_EXTENSION[module_choice])
        substitutes = SUBSTITUTES_TEMPLATE.copy()

        # Compiler environment variables; names are lowercase in spack
        substitutes['CC'] = compiler['compiler']['paths']['cc']
        substitutes['CXX'] = compiler['compiler']['paths']['cxx']
        substitutes['F77'] = compiler['compiler']['paths']['f77']
        substitutes['FC'] = compiler['compiler']['paths']['fc']
        logging.debug("  ... ... CC  : {}".format(substitutes['CC']))
        logging.debug("  ... ... CXX : {}".format(substitutes['CXX']))
        logging.debug("  ... ... F77 : {}".format(substitutes['F77']))
        logging.debug("  ... ... FC' : {}".format(substitutes['FC']))

        # Compiler flags; names are lowercase in spack
        for flag_name in compiler['compiler']['flags']:
            flag_values = compiler['compiler']['flags'][flag_name]
            substitutes['COMPFLAGS'] += setenv_command(module_choice, flag_name.upper(), flag_values)
        substitutes['COMPFLAGS'] = substitutes['COMPFLAGS'].rstrip('\n')
        logging.debug("  ... ... COMPFLAGS: {}".format(substitutes['COMPFLAGS']))

        # Existing non-spack modules to load
        for module in compiler['compiler']['modules']:
            substitutes['MODULELOADS'] += module_load_command(module_choice, module)
            substitutes['MODULEPREREQS'] += module_prereq_command(module_choice, module)
        substitutes['MODULELOADS'] = substitutes['MODULELOADS'].rstrip('\n')
        substitutes['MODULEPREREQS'] = substitutes['MODULEPREREQS'].rstrip('\n')
        logging.debug("  ... ... MODULELOADS: {}".format(substitutes['MODULELOADS']))
        logging.debug("  ... ... MODULEPREREQS: {}".format(substitutes['MODULEPREREQS']))

        # Environment variables; case-sensitive in spack
        if compiler['compiler']['environment']:
            # prepend_path
            if 'prepend_path' in compiler['compiler']['environment'].keys():
                for env_name in compiler['compiler']['environment']['prepend_path']:
                    env_values = compiler['compiler']['environment']['prepend_path'][env_name]
                    substitutes['ENVVARS'] += prepend_path_command(module_choice, env_name, env_values)
            # set
            if 'set' in compiler['compiler']['environment'].keys():
                for env_name in compiler['compiler']['environment']['set']:
                    env_values = compiler['compiler']['environment']['set'][env_name]
                    substitutes['ENVVARS'] += setenv_command(module_choice, env_name, env_values)
            substitutes['ENVVARS'] = substitutes['ENVVARS'].rstrip('\n')
            logging.debug("  ... ... ENVVARS  : {}".format(substitutes['ENVVARS']))

        # Extra rpaths - not supported
        if compiler['compiler']['extra_rpaths']:
            raise Exception("Support for extra_rpaths not yet implemented")

        # Spack compiler module hierarchy
        substitutes['MODULEPATH'] = os.path.join(module_dir, compiler_name, compiler_version)
        logging.debug("  ... ... MODULEPATH  : {}".format(substitutes['MODULEPATH']))
        if not os.path.isdir(substitutes['MODULEPATH']):
            raise Exception("Compiler module path {} does not exist".format(substitutes['MODULEPATH']))

        # For tcl modules remove the compiler prefices from the module contents
        if module_choice == 'tcl':
            logging.info("  ... ... removing compiler prefices from tcl modulefiles in {}".format(substitutes['MODULEPATH']))
            for root,ddir,files in os.walk(substitutes['MODULEPATH']):
                for ffile in files:
                    filepath = os.path.join(root, ffile)
                    logging.debug("  ... ... ... removing compiler prefices in {}".format(filepath))
                    cmd = "sed -i 's#is-loaded {}/{}/#is-loaded #g' {}".format(compiler_name, compiler_version, filepath)
                    status = os.system(cmd)
                    if not status == 0:
                        raise Exception("Error while calling '{}'".format(cmd))
                    cmd = "sed -i 's#load {}/{}/#load #g' {}".format(compiler_name, compiler_version, filepath)
                    status = os.system(cmd)
                    if not status == 0:
                        raise Exception("Error while calling '{}'".format(cmd))

        # Read compiler template into module_content string
        with open(COMPILER_TEMPLATES[module_choice]) as f:
            module_content = f.read()

        # Substitute variables in module_content
        for key in substitutes.keys():
            module_content = module_content.replace("@{}@".format(key), substitutes[key])

        # Write compiler lua module
        if not os.path.isdir(compiler_module_dir):
            os.makedirs(compiler_module_dir)
        with open(compiler_module_file, 'w') as f:
            f.write(module_content)
        logging.info("  ... writing {}".format(compiler_module_file))

## Create mpi modules
for mpi in mpi_list:
    (mpi_name, mpi_version) = mpi.split('@')
    for package_name in package_config.keys():
        if package_name == mpi_name:
            for i in range(len(package_config[package_name]['externals'])):
                (package_name_dummy, package_version) = package_config[package_name]['externals'][i]['spec'].split('@',1)
                # Strip off any compiler specification or variants from the MPI package config
                package_version = package_version.split('+')[0].split('~')[0].split('-')[0].split('%')[0].split('^')[0].strip()
                if package_version == mpi_version:
                    for compiler in compiler_list:
                        (compiler_name, compiler_version) = compiler.split('@')
                        logging.info("  ... configuring stack mpi library {}@{} for compiler {}@{}".format(
                                                   mpi_name, mpi_version, compiler_name, compiler_version))

                        # Path and name for lua module file
                        mpi_module_dir = os.path.join(module_dir, compiler_name,
                                                   compiler_version, 'stack-'+mpi_name)
                        mpi_module_file = os.path.join(mpi_module_dir, mpi_version + MODULE_FILE_EXTENSION[module_choice])
                        substitutes = SUBSTITUTES_TEMPLATE.copy()
                        #
                        if 'modules' in package_config[mpi_name]['externals'][i].keys():
                            # Existing non-spack modules to load
                            for module in package_config[mpi_name]['externals'][i]['modules']:
                                substitutes['MODULELOADS'] += module_load_command(module_choice, module)
                                substitutes['MODULEPREREQS'] += module_prereq_command(module_choice, module)
                            substitutes['MODULELOADS'] = substitutes['MODULELOADS'].rstrip('\n')
                            substitutes['MODULEPREREQS'] = substitutes['MODULEPREREQS'].rstrip('\n')
                            logging.debug("  ... ... MODULELOADS: {}".format(substitutes['MODULELOADS']))
                            logging.debug("  ... ... MODULEPREREQS: {}".format(substitutes['MODULEPREREQS']))
                            # mpi_name_ROOT - replace "-" in mpi_name with "_" for environment variables
                            if 'prefix' in package_config[mpi_name]['externals'][i].keys():
                                prefix = package_config[mpi_name]['externals'][i]['prefix']
                                substitutes['MPIROOT'] = setenv_command(module_choice, mpi_name.replace('-','_')+'_ROOT', prefix)
                                logging.debug("  ... ... MPIROOT: {}".format(substitutes['MPIROOT']))
                        elif 'prefix' in package_config[mpi_name]['externals'][i].keys():
                            prefix = package_config[mpi_name]['externals'][i]['prefix']
                            # PATH and compiler wrapper environment variables
                            bindir = os.path.join(prefix, 'bin')
                            if os.path.isdir(bindir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "PATH", bindir)
                            # LD_LIBRARY_PATH AND PKG_CONFIG_PATH - do we need to worry about DYLD_LIBRARY_PATH for macOS?
                            libdir = os.path.join(prefix, 'lib')
                            if os.path.isdir(libdir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "LD_LIBRARY_PATH", libdir)
                            pkgconfigdir = os.path.join(libdir, 'pkgconfig')
                            if os.path.isdir(pkgconfigdir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "PKG_CONFIG_PATH", pkgconfigdir)
                            lib64dir = os.path.join(prefix, 'lib64')
                            if os.path.isdir(lib64dir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "LD_LIBRARY_PATH", lib64dir)
                            pkgconfig64dir = os.path.join(lib64dir, 'pkgconfig')
                            if os.path.isdir(pkgconfig64dir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "PKG_CONFIG_PATH", pkgconfig64dir)
                            # MANPATH
                            mandir = os.path.join(prefix, 'share/man')
                            if os.path.isdir(mandir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "MANPATH", mandir)
                            # ACLOCAL_PATH
                            aclocaldir = os.path.join(prefix, 'share/aclocal')
                            if os.path.isdir(aclocaldir):
                                substitutes['ENVVARS'] += prepend_path_command(module_choice, "ACLOCAL_PATH", aclocaldir)
                            # mpi_name_ROOT - replace "-" in mpi_name with "_" for environment variables
                            substitutes['MPIROOT'] = setenv_command(module_choice, mpi_name.replace('-','_')+'_ROOT', prefix)
                        else:
                            raise Exception("External packages must have 'prefix' and/or 'modules'")

                        # Compiler wrapper environment variables
                        if 'intel' in mpi_name:
                            substitutes['MPICC']    = os.path.join('mpiicc')
                            substitutes['MPICXX']   = os.path.join('mpiicpc')
                            substitutes['MPIF77']   = os.path.join('mpiifort')
                            substitutes['MPIF90']   = os.path.join('mpiifort')
                        else:
                            substitutes['MPICC']    = os.path.join('mpicc')
                            substitutes['MPICXX']   = os.path.join('mpic++')
                            substitutes['MPIF77']   = os.path.join('mpif77')
                            substitutes['MPIF90']   = os.path.join('mpif90')

                        # Spack compiler module hierarchy
                        substitutes['MODULEPATH'] = os.path.join(module_dir, mpi_name, mpi_version,
                                                                   compiler_name, compiler_version)
                        logging.debug("  ... ... MODULEPATH  : {}".format(substitutes['MODULEPATH']))
                        if not os.path.isdir(substitutes['MODULEPATH']):
                            raise Exception("Compiler module path {} does not exist".format(substitutes['MODULEPATH']))

                        # For tcl modules remove the compiler/mpi prefices from the module contents
                        if module_choice == 'tcl':
                            logging.info("  ... ... removing compiler/mpi prefices from tcl modulefiles in {}".format(substitutes['MODULEPATH']))
                            for root,ddir,files in os.walk(substitutes['MODULEPATH']):
                                for ffile in files:
                                    filepath = os.path.join(root, ffile)
                                    logging.debug("  ... ... ... removing compiler/mpi prefices in {}".format(filepath))
                                    # First, compiler-only dependent modules
                                    cmd = "sed -i 's#is-loaded {}/{}/#is-loaded #g' {}".format(compiler_name, compiler_version, filepath)
                                    status = os.system(cmd)
                                    if not status == 0:
                                        raise Exception("Error while calling '{}'".format(cmd))
                                    cmd = "sed -i 's#load {}/{}/#load #g' {}".format(compiler_name, compiler_version, filepath)
                                    status = os.system(cmd)
                                    if not status == 0:
                                        raise Exception("Error while calling '{}'".format(cmd))
                                    # Then, compiler+mpi-dependent modules
                                    cmd = "sed -i 's#is-loaded {}/{}/{}/{}/#is-loaded #g' {}".format(mpi_name, mpi_version,
                                                                                 compiler_name, compiler_version, filepath)
                                    status = os.system(cmd)
                                    if not status == 0:
                                        raise Exception("Error while calling '{}'".format(cmd))
                                    cmd = "sed -i 's#load {}/{}/{}/{}/#load #g' {}".format(mpi_name, mpi_version,
                                                                       compiler_name, compiler_version, filepath)
                                    status = os.system(cmd)
                                    if not status == 0:
                                        raise Exception("Error while calling '{}'".format(cmd))

                        # Read compiler lua template into module_content string
                        with open(MPI_TEMPLATES[module_choice]) as f:
                            module_content = f.read()

                        # Substitute variables in module_content
                        for key in substitutes.keys():
                            module_content = module_content.replace("@{}@".format(key), substitutes[key])

                        # Write mpi lua module
                        if not os.path.isdir(mpi_module_dir):
                            os.makedirs(mpi_module_dir)
                        with open(mpi_module_file, 'w') as f:
                            f.write(module_content)
                        logging.info("  ... writing {}".format(mpi_module_file))

## Create python modules
for package_name in package_config.keys():
    if package_name == 'python':
        # For now, can only handle one Python version
        if len(package_config[package_name]['externals'])>1:
            raise Exception("Currently not supported: More than one external python package per environment")
        for i in range(len(package_config[package_name]['externals'])):
            (python_name, python_version) = package_config[package_name]['externals'][i]['spec'].split('@',1)
            # Strip off any compiler specification or variants from the Python package config
            python_version = python_version.split('+')[0].split('~')[0].split('-')[0].split('%')[0].split('^')[0].strip()
            # Loop through compilers
            for compiler in compiler_list:
                (compiler_name, compiler_version) = compiler.split('@')
                logging.info("  ... configuring stack python interpreter {}@{} for compiler {}@{}".format(
                                            python_name, python_version, compiler_name, compiler_version))

                # Path and name for lua module file
                python_module_dir = os.path.join(module_dir, compiler_name, compiler_version, 'stack-'+python_name)
                python_module_file = os.path.join(python_module_dir, python_version + MODULE_FILE_EXTENSION[module_choice])

                substitutes = SUBSTITUTES_TEMPLATE.copy()
                #
                if 'modules' in package_config[python_name]['externals'][i].keys():
                    # Existing non-spack modules to load
                    for module in package_config[python_name]['externals'][i]['modules']:
                        substitutes['MODULELOADS'] += module_load_command(module_choice, module)
                        substitutes['MODULEPREREQS'] += module_prereq_command(module_choice, module)
                    substitutes['MODULELOADS'] = substitutes['MODULELOADS'].rstrip('\n')
                    substitutes['MODULEPREREQS'] = substitutes['MODULEPREREQS'].rstrip('\n')
                    logging.debug("  ... ... MODULELOADS: {}".format(substitutes['MODULELOADS']))
                    logging.debug("  ... ... MODULEPREREQS: {}".format(substitutes['MODULEPREREQS']))
                    # python_name_ROOT - replace "-" in python_name with "_" for environment variables
                    if 'prefix' in package_config[python_name]['externals'][i].keys():
                        prefix = package_config[python_name]['externals'][i]['prefix']
                        substitutes['PYTHONROOT'] = setenv_command(module_choice, python_name.replace('-','_')+"_ROOT", prefix)
                        logging.debug("  ... ... PYTHONROOT: {}".format(substitutes['PYTHONROOT']))
                elif 'prefix' in package_config[python_name]['externals'][i].keys():
                    prefix = package_config[python_name]['externals'][i]['prefix']
                    # PATH
                    bindir = os.path.join(prefix, 'bin')
                    if os.path.isdir(bindir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PATH", bindir)
                    # LD_LIBRARY_PATH AND PKG_CONFIG_PATH - do we need to worry about DYLD_LIBRARY_PATH for macOS?
                    # Also: PYTHONPATH = check site-packages and dist-packages
                    libdir = os.path.join(prefix, 'lib')
                    if os.path.isdir(libdir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "LD_LIBRARY_PATH", libdir)
                    pkgconfigdir = os.path.join(libdir, 'pkgconfig')
                    if os.path.isdir(pkgconfigdir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PKG_CONFIG_PATH", pkgconfigdir)
                    # Python version for constructing PYTHONPATH is X.Y (major.minor, no patch-level)
                    python_version_for_pythonpath = python_version[:python_version.rfind('.')]
                    # Check site-packages and dist-packages
                    pythonpathdir = os.path.join(libdir, 'python{}'.format(python_version_for_pythonpath), 'site-packages')
                    if os.path.isdir(pythonpathdir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PYTHONPATH", pythonpathdir)
                    pythonpathdir = os.path.join(libdir, 'python{}'.format(python_version_for_pythonpath), 'dist-packages')
                    if os.path.isdir(pythonpathdir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PYTHONPATH", pythonpathdir)
                    lib64dir = os.path.join(prefix, 'lib64')
                    if os.path.isdir(lib64dir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "LD_LIBRARY_PATH", lib64dir)
                    pkgconfig64dir = os.path.join(lib64dir, 'pkgconfig')
                    if os.path.isdir(pkgconfig64dir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PKG_CONFIG_PATH", pkgconfig64dir)
                    pythonpath64dir = os.path.join(lib64dir, 'python{}'.format(python_version_for_pythonpath), 'site-packages')
                    if os.path.isdir(pythonpath64dir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PYTHONPATH", pythonpath64dir)
                    pythonpath64dir = os.path.join(lib64dir, 'python{}'.format(python_version_for_pythonpath), 'dist-packages')
                    if os.path.isdir(pythonpath64dir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "PYTHONPATH", pythonpath64dir)
                    # MANPATH
                    mandir = os.path.join(prefix, 'share/man')
                    if os.path.isdir(mandir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "MANPATH", mandir)
                    # ACLOCAL_PATH
                    aclocaldir = os.path.join(prefix, 'share/aclocal')
                    if os.path.isdir(aclocaldir):
                        substitutes['ENVVARS'] += prepend_path_command(module_choice, "ACLOCAL_PATH", aclocaldir)
                    # python_name_ROOT - replace "-" in python_name with "_" for environment variables
                    substitutes['PYTHONROOT'] = setenv_command(module_choice, python_name.replace('-','_')+"_ROOT", prefix)
                else:
                    raise Exception("External packages must have 'prefix' and/or 'modules'")

                # Read compiler lua template into module_content string
                with open(PYTHON_TEMPLATES[module_choice]) as f:
                    module_content = f.read()

                # Substitute variables in module_content
                for key in substitutes.keys():
                    module_content = module_content.replace("@{}@".format(key), substitutes[key])

                # Write python lua module
                if not os.path.isdir(python_module_dir):
                    os.makedirs(python_module_dir)
                with open(python_module_file, 'w') as f:
                    f.write(module_content)
                logging.info("  ... writing {}".format(python_module_file))

