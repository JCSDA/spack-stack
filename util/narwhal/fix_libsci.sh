#!/usr/bin/env bash

# Utility script to work arounds issues on Narwhal, where an old cray-libsci
# implementation is found and used by spack packages that use autotools,
# libtool, and configure. This is because of symbolic links in /opt/cray/pe/lib64
# pointing to the old (v21) libsci installation, and /etc/ld.so.conf.d/ containing
# a file that tells the build system to include libraries from /opt/cray/pe/lib64.

# The approach is to scan all shared libraries in a spack-stack environment and
# use patchelf to replace the "bad" libsci references in those with references
# to the "good" libsci version (determined by looking at the module that is loaded).

# Check input requirements
echo
echo "Checking for patchelf ..."
which patchelf || (echo "ERROR, patchelf not found!" && exit 1)

echo
echo "Checking for active spack environment ..."
[ ! -z ${SPACK_ENV} ] && echo ${SPACK_ENV} \
    || (echo "ERROR, not in an active spack environment!" && exit 1)

echo
echo "Checking for libsci in user environment ..."
[ ! -z ${CRAY_LIBSCI_PREFIX} ] && echo ${CRAY_LIBSCI_PREFIX} \
    || (echo "ERROR, CRAY_LIBSCI_PREFIX not defined!" && exit 1)

BAD_LIBSCI_PATH="/opt/cray/pe/lib64"
GOOD_LIBSCI_PATH="${CRAY_LIBSCI_PREFIX}/lib"
LIBSCI_PREFIX="libsci"

echo
for shlib in `lfs find ${SPACK_ENV}/install -type f -name 'lib*.so*'`; do
  # Skip backups taken by this program
  if [[ "${shlib}" == *"backup.libsci-original"* ]]; then
    echo "Skipping ${shlib} ..."
    continue
  fi
  # Check shared library
  echo "Checking ${shlib} ..."
  # First pass: check and fix, second pass: re-check and error out if still bad
  for (( pass=1; pass<=2; pass++ )); do
    # Check if grep finds a link to the bad libsci (if so, $? is zero)
    ldd $shlib | grep ${BAD_LIBSCI_PATH}/${LIBSCI_PREFIX} > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
      if [[ ${pass} -eq 1 ]]; then
        echo "Fixing ${shlib} ..."
      elif [[ ${pass} -eq 2 ]]; then
        echo "ERROR, when re-checking ${shlib}, still found bad libsci links!"
        ldd $shlib | grep ${BAD_LIBSCI_PATH}/${LIBSCI_PREFIX}
        exit 1
      fi
      # Get all offending references to the "bad" libsci (split multiline string into array)
      results=`ldd $shlib | grep ${BAD_LIBSCI_PATH}/${LIBSCI_PREFIX}`
      IFS=$'\n' read -r -d '' -a results <<< "$results"
      # Loop over lines containing references to "bad" libsci
      for (( i=0; i<${#results[@]}; i++ )); do
        # Split each line into items by whitespace
        IFS=' ' read -r -a items <<< "${results[$i]}"
        # Remove all leading and trailing whitespaces from each of the items
        for (( j=0; j<${#items[@]}; j++ )); do
          items[$j]=$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'<<<"${items[$j]}")
        done
        # Sanity check 1. The item with index 1 must be '=>' after removing whitespaces
        if [[ ! "${items[1]}" == "=>" ]]; then
          echo "ERROR parsing ldd output for file ${shlib}: '${results[$i]}'"
          exit 1
        fi
        # Sanity check 2. The name of the library (item[0]) must match the
        # name of the library it is linked to (filename from target path item[2])
        libname=${items[0]}
        test_libname=$(echo "${items[2]}" | rev | cut -d'/' -f1 | rev)
        if [[ ! "${items[0]}" == "${test_libname}" ]]; then
          echo "ERROR matching library name in ldd output for file ${shlib}: '${results[$i]}'"
          exit 1
        fi
        replacement=${GOOD_LIBSCI_PATH}/${libname}
        # Sanity check 3. The library must exist in the "good" libsci path.
        if [[ ! -e ${replacement} ]]; then
          echo "ERROR, replacement ${replacement} for ${to_replace} does not exist!"
          exit 1
        fi
        # Create a backup of the original shared library and replace the old
        # library (referenced as ${libname}) with the new one (${replacement})
        if [[ ! -f ${shlib}.backup.libsci-original ]]; then
          echo "Creating backup ${shlib}.backup.libsci-original"
          cp -a ${shlib} ${shlib}.backup.libsci-original
        fi
        # Patch shared library. Replace reference (rpath/direct link) with direct link
        echo "Executing 'patchelf --replace-needed ${libname} ${replacement} ${shlib}'"
        patchelf --replace-needed ${libname} ${replacement} ${shlib}
        if [[ $? -ne 0 ]]; then
          echo "ERROR executing 'patchelf --replace-needed ${libname} ${replacement} ${shlib}'"
          exit 1
        fi
      done
    else
      break
    fi
  done
done
