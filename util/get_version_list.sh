#!/bin/bash

# Gets list of versions from active or specified environment and prints a
# wiki-formatted table to be inserted into the spack-stack wiki.
# Only reports packages directly used by *-env metapackages.
# Uses SPACK_ENV by default to derive list of installed packages.
# The entire output can be copied and pasted into the wiki page at
# https://github.com/JCSDA/spack-stack/wiki/Package-versions
# noting that <SITE> should be replaced by the appropriate site name.

# Usage:
#  $ . setup.sh
#  $ ./util/get_version_list.sh envs/unified-dev

# Alex Richert, Jan 2025

set -e

if [ -z $SPACK_ENV ]; then
  export SPACK_ENV=$1
fi

export SPACK_STACK_DIR=${SPACK_STACK_DIR:-$(realpath ${SPACK_ENV}/../..)}
spackstackver=$(echo $SPACK_STACK_DIR | grep -oP "/\Kspack-stack-[^/]+")
echo "# $spackstackver"
# Determine which packages to report versions of by looking at -env packages
envmetapkgs=$(grep -Po '(-) \K[^\s]+-env' ${SPACK_STACK_DIR}/configs/templates/unified-dev/spack.yaml | grep '-env$' | sort | uniq)
secondarymetapkgs=$(for p in $envmetapkgs ; do spack dependencies $p ; done | grep '-env$' | sort | uniq)
metapkgs=$(echo -e "${envmetapkgs}\n${secondarymetapkgs}")
deplist=$(for p in $metapkgs ; do spack dependencies $p ; done | grep -v '-env$' | sort | uniq)
installedlist=$(spack find --format '{name}')
pkgstoreport=$(echo "$installedlist" | grep -xf <(echo "$deplist"))
listfortable=$(spack find --format '| {name} | {version} |' $pkgstoreport)
echo -e "| Package_name | Version |\n| --- | --- |\n$listfortable" | column -t | sed 's:Package_name:Package name:'
echo
echo "_Versions taken from <SITE>:${SPACK_ENV}_"
