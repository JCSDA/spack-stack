# Use '-i' when sourcing this file to attempt to reset $PATH to system defaults (i.e., based on /etc/profile)
# This may have unwanted/unexpected behavior on some systems, so use carefully.
if [ "$1" == "-i" ]; then
  echo "Resetting PATH to system defaults"
  PATH=$(env -u PATH -u PROFILEREAD bash -c 'echo $PATH')
fi

# https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
# Portable way to get current directory
SPACK_STACK_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export SPACK_STACK_DIR
echo "Setting environment variable SPACK_STACK_DIR to ${SPACK_STACK_DIR}"

source ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh
echo "Sourcing spack environment ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh"
