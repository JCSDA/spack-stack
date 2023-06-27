#!/usr/bin/env python3

# Check output of `spack concretize` for duplicate packages.
# Usage:
#   show_duplicate_packages.py log.concretize
#    -OR-
#   spack concretize | tee log.concretize | show_duplicate_packages.py > list_of_duplicates.txt
#
# '-d' argument prints only duplicates (and disables highlighting).
#
# Alex Richert, June 2023

import argparse
import re
import sys
from collections import defaultdict

def colorize_spec(line, package_name, colorize=False):
    if not colorize: return line
    c1 = r'\033[93m' ; c2 = r'\033[0m'
    return re.sub("(\w{7}\s+)(%s)@"%package_name, f"\\1{c1}\\2{c2}@", line)

def show_duplicate_packages(txt_to_check, ignore_list=[], only_show_dups=False):
    dd = defaultdict(set)
    for line in txt_to_check.split("\n"):
        line = line.replace("^", "")
        package_name = re.findall("\s\w{7}\s+(\^?[^\s@]+)@", line)
        if not package_name: continue
        if package_name[0] in ignore_list: continue
        line = "  ".join(line.split()[1:])
        dd[package_name[0]].add(line)
    duplicates_found = False
    for key in sorted(dd.keys()):
        multiple = len(dd[key])>1
        if only_show_dups and not multiple: continue
        if only_show_dups: colorize = False
        else: colorize = multiple
        if multiple: duplicates_found = True
        for line in dd[key]:
            print(colorize_spec(line, key, colorize=colorize))
    sys.stderr.write("===\n%suplicates found%s\n" % (("D","!") if duplicates_found else ("No d",".")))
    sys.stderr.flush()
    return int(duplicates_found)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check output of `spack concretize` for duplicate packages")
    parser.add_argument("filename", nargs="?")
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-i", nargs="*", default=[])
    args = parser.parse_args()
    if args.filename:
        with open(args.filename, "r") as f:
            txt_to_check = f.read()
    else:
        txt_to_check = sys.stdin.read()
    ret = show_duplicate_packages(txt_to_check, only_show_dups=args.d, ignore_list=args.i)
    sys.exit(ret)

