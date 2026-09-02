#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SPACK_STACK_DIR=$(dirname $(dirname ${SCRIPT_DIR}))

set -e

##################################################################################################
# Packages for which to run tests when "-t" is specified; caveat: must be listed in order of     #
# their respective dependencies (e.g. A depends on B --> B comes first)                          #
##################################################################################################

SPACK_STACK_PACKAGES_TO_TEST=(
  "oops"
  "ioda"
  "ioda-converters"
  "ropp-ufo"
  "ufo"
)

# IODA data repositories store their test inputs with Git LFS. Spack invokes
# Git directly while populating the source mirror, before any concretized
# package dependency can provide git-lfs. The site module purge removes it
# from PATH, so make the site installation available explicitly.
setup_git_lfs() {
  local git_lfs_bin
  case "${host}" in
    discover|discover-gmao)
      git_lfs_bin=/discover/swdev/gmao_SIteam/other/SLES15.4/git-lfs/3.7.1/bin
      ;;
    nas)
      git_lfs_bin=/nobackup/gmao_SIteam/git-lfs/3.7.0/bin
      ;;
    nas-toss5)
      git_lfs_bin=/nobackup/gmao_SIteam/git-lfs/3.7.1/bin
      ;;
    *)
      return
      ;;
  esac

  if [[ ! -x "${git_lfs_bin}/git-lfs" ]]; then
    echo "ERROR: required git-lfs executable not found: ${git_lfs_bin}/git-lfs"
    exit 1
  fi
  export PATH="${git_lfs_bin}:${PATH}"
  echo "INFO: added git-lfs to PATH: ${git_lfs_bin}"
}

##################################################################################################
# Options                                                                                        #
##################################################################################################

##################################################################################################
# macOS Prerequisites Check                                                                      #
##################################################################################################

check_macos_prerequisites() {
  if ! command -v brew &> /dev/null; then
    echo "ERROR: brew is not installed or not in PATH."
    exit 1
  fi

  local missing_pkgs=()
  local required_pkgs=(coreutils gcc git lmod wget bash tcsh cmake openssl rust)

  for pkg in "${required_pkgs[@]}"; do
    if ! brew --prefix "$pkg" &> /dev/null; then
      missing_pkgs+=("$pkg")
    fi
  done

  if [ ${#missing_pkgs[@]} -ne 0 ]; then
    echo "ERROR: Missing required Homebrew packages: ${missing_pkgs[*]}"
    echo "Please run: brew install ${missing_pkgs[*]}"
    exit 1
  fi
}


usage() {
  set +x
  echo
  echo "Usage: $0 [-r <ROLE>] -m <MODE> [-d <ENV_DIRS>] [-c <BUILDCACHE_DIR>] [-H <HOSTNAME>]"
  echo
  echo "  -r  Set role, can be 'ops' or 'dev'; required except with -m local"
  echo "  -m  Set mode, can be 'build', 'install', or 'local';"
  echo "      build: build environments and update build caches;"
  echo "      install: install environments using build caches;"
  echo "      local: one-step, per-machine install and cache update (macos.gmao and bucy)"
  echo "  -d  Build or install environments in ENV_DIRS;"
  echo "      if not set, the default location is used"
  echo "  -c  Provide location of build caches as BUILDCACHE_DIR;"
  echo "      if not set, authoritative build caches are used"
  echo "  -u  Flag to update bootstrap and source caches;"
  echo "      requires role 'dev' and mode 'build', or mode 'local'"
  echo "  -e  Continue builds/install in existing environments;"
  echo "      by default, exit with an error if already exist"
  echo "  -C  Set a comma-separated list of compilers to use (e.g. gcc@=15.3.0,nag@=7.2.7243);"
  echo "      overrides the default compilers for the site"
  echo "  -N  Path to nagfor executable (e.g. /opt/nag/bin/nagfor);"
  echo "      forces NAG stack to be built using this specific compiler"
  echo "  -a  Set PBS/SLURM account (default: s1873);"
  echo "      overrides the ACCOUNT environment variable"
  echo "  -p  Set SLURM partition (e.g. preops, normal, compute);"
  echo "      overrides the default partition for the site;"
  echo "      also accepted as --partition=<value>;"
  echo "      NOTE: only applies to NCCS hosts (discover, discover-gmao)"
  echo "  -q  Set SLURM QOS (e.g. benchmark, high, normal);"
  echo "      overrides the default QOS for the site;"
  echo "      also accepted as --qos=<value>;"
  echo "      NOTE: only applies to NCCS hosts (discover, discover-gmao)"
  echo "      --constraint=<value>"
  echo "          Set SLURM node constraint (e.g. mil, cas, sky);"
  echo "          overrides the default constraint for the site;"
  echo "          no short form available (-c and -C are already used);"
  echo "          NOTE: only applies to NCCS hosts (discover, discover-gmao)"
  echo "  -s  Submit 'spack install' to batch scheduler"
  echo "  -L  Disable Spack install locks and serialize package installs; use only when this is the sole process modifying the install tree;"
  echo "      also accepted as --disable-locks"
  echo "  -t  Run tests for specific thirdparty dependencies;"
  echo "      these are currently hardcoded in batch_install.sh"
  echo "  -o  Concretize-only: stop after concretization (do not install);"
  echo "      also accepted as --concretize-only"
  echo "  -n  Dry-run: print what would be executed without running anything"
  echo "  -H  Provide hostname manually (overrides autodetection);"
  echo "      useful when VPN/etc masks the real hostname"
  echo "  -h  display this help"
  echo
}

# Normalize long options before getopts processes the short options.
normalized_args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --concretize-only)
      normalized_args+=("-o")
      ;;
    --disable-locks)
      normalized_args+=("-L")
      ;;
    --partition=*)
      normalized_args+=("-p" "${1#*=}")
      ;;
    --partition)
      if [[ -z "${2:-}" ]]; then
        echo "ERROR, --partition requires a value"
        exit 1
      fi
      normalized_args+=("-p" "$2")
      shift
      ;;
    --qos=*)
      normalized_args+=("-q" "${1#*=}")
      ;;
    --qos)
      if [[ -z "${2:-}" ]]; then
        echo "ERROR, --qos requires a value"
        exit 1
      fi
      normalized_args+=("-q" "$2")
      shift
      ;;
    --constraint=*)
      SPACK_STACK_SLURM_CONSTRAINT="${1#*=}"
      ;;
    --constraint)
      if [[ -z "${2:-}" ]]; then
        echo "ERROR, --constraint requires a value"
        exit 1
      fi
      SPACK_STACK_SLURM_CONSTRAINT="$2"
      shift
      ;;
    --help)
      normalized_args+=("-h")
      ;;
    --*)
      echo "ERROR, unknown argument: $1"
      usage
      exit 1
      ;;
    *)
      normalized_args+=("$1")
      ;;
  esac
  shift
done
set -- "${normalized_args[@]}"

while getopts r:m:d:c:C:N:H:a:p:q:nouestLh flag
do
  case "${flag}" in
    r)
      SPACK_STACK_ROLE=${OPTARG}
      ;;
    m)
      SPACK_STACK_MODE=${OPTARG}
      ;;
    d)
      SPACK_STACK_ENVIRONMENT_DIRS=$(readlink -f ${OPTARG})
      ;;
    c)
      SPACK_STACK_BUILDCACHE_DIR=$(readlink -f ${OPTARG})
      ;;
    C)
      SPACK_STACK_COMPILER_OPT=${OPTARG}
      ;;
    N)
      SPACK_STACK_NAGFOR_PATH=${OPTARG}
      ;;
    H)
      SPACK_STACK_BATCH_HOST_OPT=${OPTARG}
      ;;
    a)
      ACCOUNT=${OPTARG}
      ;;
    p)
      SPACK_STACK_SLURM_PARTITION=${OPTARG}
      ;;
    q)
      SPACK_STACK_SLURM_QOS=${OPTARG}
      ;;
    n)
      SPACK_STACK_DRY_RUN="true"
      ;;
    o)
      SPACK_STACK_CONCRETIZE_ONLY="true"
      ;;
    u)
      SPACK_STACK_UPDATE_DEV_CACHES="true"
      ;;
    e)
      SPACK_STACK_IGNORE_ENV_EXIST="true"
      ;;
    s)
      SPACK_STACK_SUBMIT_TO_SCHEDULER="true"
      ;;
    L)
      SPACK_STACK_DISABLE_LOCKS="true"
      ;;
    t)
      SPACK_STACK_RUN_TESTS="true"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

echo "INFO: $0 options:"
echo "  SPACK_STACK_ROLE:                            ${SPACK_STACK_ROLE:-not set}"
echo "  SPACK_STACK_MODE:                            ${SPACK_STACK_MODE:-not set}"
echo "  SPACK_STACK_ENVIRONMENT_DIRS:                ${SPACK_STACK_ENVIRONMENT_DIRS:-${SPACK_STACK_DIR}/envs}"
echo "  SPACK_STACK_BUILDCACHE_DIR:                  ${SPACK_STACK_BUILDCACHE_DIR:-use default caches}"
echo "  SPACK_STACK_BATCH_HOST_OPT:                  ${SPACK_STACK_BATCH_HOST_OPT:-autodetect}"
echo "  SPACK_STACK_DRY_RUN:                         ${SPACK_STACK_DRY_RUN:-false}"
echo "  SPACK_STACK_UPDATE_DEV_CACHES:               ${SPACK_STACK_UPDATE_DEV_CACHES:-false}"
echo "  SPACK_STACK_IGNORE_ENV_EXIST:                ${SPACK_STACK_IGNORE_ENV_EXIST:-false}"
echo "  SPACK_STACK_SUBMIT_TO_SCHEDULER:             ${SPACK_STACK_SUBMIT_TO_SCHEDULER:-false}"
echo "  SPACK_STACK_DISABLE_LOCKS:                    ${SPACK_STACK_DISABLE_LOCKS:-false}"
echo "  SPACK_STACK_RUN_TESTS:                       ${SPACK_STACK_RUN_TESTS:-false}"
echo "  ACCOUNT:                                     ${ACCOUNT:-s1873 (default)}"
echo "  SPACK_STACK_SLURM_PARTITION:                 ${SPACK_STACK_SLURM_PARTITION:-use site default}"
echo "  SPACK_STACK_SLURM_QOS:                       ${SPACK_STACK_SLURM_QOS:-use site default}"
echo "  SPACK_STACK_SLURM_CONSTRAINT:                ${SPACK_STACK_SLURM_CONSTRAINT:-use site default}"

# Set default account if not provided via -a or environment
ACCOUNT=${ACCOUNT:-s1873}

if [[ -z ${SPACK_STACK_MODE} ]]; then
  echo "ERROR, SPACK_STACK_MODE not defined. Provide -m MODE as argument"
  exit 1
elif [[ ! ${SPACK_STACK_MODE} == "build" && ! ${SPACK_STACK_MODE} == "install" && ! ${SPACK_STACK_MODE} == "local" ]]; then
  echo "ERROR, invalid mode '${SPACK_STACK_MODE}'"
  exit 1
fi

if [[ "${SPACK_STACK_MODE}" != "local" && -z ${SPACK_STACK_ROLE} ]]; then
  echo "ERROR, SPACK_STACK_ROLE not defined. Provide -r ROLE as argument"
  exit 1
elif [[ -n ${SPACK_STACK_ROLE} && ! ${SPACK_STACK_ROLE} == "dev" && ! ${SPACK_STACK_ROLE} == "ops" ]]; then
  echo "ERROR, invalid role '${SPACK_STACK_ROLE}'"
  exit 1
fi

# Role ops cannot write to the default (authoritative) build cache
if [[ ${SPACK_STACK_ROLE} == "ops" && ${SPACK_STACK_MODE} == "build" && -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
  echo "ERROR, SPACK_STACK_BUILDCACHE_DIR not defined. Provide -c BUILDCACHE_DIR"
  echo "as argument when role is 'ops' and mode is 'build'"
  exit 1
fi

# Updating shared-site bootstrap and source caches requires role dev and mode build.
# Local mirrors on macOS and bucy can be updated without a role.
if [[ ${SPACK_STACK_UPDATE_DEV_CACHES} == "true" ]]; then
  if [[ "${SPACK_STACK_MODE}" != "local" && \
        ( ! ${SPACK_STACK_ROLE} == "dev" || ! ${SPACK_STACK_MODE} == "build" ) ]]; then
    echo "ERROR, SPACK_STACK_UPDATE_DEV_CACHES requires role 'dev' and mode 'build', or mode 'local'"
    exit 1
  fi
fi

##################################################################################################

if [[ -n "${SPACK_STACK_BATCH_HOST_OPT}" ]]; then
  SPACK_STACK_BATCH_HOST="${SPACK_STACK_BATCH_HOST_OPT}"
else
  # Remove domain name suffices and digits to determine hostname
  SPACK_STACK_BATCH_HOST=$(echo ${HOSTNAME} | cut -d "." -f 1)
  SPACK_STACK_BATCH_HOST=${SPACK_STACK_BATCH_HOST//[0-9]/}
fi

case ${SPACK_STACK_BATCH_HOST} in
  nas)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=15.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/swbuild/gmao_SIteam/spack-stack/bootstrap-mirror-toss4"
    SPACK_STACK_CARGO_MIRROR="/swbuild/gmao_SIteam/spack-stack/cargo-mirror"
    SPACK_STACK_ENVIRONMENT_DIRS=${SPACK_STACK_ENVIRONMENT_DIRS:-${PWD}/envs/toss4}
    ;;
  nas-toss5)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=15.3.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/swbuild/gmao_SIteam/spack-stack/bootstrap-mirror-toss5"
    SPACK_STACK_CARGO_MIRROR="/swbuild/gmao_SIteam/spack-stack/cargo-mirror"
    SPACK_STACK_ENVIRONMENT_DIRS=${SPACK_STACK_ENVIRONMENT_DIRS:-${PWD}/envs/toss5}
    ;;
  discover)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=14.2.0" "gcc@=15.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/discover/nobackup/projects/gmao/SIteam/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/discover/nobackup/projects/gmao/SIteam/spack-stack/cargo-mirror"
    ;;
  discover-gmao)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=15.2.0" "nag@=7.2.7238")
    SPACK_STACK_BATCH_TEMPLATES=("geos-dev" "geos-dev-nag")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/discover/nobackup/projects/gmao/SIteam/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/discover/nobackup/projects/gmao/SIteam/spack-stack/cargo-mirror"
    ;;
  bucy)
    SPACK_STACK_BATCH_COMPILERS=("gcc@=15.2.0" "gcc@=16.1.0" "oneapi@=2024.2.0" "oneapi@=2025.3.0" "nag@=7.2.43" "llvm@=22.1.0")
    SPACK_STACK_BATCH_TEMPLATES=("geos-dev" "geos-dev-nag")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/ford1/share/gmao_SIteam/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/ford1/share/gmao_SIteam/spack-stack/cargo-mirror"
    SPACK_STACK_ENVIRONMENT_DIRS=${SPACK_STACK_ENVIRONMENT_DIRS:-${PWD}/envs/bucy}
    ;;
  macos.gmao)
    # Detect NAG Fortran Compiler
    nag_path_tmp=""
    if [[ -n "${SPACK_STACK_NAGFOR_PATH}" && -x "${SPACK_STACK_NAGFOR_PATH}" ]]; then
      nag_path_tmp="${SPACK_STACK_NAGFOR_PATH}"
    elif command -v nagfor &> /dev/null; then
      nag_path_tmp=$(which nagfor)
    fi

    if [[ -n "${nag_path_tmp}" ]]; then
      export MAC_GMAO_NAG_PATH="${nag_path_tmp}"
      export MAC_GMAO_NAG_VERSION=$("${MAC_GMAO_NAG_PATH}" -V 2>&1 | head -n1 | sed -E 's/.*Release ([0-9]+\.[0-9]+).*Build ([0-9]+).*/\1.\2/' || echo "7.2.7243")
      export MAC_GMAO_NAG_PREFIX=$(dirname $(dirname "${MAC_GMAO_NAG_PATH}"))
    fi

    # Note: clang (aka flang) is on hold for macOS until we move to
    # 1. FMS 2025 (for GEOS purposes)
    # 2. ESMF PR https://github.com/esmf-org/esmf/pull/558 is merged and released/tagged
    SPACK_STACK_BATCH_COMPILERS=("gcc@=15.3.0" "gcc@=16.2.0" "clang@=22.1.8")
    #SPACK_STACK_BATCH_COMPILERS=("gcc@=15.3.0" "gcc@=16.2.0" )
    if [[ -n "${MAC_GMAO_NAG_VERSION}" ]]; then
      SPACK_STACK_BATCH_COMPILERS+=("nag@=${MAC_GMAO_NAG_VERSION}")
    fi

    # Auto-detect Apple Clang version
    if command -v clang &> /dev/null; then
      export MAC_GMAO_APPLE_CLANG_VERSION=$(clang --version | grep "Apple clang version" | awk '{print $4}')
    else
      export MAC_GMAO_APPLE_CLANG_VERSION="21.0.0"
    fi

    SPACK_STACK_BATCH_TEMPLATES=("geos-dev" "geos-dev-nag")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="${HOME}/spack-stack-mirrors/spack-bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="${HOME}/spack-stack-mirrors/spack-cargo-mirror"
    ;;
  *)
    echo "ERROR, host ${SPACK_STACK_BATCH_HOST} not configured"
    exit 1
    ;;
esac

if [[ "${SPACK_STACK_MODE}" == "local" &&
      "${SPACK_STACK_BATCH_HOST}" != "macos.gmao" &&
      "${SPACK_STACK_BATCH_HOST}" != "bucy" ]]; then
  echo "ERROR, mode 'local' is supported only for hosts macos.gmao and bucy"
  exit 1
fi

if [[ "${SPACK_STACK_MODE}" == "local" && "${SPACK_STACK_SUBMIT_TO_SCHEDULER}" == "true" ]]; then
  echo "ERROR, mode 'local' cannot be submitted to a batch scheduler"
  exit 1
fi

# Apply -C compiler override for all hosts (not just macos.gmao)
if [[ -n "${SPACK_STACK_COMPILER_OPT}" ]]; then
  IFS=',' read -r -a SPACK_STACK_BATCH_COMPILERS <<< "${SPACK_STACK_COMPILER_OPT}"
fi

##################################################################################################

function fix_permissions() {
  host=$1
  dir=$2
  executables=$3
  echo "Repairing permissions for directory ${dir} on ${host} ..."
  set +e
  case ${host} in
    nas)
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      if [[ ${executables} -eq 1 ]]; then
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    nas-toss5)
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      if [[ ${executables} -eq 1 ]]; then
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    discover)
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      if [[ ${executables} -eq 1 ]]; then
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    discover-gmao)
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      if [[ ${executables} -eq 1 ]]; then
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    bucy)
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      if [[ ${executables} -eq 1 ]]; then
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    macos.gmao)
      ;;
    *)
      echo "ERROR, xargs-chmod command not configured for ${host}"
      exit 1
      ;;
  esac
  set -e
}

##################################################################################################

function tasks_per_node() {
  host=$1
  case ${host} in
    nas)
      tpn=120
      ;;
    nas-toss5)
      tpn=240
      ;;
    discover)
      tpn=120
      ;;
    discover-gmao)
      tpn=120
      ;;
    *)
      echo "ERROR, tasks_per_node command not configured for ${host}"
      exit 1
      ;;
  esac
  echo "${tpn}"
}

##################################################################################################

function run_interactive_job() {
  host=$1
  script=$2
  reuse_build_cache=$3
  env_name=$4
  tpn=$(tasks_per_node ${host})
  walltime="08:00:00"
  job_name="spack.${host}.${env_name}"
  echo "Starting batch job on ${host} with ${tpn} tasks, walltime ${walltime}, account ${ACCOUNT} for ${script} ..."
  case ${host} in
    nas)
      # Determine PBS model based on login node name
      login_node=$(hostname | cut -d "." -f 1)
      case ${login_node} in
        pfe*)
          pbs_model="rom_ait"
          ;;
        afe*)
          pbs_model="mil_ait"
          ;;
        *)
          echo "ERROR, cannot determine PBS model from login node '${login_node}' on ${host}"
          echo "Expected login node name starting with 'pfe' or 'afe'"
          exit 1
          ;;
      esac
      echo "  Login node: ${login_node}, PBS model: ${pbs_model}"
       qsub -V \
           -l select=1:ncpus=${tpn}:mpiprocs=${tpn}:model=${pbs_model} \
           -q normal \
           -l walltime=${walltime} \
           -l site=needed=/home3+/nobackupp18+/nobackupp28+/vast_swbuild/swbuild4 \
           -W group_list=${ACCOUNT} \
           -W block=true \
           -W umask=0022 \
           -j oe -k oed \
           -N ${job_name} \
           ${script}
      ;;
    nas-toss5)
      # All nas-toss5 login nodes start with athfe
      login_node=$(hostname | cut -d "." -f 1)
      if [[ ! ${login_node} == athfe* ]]; then
        echo "WARNING, expected login node name starting with 'athfe' on ${host}, got '${login_node}'"
      fi
      qsub -V \
           -l select=1:ncpus=${tpn}:mpiprocs=${tpn}:model=tur_ath \
           -q normal \
           -l walltime=${walltime} \
           -l site=needed=/home3+/nobackupp18+/nobackupp28+/vast_swbuild/swbuild4 \
           -W group_list=${ACCOUNT} \
           -W block=true \
           -W umask=0022 \
           -j oe -k oed \
           -N ${job_name} \
           ${script}
      ;;
    discover)
      slurm_constraint="${SPACK_STACK_SLURM_CONSTRAINT:+--constraint=${SPACK_STACK_SLURM_CONSTRAINT}}"
      slurm_constraint="${slurm_constraint:---constraint=mil}"
      if [[ -n "${SPACK_STACK_SLURM_PARTITION}" ]]; then
        slurm_partition="--partition=${SPACK_STACK_SLURM_PARTITION}"
      elif [[ "${ACCOUNT}" == "s1873" ]]; then
        slurm_partition="--partition=preops"
      else
        slurm_partition=""
      fi
      if [[ -n "${SPACK_STACK_SLURM_QOS}" ]]; then
        slurm_qos="--qos=${SPACK_STACK_SLURM_QOS}"
      elif [[ "${ACCOUNT}" == "s1873" ]]; then
        slurm_qos="--qos=benchmark"
      else
        slurm_qos=""
      fi
      slurm_log="${job_name}.log"
      echo "INFO: sbatch output redirected to ${slurm_log}"
      sbatch --wait \
             --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} \
             ${slurm_constraint} ${slurm_partition} ${slurm_qos} \
             --job-name=${job_name} \
             --account=${ACCOUNT} \
             --output="${slurm_log}" --error="${slurm_log}" \
             ${script}
      echo "INFO: sbatch job complete, log: ${slurm_log}"
      ;;
    discover-gmao)
      slurm_constraint="${SPACK_STACK_SLURM_CONSTRAINT:+--constraint=${SPACK_STACK_SLURM_CONSTRAINT}}"
      slurm_constraint="${slurm_constraint:---constraint=mil}"
      if [[ -n "${SPACK_STACK_SLURM_PARTITION}" ]]; then
        slurm_partition="--partition=${SPACK_STACK_SLURM_PARTITION}"
      elif [[ "${ACCOUNT}" == "s1873" ]]; then
        slurm_partition="--partition=preops"
      else
        slurm_partition=""
      fi
      if [[ -n "${SPACK_STACK_SLURM_QOS}" ]]; then
        slurm_qos="--qos=${SPACK_STACK_SLURM_QOS}"
      elif [[ "${ACCOUNT}" == "s1873" ]]; then
        slurm_qos="--qos=benchmark"
      else
        slurm_qos=""
      fi
      slurm_log="${job_name}.log"
      echo "INFO: sbatch output redirected to ${slurm_log}"
      sbatch --wait \
             --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} \
             ${slurm_constraint} ${slurm_partition} ${slurm_qos} \
             --job-name=${job_name} \
             --account=${ACCOUNT} \
             --output="${slurm_log}" --error="${slurm_log}" \
             ${script}
      echo "INFO: sbatch job complete, log: ${slurm_log}"
      ;;
    *)
      echo "ERROR, run_interactive_job command not configured for ${host}"
      exit 1
      ;;
  esac
}

##################################################################################################

echo
echo "Welcome to GMAO SPACK-STACK BATCH INSTALL"
echo

LOG_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "${SPACK_STACK_DIR}/logs"

if [[ ! -e "setup.sh" || ! -e ".spackstack" ]]; then
  echo "ERROR, this script must be executed from the top-level spack-stack directory"
  exit 1
fi

host=${SPACK_STACK_BATCH_HOST}
module_choice=${SPACK_STACK_MODULE_CHOICE}
bootstrap_mirror_path=${SPACK_STACK_BOOTSTRAP_MIRROR}
cargo_mirror_path=${SPACK_STACK_CARGO_MIRROR}
export SPACK_CARGO_HOME=${cargo_mirror_path}

if [[ -z ${SPACK_STACK_ENVIRONMENT_DIRS} ]]; then
  environment_dirs=${PWD}/envs
else
  environment_dirs=${SPACK_STACK_ENVIRONMENT_DIRS}
fi
[[ "${SPACK_STACK_DRY_RUN}" != "true" ]] && mkdir -p ${environment_dirs}

if [[ ! -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
  buildcache_dir=${SPACK_STACK_BUILDCACHE_DIR}
  if [[ "${SPACK_STACK_MODE}" == "install" && ! -d ${buildcache_dir} ]]; then
    echo "ERROR, build cache ${buildcache_dir} not found,"
    echo "must exist before installing environments"
    exit 1
  else
    [[ "${SPACK_STACK_DRY_RUN}" != "true" ]] && mkdir -p ${buildcache_dir}
  fi
fi

if [[ "${SPACK_STACK_MODE}" == "install" ]]; then
  update_bootstrap_mirror="false"
  update_cargo_mirror="false"
  update_source_cache="false"
  update_build_cache="false"
  publish_build_cache="false"
  reuse_build_cache="true"
elif [[ "${SPACK_STACK_MODE}" == "build" ]]; then
  if [[ "${SPACK_STACK_ROLE}" == "ops" ]]; then
    update_bootstrap_mirror="false"
    update_cargo_mirror="false"
    update_source_cache="false"
  elif [[ "${SPACK_STACK_ROLE}" == "dev" ]]; then
    if [[ ${SPACK_STACK_UPDATE_DEV_CACHES} == "true" ]]; then
      update_bootstrap_mirror="true"
      update_cargo_mirror="true"
      update_source_cache="true"
    else
      update_bootstrap_mirror="false"
      update_cargo_mirror="false"
      update_source_cache="false"
    fi
  else
    echo "ERROR, invalid role ${SPACK_STACK_ROLE}"
    exit 1
  fi
  update_build_cache="true"
  publish_build_cache="true"
  reuse_build_cache="true"
elif [[ "${SPACK_STACK_MODE}" == "local" ]]; then
  # A macOS stack is private to one workstation. Prepare its local source,
  # bootstrap, and Cargo mirrors when requested. Install directly into the
  # final environment, generate modules, and publish a private buildcache.
  if [[ ${SPACK_STACK_UPDATE_DEV_CACHES} == "true" ]]; then
    update_bootstrap_mirror="true"
    update_cargo_mirror="true"
    update_source_cache="true"
  else
    update_bootstrap_mirror="false"
    update_cargo_mirror="false"
    update_source_cache="false"
  fi
  update_build_cache="false"
  publish_build_cache="true"
  reuse_build_cache="true"
else
  echo "ERROR, invalid mode ${SPACK_STACK_MODE}"
  exit 1
fi

ignore_env_exist=${SPACK_STACK_IGNORE_ENV_EXIST:-false}

if [[ "${SPACK_STACK_SUBMIT_TO_SCHEDULER}" == "true" ]]; then
  submit_to_scheduler="true"
else
  submit_to_scheduler="false"
fi

if [[ "${SPACK_STACK_RUN_TESTS}" == "true" ]]; then
  test_packages=("${SPACK_STACK_PACKAGES_TO_TEST[@]}")
else
  test_packages=()
fi

if [[ "${SPACK_STACK_DISABLE_LOCKS}" == "true" ]]; then
  spack_install_lock_flag="--disable-locks"
else
  spack_install_lock_flag=""
fi

# A full node is allocated for isolation, but large package builds can slow down
# when every hardware thread is used. Cap Spack's per-package build parallelism.
spack_build_jobs=24

# Loop through all compilers and templates for this host
first_pass="true"
for compiler in "${SPACK_STACK_BATCH_COMPILERS[@]}"; do

  if [[ ! ${compiler} == *"@="* ]]; then
    echo "ERROR, '@=' not found in compiler string '${compiler}'"
    exit 1
  fi

  compiler_name=$(echo ${compiler} | cut -d "@" -f 1)
  compiler_version=$(echo ${compiler} | cut -d "=" -f 2)

  for template in "${SPACK_STACK_BATCH_TEMPLATES[@]}"; do

    echo
    #############################################################
    # Add excluded combinations of compilers and templates here #
    #############################################################
    if [[ "${template}" == "geos-dev" && "${compiler_name}" == "nag" ]]; then
      echo "Skipping template ${template} with compiler ${compiler} (fms not supported by nag)"
      continue
    elif [[ "${template}" == "geos-dev-nag" && "${compiler_name}" != "nag" ]]; then
      echo "Skipping template ${template} with compiler ${compiler} (geos-dev-nag is only for nag)"
      continue
    fi
    echo "Processing template ${template} with compiler ${compiler}"
    #############################################################

    # Build environment name. Prefices are defined here
    case ${template} in
      unified-dev)
        env_name_prefix="ue"
        ;;
      geos-dev)
        env_name_prefix="ge"
        ;;
      geos-dev-nag)
        env_name_prefix="ge"
        ;;
      *)
        echo "ERROR, template ${template} not configured"
        exit 1
        ;;
    esac
    env_name=${env_name_prefix}-${compiler_name}-${compiler_version}
    [[ "${update_build_cache}" == "true" ]] && env_name=${env_name}-build
    env_dir=${environment_dirs}/${env_name}
    # Different sites can legitimately build an identically named environment
    # at the same time (for example NAS TOSS4 and TOSS5). Keep the generated
    # job scripts distinct as well, since they share this working directory.
    install_script_name=spack-install.${host}.${env_name}.sh

    # Reset env_exists for this specific environment target
    env_exists="false"

    # Bail out if the environment already exists
    if [[ -d ${env_dir} ]]; then
      if [[ ${ignore_env_exist} == "true" ]]; then
        env_exists="true"
      else
        if [[ "${SPACK_STACK_DRY_RUN}" == "true" ]]; then
          echo "[DRY-RUN] ERROR: environment ${env_dir} already exists. (Would exit here)"
          continue
        else
          echo "ERROR, environment ${env_dir} already exists"
          exit 1
        fi
      fi
    fi

    if [[ "${SPACK_STACK_DRY_RUN}" == "true" ]]; then
      echo "--------------------------------------------------------------------------------"
      echo "[DRY-RUN] Target Environment: ${env_name}"
      echo "[DRY-RUN] Directory: ${env_dir}"
      echo "--------------------------------------------------------------------------------"
      if [[ "${update_bootstrap_mirror}" == "true"* ]]; then
        echo "[DRY-RUN] spack bootstrap mirror --binary-packages ${PWD}/tmp-bootstrap-mirror"
        echo "[DRY-RUN] rsync -a ${PWD}/tmp-bootstrap-mirror/ ${bootstrap_mirror_path}/"
        echo "[DRY-RUN] spack buildcache update-index ${bootstrap_mirror_path}/bootstrap_cache"
        update_bootstrap_mirror="false"
      fi

      if [[ ! ${env_exists} == "true" ]]; then
        if [[ "${host}" == "macos.gmao" ]]; then
          echo "[DRY-RUN] Would check macOS prerequisites and generate YAML configs from templates"
        fi
        echo "[DRY-RUN] spack stack create env --name=${env_name} \\"
        echo "          --site=${host} --compiler=${compiler_name}-${compiler_version} \\"
        echo "          --template=${template} --dir=${environment_dirs} --treat-warnings-as-errors"
        if [[ "${host}" == "macos.gmao" ]]; then
          echo "[DRY-RUN] grep -vE 'geos-gcm-env([^[:space:]]*)?[[:space:]]+~debug' ${env_dir}/spack.yaml  # remove ~debug spec (esmf ~debug unsupported on macOS)"
        fi
      fi
      echo "[DRY-RUN] spack env activate -p ${env_dir}"
      if [[ "${SPACK_STACK_DISABLE_LOCKS}" == "true" ]]; then
        echo "[DRY-RUN] generated batch script exports a job-local SPACK_USER_CONFIG_PATH with config:locks:false"
      fi
      if [[ "${submit_to_scheduler}" == "true" && ( "${host}" == "discover" || "${host}" == "discover-gmao" ) ]]; then
        echo "[DRY-RUN] generated batch script uses project-space paths from site config.yaml for build, test, and cache stages"
      fi
      if [[ "${host}" == "macos.gmao" && ! ${env_exists} == "true" ]]; then
        echo "[DRY-RUN] spack external find --not-buildable autoconf automake bash cmake cvs doxygen gawk git-lfs groff libtool ninja npm subversion swig texinfo"
        echo "[DRY-RUN] generating spack-macos-externals.yaml and applying with 'spack config add -f'"
      fi
      echo "[DRY-RUN] spack bootstrap list  # add local-sources and local-binaries if missing"
      if [[ "${update_build_cache}" == "true" ]]; then
        echo "[DRY-RUN] spack config add config:install_tree:padded_length:200"
      fi
      echo "[DRY-RUN] spack bootstrap now"
      echo "[DRY-RUN] spack concretize --force --fresh"
      echo "[DRY-RUN] ./util/show_duplicate_packages.py -i crtm -i crtm-fix -i esmf -i mapl -i neptune-env -i py-cython -i ip -i fms -i geos-gcm-env -i py-versioneer"

      if [[ "${update_source_cache}" == "true"* ]]; then
        echo "[DRY-RUN] spack mirror create -a -d <source_mirror_path>"
        if [[ "${host}" == "discover" || "${host}" == "discover-gmao" || "${host}" == "nas" || "${host}" == "nas-toss5" ]]; then
          echo "[DRY-RUN] prepending the site Git LFS installation to PATH for Git LFS source archives"
        fi
      fi
      if [[ "${update_cargo_mirror}" == "true"* ]]; then
        echo "[DRY-RUN] ./util/fetch_cargo_deps.py"
      fi

      echo "[DRY-RUN] Generating ${install_script_name} and executing via:"
      echo "[DRY-RUN]   Generated install commands: spack ${spack_install_lock_flag} install ..."
      if [[ "${submit_to_scheduler}" == "true" ]]; then
        echo "[DRY-RUN]   Scheduled package builds use --jobs=${spack_build_jobs} (the SLURM allocation remains a full node)"
      fi
      if [[ "${SPACK_STACK_DISABLE_LOCKS}" == "true" && "${submit_to_scheduler}" == "true" ]]; then
        echo "[DRY-RUN]   -L also adds --concurrent-packages=1"
      fi
      if [[ "${host}" == "discover" || "${host}" == "discover-gmao" ]] && \
         [[ "${compiler}" == "oneapi@=2025.3.0" ]]; then
        echo "[DRY-RUN]   Job preflight: module load comp/intel/2025.3.0 mpi/impi/2021.17"
      fi
      if [[ "${host}" == "discover" || "${host}" == "discover-gmao" ]] && \
         [[ "${compiler}" == "gcc@=15.2.0" ]]; then
        echo "[DRY-RUN]   Job preflight: module load comp/gcc/15.2.0 mpi/openmpi/5.0.10/gcc-15.2.0"
      fi
      if [[ "${host}" == "nas" ]] && [[ "${compiler}" == "gcc@=15.2.0" ]]; then
        echo "[DRY-RUN]   Job preflight: module load comp-gcc/15.2.0 mpi-openmpi/4.1.8/gcc/15.2.0"
      fi
      if [[ "${host}" == "discover-gmao" ]] && \
         [[ "${compiler}" == "nag@=7.2.7238" ]]; then
        echo "[DRY-RUN]   Job preflight: module load comp/gcc/12.3.0 comp/nag/7.2-7238 mpi/openmpi/4.1.6/nag_7.2.7238-gcc_12.3.0"
      fi
      if [[ "${submit_to_scheduler}" == "true" ]]; then
        tpn_dry=$(tasks_per_node ${host})
        case ${host} in
          nas)
            login_node=$(hostname | cut -d "." -f 1)
            case ${login_node} in
              pfe*) pbs_model_dry="rom_ait" ;;
              afe*) pbs_model_dry="mil_ait" ;;
              *)    pbs_model_dry="<rom_ait|mil_ait>" ;;
            esac
            echo "[DRY-RUN]   qsub -V \\"
            echo "[DRY-RUN]        -l select=1:ncpus=${tpn_dry}:mpiprocs=${tpn_dry}:model=${pbs_model_dry} \\"
            echo "[DRY-RUN]        -q normal -l walltime=08:00:00 \\"
            echo "[DRY-RUN]        -l site=needed=/home3+/nobackupp18+/nobackupp28+/vast_swbuild/swbuild4 \\"
            echo "[DRY-RUN]        -W group_list=${ACCOUNT} -W block=true -W umask=0022 \\"
            echo "[DRY-RUN]        -j oe -k oed -N spack.${host}.${env_name} \\"
            echo "[DRY-RUN]        ${install_script_name}"
            ;;
          nas-toss5)
            echo "[DRY-RUN]   qsub -V \\"
            echo "[DRY-RUN]        -l select=1:ncpus=${tpn_dry}:mpiprocs=${tpn_dry}:model=tur_ath \\"
            echo "[DRY-RUN]        -q normal -l walltime=08:00:00 \\"
            echo "[DRY-RUN]        -l site=needed=/home3+/nobackupp18+/nobackupp28+/vast_swbuild/swbuild4 \\"
            echo "[DRY-RUN]        -W group_list=${ACCOUNT} -W block=true -W umask=0022 \\"
            echo "[DRY-RUN]        -j oe -k oed -N spack.${host}.${env_name} \\"
            echo "[DRY-RUN]        ${install_script_name}"
            ;;
          discover)
            if [[ "${ACCOUNT}" == "s1873" ]]; then
              slurm_extra_dry="--partition=preops --qos=benchmark"
            else
              slurm_extra_dry="(default partition/qos)"
            fi
            echo "[DRY-RUN]   sbatch --wait \\"
            echo "[DRY-RUN]          --nodes=1 --ntasks-per-node=${tpn_dry} --time=08:00:00 \\"
            echo "[DRY-RUN]          --constraint=mil ${slurm_extra_dry} \\"
            echo "[DRY-RUN]          --job-name=spack.${host}.${env_name} \\"
            echo "[DRY-RUN]          --account=${ACCOUNT} \\"
            echo "[DRY-RUN]          --output=spack.${host}.${env_name}.log --error=spack.${host}.${env_name}.log \\"
            echo "[DRY-RUN]          ${install_script_name}"
            ;;
          discover-gmao)
            if [[ "${ACCOUNT}" == "s1873" ]]; then
              slurm_extra_dry="--partition=preops --qos=benchmark"
            else
              slurm_extra_dry="(default partition/qos)"
            fi
            echo "[DRY-RUN]   sbatch --wait \\"
            echo "[DRY-RUN]          --nodes=1 --ntasks-per-node=${tpn_dry} --time=08:00:00 \\"
            echo "[DRY-RUN]          --constraint=mil ${slurm_extra_dry} \\"
            echo "[DRY-RUN]          --job-name=spack.${host}.${env_name} \\"
            echo "[DRY-RUN]          --account=${ACCOUNT} \\"
            echo "[DRY-RUN]          --output=spack.${host}.${env_name}.log --error=spack.${host}.${env_name}.log \\"
            echo "[DRY-RUN]          ${install_script_name}"
            ;;
          *)
            echo "[DRY-RUN]   run_interactive_job ${host} ${install_script_name} ${reuse_build_cache}"
            ;;
        esac
      else
        echo "[DRY-RUN]   bash ${install_script_name}"
      fi

      if [[ "${update_build_cache}" == "true" ]]; then
        echo "[DRY-RUN] spack buildcache push -u <binary_mirror_path>"
        echo "[DRY-RUN] spack buildcache update-index local-binary"
        echo "[DRY-RUN] fix_permissions ${host} <binary_mirror_path> 0"
      elif [[ "${publish_build_cache}" == "true" ]]; then
        echo "[DRY-RUN] spack buildcache push -u <binary_mirror_path>"
        echo "[DRY-RUN] spack buildcache update-index local-binary"
        echo "[DRY-RUN] fix_permissions ${host} <binary_mirror_path> 0"
      else
        echo "[DRY-RUN] spack module ${module_choice} refresh --yes --upstream-modules"
        echo "[DRY-RUN] spack stack setup-meta-modules"
      fi
      if [[ "${update_source_cache}" == "true" ]]; then
        echo "[DRY-RUN] fix_permissions ${host} <source_mirror_path> 0"
      fi
      if [[ "${update_cargo_mirror}" == "true" ]]; then
        echo "[DRY-RUN] fix_permissions ${host} ${cargo_mirror_path} 0"
      fi

      echo "[DRY-RUN] spack clean -d -f -m -p -s"
      echo "[DRY-RUN] spack env deactivate"
      echo ""
      first_pass="false"
      continue
    fi

    # Reset environment
    echo "Resetting environment ..."
    case ${host} in
      nas)
        umask 0022
        set +e
        module purge
        module use /nasa/modulefiles/toss4
        module use /nobackup/gmao_SIteam/modulefiles
        module use /nasa/modulefiles/testing
        set -e
        ;;
      nas-toss5)
        umask 0022
        set +e
        module purge
        module use /opt/cray/pe/modulefiles
        module use /nasa/modulefiles/toss5_crayex
        module use /nobackup/gmao_SIteam/modulefiles-TOSS5
        set -e
        ;;
      discover)
        umask 0022
        set +e
        module purge
        set -e
        ;;
      discover-gmao)
        umask 0022
        set +e
        module purge
        set -e
        ;;
      bucy)
        umask 0022
        set +e
        module purge
        set -e
        ;;
      macos.gmao)
        set +e
        ulimit -s unlimited 2>/dev/null || ulimit -s hard 2>/dev/null || ulimit -s 65532 2>/dev/null || true
        if ! command -v module &> /dev/null; then
          if command -v brew &> /dev/null; then
            . $(brew --prefix)/opt/lmod/init/bash 2>/dev/null || true
          fi
        fi
        set -e
        ;;
      *)
        echo "ERROR, host ${host} not configured for resetting environment"
        exit 1
        ;;
    esac

    setup_git_lfs

    # Info prints
    ulimit -a
    module li

    source setup.sh
    if [[ "${first_pass}" == "true" ]]; then
      spack clean -a
    else
      # Don't remove software and configuration needed to bootstrap Spack
      spack clean -d -f -m -p -s
    fi

    # Update bootstrap mirror if requested before creating any
    # environments. It is sufficient to do this one time only.
    if [[ "${update_bootstrap_mirror}" == "true"*  ]]; then
      tmp_bootstrap_mirror_path=${PWD}/tmp-bootstrap-mirror
      echo "Creating bootstrap mirror ${tmp_bootstrap_mirror_path} ..."
      rm -fr ${tmp_bootstrap_mirror_path}
      spack bootstrap mirror --binary-packages ${tmp_bootstrap_mirror_path} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.bootstrap-mirror.${LOG_TIMESTAMP}
      rsync -a ${tmp_bootstrap_mirror_path}/ ${bootstrap_mirror_path}/
      rm -fr ${tmp_bootstrap_mirror_path}
      # Update buildcache index
      spack buildcache update-index ${bootstrap_mirror_path}/bootstrap_cache
      # Fix permissions for the bootstrap mirror
      fix_permissions ${host} ${bootstrap_mirror_path} 0
      update_bootstrap_mirror="false"
      # When spack creates a bootstrap mirror, it populates the "spack" scope
      # with compilers and packages it finds, which can create problems later
      echo "Removing package config in spack/etc/spack created by spack boostrap mirror"
      rm -vf spack/etc/spack/packages.yaml
    fi

    if [[ ! ${env_exists} == "true" ]]; then
      if [[ "${host}" == "macos.gmao" ]]; then
        check_macos_prerequisites

        macos_site_dir="${SPACK_STACK_DIR}/configs/sites/tier2/macos.gmao"
        brew_prefix=$(brew --prefix)

        # Use NAG vars if available
        nag_version=${MAC_GMAO_NAG_VERSION}
        nag_path=${MAC_GMAO_NAG_PATH}
        nag_prefix=${MAC_GMAO_NAG_PREFIX}

        apple_clang_version=${MAC_GMAO_APPLE_CLANG_VERSION:-"21.0.0"}

        for template_file in "${macos_site_dir}"/*.yaml.template; do
          if [[ -f "${template_file}" ]]; then
            filename=$(basename "${template_file}")
            base_filename="${filename%.template}"

            # Special case for NAG template: inject version into filename
            if [[ "${base_filename}" == "packages_nag.yaml" && -n "${nag_version}" ]]; then
              base_filename="packages_nag-${nag_version}.yaml"
            fi

            sed_cmd="sed -e \"s#@HOME@#${HOME}#g\" -e \"s#@BREW_PREFIX@#${brew_prefix}#g\" -e \"s#@APPLE_CLANG_VERSION@#${apple_clang_version}#g\""
            if [[ -n "${nag_version}" ]]; then
              sed_cmd="${sed_cmd} -e \"s#@NAG_VERSION@#${nag_version}#g\" -e \"s#@NAG_PREFIX@#${nag_prefix}#g\" -e \"s#@NAG_PATH@#${nag_path}#g\""
            fi

            eval "${sed_cmd} \"${template_file}\"" > "${SPACK_STACK_DIR}/configs/sites/tier2/${host}/${base_filename}"
            if [[ -d "${SPACK_STACK_DIR}/.git" ]]; then
              grep -q "^configs/sites/tier2/${host}/${base_filename}$" "${SPACK_STACK_DIR}/.git/info/exclude" 2>/dev/null || echo "configs/sites/tier2/${host}/${base_filename}" >> "${SPACK_STACK_DIR}/.git/info/exclude"
            fi
          fi
        done
      fi

      spack stack create env --name=${env_name} \
                             --site=${host} \
                             --compiler=${compiler_name}-${compiler_version} \
                             --template=${template} \
                             --dir=${environment_dirs} \
                             --treat-warnings-as-errors \
                             2>&1 | tee ${SPACK_STACK_DIR}/logs/log.create.${env_name}.${LOG_TIMESTAMP}

      # On macOS, esmf ~debug does not work with gfortranclang/GEOS, so remove
      # the geos-gcm-env ~debug spec from the environment spack.yaml if present.
      if [[ "${host}" == "macos.gmao" ]]; then
        env_spack_yaml="${env_dir}/spack.yaml"
        if grep -qE 'geos-gcm-env([^[:space:]]*)?[[:space:]]+~debug' "${env_spack_yaml}" 2>/dev/null; then
          echo "INFO: macOS: removing GEOS-GCM '~debug' specs from ${env_spack_yaml}"
          grep -vE 'geos-gcm-env([^[:space:]]*)?[[:space:]]+~debug' "${env_spack_yaml}" > "${env_spack_yaml}.tmp" && mv "${env_spack_yaml}.tmp" "${env_spack_yaml}"
        fi
      fi

      # Clean up the generated yamls in the site configuration now that the env is created
      if [[ "${host}" == "macos.gmao" && ! ${env_exists} == "true" ]]; then
        rm -f "${SPACK_STACK_DIR}/configs/sites/tier2/${host}/mirrors.yaml"
        rm -f "${SPACK_STACK_DIR}/configs/sites/tier2/${host}/packages_*.yaml"
      fi
    fi
    spack env activate -p ${env_dir}

    # Environment configuration can select a different miscellaneous-cache
    # location. Clear it after activation so package and patch indexes reflect
    # local recipe changes made since the environment was created.
    spack clean -m

    if [[ "${host}" == "macos.gmao" && ! ${env_exists} == "true" ]]; then
      echo "Running spack external find for macOS generic packages..."
      # cmake is excluded here and injected manually below with ~doc to prevent
      # the solver from considering cmake+doc (which pulls in py-sphinx@:6.1 -> python@:3.12)
      spack external find --not-buildable autoconf automake bash cvs doxygen gawk git-lfs groff libtool ninja npm subversion swig texinfo

      brew_prefix=$(brew --prefix)
      tcsh_version=$(${brew_prefix}/bin/tcsh --version | awk '{print $2}')
      rust_version=$(${brew_prefix}/bin/rustc --version | awk '{print $2}')
      cmake_version=$(${brew_prefix}/bin/cmake --version | head -1 | awk '{print $3}')

      if [[ -z "${rust_version}" ]]; then
        echo "ERROR: Unable to determine the Homebrew Rust version from ${brew_prefix}/bin/rustc"
        exit 1
      fi

      echo "Manually injecting tricky macOS packages into Spack configuration..."
      cat << EOF > spack-macos-externals.yaml
packages:
  cmake:
    externals:
    - spec: cmake@${cmake_version}+ownlibs+doc
      prefix: ${brew_prefix}
    buildable: false
  tcsh:
    externals:
    - spec: tcsh@${tcsh_version}
      prefix: ${brew_prefix}
  rust:
    externals:
    - spec: rust@${rust_version}
      prefix: ${brew_prefix}
      extra_attributes:
        cargo: ${brew_prefix}/bin/cargo
        compilers:
          rust: ${brew_prefix}/bin/rustc
EOF
      spack config add -f spack-macos-externals.yaml
      rm -f spack-macos-externals.yaml
    fi

    echo "Registering bootstrap mirror ${bootstrap_mirror_path} ..."
    if [[ ! -d ${bootstrap_mirror_path} ]]; then
      echo "ERROR, directory ${bootstrap_mirror_path} not found"
      exit 1
    fi
    spack bootstrap list | grep local-sources || \
        spack bootstrap add --trust local-sources ${bootstrap_mirror_path}/metadata/sources
    spack bootstrap list | grep local-binaries || \
        spack bootstrap add --trust local-binaries ${bootstrap_mirror_path}/metadata/binaries

    # Check that the site has mirrors configured for local source and build caches,
    # and extract the local path on disk. Need to strip leading "file://" from path.
    # Use awk to grab the last field since spack mirror list uses variable-width columns.
    result=$(spack mirror list | grep local-source) || \
        (echo "ERROR, no local source cache configured" && exit 1)
    source_mirror_path=$(echo ${result} | awk '{print $NF}')
    source_mirror_path=${source_mirror_path#file://}
    echo "Spack source mirror path: ${source_mirror_path}"
    # For build caches, additional logic is needed. If buildcache_dir is defined,
    # update the location of the default build cache to this directory.
    result=$(spack mirror list | grep local-binary) || \
        (echo "ERROR, no local binary cache configured" && exit 1)
    binary_mirror_path=$(echo ${result} | awk '{print $NF}')
    binary_mirror_path=${binary_mirror_path#file://}
    # If buildcache_dir is set, update binary_mirror_path
    if [[ ! -z ${buildcache_dir} ]]; then
      sed -i "s#${binary_mirror_path}#${buildcache_dir}#g" ${env_dir}/site/mirrors.yaml
      result=$(spack mirror list | grep local-binary)
      binary_mirror_path=$(echo ${result} | awk '{print $NF}')
      binary_mirror_path=${binary_mirror_path#file://}
    fi
    echo "Spack binary mirror path: ${binary_mirror_path}"

    if [[ "${update_build_cache}" == "true" ]]; then
      spack config add config:install_tree:padded_length:200
    fi

    # Bootstrap spack explicitly
    echo "Bootstrapping spack ..."
    spack bootstrap now 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.bootstrap.${env_name}.${LOG_TIMESTAMP}

    # Concretize environment, and check that spack.lock is created
    spack concretize --force --fresh 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.concretize.${env_name}.${LOG_TIMESTAMP}
    if [[ ! -e ${env_dir}/spack.lock ]]; then
      echo "ERROR during concretization of environment ${env_name}, spack.lock not found"
      exit 1
    fi

    # Check for duplicate packages. py-versioneer is intentionally duplicated:
    # py-pyogrio requires 0.28 while py-partd (required by modern py-dask)
    # requires 0.29; both are build-only dependencies.
    ./util/show_duplicate_packages.py -i crtm -i crtm-fix -i esmf -i mapl -i neptune-env -i py-cython -i ip -i fms -i geos-gcm-env -i py-versioneer

    # Stop here if --concretize-only / -o was requested
    if [[ "${SPACK_STACK_CONCRETIZE_ONLY}" == "true"* ]]; then
      echo "INFO: --concretize-only requested; stopping after concretization."
      echo "INFO: Concretization log: ${SPACK_STACK_DIR}/logs/log.concretize.${env_name}.${LOG_TIMESTAMP}"
      exit 0
    fi

    # Update local source cache if requested
    if [[ "${update_source_cache}" == "true"* ]]; then
      echo "Updating local source cache ..."
      spack mirror create -a -d ${source_mirror_path}
    fi

    # Update local cargo mirror if requested; this can be
    # unreliable, therefore ignore errors and proceed ...
    if [[ "${update_cargo_mirror}" == "true"* ]]; then
      set +e
      echo "Updating local cargo mirror ..."
      export CARGO_HTTP_MULTIPLEXING=false
      export CARGO_HTTP_TIMEOUT=600
      export CARGO_HTTP_LOW_SPEED_LIMIT=1
      export CARGO_HTTP_LOW_SPEED_TIMEOUT=600
      export CARGO_NET_RETRY=10
      ./util/fetch_cargo_deps.py
      set -e
    fi

    # Install the environment with the correct flags
    case ${reuse_build_cache} in
      "true")
        buildcache_install_flags="--no-check-signature"
        ;;
      "false")
        buildcache_install_flags="--no-cache"
        ;;
      *)
        echo "ERROR, unkown reuse_build_cache value ${reuse_build_cache} for setting install flags"
        exit 1
        ;;
    esac

    case ${submit_to_scheduler} in
      "true")
        if [[ "${SPACK_STACK_DISABLE_LOCKS}" == "true" ]]; then
          # --disable-locks is a command-line setting and is not inherited by
          # the worker processes used for concurrent package installation.
          # Keep installs serial when locks are disabled.
          parallel_install_flags="--concurrent-packages=1 --jobs=${spack_build_jobs}"
        else
          parallel_install_flags="--concurrent-packages=2 --jobs=${spack_build_jobs}"
        fi
        ;;
      "false")
        parallel_install_flags=""
        ;;
      *)
        echo "ERROR, unkown submit_to_scheduler value ${submit_to_scheduler} for setting install flags"
        exit 1
        ;;
    esac

    install_script=${PWD}/${install_script_name}

    # Locally ignore the generated install script in git without changing global .gitignore
    if [[ -d "${SPACK_STACK_DIR}/.git" ]] && ! grep -q "^spack-install\.\*\.sh$" "${SPACK_STACK_DIR}/.git/info/exclude" 2>/dev/null; then
      echo "spack-install.*.sh" >> "${SPACK_STACK_DIR}/.git/info/exclude"
    fi

    cat << EOF > ${install_script}
#!/usr/bin/env bash

set -e

# Initialize the module system (needed when running as a batch job via sbatch,
# where lmod shell functions are not automatically available).
if [[ -f /usr/share/lmod/lmod/init/bash ]]; then
  source /usr/share/lmod/lmod/init/bash
fi
set +e
module purge
set -e

# IODA data repositories contain Git LFS objects. Keep the site Git LFS
# executable available in case this job needs to fetch a version-controlled
# source rather than consume a pre-created source archive.
case "${host}" in
  discover|discover-gmao)
    git_lfs_bin=/discover/swdev/gmao_SIteam/other/SLES15.4/git-lfs/3.7.1/bin
    ;;
  nas)
    git_lfs_bin=/nobackup/gmao_SIteam/git-lfs/3.7.0/bin
    ;;
  nas-toss5)
    git_lfs_bin=/nobackup/gmao_SIteam/git-lfs/3.7.1/bin
    ;;
  *)
    git_lfs_bin=
    ;;
esac
if [[ -n "\${git_lfs_bin}" ]]; then
  if [[ ! -x "\${git_lfs_bin}/git-lfs" ]]; then
    echo "ERROR: required git-lfs executable not found: \${git_lfs_bin}/git-lfs"
    exit 1
  fi
  export PATH="\${git_lfs_bin}:\${PATH}"
  echo "INFO: added git-lfs to PATH: \${git_lfs_bin}"
fi

# Point cargo at the local mirror so rust builds don't try to reach the internet.
export SPACK_CARGO_HOME=${cargo_mirror_path}
export CARGO_NET_OFFLINE=true

if [[ "${SPACK_STACK_DISABLE_LOCKS}" == "true" ]]; then
  # Spack's package workers do not inherit command-line configuration or the
  # environment's config scopes. Give every worker a private user config scope
  # with locking disabled for this isolated recovery job only.
  spack_lock_config_dir=\$(mktemp -d "\${TMPDIR:-/tmp}/spack-stack-lock-config.XXXXXX")
  cat > "\${spack_lock_config_dir}/config.yaml" <<'LOCK_CONFIG_EOF'
config:
  locks: false
LOCK_CONFIG_EOF
  export SPACK_USER_CONFIG_PATH="\${spack_lock_config_dir}"
  # setup.sh normally disables local configuration for reproducibility. The
  # private scope above is intentionally the sole local configuration for -L.
  unset SPACK_DISABLE_LOCAL_CONFIG
  echo "INFO: -L using job-local config: \${spack_lock_config_dir}/config.yaml"
fi

# Build stages use the paths configured in the site config.yaml
# (under /discover/nobackup/projects/gmao/SIteam/spack-stack/cache/).
# TSE_TMPDIR is not used: its 200k inode quota is insufficient for large
# packages like rustc which extract tens of thousands of files.

# On Discover, the 2025.3 Intel MPI module is visible only after its compiler
# module is loaded. Preload the pair in the batch shell so every Spack package
# worker inherits a valid module hierarchy.
if [[ "${host}" == "discover" || "${host}" == "discover-gmao" ]] && \
   [[ "${compiler}" == "oneapi@=2025.3.0" ]]; then
  echo "INFO: preloading comp/intel/2025.3.0 and mpi/impi/2021.17"
  module load comp/intel/2025.3.0 mpi/impi/2021.17
elif [[ "${host}" == "discover" || "${host}" == "discover-gmao" ]] && \
     [[ "${compiler}" == "gcc@=15.2.0" ]]; then
  echo "INFO: preloading comp/gcc/15.2.0 and mpi/openmpi/5.0.10/gcc-15.2.0"
  module load comp/gcc/15.2.0 mpi/openmpi/5.0.10/gcc-15.2.0
elif [[ "${host}" == "nas" ]] && [[ "${compiler}" == "gcc@=15.2.0" ]]; then
  # The TOSS4 Open MPI module has a Tcl prereq on the matching GCC module.
  # Load them in order so Spack workers inherit a valid module hierarchy.
  echo "INFO: preloading comp-gcc/15.2.0 and mpi-openmpi/4.1.8/gcc/15.2.0"
  module load comp-gcc/15.2.0 mpi-openmpi/4.1.8/gcc/15.2.0
elif [[ "${host}" == "discover-gmao" ]] && \
     [[ "${compiler}" == "nag@=7.2.7238" ]]; then
  # This external OpenMPI was built with GCC C/C++ and NAG Fortran. Lmod
  # requires the two compiler modules before the compiler-specific MPI module.
  echo "INFO: preloading comp/gcc/12.3.0, comp/nag/7.2-7238, and mpi/openmpi/4.1.6/nag_7.2.7238-gcc_12.3.0"
  module load comp/gcc/12.3.0 comp/nag/7.2-7238 mpi/openmpi/4.1.6/nag_7.2.7238-gcc_12.3.0
fi

$(declare -p test_packages)

# If no tests are required, install everything
if [[ \${#test_packages[@]} -eq 0 ]]; then
  set -o pipefail
  spack ${spack_install_lock_flag} install --verbose ${buildcache_install_flags} ${parallel_install_flags} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}
  set +o pipefail
else
  for (( idx=0; idx<\${#test_packages[@]}; idx++ )); do
    test_package=\${test_packages[\${idx}]}
    # First, check if this package is in this environment
    set +e
    grep -e "\${test_package}@" log.concretize.${env_name}.${LOG_TIMESTAMP} || continue
    set -e
    idx_padded=\$(printf "%03d" "\$((idx+1))")
    set -o pipefail
    spack ${spack_install_lock_flag} install --verbose ${buildcache_install_flags} ${parallel_install_flags} --only=dependencies \${test_package} \\
      2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.\${idx_padded}.\${test_package}-dependencies
    spack ${spack_install_lock_flag} install --verbose --no-cache --test=root \${test_package} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.\${idx_padded}.\${test_package}
    set +o pipefail
  done
  # idx now equals the length of the array; install the rest
  idx_padded=\$(printf "%03d" "\$((idx+1))")
  set -o pipefail
  spack ${spack_install_lock_flag} install --verbose ${buildcache_install_flags} ${parallel_install_flags} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.\${idx_padded}
  set +o pipefail
fi
EOF
    chmod u+x ${install_script}
    if [[ "${submit_to_scheduler}" == "true" ]]; then
      run_interactive_job ${host} ${install_script} ${reuse_build_cache} ${env_name}
    else
      bash ${install_script}
    fi

    # Publish binaries for build mode and for the private local mode. Local
    # mode keeps the final environment name and still generates its modules.
    if [[ "${publish_build_cache}" == "true" ]]; then
      spack buildcache push -u ${binary_mirror_path}
      spack buildcache update-index local-binary
    fi

    # In install mode, create environment modules
    if [[ "${update_build_cache}" == "false" ]]; then
      spack module ${module_choice} refresh --yes --upstream-modules 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.modules.${env_name}.${LOG_TIMESTAMP}
      spack stack setup-meta-modules 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.setup-meta-modules.${env_name}.${LOG_TIMESTAMP}
    fi

    # When creating or updating buildcaches, fix permissions for mirrors.
    # Mirrors do not contain executables, therefore skip looking for them.
    if [[ "${update_source_cache}" == "true" ]]; then
      fix_permissions ${host} ${source_mirror_path} 0
    fi
    if [[ "${publish_build_cache}" == "true" ]]; then
      fix_permissions ${host} ${binary_mirror_path} 0
    fi
    if [[ "${update_cargo_mirror}" == "true" ]]; then
      fix_permissions ${host} ${cargo_mirror_path} 0
    fi

    # Clean up (don't remove software and configuration needed to bootstrap Spack)
    spack clean -d -f -m -p -s
    spack env deactivate
    first_pass="false"

  done

done

# Repair permissions for environments if in installer mode
if [[ "${update_build_cache}" == "false" ]]; then
  # Also search for exectuables
  if [[ "${SPACK_STACK_DRY_RUN}" == "true" ]]; then
    echo "[DRY-RUN] fix_permissions ${host} ${environment_dirs} 1"
  else
    fix_permissions ${host} ${environment_dirs} 1
  fi
fi

echo "SUCCESS"
echo

exit 0
