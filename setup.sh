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

source ${SPACK_STACK_DIR:?}/spack/share/spack/setup-env.sh
echo "Sourcing spack environment ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh"

libpath=${SPACK_STACK_DIR}/lib/jcsda-emc/spack-stack
if [ -d ${libpath}/stack/cmd ]; then
  spack config --scope defaults add "config:extensions:$libpath"
else
  echo "FATAL ERROR: Could not find spack-stack extensions in ${libpath}"
  return 1
fi

# Register the jcsda-emc repos
msg1="Added repo with namespace"
msg2="Repository is already registered with Spack"
for repo in jcsda-emc jcsda-emc-bundles; do
  othererrors=$( ( spack repo add ${SPACK_STACK_DIR}/repos/$repo --scope defaults |& grep -v -e "$msg1" -e "$msg2" ) || true )
  if [ $(echo "$othererrors" | grep -c .) -ne 0 ]; then
    echo "$othererrors"
    return 2
  fi
  if [ ! -d ${SPACK_STACK_DIR}/repos/$repo ]; then
    echo "FATAL ERROR: Repo directory ${SPACK_STACK_DIR}/repos/$repo does not exist!"
    return 3
  fi
done

echo "spack-stack extensions and repos are registered"
