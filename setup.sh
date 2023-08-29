# Use '-i' when sourcing this file to attempt to reset $PATH to system defaults (i.e., based on /etc/profile),
# then load any modules (e.g., python) critical for loading and working with Spack.
# This may have unwanted/unexpected behavior on some systems, so use carefully.
if [ "$1" == "-i" ]; then
  echo "Resetting PATH to system defaults"
  PATH=$(env -u PATH -u PROFILEREAD bash -i -c 'echo $PATH')
  case "$(hostname -s)" in
    Orion-login-[1-4]) module load python/3.7.5 ;;
    alogin0[1-3]) module load intel/19.1.3.304 python/3.8.6 ;;
  esac
fi

# https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
# Portable way to get current directory
SPACK_STACK_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export SPACK_STACK_DIR
echo "Setting environment variable SPACK_STACK_DIR to ${SPACK_STACK_DIR}"

source ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh
echo "Sourcing spack environment ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh"
