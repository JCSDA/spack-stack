#!/usr/bin/env python3

# Whitelist file patterns (checked with re.match()) that will be satisfied by
# compiler & MPI modules (though arguably these should be added as extra
# rpaths).
whitelist = [
    "^libmkl.+",
]

########

import argparse
import glob
import os
import platform
import re
import subprocess
import sys

parser = argparse.ArgumentParser(description="Check executables and shared libraries for missing dependencies")

parser.add_argument(
    "path",
    nargs="?",
    default=os.getcwd(),
    help="Spack environment path ($SPACK_ENV) that contains install/ subdirectory (default: current directory)",
)
parser.add_argument(
    "--progress",
    "-p",
    action="store_true",
    help="Print progress to stderr",
)

args = parser.parse_args()

platform = platform.system()
if platform=="Linux":
    ldd_cmd = "ldd"
    error_pattern = " => not found"
    getlibname = lambda line: re.findall("^[^ ]+", line)[0]
elif platform=="Darwin":
    print("macOS not yet supported", file=sys.stderr)
    sys.exit(1)
else:
    print(f"Platform '{platform}' not supported", file=sys.stderr)
    sys.exit(1)

searchpath = os.path.join(args.path, "install")

bin_list = glob.glob(os.path.join(searchpath, "*/*/*/bin/*"))
dlib_list = glob.glob(os.path.join(searchpath, "*/*/*/lib*/*.{so,dylib}"))

master_list = bin_list + dlib_list

assert master_list, "No files found! Check directory and ensure it contains install/ subdirectory"

for i in range(len(master_list)):
    file_to_check = master_list[i]
    if args.progress: print(f"\rProgress: {i+1}/{len(master_list)}", file=sys.stderr, end="")
    p = subprocess.Popen([ldd_cmd, file_to_check], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    raw_output, null = p.communicate()
    output = raw_output.decode(sys.stdout.encoding).strip()
    if error_pattern in output:
        missing_set = set([getlibname(l.strip()) for l in output.split("\n") if error_pattern in l])
        missing_list = [l for l in missing_set if not any([re.match(p, l) for p in whitelist])]
        if not missing_list: continue
        missing_output = ",".join(sorted(missing_list))
        print(f"\rWARNING: File {file_to_check} contains the following missing libraries: {missing_output}")

if args.progress: print()
