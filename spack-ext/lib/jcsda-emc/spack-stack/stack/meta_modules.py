#!/usr/bin/env python3

import copy
import logging
import os
import re
import sys

import spack
import spack.environment as ev
#    import spack.repo
from spack.provider_index import ProviderIndex

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# Get basic directory information
logging.info("Configuring basic directory information ...")
this_script_dir = os.path.realpath(os.path.split(__file__)[0])
base_dir = os.path.realpath(os.path.join(this_script_dir, ".."))
spack_dir = spack.paths.spack_root
logging.info("  ... script directory: {}".format(this_script_dir))
logging.info("  ... base directory: {}".format(base_dir))
logging.info("  ... spack directory: {}".format(spack_dir))

# Templates for creating compiler modules
COMPILER_TEMPLATES = {
    "lmod": os.path.join(this_script_dir, "templates/compiler.lua"),
    "tcl": os.path.join(this_script_dir, "templates/compiler"),
}
MPI_TEMPLATES = {
    "lmod": os.path.join(this_script_dir, "templates/mpi.lua"),
    "tcl": os.path.join(this_script_dir, "templates/mpi"),
}
MODULE_FILE_EXTENSION = {
    "lmod": ".lua",
    "tcl": ""
}

SUBSTITUTES_TEMPLATE = {
    "MODULELOADS": "",
    "MODULEPATHS": "",
    "CC": "",
    "CXX": "",
    "F77": "",
    "FC": "",
    "COMPFLAGS": "",
    "ENVVARS": "",
    "MPICC": "",
    "MPICXX": "",
    "MPIF77": "",
    "MPIROOT": "",
}


# DH* TODO: IMPORT THIS FROM SPACK, THEY MAINTAIN THE SAME DICTIONARY
COMPILER_TRANSLATION_TABLE = {
    "gcc" : "gcc",
    "clang" : "llvm",
    "intel" : "intel-oneapi-compilers-classic",
    "oneapi" : "intel-oneapi-compilers",
}


def setenv_command(module_choice, key, value):
    if module_choice == "lmod":
        return 'setenv("{}", "{}")\n'.format(key, value)
    else:
        return "setenv {{{}}} {{{}}}\n".format(key, value)


def unsetenv_command(module_choice, key, value):
    if module_choice == "lmod":
        return 'unsetenv("{}", "{}")\n'.format(key, value)
    else:
        return "unsetenv {{{}}} {{{}}}\n".format(key, value)


def append_path_command(module_choice, key, value):
    if module_choice == "lmod":
        return 'append_path("{}", "{}")\n'.format(key, value)
    else:
        return "append-path {{{}}} {{{}}}\n".format(key, value)


def prepend_path_command(module_choice, key, value):
    if module_choice == "lmod":
        return 'prepend_path("{}", "{}")\n'.format(key, value)
    else:
        return "prepend-path {{{}}} {{{}}}\n".format(key, value)


def envmod_command(module_choice, action, env_name, env_values):
    if action == "set":
        module_action = "setenv"
    elif action == "unset":
        module_action = "unsetenv"
    elif action == "append_path":
        if module_choice == "lmod":
            module_action = "append_path"
        else:
            module_action = "append-path"
    elif action == "prepend_path":
        if module_choice == "lmod":
            module_action = "prepend_path"
        else:
            module_action = "prepend-path"
    if module_choice == "lmod":
        return f'{module_action}("{env_name}", "{env_values}")\n'#.format(module_action, env_name, env_values)
    else:
        return f"{module_action} {{{env_name}}} {{{env_values}}}\n"#.format(module_action, env_name, env_values)


def module_load_command(module_choice, module):
    if module_choice == "lmod":
        return f"""load("{module}")
prereq("{module}")\n"""
    else:
        return f"""if {{ [ module-info mode load ] && ![ is-loaded {module} ] }} {{
    module load {module}
}}\n"""


def modulepath_prepend_command(module_choice, modulepath):
    return envmod_command(module_choice, "prepend_path", "MODULEPATH", modulepath)
    #if module_choice == "lmod":
    #    return 'prepend_path("MODULEPATH", "{}")\n'.format(modulepath)
    #else:
    #    return "prepend-path {{MODULEPATH}} {{{}}}\n".format(modulepath)


def substitute_config_vars(config_str):
    """
    Substitute spack-specific and environment variables that may be present
    in configuration files. See:
    https://spack.readthedocs.io/en/latest/configuration.html#config-file-variables
    """
    spack_vars = {
        "ENV": ev.active_environment().path,
        "SPACK": os.getenv("SPACK_ROOT"),
        "TEMPDIR": None,
        "USER": os.getenv("HOME"),
        "USER_CACHE_PATH": os.path.join(os.getenv("HOME"), ".spack"),
    }

    if config_str.startswith("~"):
        config_str = config_str.replace("~", os.getenv("HOME"))

    # Get var as it appears in the string (e.g. ${env}), and its name (e.g. env)
    matches = re.findall(r"(\$(\w+))|(\${(\w+)})", config_str)
    for match in matches:
        if match[0]:
            pair = (match[0], match[1])
        else:
            pair = (match[2], match[3])

        var_string = pair[0]
        var_name = pair[1].upper()

        sub_value = spack_vars[var_name] if spack_vars[var_name] else os.getenv(var_name)
        config_str = config_str.replace(var_string, sub_value)

    return config_str


def get_preferred_compiler():
    """DH* 20250730 - DO WE NEED BOTH WAYS TO DETERMINE THE PREFERRED COMPILER?
    # MAYBE KEEP FOR NOW UNTIL WE KNOW BETTER WHAT IS NEEDED AND WHAT NOT. TODO:
    UPDATE DOCSTRING"""
    ## Method 1
    #try:
    #    preferred_compilers = spack.config.get("packages")["all"]["require"]
    #except:
    #    raise Exception(
    #        """Unable to detect preferred compiler from environment.
    #        Does the environment have the config entry 'packages:all:require?'"""
    #    )
    #if len(preferred_compilers)>1:
    #    raise Exception(f"Invalid value for packages:all:require is {preferred_compilers}")
    #match = re.search(r'%\[when=%fortran\](\S+)', preferred_compilers[0])
    ## Translate legacy names (intel, oneapi, ...) to new names (intel-oneapi-compilers-classic, ...)
    #if match and match.group(1) in spack.aliases.LEGACY_COMPILER_TO_BUILTIN.keys():
    #    preferred_compiler_v1 = spack.aliases.LEGACY_COMPILER_TO_BUILTIN[match.group(1)]
    #else:
    #    preferred_compiler_v1 = match.group(1)
    ## Method 2
    #try:
    #    preferred_compilers = spack.config.get("packages")["fortran"]["require"]
    #except:
    #    raise Exception(
    #        """Unable to detect preferred compiler from environment.
    #        Does the environment have the config entry 'packages:fortran:require?'"""
    #    )
    #if len(preferred_compilers)>1:
    #    raise Exception(f"Invalid value for packages:fortran:require is {preferred_compilers}")
    #preferred_compiler_v2 = preferred_compilers[0]
    #if preferred_compiler_v1 == preferred_compiler_v2:
    #    preferred_compiler = preferred_compiler_v1
    #    del preferred_compilers
    #    del preferred_compiler_v1
    #    del preferred_compiler_v2
    #else:
    #    raise Exception(f"Multiple preferred compilers in spack config: {preferred_compiler_v1} vs {preferred_compiler_v2}")
    #return preferred_compiler
    # Determine preferred compiler
    try:
        preferred_compilers = spack.config.get("packages")["all"]["prefer"]
    except:
        raise Exception(
            """Unable to detect preferred compiler from environment.
            Does the environment have the config entry 'packages:all:prefer?'"""
        )
    if len(preferred_compilers)>1:
        raise Exception(f"Invalid value for packages:all:prefer is {preferred_compilers}")
    preferred_compiler_legacy_name = preferred_compilers[0].replace('%','')
    if preferred_compiler_legacy_name in spack.aliases.LEGACY_COMPILER_TO_BUILTIN.keys():
        preferred_compiler = spack.aliases.LEGACY_COMPILER_TO_BUILTIN[preferred_compiler_legacy_name]
    else:
        preferred_compiler = preferred_compiler_legacy_name
    return preferred_compiler


def remove_compiler_prefices_from_tcl_modulefiles(modulepath, compiler_list, mpi_provider):
    """Remove compiler and mpi prefices from tcl modulefiles in modulepath"""
    logging.info(f"  ... ... removing compiler/mpi prefices from tcl modulefiles in {modulepath}")
    module_replace_patterns = ["is-loaded", "module load", "depends-on"]
    # sed syntax differs on macOS
    if sys.platform == "darwin":
        sed_syntax_fix = "''"
    else:
        sed_syntax_fix = ""
    for root, ddir, files in os.walk(modulepath):
        for ffile in files:
            filepath = os.path.join(root, ffile)
            logging.debug(f"  ... ... ... {filepath}")
            for pattern in module_replace_patterns:
                for compiler in compiler_list:
                    # First, compiler-dependent modules
                    (compiler_name, compiler_version) = compiler.split("@")
                    cmd = "sed -i {4} 's#{0} {1}/{2}/#{0} #g' {3}".format(
                        pattern, compiler_name, compiler_version, filepath, sed_syntax_fix
                    )
                    status = os.system(cmd)
                    if not status == 0:
                        raise Exception(f"Error while calling '{cmd}'")
                    # If mpi_provider is not None, also do compiler+mpi-dependent modules
                    if not mpi_provider:
                        continue
                    cmd = "sed -i {6} 's#{0} {1}/{2}/{3}/{4}/#{0} #g' {5}".format(
                        pattern,
                        mpi_provider.name,
                        mpi_provider.version,
                        compiler_name,
                        compiler_version,
                        filepath,
                        sed_syntax_fix,
                    )
                    status = os.system(cmd)
                    if not status == 0:
                        raise Exception(f"Error while calling '{cmd}'")


def setup_meta_modules():
    # Find currently active spack environment, activate here
    logging.info("Configuring active spack environment ...")
    env_dir = ev.active_environment().path
    if not env_dir:
        raise Exception("No active spack environment")
    env = spack.environment.Environment(env_dir)
    spack.environment.environment.activate(env)
    logging.info("  ... environment directory: {}".format(env_dir))

    # Parse spack main config from environment
    logging.info("Parsing spack environment main config ...")
    main_config = spack.config.get("config")
    install_dir = substitute_config_vars(main_config["install_tree"]["root"])

    if not os.path.isabs(install_dir):
        install_dir = os.path.realpath(os.path.join(env_dir, install_dir))
    else:
        install_dir = os.path.realpath(install_dir)
    logging.info("  ... install directory: {}".format(install_dir))

    # Parse spack module config from environment
    logging.info("Parsing spack environment modules config ...")
    module_config = spack.config.get("modules")

    # Check which modules are used - tcl or lmod (can only be one)
    if len(module_config["default"]["enable"]) > 1:
        raise Exception("Can use either lmod or tcl modules, not both")
    module_choice = module_config["default"]["enable"][0]
    logging.info("  ... configured to use {} modules".format(module_choice))

    # Top-level module directory
    module_dir = substitute_config_vars(module_config["default"]["roots"][module_choice])
    if not os.path.isabs(module_dir):
        module_dir = os.path.realpath(os.path.join(env_dir, module_dir))
    else:
        module_dir = os.path.realpath(module_dir)
    logging.info(f"  ... module directory: {module_dir}")

    # Get all specs and determine compilers
    hashes = env.all_hashes()
    specs = spack.store.STORE.db.query(hashes=hashes)
    q = ProviderIndex(specs=specs, repository=spack.repo.PATH)

    c_providers = q.providers_for("c")
    cxx_providers = q.providers_for("cxx")
    fortran_providers = q.providers_for("fortran")
    compilers = list(set(c_providers + cxx_providers + fortran_providers))
    if not compilers:
        raise Exception("No compilers found")
    logging.info(f"  ... compilers: {compilers}")

    # To remove compiler prefices from tcl modulefiles, we need
    # a mock compiler "none@none" for external packages. We also
    # need this a list for lmod to check the core compiler, but we
    # don't need the mock compiler.
    if module_choice == "lmod":
        compiler_list = [x.name+"@"+str(x.version) for x in compilers]
    else:
        compiler_list = [x.name+"@"+str(x.version) for x in compilers] + ["none@none"]
    logging.debug(f"  ... compiler_list: {compiler_list}")

    # Core compilers is only a valid options for lmod
    if module_choice == "lmod":
        # Determine core compiler(s) and make sure they are not used
        core_compilers = module_config["default"][module_choice]["core_compilers"]
        logging.info("  ... core compilers: {}".format(core_compilers))
        # Check that none of the compilers used for the stack is a core compiler
        for core_compiler in core_compilers:
            if any(core_compiler in x for x in compiler_list):
                raise Exception("Not supported: spack-stack compilers in core compilers")

    # Determine the preferred compiler and sort the list of compilers so that
    # the preferred compiler comes last. This is so that all other compilers
    # populate the MODULEPATHS_SAVE list before the preferred compiler
    # takes it and adds it to the stack-COMPILER metamodule. Likewise, we need
    # to save the list of compiler substitutions from the preferred compiler
    # so that we have access to it when we build the MPI meta module.
    preferred_compiler = get_preferred_compiler()
    logging.info("  ... preferred compiler: {}".format(preferred_compiler))

    # Sort the list using a custom key
    def custom_sort_key(entry):
        # Return a tuple where the first element is 1 if the entry contains the word, else 0
        # The second element is the entry itself for natural sorting within groups
        return (1 if preferred_compiler in entry else 0, entry)
    compilers = sorted(compilers, key=custom_sort_key)

   # Get mpi providers (currently only one mpi provider is supported)
    mpi_providers = q.providers_for("mpi")
    if len(mpi_providers)>1:
        raise Exception(f"Expected no or one MPI provider, but got {mpi_providers}")
    logging.info(f"  ... mpi_providers: {mpi_providers}")

    # Prepare meta module directory
    logging.info("Preparing meta module directory ...")
    meta_module_dir = os.path.join(module_dir, "Core")
    if not os.path.isdir(meta_module_dir):
        os.mkdir(meta_module_dir)
    logging.info("  ... meta module directory : {}".format(meta_module_dir))

    # Create compiler modules
    logging.info("Creating compiler modules ...")

    # Initialize saved substitutes to None (populate for preferred compiler later)
    COMPILER_SUBSTITUTES_SAVE = None

    # Collect and save modulepaths for the preferred compiler
    MODULEPATHS_SAVE = []

    # For tcl, append modulepath for external specs and for specs without
    # compiler dependencies; remove the compiler prefices from the moduless
    if module_choice == "tcl":
        modulepath_save = os.path.join(module_dir, "none", "none")
        if not os.path.isdir(modulepath_save):
            os.makedirs(modulepath_save)
        logging.info("  ... appending {} to MODULEPATHS_SAVE".format(modulepath_save))
        MODULEPATHS_SAVE.append(modulepath_save)
        remove_compiler_prefices_from_tcl_modulefiles(
            modulepath_save,
            compiler_list,
            mpi_provider = None
        )

    for compiler in compilers:
        logging.info(f"  ... configuring compiler {compiler.name}@{compiler.version}")

        modulepath_save = os.path.join(module_dir, compiler.name, str(compiler.version))
        if not os.path.isdir(modulepath_save):
            os.makedirs(modulepath_save)
        logging.info("  ... ... appending {} to MODULEPATHS_SAVE".format(modulepath_save))
        MODULEPATHS_SAVE.append(modulepath_save)

        # For tcl modules remove the compiler prefices from the module contents
        if module_choice == "tcl":
            remove_compiler_prefices_from_tcl_modulefiles(
                modulepath_save,
                compiler_list,
                mpi_provider = None
            )

        # The remainder of the loop is only needed for the preferred compiler
        if not compiler.name in preferred_compiler:
            continue

        logging.info(
            "  ... configuring stack compiler {}@{}".format(compiler.name, compiler.version)
        )
        compiler_module_dir = os.path.join(meta_module_dir, "stack-" + compiler.name)
        compiler_module_file = os.path.join(
            compiler_module_dir, str(compiler.version) + MODULE_FILE_EXTENSION[module_choice]
        )
        substitutes = SUBSTITUTES_TEMPLATE.copy()

        if not compiler.external:
            raise Exception(f"spack-built compiler {compiler} not yet supported")

        # Use existing modules for external mpi providers; otherwise, use spack-built module
        if compiler.external and compiler.external_modules:
            for module in compiler.external_modules:
                substitutes["MODULELOADS"] += module_load_command(module_choice, module)
        else:
            module = "{}/{}".format(compiler.name, compiler.version)
            substitutes["MODULELOADS"] += module_load_command(module_choice, module)
        substitutes["MODULELOADS"] = substitutes["MODULELOADS"].rstrip("\n")
        logging.debug("  ... ... MODULELOADS: {}".format(substitutes["MODULELOADS"]))

        # Compiler environment variables; names are lowercase in spack
        substitutes["CC"] = compiler.extra_attributes["compilers"]["c"]
        substitutes["CXX"] = compiler.extra_attributes["compilers"]["cxx"]
        substitutes["F77"] = compiler.extra_attributes["compilers"]["fortran"]
        substitutes["FC"] = compiler.extra_attributes["compilers"]["fortran"]
        logging.debug("  ... ... CC  : {}".format(substitutes["CC"]))
        logging.debug("  ... ... CXX : {}".format(substitutes["CXX"]))
        logging.debug("  ... ... F77 : {}".format(substitutes["F77"]))
        logging.debug("  ... ... FC' : {}".format(substitutes["FC"]))

        # Compiler flags; names are lowercase in spack
        if "flags" in compiler.extra_attributes.keys():
            for flag_name in compiler.extra_attributes["flags"].keys():
                flag_values = compiler.extra_attributes["flags"][flag_name]
                substitutes["COMPFLAGS"] += setenv_command(
                    module_choice, flag_name.upper(), flag_values
                )
        substitutes["COMPFLAGS"] = substitutes["COMPFLAGS"].rstrip("\n")
        logging.debug("  ... ... COMPFLAGS: {}".format(substitutes["COMPFLAGS"]))

        # Environment variables
        if "environment" in compiler.extra_attributes.keys():
            for action in compiler.extra_attributes["environment"].keys():
                for env_name in compiler.extra_attributes["environment"][action]:
                    env_values = compiler.extra_attributes["environment"][action][env_name]
                    substitutes["ENVVARS"] += envmod_command(
                        module_choice,
                        action,
                        env_name,
                        env_values
                    )
        substitutes["ENVVARS"] = substitutes["ENVVARS"].rstrip("\n")
        logging.debug("  ... ... ENVVARS  : {}".format(substitutes["ENVVARS"]))

        # Spack compiler module hierarchy - append all saved modulepaths
        for modulepath in MODULEPATHS_SAVE:
            substitutes["MODULEPATHS"] += modulepath_prepend_command(module_choice, modulepath)
        substitutes["MODULEPATHS"] = substitutes["MODULEPATHS"].rstrip("\n")
        logging.debug("  ... ... MODULEPATHS  : {}".format(substitutes["MODULEPATHS"]))

        # Read compiler template into module_content string
        with open(COMPILER_TEMPLATES[module_choice]) as f:
            module_content = f.read()

        # Substitute variables in module_content
        for key in substitutes.keys():
            module_content = module_content.replace("@{}@".format(key), substitutes[key])

        # Write compiler lua module
        if not os.path.isdir(compiler_module_dir):
            os.makedirs(compiler_module_dir)
        with open(compiler_module_file, "w") as f:
            f.write(module_content)
        logging.info("  ... writing {}".format(compiler_module_file))

        # If this is the last compiler in the list (i.e. the preferred compiler),
        # then save the substitutes for later when building the MPI meta module
        if compiler == compilers[-1]:
            COMPILER_SUBSTITUTES_SAVE = substitutes

    # Collect and save modulepaths for MPI with preferred compiler
    MODULEPATHS_SAVE = []

    # Create mpi modules - currently, only one mpi provider is allowed
    for mpi_provider in mpi_providers:

        # For tcl, append modulepath for external specs and for specs without
        # compiler dependencies; remove the compiler/mpi prefices from the moduless
        if module_choice == "tcl":
            modulepath_save = os.path.join(module_dir, mpi_provider.name, str(mpi_provider.version), "none", "none")
            if not os.path.isdir(modulepath_save):
                os.makedirs(modulepath_save)
            logging.info("  ... appending {} to MODULEPATHS_SAVE".format(modulepath_save))
            MODULEPATHS_SAVE.append(modulepath_save)
            remove_compiler_prefices_from_tcl_modulefiles(
                modulepath_save,
                compiler_list,
                mpi_provider = mpi_provider
            )

        for compiler in compilers:
            logging.info(
                "  ... configuring stack mpi library {}@{} for compiler {}@{}".format(
                    mpi_provider.name, mpi_provider.version, compiler.name, compiler.version
                )
            )

            # Spack mpi+compiler module hierarchy
            modulepath_save = os.path.join(
                module_dir, mpi_provider.name, str(mpi_provider.version), compiler.name, str(compiler.version)
            )
            if not os.path.isdir(modulepath_save):
                os.makedirs(modulepath_save)
            logging.info("  ... ... appending {} to MODULEPATHS_SAVE".format(modulepath_save))
            MODULEPATHS_SAVE.append(modulepath_save)

            # For tcl modules remove the compiler/mpi prefices from the module contents
            if module_choice == "tcl":
                remove_compiler_prefices_from_tcl_modulefiles(
                    modulepath_save,
                    compiler_list,
                    mpi_provider = mpi_provider
                )

            # The remainder of the loop is only needed for the preferred compiler
            if not compiler.name in preferred_compiler:
                continue

            # Path and name for mpi module file
            mpi_module_dir = os.path.join(
                module_dir, compiler.name, str(compiler.version), "stack-" + mpi_provider.name
            )
            mpi_module_file = os.path.join(
                mpi_module_dir, str(mpi_provider.version).split("-")[0] + MODULE_FILE_EXTENSION[module_choice]
            )

            substitutes = SUBSTITUTES_TEMPLATE.copy()
            # Use existing modules for external mpi providers; otherwise, use spack-built module
            if mpi_provider.external and mpi_provider.external_modules:
                for module in mpi_provider.external_modules:
                    substitutes["MODULELOADS"] += module_load_command(module_choice, module)
            else:
                module = "{}/{}".format(mpi_provider.name, mpi_provider.version)
                substitutes["MODULELOADS"] += module_load_command(module_choice, module)
            substitutes["MODULELOADS"] = substitutes["MODULELOADS"].rstrip("\n")
            logging.debug("  ... ... MODULELOADS: {}".format(substitutes["MODULELOADS"]))

            # Compiler wrapper environment variables
            if mpi_provider.name == "intel-oneapi-mpi" and compiler.name == "intel-oneapi-compilers":
                substitutes["MPICC"]  = os.path.join("mpiicx")
                substitutes["MPICXX"] = os.path.join("mpiicpx")
                if "ifx" in COMPILER_SUBSTITUTES_SAVE["FC"] and not "ifort" in COMPILER_SUBSTITUTES_SAVE["FC"]:
                    substitutes["MPIF77"] = os.path.join("mpiifx")
                    substitutes["MPIF90"] = os.path.join("mpiifx")
                elif not "ifx" in COMPILER_SUBSTITUTES_SAVE["FC"] and "ifort" in COMPILER_SUBSTITUTES_SAVE["FC"]:
                    substitutes["MPIF77"] = os.path.join("mpiifort")
                    substitutes["MPIF90"] = os.path.join("mpiifort")
                else:
                    raise Exception(f"For {mpi_provider.name}, cannot determine MPI wrapper from FC={COMPILER_SUBSTITUTES_SAVE['FC']}")
            elif mpi_provider.name == "intel-oneapi-mpi" and compiler.name == "intel-oneapi-compilers-classic":
                substitutes["MPICC"]  = os.path.join("mpiicc")
                substitutes["MPICXX"] = os.path.join("mpiicpc")
                substitutes["MPIF77"] = os.path.join("mpiifort")
                substitutes["MPIF90"] = os.path.join("mpiifort")
            else:
                substitutes["MPICC"]  = os.path.join("mpicc")
                substitutes["MPICXX"] = os.path.join("mpic++")
                substitutes["MPIF77"] = os.path.join("mpif77")
                substitutes["MPIF90"] = os.path.join("mpif90")
            # Also set the direct compiler environment variables
            substitutes["CC"]  = COMPILER_SUBSTITUTES_SAVE["CC"]
            substitutes["CXX"] = COMPILER_SUBSTITUTES_SAVE["CXX"]
            substitutes["F77"] = COMPILER_SUBSTITUTES_SAVE["F77"]
            substitutes["FC"]  = COMPILER_SUBSTITUTES_SAVE["FC"]

            # Spack mpi+compiler module hierarchy - append all saved modulepaths
            for modulepath in MODULEPATHS_SAVE:
                substitutes["MODULEPATHS"] += modulepath_prepend_command(module_choice, modulepath)
            substitutes["MODULEPATHS"] = substitutes["MODULEPATHS"].rstrip("\n")
            logging.debug("  ... ... MODULEPATHS  : {}".format(substitutes["MODULEPATHS"]))

            # Read compiler lua template into module_content string
            with open(MPI_TEMPLATES[module_choice]) as f:
                module_content = f.read()

            # Substitute variables in module_content
            for key in substitutes.keys():
                module_content = module_content.replace(
                    "@{}@".format(key), substitutes[key]
                )

            # Write mpi lua module
            if not os.path.isdir(mpi_module_dir):
                os.makedirs(mpi_module_dir)
            with open(mpi_module_file, "w") as f:
                f.write(module_content)
            logging.info("  ... writing {}".format(mpi_module_file))

    logging.info("Metamodule generation completed successfully in {}".format(meta_module_dir))
