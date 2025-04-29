#!/usr/bin/env python3

# Check spack.lock for duplicate packages.
# Looks for spack.lock in $SPACK_ENV by default, otherwise assumes current directory.
#
# Usage:
#   show_duplicate_packages.py
#
# '-i' argument ignores a specific package, and can be invoked multiple times.
#
# Alex Richert, June 2023

import argparse
import json
import os
import re
import sys
from collections import defaultdict

def show_duplicate_packages(json_to_check, ignore_list=[], only_show_dups=False):
    dd = defaultdict(set)
    json_dict = json.loads(json_to_check)
    for _hash in json_dict["concrete_specs"].keys():
        pkg_name = json_dict["concrete_specs"][_hash]["name"]
        pkg_version = json_dict["concrete_specs"][_hash]["version"]
        key = pkg_name + "@" + pkg_version + "/" +_hash
        dd[pkg_name].add(key)
    duplicates_found = False
    for pkg_name in sorted(dd.keys()):
        if [pkg_name] in ignore_list:
            continue
        if len(dd[pkg_name])>1:
            print(dd[pkg_name])
            duplicates_found = True
    sys.stderr.write("===\n%suplicates found%s\n" % (("D","!") if duplicates_found else ("No d",".")))
    sys.stderr.flush()
    return int(duplicates_found)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check output of `spack concretize` for duplicate packages")
    parser.add_argument("-d", action="store_true", help="Only show duplicates (default output is colorized list of all packages)")
    parser.add_argument("-i", default=[], nargs="*", action="append", help="Ignore package name (e.g., 'hdf5', 'netcdf-c')")
    args = parser.parse_args()
    spack_env = os.getenv("SPACK_ENV")
    basedir = spack_env if spack_env else "./"
    with open(os.path.join(basedir, "spack.lock"), "r") as f:
        json_to_check = f.read()
    ret = show_duplicate_packages(json_to_check, only_show_dups=args.d, ignore_list=args.i)
    sys.exit(ret)
