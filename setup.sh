# https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
# Portable way to get current directory
SPACK_STACK_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

hostname=$(hostname -f)
case $hostname in
  *acorn.wcoss2*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/wcoss2/setup.sh
    ;;
  *atlantis*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/atlantis/setup.sh
    ;;
  *barfoot*)
    . ${SPACK_STACK_DIR}/configs/sites/tier2/barfoot/setup.sh
    ;;
  *blueback*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/blueback/setup.sh
    ;;
  *derecho*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/derecho/setup.sh
    ;;
  *Hercules*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/hercules/setup.sh
    ;;
  *narwhal*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/narwhal/setup.sh
    ;;
  *nautilus*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/nautilus/setup.sh
    ;;
  *Orion*)
    . ${SPACK_STACK_DIR}/configs/sites/tier1/orion/setup.sh
    ;;
esac

export SPACK_STACK_DIR
echo "Setting environment variable SPACK_STACK_DIR to ${SPACK_STACK_DIR}"

# Avoid using ~/.spack directory for caching, spack repo clones, etc.
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=${SPACK_STACK_DIR}/cache/user_cache

echo "Enabling shell completions for spack-stack extensions..."
${SPACK_STACK_DIR}/spack/bin/spack commands --update-completion
source ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh
echo "Sourcing spack environment ${SPACK_STACK_DIR}/spack/share/spack/setup-env.sh"

# Avoid using ~/.spack directory for bootstraping
echo "Changing bootstrap path to $(spack bootstrap root '$spack/bootstrap')"

# Get the current hash of the spack-stack code
export SPACK_STACK_HASH=`cd $SPACK_STACK_DIR && git rev-parse --short HEAD`
echo "Current hash of spack-stack is ${SPACK_STACK_HASH}"
