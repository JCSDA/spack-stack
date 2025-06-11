#!/usr/bin/env bash

ierror=0

searchfor="libirc.so"

echo "Checking shared libraries for ${searchfor} ..."
for file in `find ${SPACK_ENV} -type f -iname '*.so*'`; do
  # Return code from grep is 1 if not found, 0 if found
  ldd $file 2>&1 | grep "${searchfor}"
  if [[ $? -eq 0 ]]; then
    echo "Found ${searchfor} linked in ${file}"
    ierror=1
  fi
done

echo "Checking executables for ${searchfor} ..."
for file in `find ${SPACK_ENV} -type f -executable`; do
  # Return code from grep is 1 if not found, 0 if found
  ldd $file 2>&1 | grep "${searchfor}"
  if [[ $? -eq 0 ]]; then
    echo "Found ${searchfor} linked in ${file}"
    ierror=1
  fi
done

exit ${ierror}
