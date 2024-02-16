# https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
# Portable way to get current directory
SPACK_STACK_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export SPACK_STACK_DIR
echo "Setting environment variable SPACK_STACK_DIR to ${SPACK_STACK_DIR}"

source ${SPACK_STACK_DIR:?}/spack/share/spack/setup-env.sh
echo "Sourcing spack environment ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh"
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$SPACK_ROOT/user_cache

# Get the current hash of the spack-stack code
export SPACK_STACK_HASH=`git rev-parse --short HEAD`
echo "Current hash of spack-stack is ${SPACK_STACK_HASH}"

# Register the spack extension
libpath=${SPACK_STACK_DIR}/spack-ext/lib/jcsda-emc/spack-stack
if [ -d ${libpath}/stack/cmd ]; then
  spack config --scope defaults add "config:extensions:$libpath"
else
  echo "FATAL ERROR: Could not find spack-stack extensions in ${libpath}"
  return 1
fi

# Register the jcsda-emc repos
msg1="Added repo with namespace"
msg2="Repository is already registered with Spack"
for repo in spack-stack; do
  repodir=${SPACK_STACK_DIR}/spack-ext/repos/$repo
  othererrors=$( ( spack repo add $repodir --scope defaults 2>&1 | grep -v -e "$msg1" -e "$msg2" ) || true )
  if [ $(echo "$othererrors" | grep -c .) -ne 0 ]; then
    echo "$othererrors"
    return 2
  fi
  if [ ! -d $repodir ]; then
    echo "FATAL ERROR: Repo directory $repodir does not exist!"
    return 3
  fi
done

echo "spack-stack extensions and repos are registered"
