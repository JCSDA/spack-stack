#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SPACK_STACK_DIR=$(dirname $(dirname ${SCRIPT_DIR}))

set -e

##################################################################################################
# Options                                                                                        #
##################################################################################################

usage() {
  set +x
  echo
  echo "Usage: $0 -r <ROLE> -m <MODE> [-d <ENV_DIRS>] [-c <BUILDCACHE_DIR>]"
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
  echo "  -h  display this help"
  echo
}

while getopts r:m:d:c:uhe flag
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
    u)
      SPACK_STACK_UPDATE_DEV_CACHES="true"
      ;;
    e)
      SPACK_STACK_IGNORE_ENV_EXIST="true"
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
echo "  SPACK_STACK_UPDATE_DEV_CACHES:               ${SPACK_STACK_UPDATE_DEV_CACHES:-false}"
echo "  SPACK_STACK_IGNORE_ENV_EXIST:                ${SPACK_STACK_IGNORE_ENV_EXIST:-false}"

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

# Remove domain name suffices and digits to determine hostname
SPACK_STACK_BATCH_HOST=$(echo ${HOSTNAME} | cut -d "." -f 1)
SPACK_STACK_BATCH_HOST=${SPACK_STACK_BATCH_HOST//[0-9]/}

case ${SPACK_STACK_BATCH_HOST} in
  atlantis)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.1" "oneapi@=2025.0.3" "intel@=2021.6.0" "gcc@=11.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/neptune_diagnostics/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/neptune_diagnostics/spack-stack/cargo-mirror"
    ;;
  blueback)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.1" "oneapi@=2025.0.4" "gcc@=13.3.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/cargo-mirror"
    ;;
  cole)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.1" "gcc@=12.3.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/work1/heinzell/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/p/work1/heinzell/spack-stack/cargo-mirror"
    ;;
  narwhal)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "intel@=2021.10.0" "gcc@=12.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/cargo-mirror"
    ;;
  nautilus)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.1" "oneapi@=2025.0.0" "intel@=2021.5.0" "gcc@=11.2.1")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/cargo-mirror"
    ;;
  tusk)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.0" "gcc@=12.1.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/work1/heinzell/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/p/work1/heinzell/spack-stack/cargo-mirror"
    ;;
  blackpearl)
    # DH* TODO UPDATE oneifx@=2024.1.2 to oneifx@=2025.x.y
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2024.2.1" "oneapi@=2024.1.2" "gcc@=13.3.0" "aocc@=4.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/home/dom/prod/spack-bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/home/dom/prod/spack-cargo-mirror"
    ;;
  bounty)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2025.0.0" "gcc@=13.3.1" "aocc@=5.0.0" "clang@=19.1.4")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/home/dom/prod/spack-bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/home/dom/prod/spack-cargo-mirror"
    ;;
  *)
    echo "ERROR, host ${SPACK_STACK_BATCH_HOST} not configured"
    exit 1
    ;;
esac

##################################################################################################

function fix_permissions() {
  host=$1
  dir=$2
  executables=$3
  echo "Repairing permissions for directory ${dir} on ${host} ..."
  set +e
  case ${host} in
    atlantis)
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      if [[ ${executables} -eq 1 ]]; then
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    blueback)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    cole)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    narwhal)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    nautilus)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    tusk)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    blackpearl)
      ;;
    bounty)
      ;;
    *)
      echo "ERROR, xargs-chmod command not configured for ${host}"
      exit 1
      ;;
  esac
  set -e
}

##################################################################################################

echo
echo "Welcome to NRL SPACK-STACK BATCH INSTALL"
echo

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
mkdir -p ${environment_dirs}

if [[ ! -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
  buildcache_dir=${SPACK_STACK_BUILDCACHE_DIR}
  if [[ "${SPACK_STACK_MODE}" == "install" && ! -d ${buildcache_dir} ]]; then
    echo "ERROR, build cache ${buildcache_dir} not found,"
    echo "must exist before installing environments"
    exit 1
  else
    mkdir -p ${buildcache_dir}
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

# For Cray systems, capture the default=current environment (loaded modules)
# so that it can be restored between building stacks for different compilers
case ${host} in
  atlantis)
    ;;
  blueback)
    module_snapshot=${PWD}/spack-stack.default-modules
    module snapshot -f ${module_snapshot}
    ;;
  cole)
    module_snapshot=${PWD}/spack-stack.default-modules
    module snapshot -f ${module_snapshot}
    ;;
  narwhal)
    module_snapshot=${PWD}/spack-stack.default-modules
    module snapshot -f ${module_snapshot}
    ;;
  nautilus)
    ;;
  tusk)
    module_snapshot=${PWD}/spack-stack.default-modules
    module snapshot -f ${module_snapshot}
    ;;
  blackpearl)
    ;;
  bounty)
    ;;
esac

# Loop through all compilers and templates for this host
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
    # cylc-dev only with gcc
    if [[ "${template}" == "cylc-dev" && ! "${compiler_name}" == "gcc" ]]; then
      echo "Skipping template ${template} with compiler ${compiler}"
      continue
    # unified-env not with intel
    elif [[ "${template}" == "unified-dev" &&  "${compiler_name}" == "intel" ]]; then
      echo "Skipping template ${template} with compiler ${compiler}"
      continue
    # With clang, only neptune-dev
    elif [[ "${compiler_name}" == "clang" && ! "${template}" == "neptune-dev" ]]; then
      echo "Skipping template ${template} with compiler ${compiler}"
      continue
    # With aocc, only neptune-dev
    elif [[ "${compiler_name}" == "aocc" && ! "${template}" == "neptune-dev" ]]; then
      echo "Skipping template ${template} with compiler ${compiler}"
      continue
    fi
    echo "Processing template ${template} with compiler ${compiler}"
    #############################################################

    # Build environment name. Prefices are defined here
    case ${template} in
      unified-dev)
        env_name_prefix="ue"
        ;;
      neptune-dev)
        env_name_prefix="ne"
        ;;
      cylc-dev)
        env_name_prefix="ce"
        ;;
      *)
        echo "ERROR, template ${template} not configured"
        exit 1
        ;;
    esac
    env_name=${env_name_prefix}-${compiler_name}-${compiler_version}
    [[ "${update_build_cache}" == "true" ]] && env_name=${env_name}-build
    env_dir=${environment_dirs}/${env_name}

    # Bail out if the environment already exists
    if [[ -d ${env_dir} ]]; then
      if [[ ${ignore_env_exist} == "true" ]]; then
        env_exists="true"
      else
        echo "ERROR, environment ${env_dir} already exists"
        exit 1
      fi
    else
      env_exists="false"
    fi

    # Reset environment
    echo "Resetting environment ..."
    case ${host} in
      atlantis)
        umask 0022
        module purge
        ;;
      blueback)
        # Check if snapshot to restore default environment exists, then restore
        if [[ ! -e ${module_snapshot} ]]; then
          echo "ERROR, ${module_snapshot} not found for resetting environment"
          exit 1
        fi
        # Unloading modules on Blueback always throws an error:
        # environment: line 0: unalias: mpirun: not found
        set +e
        echo "Please ignore warning 'environment: line 0: unalias: mpirun: not found' ..."
        module purge
        module restore -f ${module_snapshot}
        set -e
        umask 0022
        set +e
        case ${compiler} in
          oneapi@=2024.2.1)
            module purge
            module load PrgEnv-intel/8.5.0
            module unload intel
            module load intel-oneapi/2024.2
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.20.1
            module unload cray-libsci
            module load cray-libsci/24.07.0
            ;;
          oneapi@=2025.0.4)
            module purge
            module load PrgEnv-intel/8.5.0
            module unload intel
            module load intel-oneapi/2025.0
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.20.1
            module unload cray-libsci
            module load cray-libsci/24.07.0
            ;;
          gcc@=13.3.0)
            module purge
            module load PrgEnv-gnu/8.5.0
            module unload gcc
            # Confusing: the module is called gcc-native/13.2,
            # but the actual version of the compiler is 13.3
            module load gcc-native/13.2
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.20.1
            module unload cray-libsci
            module load cray-libsci/24.07.0
            ;;
          *)
            echo "ERROR, compiler ${compiler} not configured for resetting environment"
            exit 1
            ;;
        esac
        set -e
        ;;
      cole)
        # Check if snapshot to restore default environment exists, then restore
        if [[ ! -e ${module_snapshot} ]]; then
          echo "ERROR, ${module_snapshot} not found for resetting environment"
          exit 1
        fi
        # Unloading modules on Cole always throws an error:
        # environment: line 0: unalias: mpirun: not found
        set +e
        echo "Please ignore warning 'environment: line 0: unalias: mpirun: not found' ..."
        module purge
        module restore -f ${module_snapshot}
        set -e
        umask 0022
        set +e
        case ${compiler} in
          oneapi@=2024.2.1)
            module purge
            module use /p/work1/heinzell/spack-stack/oneapi-2024.2.1/modulefiles
            module load PrgEnv-intel/8.5.0
            module unload intel
            module load intel/2024.2.1
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.20.1
            module unload cray-libsci
            module load cray-libsci/24.03.0
            ;;
          gcc@=12.3.0)
            module purge
            module load PrgEnv-gnu/8.5.0
            module unload gcc
            module load gcc-native/12.3
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.20.1
            module unload cray-libsci
            module load cray-libsci/24.03.0
            ;;
          *)
            echo "ERROR, compiler ${compiler} not configured for resetting environment"
            exit 1
            ;;
        esac
        set -e
        ;;
      narwhal)
        # Check if snapshot to restore default environment exists, then restore
        if [[ ! -e ${module_snapshot} ]]; then
          echo "ERROR, ${module_snapshot} not found for resetting environment"
          exit 1
        fi
        # Unloading modules on Narwhal always throws an error:
        # environment: line 0: unalias: mpirun: not found
        set +e
        echo "Please ignore warning 'environment: line 0: unalias: mpirun: not found' ..."
        module purge
        module restore -f ${module_snapshot}
        set -e
        umask 0022
        set +e
        case ${compiler} in
          oneapi@=2024.2.0)
            module purge
            module load PrgEnv-intel/8.4.0
            module unload intel
            module load intel/2024.2
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.12.1.2.2.1
            module unload cray-libsci
            module load cray-libsci/23.05.1.4
            ;;
          intel@=2021.10.0)
            module purge
            module load PrgEnv-intel/8.4.0
            module unload intel
            module load intel-classic/2023.2.0
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.12.1.2.2.1
            module unload cray-libsci
            module load cray-libsci/23.05.1.4
            ;;
          gcc@=12.2.0)
            module purge
            module load PrgEnv-gnu/8.4.0
            module unload gcc
            module load gcc/12.2.0
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.12.1.2.2.1
            module unload cray-libsci
            module load cray-libsci/23.05.1.4
            ;;
          *)
            echo "ERROR, compiler ${compiler} not configured for resetting environment"
            exit 1
            ;;
        esac
        set -e
        ;;
      nautilus)
        umask 0022
        module purge
        ;;
      tusk)
        # Check if snapshot to restore default environment exists, then restore
        if [[ ! -e ${module_snapshot} ]]; then
          echo "ERROR, ${module_snapshot} not found for resetting environment"
          exit 1
        fi
        # Unloading modules on Tusk always throws an error:
        # environment: line 0: unalias: mpirun: not found
        set +e
        echo "Please ignore warning 'environment: line 0: unalias: mpirun: not found' ..."
        module purge
        module restore -f ${module_snapshot}
        set -e
        umask 0022
        set +e
        case ${compiler} in
          oneapi@=2024.2.0)
            module purge
            module load PrgEnv-intel/8.4.0
            module unload intel
            module load intel/2024.2
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.12.1.2.2.1
            module unload cray-libsci
            module load cray-libsci/23.05.1.4
            ;;
          gcc@=12.1.0)
            module purge
            module load PrgEnv-gnu/8.4.0
            module unload gcc
            module load gcc/12.1.0
            module unload cray-mpich
            module unload craype-network-ofi
            module load libfabric/1.12.1.2.2.1
            module unload cray-libsci
            module load cray-libsci/23.05.1.4
            ;;
          *)
            echo "ERROR, compiler ${compiler} not configured for resetting environment"
            exit 1
            ;;
        esac
        set -e
        ;;
      blackpearl)
        ulimit -s unlimited
        ;;
      bounty)
        ulimit -s unlimited
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
    spack clean -a

    if [[ ! ${env_exists} == "true" ]]; then
      spack stack create env --name=${env_name} \
                             --site=${host} \
                             --compiler=${compiler_name}@=${compiler_version} \
                             --template=${template} \
                             --dir=${environment_dirs} \
                             2>&1 | tee log.create.${env_name}.001
    fi
    spack env activate -p ${env_dir}

    # Workaround for building cylc environment on Narwhal: We need to use GNU
    # compilers without the Cray wrappers. Until we can come up with a smarter
    # solution, use this.
    if [[ ${host} == "narwhal" && ${template} == "cylc-dev" ]]; then
      echo "Applying workaround for ${template} on ${host}"
      cp -av configs/sites/tier1/narwhal/compilers.gcc-direct.tmp ${env_dir}/site/compilers.yaml
    elif [[ ${host} == "blueback" && ${template} == "cylc-dev" ]]; then
      echo "Applying workaround for ${template} on ${host}"
      cp -av configs/sites/tier1/blueback/compilers.gcc-direct.tmp ${env_dir}/site/compilers.yaml
    fi

    # Update bootstrap mirror if requested
    if [[ "${update_bootstrap_mirror}" == "true"*  ]]; then
      tmp_bootstrap_mirror_path=${PWD}/tmp-bootstrap-mirror-${env_name}
      echo "Creating bootstrap mirror ${tmp_bootstrap_mirror_path} ..."
      rm -fr ${tmp_bootstrap_mirror_path}
      if [[ -d ${tmp_bootstrap_mirror_path} ]]; then
        echo "ERROR, directory ${tmp_bootstrap_mirror_path} already exists"
        exit 1
      fi
      spack bootstrap mirror --binary-packages ${tmp_bootstrap_mirror_path} 2>&1 | tee log.bootstrap-mirror.${env_name}.001
      rsync -a ${tmp_bootstrap_mirror_path}/ ${bootstrap_mirror_path}/
      rm -fr ${tmp_bootstrap_mirror_path}
      # Update buildcache index
      spack buildcache update-index ${bootstrap_mirror_path}/bootstrap_cache
    fi

    echo "Registering bootstrap mirror ${bootstrap_mirror_path} ..."
    if [[ ! -d ${bootstrap_mirror_path} ]]; then
      echo "ERROR, directory ${bootstrap_mirror_path} not found"
      exit 1
    fi
    spack bootstrap add --trust local-sources ${bootstrap_mirror_path}/metadata/sources || true
    spack bootstrap add --trust local-binaries ${bootstrap_mirror_path}/metadata/binaries || true

    # Check that the site has mirrors configured for local source and build caches,
    # and extract the local path on disk. Need to strip leading "file://" from path
    result=$(spack mirror list | grep local-source) || \
        (echo "ERROR, no local source cache configured" && exit 1)
    source_mirror_path=$(echo ${result} | cut -d " " -f 3)
    source_mirror_path=${source_mirror_path:7}
    echo "Spack source mirror path: ${source_mirror_path}"
    # For build caches, additional logic is needed. If buildcache_dir is defined,
    # update the location of the default build cache to this directory.
    result=$(spack mirror list | grep local-binary) || \
        (echo "ERROR, no local binary cache configured" && exit 1)
    binary_mirror_path=$(echo ${result} | cut -d " " -f 3)
    binary_mirror_path=${binary_mirror_path:7}
    # If buildcache_dir is set, update binary_mirror_path
    if [[ ! -z ${buildcache_dir} ]]; then
      sed -i "s#${binary_mirror_path}#${buildcache_dir}#g" ${env_dir}/site/mirrors.yaml
      result=$(spack mirror list | grep local-binary)
      binary_mirror_path=$(echo ${result} | cut -d " " -f 3)
      binary_mirror_path=${binary_mirror_path:7}
    fi
    echo "Spack binary mirror path: ${binary_mirror_path}"

    if [[ "${update_build_cache}" == "true" ]]; then
      spack config add config:install_tree:padded_length:200
    fi

    # Bootstrap spack explicitly
    echo "Bootstrapping spack ..."
    spack bootstrap now 2>&1 | tee log.bootstrap.${env_name}.001

    # Concretize environment, and check that spack.lock is created
    spack concretize --force --fresh 2>&1 | tee log.concretize.${env_name}.001
    if [[ ! -e ${env_dir}/spack.lock ]]; then
      echo "ERROR during concretization of environment ${env_name}, spack.lock not found"
      exit 1
    fi

    # Check for duplicate packages
    ./util/show_duplicate_packages.py -i crtm -i crtm-fix -i esmf -i mapl

    # Update local source cache if requested
    if [[ "${update_source_cache}" == "true"* ]]; then
      echo "Updating local source cache ..."
      spack mirror create -a -d ${source_mirror_path}
    fi

    # Update local cargo mirror if requested
    if [[ "${update_cargo_mirror}" == "true"* ]]; then
      echo "Updating local cargo mirror ..."
      ./util/fetch_cargo_deps.py
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
    spack install --verbose ${buildcache_install_flags} 2>&1 | tee log.install.${env_name}.001

    # Run another spack install without redirects to catch build errors
    spack install

    # In build mode, update local binary cache
    if [[ "${update_build_cache}" == "true" ]]; then
      spack buildcache push -u ${binary_mirror_path}
      spack buildcache update-index local-binary
    fi

    # In install mode, create environment modules
    if [[ "${update_build_cache}" == "false" ]]; then
      spack module ${module_choice} refresh --yes --upstream-modules 2>&1 | tee log.modules.${env_name}.001
      spack stack setup-meta-modules 2>&1 | tee log.setup-meta-modules.${env_name}.001
    fi

    # In install mode, run post-install scripts if applicable
    if [[ "${update_build_cache}" == "false" ]]; then
      case ${host} in
        atlantis)
          ;;
        blueback)
          ;;
        cole)
          ;;
        narwhal)
          ;;
        nautilus)
          ;;
        tusk)
          ;;
        blackpearl)
          ;;
        bounty)
          ;;
        *)
          echo "ERROR, post-install scripts not configured for ${host}"
          exit 1
          ;;
      esac
    fi

    # When creating or updating buildcaches, fix permissions for mirrors.
    # Mirrors do not contain executables, therefore skip looking for them.
    if [[ "${update_bootstrap_mirror}" == "true" ]]; then
      fix_permissions ${host} ${bootstrap_mirror_path} 0
    fi
    if [[ "${update_source_cache}" == "true" ]]; then
      fix_permissions ${host} ${source_mirror_path} 0
    fi
    if [[ "${update_build_cache}" == "true" ]]; then
      fix_permissions ${host} ${binary_mirror_path} 0
    fi
    if [[ "${update_cargo_mirror}" == "true" ]]; then
      fix_permissions ${host} ${cargo_mirror_path} 0
    fi

    # Clean up
    spack clean -a
    spack env deactivate

  done

done

# Remove module snapshots for Cray systems
case ${host} in
  atlantis)
    ;;
  blueback)
    rm -vf ${module_snapshot}
    ;;
  cole)
    rm -vf ${module_snapshot}
    ;;
  narwhal)
    rm -vf ${module_snapshot}
    ;;
  nautilus)
    ;;
  tusk)
    rm -vf ${module_snapshot}
    ;;
  blackpearl)
    ;;
  bounty)
    ;;
esac

# Repair permissions for environments if in installer mode
if [[ "${update_build_cache}" == "false" ]]; then
  # Also search for exectuables
  fix_permissions ${host} ${environment_dirs} 1
fi

echo "SUCCESS"
echo

exit 0
