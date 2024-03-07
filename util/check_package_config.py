#!/usr/bin/env python3
# This utility checks whether the package versions and variants set in
# common/packages.yaml are being respected in the concretization, and
# whether the externals in site/packages.yaml are being used.
#
# To use this script, run it in a loaded spack-stack environment.
# Package names to be ignored can be provided as optional arguments
# using -i/--ignore.
#
# Usage:
#  $ spack env active myenv
#  $ ${SPACK_STACK_DIR}/util/check_package_config.py
# Ignore packages foo and bar:
#  $ ${SPACK_STACK_DIR}/util/check_package_config.py -i foo -i bar
#
# Alex Richert, Jan 2024

import json
import os
import sys

SPACK_ROOT = os.getenv("SPACK_ROOT")
assert SPACK_ROOT, "$SPACK_ROOT must be set but is not!"
sys.path.append(os.path.join(SPACK_ROOT, "lib/spack/external/_vendoring"))
from ruamel import yaml

SPACK_ENV = os.getenv("SPACK_ENV")
assert SPACK_ENV, "$SPACK_ENV must be set but is not!"

# Load common/packages.yaml and site/packages.yaml for versions and externals, respectively
packages_versions_path = os.path.join(SPACK_ENV, "common", "packages.yaml")
with open(packages_versions_path, "r") as f:
    packages_versions = yaml.safe_load(f)

packages_externals_path = os.path.join(SPACK_ENV, "site", "packages.yaml")
with open(packages_externals_path, "r") as f:
    packages_externals = yaml.safe_load(f)

# Load spack.lock
spack_lock_path = os.path.join(SPACK_ENV, "spack.lock")
with open(spack_lock_path, "r") as f:
    spack_lock = json.load(f)

iret = 0

# Set up list of packages to ignore
args = sys.argv[1:]
if args:
    assert args[-1] not in ("-i", "--ignore"), "-i/--ignore option requires package name"
    ignore_list = [args[iarg+1] for iarg in range(len(args)) if args[iarg] in ("-i", "--ignore")]
    if ignore_list:
        print("Ignoring the following packages: %s" % ", ".join(ignore_list), file=sys.stderr)
else:
    ignore_list = []

# Iterate over concretized packages
for concrete_spec in spack_lock["concrete_specs"].values():
    concrete_name = concrete_spec["name"]
    # Ignore user-specified packages:
    if concrete_name in ignore_list:
        continue
    concrete_version = concrete_spec["version"]
    if concrete_name in packages_versions["packages"].keys():
        # Check whether concretized package has specified version from common/packages.yaml
        if "version" in packages_versions["packages"][concrete_name].keys():
            config_version = packages_versions["packages"][concrete_name]["version"][0]
            if concrete_version != config_version:
                iret = 1
                print(
                    f"WARNING: '{concrete_name}' concretized version {concrete_version} does not match {config_version} specified in $SPACK_ENV/common/packages.yaml"
                )
        # Check whether concretized variants match settings from common/packages.yaml
        if "variants" in packages_versions["packages"][concrete_name].keys():
            config_variants = packages_versions["packages"][concrete_name]["variants"].split()
            for config_variant in config_variants:
                variant_mismatch = False
                # Boolean variant
                if config_variant[0] in ("+", "~"):
                    config_value = config_variant[0] == "+"
                    if not 'config_variant[1:]' in concrete_spec["parameters"].keys():
                        variant_mismatch = True
                    elif concrete_spec["parameters"][config_variant[1:]] != config_value:
                        variant_mismatch = True
                # Named variant
                elif "=" in config_variant:
                    config_variant, config_value = config_variant.split("=")
                    if not config_variant in concrete_spec["parameters"].keys():
                        variant_mismatch = True
                    else:
                        concrete_values = concrete_spec["parameters"][config_variant]
                        if type(concrete_values) is str:
                            concrete_values = [concrete_values]
                        if set(config_value.split(",")) != set(concrete_values):
                            variant_mismatch = True
                if variant_mismatch:
                    iret = 1
                    print(
                        f"WARNING: '{concrete_name}' concretized variant '{config_variant}' does not match configured value in $SPACK_ENV/common/packages.yaml"
                    )
    # Check whether concretized package is an external based on site/packages.yaml
    if concrete_name in packages_externals["packages"].keys():
        is_external_config = "externals" in packages_externals["packages"][concrete_name].keys()
    else:
        is_external_config = False
    is_external_concrete = "external" in concrete_spec.keys()
    if is_external_config != is_external_concrete:
        iret = 1
        print(
            f"WARNING: '{concrete_name}' is %sconfigured as external in $SPACK_ENV/site/packages.yaml but was %sconcretized as external"
            % ((not is_external_config) * "not ", (not is_external_concrete) * "not ")
        )

sys.exit(iret)
