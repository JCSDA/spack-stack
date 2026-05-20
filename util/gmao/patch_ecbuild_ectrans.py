#!/usr/bin/env python3
"""
Patch/revert ecbuild_add_lang_flags.cmake to work around an ectrans build
failure with oneapi at NAS (nas/nas-toss5).

The problem: ecbuild's Fortran flag checker incorrectly determines that
'-march=core-avx2 -no-fma' is not supported by ifx (via spack compiler
wrapper), and calls ecbuild_critical() which aborts the build. The flags
are actually valid -- the check is a false negative.

The fix: replace the ecbuild_critical() call in the else() block with
the same logic as the if(_flag_ok) block, so the flags are always added
regardless of the check result.

See: https://github.com/JCSDA/spack-stack/issues/1775#issuecomment-3898802720

Usage:
    patch_ecbuild_ectrans.py --patch  <ecbuild_add_lang_flags.cmake>
    patch_ecbuild_ectrans.py --revert <ecbuild_add_lang_flags.cmake>
"""

import argparse
import shutil
import sys
from pathlib import Path

OLD = """    else()
      ecbuild_critical( "${_lang} compiler ${CMAKE_${_lang}_COMPILER} does not recognise ${_lang} flag '${_flags}'" )"""

NEW = """    else()
      ecbuild_info( "${_lang} compiler ${CMAKE_${_lang}_COMPILER} does not recognise ${_lang} flag '${_flags}' -- forcing anyway (NAS oneapi workaround)" )
      if( _PAR_BUILD )
        set( CMAKE_${_lang}_FLAGS_${_PAR_BUILD} "${CMAKE_${_lang}_FLAGS_${_PAR_BUILD}} ${_flags}" PARENT_SCOPE )
        ecbuild_info( "Added ${_lang} flag [${_flags}] to build type ${_PAR_BUILD}" )
      else()
        set( CMAKE_${_lang}_FLAGS "${CMAKE_${_lang}_FLAGS} ${_flags}" PARENT_SCOPE )
        ecbuild_info( "Added ${_lang} flag [${_flags}]" )
      endif()"""


def patch(cmake_file: Path):
    backup = Path(str(cmake_file) + ".orig")
    content = cmake_file.read_text()
    if OLD not in content:
        if NEW in content:
            print(f"Patch already applied to {cmake_file} -- skipping")
            return
        print(f"WARNING: expected patch target not found in {cmake_file} -- skipping", file=sys.stderr)
        return
    shutil.copy(cmake_file, backup)
    cmake_file.write_text(content.replace(OLD, NEW, 1))
    print(f"Patched {cmake_file} (backup: {backup})")


def revert(cmake_file: Path):
    backup = Path(str(cmake_file) + ".orig")
    if not backup.exists():
        print(f"WARNING: backup {backup} not found -- cannot revert", file=sys.stderr)
        return
    shutil.copy(backup, cmake_file)
    backup.unlink()
    print(f"Reverted {cmake_file} (removed {backup})")


def main():
    parser = argparse.ArgumentParser(description="Patch/revert ecbuild for ectrans NAS oneapi workaround")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--patch", action="store_true", help="Apply the patch")
    group.add_argument("--revert", action="store_true", help="Revert the patch")
    parser.add_argument("cmake_file", type=Path, help="Path to ecbuild_add_lang_flags.cmake")
    args = parser.parse_args()

    if not args.cmake_file.exists():
        print(f"ERROR: file not found: {args.cmake_file}", file=sys.stderr)
        sys.exit(1)

    if args.patch:
        patch(args.cmake_file)
    else:
        revert(args.cmake_file)


if __name__ == "__main__":
    main()
