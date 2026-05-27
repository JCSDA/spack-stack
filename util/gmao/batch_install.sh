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
  echo "Usage: $0 -r <ROLE> -m <MODE> [-d <ENV_DIRS>] [-c <BUILDCACHE_DIR>] [-H <HOSTNAME>]"
  echo
  echo "  -r  Set role, can be 'ops' or 'dev'"
  echo "  -m  Set mode, can be 'build' or 'install';"
  echo "      build: build environments and update build caches;"
  echo "      install: install environments using build caches"
  echo "  -d  Build or install environments in ENV_DIRS;"
  echo "      if not set, the default location is used"
  echo "  -c  Provide location of build caches as BUILDCACHE_DIR;"
  echo "      if not set, authoritative build caches are used"
  echo "  -u  Flag to update bootstrap and source caches;"
  echo "      requires role 'dev' and mode 'build'"
  echo "  -e  Continue builds/install in existing environments;"
  echo "      by default, exit with an error if already exist"
  echo "  -C  Set a comma-separated list of compilers to use (e.g. gcc@=15.2.0,nag@=7.2.7243);"
  echo "      overrides the default compilers for the site"
  echo "  -N  Path to nagfor executable (e.g. /opt/nag/bin/nagfor);"
  echo "      forces NAG stack to be built using this specific compiler"
  echo "  -a  Set PBS/SLURM account (default: s1873);"
  echo "      overrides the ACCOUNT environment variable"
  echo "  -s  Submit 'spack install' to batch scheduler"
  echo "  -t  Run tests for specific thirdparty dependencies;"
  echo "      these are currently hardcoded in batch_install.sh"
  echo "  -n  Dry-run: print what would be executed without running anything"
  echo "  -H  Provide hostname manually (overrides autodetection);"
  echo "      useful when VPN/etc masks the real hostname"
  echo "  -h  display this help"
  echo
}

while getopts r:m:d:c:C:N:H:a:nuesth flag
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
    n)
      SPACK_STACK_DRY_RUN="true"
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
    t)
      SPACK_STACK_RUN_TESTS="true"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

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
echo "  SPACK_STACK_RUN_TESTS:                       ${SPACK_STACK_RUN_TESTS:-false}"
echo "  ACCOUNT:                                     ${ACCOUNT:-s1873 (default)}"

# Set default account if not provided via -a or environment
ACCOUNT=${ACCOUNT:-s1873}

if [[ -z ${SPACK_STACK_ROLE} ]]; then
  echo "ERROR, SPACK_STACK_ROLE not defined. Provide -r ROLE as argument"
  exit 1
elif [[ ! ${SPACK_STACK_ROLE} == "dev" && ! ${SPACK_STACK_ROLE} == "ops" ]]; then
  echo "ERROR, invalid role '${SPACK_STACK_ROLE}'"
  exit 1
fi

if [[ -z ${SPACK_STACK_MODE} ]]; then
  echo "ERROR, SPACK_STACK_MODE not defined. Provide -m MODE as argument"
  exit 1
elif [[ ! ${SPACK_STACK_MODE} == "build" && ! ${SPACK_STACK_MODE} == "install" ]]; then
  echo "ERROR, invalid mode '${SPACK_STACK_MODE}'"
  exit 1
fi

# Role ops cannot write to the default (authoritative) build cache
if [[ ${SPACK_STACK_ROLE} == "ops" && ${SPACK_STACK_MODE} == "build" && -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
  echo "ERROR, SPACK_STACK_BUILDCACHE_DIR not defined. Provide -c BUILDCACHE_DIR"
  echo "as argument when role is 'ops' and mode is 'build'"
  exit 1
fi

# Updating bootstrap and source caches requires role dev and mode build
if [[ ${SPACK_STACK_UPDATE_DEV_CACHES} == "true" ]]; then
  if [[ ! ${SPACK_STACK_ROLE} == "dev" || ! ${SPACK_STACK_MODE} == "build" ]]; then
    echo "ERROR, SPACK_STACK_UPDATE_DEV_CACHES requires role 'dev' and mode 'build'"
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
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=13.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/swbuild/gmao_SIteam/spack-stack/bootstrap-mirror-toss4"
    SPACK_STACK_CARGO_MIRROR="/swbuild/gmao_SIteam/spack-stack/cargo-mirror"
    SPACK_STACK_ENVIRONMENT_DIRS=${SPACK_STACK_ENVIRONMENT_DIRS:-${PWD}/envs/toss4}
    ;;
  nas-toss5)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=14.2.1")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/swbuild/gmao_SIteam/spack-stack/bootstrap-mirror-toss5"
    SPACK_STACK_CARGO_MIRROR="/swbuild/gmao_SIteam/spack-stack/cargo-mirror"
    SPACK_STACK_ENVIRONMENT_DIRS=${SPACK_STACK_ENVIRONMENT_DIRS:-${PWD}/envs/toss5}
    ;;
  discover)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=14.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/discover/swdev/jcsda/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/discover/swdev/jcsda/spack-stack/cargo-mirror"
    ;;
  discover-gmao)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "oneapi@=2025.3.0" "gcc@=15.2.0")
    #SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_BATCH_TEMPLATES=("geos-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/discover/nobackup/projects/gmao/SIteam/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/discover/nobackup/projects/gmao/SIteam/spack-stack/cargo-mirror"
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

    SPACK_STACK_BATCH_COMPILERS=("gcc@=15.2.0")
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
      slurm_constraint="--constraint=mil"
      if [[ "${ACCOUNT}" == "s1873" ]]; then
        slurm_partition="--partition=preops --qos=benchmark"
      else
        slurm_partition=""
      fi
      slurm_log="${job_name}.log"
      echo "INFO: salloc output redirected to ${slurm_log}"
      salloc --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} \
             ${slurm_constraint} ${slurm_partition} \
             --job-name=${job_name} \
             --account=${ACCOUNT} bash ${script} \
             > "${slurm_log}" 2>&1
      echo "INFO: salloc job complete, log: ${slurm_log}"
      ;;
    discover-gmao)
      slurm_constraint="--constraint=mil"
      if [[ "${ACCOUNT}" == "s1873" ]]; then
        slurm_partition="--partition=preops --qos=benchmark"
      else
        slurm_partition=""
      fi
      slurm_log="${job_name}.log"
      echo "INFO: salloc output redirected to ${slurm_log}"
      salloc --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} \
             ${slurm_constraint} ${slurm_partition} \
             --job-name=${job_name} \
             --account=${ACCOUNT} bash ${script} \
             > "${slurm_log}" 2>&1
      echo "INFO: salloc job complete, log: ${slurm_log}"
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
export CARGO_HOME=${cargo_mirror_path}

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
          echo "[DRY-RUN] grep -v 'geos-gcm-env ~debug' ${env_dir}/spack.yaml  # remove ~debug spec (esmf ~debug unsupported on macOS)"
        fi
      fi
      echo "[DRY-RUN] spack env activate -p ${env_dir}"
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
      echo "[DRY-RUN] ./util/show_duplicate_packages.py -i crtm -i crtm-fix -i esmf -i mapl -i neptune-env -i py-cython -i ip -i fms -i geos-gcm-env"

      if [[ "${update_source_cache}" == "true"* ]]; then
        echo "[DRY-RUN] spack mirror create -a -d <source_mirror_path>"
      fi
      if [[ "${update_cargo_mirror}" == "true"* ]]; then
        echo "[DRY-RUN] ./util/fetch_cargo_deps.py"
      fi

      if [[ "${host}" == "nas" || "${host}" == "nas-toss5" ]] && \
         [[ "${env_name_prefix}" == "ue" ]] && \
         [[ "${compiler_name}" == "oneapi" ]]; then
        echo "[DRY-RUN] # ectrans/ecbuild workaround (NAS oneapi only):"
        echo "[DRY-RUN] # See: https://github.com/JCSDA/spack-stack/issues/1775#issuecomment-3898802720"
        echo "[DRY-RUN] spack install ecbuild"
        echo "[DRY-RUN] ./util/gmao/patch_ecbuild_ectrans.py --patch \$(spack location -i ecbuild)/.../ecbuild_add_lang_flags.cmake"
        echo "[DRY-RUN] spack install ectrans"
        echo "[DRY-RUN] ./util/gmao/patch_ecbuild_ectrans.py --revert \$(spack location -i ecbuild)/.../ecbuild_add_lang_flags.cmake"
      fi

      echo "[DRY-RUN] Generating spack-install.${env_name}.sh and executing via:"
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
            echo "[DRY-RUN]        -l walltime=08:00:00 \\"
            echo "[DRY-RUN]        -l site=needed=/home3+/nobackupp18+/nobackupp28+/vast_swbuild/swbuild4 \\"
            echo "[DRY-RUN]        -W group_list=${ACCOUNT} -W block=true -W umask=0022 \\"
            echo "[DRY-RUN]        -j oe -k oed -N spack.${host}.${env_name} \\"
            echo "[DRY-RUN]        spack-install.${env_name}.sh"
            ;;
          nas-toss5)
            echo "[DRY-RUN]   qsub -V \\"
            echo "[DRY-RUN]        -l select=1:ncpus=${tpn_dry}:mpiprocs=${tpn_dry}:model=tur_ath \\"
            echo "[DRY-RUN]        -q normal -l walltime=08:00:00 \\"
            echo "[DRY-RUN]        -l site=needed=/home3+/nobackupp18+/nobackupp28+/vast_swbuild/swbuild4 \\"
            echo "[DRY-RUN]        -W group_list=${ACCOUNT} -W block=true -W umask=0022 \\"
            echo "[DRY-RUN]        -j oe -k oed -N spack.${host}.${env_name} \\"
            echo "[DRY-RUN]        spack-install.${env_name}.sh"
            ;;
          discover)
            if [[ "${ACCOUNT}" == "s1873" ]]; then
              slurm_extra_dry="--partition=preops --qos=benchmark"
            else
              slurm_extra_dry="(default partition/qos)"
            fi
            echo "[DRY-RUN]   salloc --nodes=1 --ntasks-per-node=${tpn_dry} --time=08:00:00 \\"
            echo "[DRY-RUN]          --constraint=mil ${slurm_extra_dry} \\"
            echo "[DRY-RUN]          --job-name=spack.${host}.${env_name} \\"
            echo "[DRY-RUN]          --account=${ACCOUNT} bash spack-install.${env_name}.sh"
            ;;
          discover-gmao)
            if [[ "${ACCOUNT}" == "s1873" ]]; then
              slurm_extra_dry="--partition=preops --qos=benchmark"
            else
              slurm_extra_dry="(default partition/qos)"
            fi
            echo "[DRY-RUN]   salloc --nodes=1 --ntasks-per-node=${tpn_dry} --time=08:00:00 \\"
            echo "[DRY-RUN]          --constraint=mil ${slurm_extra_dry} \\"
            echo "[DRY-RUN]          --job-name=spack.${host}.${env_name} \\"
            echo "[DRY-RUN]          --account=${ACCOUNT} bash spack-install.${env_name}.sh"
            ;;
          *)
            echo "[DRY-RUN]   run_interactive_job ${host} spack-install.${env_name}.sh ${reuse_build_cache}"
            ;;
        esac
      else
        echo "[DRY-RUN]   bash spack-install.${env_name}.sh"
      fi

      if [[ "${update_build_cache}" == "true" ]]; then
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
      atlantis)
        umask 0022
        module purge
        case ${compiler} in
          clang@=22.1.0)
            module use /gpfs/neptune/spack-stack/llvm-22.1.0/modulefiles
            module use /gpfs/neptune/spack-stack/openmpi-4.1.8/llvm-22.1.0/modulefiles
            ;;
          gcc@=13.4.0)
            module use /gpfs/neptune/spack-stack/gcc-13.4.0/modulefiles
            module use /gpfs/neptune/spack-stack/openmpi-4.1.8/gcc-13.4.0/modulefiles
            ;;
          oneapi@=2025.3.0)
            module use /gpfs/neptune/spack-stack/oneapi-2025.3.0/modulefiles
            ;;
        esac
        ;;
      nas)
        umask 0022
        set +e
        module purge
        set -e
        ;;
      nas-toss5)
        umask 0022
        set +e
        module purge
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
        if grep -q "geos-gcm-env ~debug" "${env_spack_yaml}" 2>/dev/null; then
          echo "INFO: macOS: removing 'geos-gcm-env ~debug' spec from ${env_spack_yaml}"
          grep -v "geos-gcm-env ~debug" "${env_spack_yaml}" > "${env_spack_yaml}.tmp" && mv "${env_spack_yaml}.tmp" "${env_spack_yaml}"
        fi
      fi

      # Clean up the generated yamls in the site configuration now that the env is created
      if [[ "${host}" == "macos.gmao" && ! ${env_exists} == "true" ]]; then
        rm -f "${SPACK_STACK_DIR}/configs/sites/tier2/${host}/mirrors.yaml"
        rm -f "${SPACK_STACK_DIR}/configs/sites/tier2/${host}/packages_*.yaml"
      fi
    fi
    spack env activate -p ${env_dir}

    if [[ "${host}" == "macos.gmao" && ! ${env_exists} == "true" ]]; then
      echo "Running spack external find for macOS generic packages..."
      spack external find --not-buildable autoconf automake bash cmake cvs doxygen gawk git-lfs groff libtool ninja npm subversion swig texinfo

      brew_prefix=$(brew --prefix)
      tcsh_version=$(${brew_prefix}/bin/tcsh --version | awk '{print $2}')
      rust_version=$(${brew_prefix}/bin/rustc --version | awk '{print $2}')

      echo "Manually injecting tricky macOS packages into Spack configuration..."
      cat << EOF > spack-macos-externals.yaml
packages:
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

    # Check for duplicate packages
    ./util/show_duplicate_packages.py -i crtm -i crtm-fix -i esmf -i mapl -i neptune-env -i py-cython -i ip -i fms -i geos-gcm-env

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
        jobs=$(tasks_per_node ${host})
        parallel_install_flags="--concurrent-packages=2 --jobs=${jobs}"
        ;;
      "false")
        parallel_install_flags=""
        ;;
      *)
        echo "ERROR, unkown submit_to_scheduler value ${submit_to_scheduler} for setting install flags"
        exit 1
        ;;
    esac

    install_script=${PWD}/spack-install.${env_name}.sh

    # Locally ignore the generated install script in git without changing global .gitignore
    if [[ -d "${SPACK_STACK_DIR}/.git" ]] && ! grep -q "^spack-install\.\*\.sh$" "${SPACK_STACK_DIR}/.git/info/exclude" 2>/dev/null; then
      echo "spack-install.*.sh" >> "${SPACK_STACK_DIR}/.git/info/exclude"
    fi

    cat << EOF > ${install_script}
#!/usr/bin/env bash

set -e

$(declare -p test_packages)

# Workaround for ectrans build failure with oneapi at NAS (nas/nas-toss5).
# ecbuild's flag checker incorrectly rejects valid Fortran flags (-march=core-avx2 -no-fma).
# Fix: patch ecbuild cmake to force-add the flags even when the check fails,
# install ectrans, then revert the patch. Spack skips already-installed packages,
# so the subsequent full install proceeds normally.
# See: https://github.com/JCSDA/spack-stack/issues/1775#issuecomment-3898802720
if [[ "${host}" == "nas" || "${host}" == "nas-toss5" ]] && \
   [[ "${env_name_prefix}" == "ue" ]] && \
   [[ "${compiler_name}" == "oneapi" ]]; then
  set -o pipefail
  echo "Installing ecbuild before ectrans workaround ..."
  spack install --verbose ${buildcache_install_flags} ecbuild 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.ecbuild
  ecbuild_flags_cmake=\$(spack location -i ecbuild)/share/ecbuild/cmake/ecbuild_add_lang_flags.cmake
  echo "Applying ectrans/ecbuild workaround to \${ecbuild_flags_cmake} ..."
  ${SPACK_STACK_DIR}/util/gmao/patch_ecbuild_ectrans.py --patch \${ecbuild_flags_cmake}
  spack install --verbose ${buildcache_install_flags} ectrans 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.ectrans
  set +o pipefail
  echo "Reverting ectrans/ecbuild workaround ..."
  ${SPACK_STACK_DIR}/util/gmao/patch_ecbuild_ectrans.py --revert \${ecbuild_flags_cmake}
fi

# If no tests are required, install everything
if [[ \${#test_packages[@]} -eq 0 ]]; then
  set -o pipefail
  spack install --verbose ${buildcache_install_flags} ${parallel_install_flags} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}
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
    spack install --verbose ${buildcache_install_flags} ${parallel_install_flags} --only=dependencies \${test_package} \\
      2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.\${idx_padded}.\${test_package}-dependencies
    spack install --verbose --no-cache --test=root \${test_package} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.\${idx_padded}.\${test_package}
    set +o pipefail
  done
  # idx now equals the length of the array; install the rest
  idx_padded=\$(printf "%03d" "\$((idx+1))")
  set -o pipefail
  spack install --verbose ${buildcache_install_flags} ${parallel_install_flags} 2>&1 | tee ${SPACK_STACK_DIR}/logs/log.install.${env_name}.${LOG_TIMESTAMP}.\${idx_padded}
  set +o pipefail
fi
EOF
    chmod u+x ${install_script}
    if [[ "${submit_to_scheduler}" == "true" ]]; then
      run_interactive_job ${host} ${install_script} ${reuse_build_cache} ${env_name}
    else
      bash ${install_script}
    fi

    # In build mode, update local binary cache
    if [[ "${update_build_cache}" == "true" ]]; then
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
    if [[ "${update_build_cache}" == "true" ]]; then
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
