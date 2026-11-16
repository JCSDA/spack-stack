#!/usr/bin/env bash

set -eu

umask 0022
module purge

if [ "$#" -lt 1 ]; then
  echo "Error: Not enough arguments. Provide Intel oneAPI installation prefix."
  exit 1
fi

ONEAPI_INSTALL_DIR=${1}
ONEAPI_VERSION="2026.0.0"
COMPILER_VERSION="2026.0"
MKL_VERSION="2026.0"
ONEAPI_DOWNLOAD_URL=https://registrationcenter-download.intel.com/akdlm/IRC_NAS/71180075-e4e3-4c6f-bbbb-19017ed0cf7d/intel-oneapi-toolkit-2026.0.0.198_offline.sh

mkdir -p ${ONEAPI_INSTALL_DIR}/src
cd ${ONEAPI_INSTALL_DIR}/src
wget ${ONEAPI_DOWNLOAD_URL}
ONEAPI_INSTALL_SCRIPT="${ONEAPI_DOWNLOAD_URL##*/}"
sh ./${ONEAPI_INSTALL_SCRIPT} -a --silent --eula accept --install-dir ${ONEAPI_INSTALL_DIR} --intel-sw-improvement-program-consent decline 2>&1 | tee log.install

# Check that compiler and mkl versions are correct
if [ ! -d "${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}" ]; then
  echo "Error, directory ${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION} does not exist"
  exit 1
fi
if [ ! -d "${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}" ]; then
  echo "Error, directory ${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION} does not exist"
  exit 1
fi

# Create modulefiles - special modules for Cray, Intel auto-generated modules elsewhere
HOSTNAME=$(hostname)
if [[ "${HOSTNAME}" == *"blueback"* || "${HOSTNAME}" == *"narwhal"* ]]; then
  mkdir -p ${ONEAPI_INSTALL_DIR}/modulefiles/intel-oneapi
  cat << EOF > ${ONEAPI_INSTALL_DIR}/modulefiles/intel-oneapi/2026.0.0
#%Module
#
# Intel oneAPI module
#

conflict intel
conflict intel-classic
conflict intel-oneapi

set INTEL_CURPATH     ${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}
set INTEL_LEVEL       ${COMPILER_VERSION}

setenv INTEL_PATH           \$INTEL_CURPATH
setenv INTEL_VERSION        \$INTEL_LEVEL
setenv INTEL_COMPILER_TYPE  "ONEAPI"

prepend-path {LD_LIBRARY_PATH} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/opt/compiler/lib:${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/lib}
setenv {OCL_ICD_FILENAMES} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/lib/libintelocl.so}
setenv {CMPLR_ROOT} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}}
prepend-path {CMAKE_PREFIX_PATH} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}}
prepend-path {NLSPATH} {}
prepend-path {LIBRARY_PATH} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/lib}
prepend-path {DIAGUTIL_PATH} {}
prepend-path {MANPATH} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/share/man}
prepend-path {PATH} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/bin}
prepend-path {PKG_CONFIG_PATH} {${ONEAPI_INSTALL_DIR}/compiler/${COMPILER_VERSION}/lib/pkgconfig}
prepend-path {LD_LIBRARY_PATH} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}/lib}
prepend-path {CMAKE_PREFIX_PATH} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}/lib/cmake}
prepend-path {CPATH} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}/include}
prepend-path {LIBRARY_PATH} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}/lib}
setenv {MKLROOT} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}}
prepend-path {PATH} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}/bin}
prepend-path {PKG_CONFIG_PATH} {${ONEAPI_INSTALL_DIR}/mkl/${MKL_VERSION}/lib/pkgconfig}

proc ModulesHelp { } {
    global INTEL_LEVEL
    global INTEL_CURPATH
}

# This module was produced with dom-gen 0.0.1

module-whatis   "Intel oneAPI compiler"
EOF

else
  cd ${ONEAPI_INSTALL_DIR}
  ./modulefiles-setup.sh --output-dir=${ONEAPI_INSTALL_DIR}/modulefiles --ignore-latest 2>&1 | tee log.modulefiles
  # Fix non-ascii symbols in Intel modulefiles; must follow links
  for file in `find ./modulefiles -type l`; do
    echo $file
    sed -i --follow-symlinks 's/®//g' $file
  done
fi
