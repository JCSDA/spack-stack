# https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
# Portable way to get current directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export SPACK_STACK_DIR=${SCRIPT_DIR}

source ${SCRIPT_DIR}/spack/share/spack/setup-env.sh
