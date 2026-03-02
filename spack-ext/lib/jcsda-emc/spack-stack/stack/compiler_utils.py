#!/usr/bin/env python3

import logging
import re

import spack
import spack.environment as ev
from spack.provider_index import ProviderIndex

from spack.extensions.stack.common import ALIASES
from spack.extensions.stack.common import GREEN, RED, RESET
from spack.extensions.stack.common import get_preferred_compiler


def get_compiler_name_and_version(string):
    compiler_name = string.replace("@=", "@").split("@")[0]
    try:
        compiler_version = string.replace("@=", "@").split("@")[1]
    except:
        compiler_version = None
    return (compiler_name, compiler_version)


def get_compiler_choice(string):
    """Parse string for a Spack version 1 compiler dependency
    declaration. By intentionally not matching old (spack v0)
    compiler dependency declarations ("%gcc", "%oneapi", ...),
    we force updating the Spack configuration files to v1."""
    COMPILER_CHOICE_REGEX_STRING = "^(%+)(" + \
        "c=|" + \
        "cxx=|" + \
        "fortran=|" + \
        "c,cxx=|" + \
        "cxx,c=|" + \
        "c,fortran=|" + \
        "fortran,c=|" + \
        "cxx,fortran=|" + \
        "fortran,cxx=|" + \
        "c,cxx,fortran=|" + \
        "fortran,c,cxx=|" + \
        "cxx,fortran,c=|" + \
        "c,fortran,cxx=|" + \
        "cxx,c,fortran=|" + \
        "fortran,cxx,c=)(\S+)\s*$"
    COMPILER_CHOICE_REGEX = re.compile(COMPILER_CHOICE_REGEX_STRING)
    match = COMPILER_CHOICE_REGEX.match(string)
    if match:
        return match.group(3)
    return None


def check_preferred_compiler():
    """For an active environment, check that the preferred compiler
    is being used for all packages except those that explicitly
    request a different compiler. For the latter packages, check
    that the explicitly requested compiler is being used."""

    logging.info("Configuring active spack environment ...")
    env_dir = ev.active_environment().path
    if not env_dir:
        raise Exception("No active spack environment")
    env = spack.environment.Environment(env_dir)
    spack.environment.environment.activate(env)
    logging.info("  ... environment directory: {}".format(env_dir))

    # Get all specs and determine compilers
    specs = env.all_specs()
    if not specs:
        raise Exception(f"{RED}No specs found - did you run 'spack concretize'?{RESET}")
    q = ProviderIndex(specs=specs, repository=spack.repo.PATH)

    c_providers = q.providers_for("c")
    cxx_providers = q.providers_for("cxx")
    fortran_providers = q.providers_for("fortran")
    compilers = list(set(c_providers + cxx_providers + fortran_providers))
    if not compilers:
        raise Exception(f"{RED}No compilers found{RESET}!")
    logging.info(f"  ... compilers: {compilers}")

    # Determine the preferred compiler
    preferred_compiler = get_preferred_compiler(spack.config)
    (preferred_compiler_name, preferred_compiler_version) = get_compiler_name_and_version(preferred_compiler)
    logging.info("  ... preferred compiler: {}".format(preferred_compiler))

    # Get package config to compare actual specs against the intended config
    package_config = spack.config.get("packages")

    logging.info("Checking all specs ...")
    errors = 0
    for spec in specs:
        # If the spec has no compiler dependency, an exception will be thrown - ignore package
        try:
            compiler_name = spec.compiler.name
            compiler_version = spec.compiler.version if preferred_compiler_version else None
        except:
            logging.info(f"  ... {spec.name}@{spec.version}/{spec.dag_hash(length=7)} has no compiler dependency")
            continue
        # If the spec compiler matches the preferred compiler for the environment, move on.
        # Note that this permits situations where a packages has an explicit preferred (but
        # not explicitly required) compiler, but Spack decides to use the preferred (and
        # different) compiler for the environment instead.
        if preferred_compiler_name == compiler_name and preferred_compiler_version  == compiler_version:
            logging.info(f"  ... {spec.name}@{spec.version}/{spec.dag_hash(length=7)} uses preferred compiler")
        else:
            spec_required_compiler_name = None
            spec_required_compiler_version = None
            spec_preferred_compiler_name = None
            spec_preferred_compiler_version = None
            for key, value in package_config[spec.name].items():
                # To simplify parsing, turn scalar values into CommentedSeq of length 1
                if isinstance(value, (str, bytes)):
                    values = CommentedSeq([value])
                else:
                    values = value
                # Loop through all values to check for required or preferred compilers
                for entry in values:
                    if key.lower() == "require":
                        choice = get_compiler_choice(entry.lower())
                        # Not a compiler preference, carry on
                        if not choice:
                            continue
                        # Check that the explicitly required compiler is a valid (existing)
                        # compiler for this environment. This requirement may be relaxed in
                        # the future if we start building compilers in spack environments.
                        if any(choice in c for c in compilers):
                            (spec_required_compiler_name, spec_required_compiler_version) = get_compiler_name_and_version(choice)
                    elif key.lower() == "prefer":
                        choice = get_compiler_choice(entry.lower())
                        # Not a compiler preference, carry on
                        if not choice:
                            continue
                        # Check that the explicitly preferred compiler is a valid (existing)
                        # compiler for this environment. This requirement may be relaxed in
                        # the future if we start building compilers in spack environments.
                        if any(choice in c for c in compilers):
                            (spec_preferred_compiler_name, spec_preferred_compiler_version) = get_compiler_name_and_version(choice)
                # If we have a hard requirement for a compiler, we can stop scanning the spec package config
                if spec_required_compiler_name:
                    break
            if spec_required_compiler_name == compiler_name and \
                ( (not spec_required_compiler_version or not compiler_version) or \
                  (spec_required_compiler_version==compiler_version) ):
                logging.info(f"  ... {spec.name}@{spec.version}/{spec.dag_hash(length=7)} uses explicitly required compiler")
            elif spec_preferred_compiler_name == compiler_name and \
                ( (not spec_preferred_compiler_version or not compiler_version) or \
                  (spec_preferred_compiler_version==compiler_version) ):
                logging.info(f"  ... {spec.name}@{spec.version}/{spec.dag_hash(length=7)} uses explicitly preferred compiler")
            else:
                errors += 1
                logging.error(f"  ... {RED}error: {spec.name}@{spec.version}/{spec.dag_hash(length=7)} does not use intended compiler\n" + \
                    f"      check also that any explicit preferred/required compiler dependencies are using Spack v1 syntax{RESET}")
    if errors==1:
        raise Exception(f"{RED}Detected {errors} compiler mismatch!{RESET}")
    elif errors:
        raise Exception(f"{RED}Detected {errors} compiler mismatches!{RESET}")
    else:
        logging.info(f"{GREEN}No compiler mismatches found.{RESET}")
