#!/usr/bin/env python3

# This utility ensures that the modules_lmod.yaml and modules_ycl.yaml appropriately match

import difflib
import os

import spack.util.spack_yaml as syaml

print("Checking modules_lmod.yaml and modules_tcl.yaml for configuration differences...")

# Load modules_lmod.yaml and modules_tcl.yaml
SPACK_STACK_DIR = os.getenv("SPACK_STACK_DIR")
modules = dict()

for lmod_or_tcl in ("lmod", "tcl"):
    yaml_path = os.path.join(SPACK_STACK_DIR, f"configs/common/modules_{lmod_or_tcl}.yaml")

    with open(yaml_path, "r") as f:
        yaml_raw = f.read().replace("lmod:", "LMOD_OR_TCL:").replace("tcl:", "LMOD_OR_TCL:")
        modules[lmod_or_tcl] = syaml.load_config(yaml_raw)

# Check subset of projection to ensure keys match
lmod_projections = modules["lmod"]["modules"]["default"]["LMOD_OR_TCL"]["projections"].keys()
tcl_projections = modules["tcl"]["modules"]["default"]["LMOD_OR_TCL"]["projections"].keys()
assert set(lmod_projections) == set(tcl_projections)-{"all", "^mpi"}

for lmod_or_tcl in ("lmod", "tcl"):
    for key in modules[lmod_or_tcl]["modules"]["default"]["LMOD_OR_TCL"]["projections"].keys():
        modules[lmod_or_tcl]["modules"]["default"]["LMOD_OR_TCL"]["projections"][key] = "DUMMYVALUE"

# Removing sections we don't want to compare; note this will
#  affect line numbers in the diff output
del(modules["lmod"]["modules"]["default"]["LMOD_OR_TCL"]["hierarchy"])
del(modules["tcl"]["modules"]["default"]["LMOD_OR_TCL"]["projections"]["all"])
del(modules["tcl"]["modules"]["default"]["LMOD_OR_TCL"]["projections"]["^mpi"])

# If sections mismatch, print a diff of the whole configuration
dump_lmod = syaml.dump_config(modules["lmod"]).split("\n")
dump_tcl = syaml.dump_config(modules["tcl"]).split("\n")
diff = "\n".join(list(difflib.context_diff(dump_lmod, dump_tcl)))
if diff:
    print(diff)
assert not diff, f"Mismatch(es) found between modules_lmod.yaml and modules_tcl.yaml"

print("No configuration differences found between modules_lmod.yaml and modules_tcl.yaml")
