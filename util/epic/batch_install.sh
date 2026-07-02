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
    
usage() {
  set +x
  echo
  echo "Usage: $0 -m <MODE> [-d <ENV_DIRS>] [-c <BUILDCACHE_DIR>]"
  echo
  echo "  -m  Set mode, can be 'build' or 'install';"
  echo "      build: build environments and update build caches;"
  echo "      install: install environments using build caches (do not update build caches)"
  echo "  -d  Build or install environments in ENV_DIRS;"
  echo "      if not set, the default location is used"
  echo "  -c  Provide location of build caches as BUILDCACHE_DIR;"
  echo "      if not set, authoritative build caches are used"
  echo "  -u  Flag to update bootstrap and source caches;"
  echo "  -e  Continue builds/install in existing environments;"
  echo "      by default, exit with an error if already exist"
  echo "  -s  Submit 'spack install' to batch scheduler"
  echo "  -t  Run tests for specific thirdparty dependencies;"
  echo "      these are currently hardcoded in batch_install.sh"
  echo "  -h  display this help"
  echo
}

while getopts r:m:d:c:uesth flag
do
  case "${flag}" in
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
echo "  SPACK_STACK_MODE:                            ${SPACK_STACK_MODE:-not set}"
echo "  SPACK_STACK_ENVIRONMENT_DIRS:                ${SPACK_STACK_ENVIRONMENT_DIRS:-${SPACK_STACK_DIR}/envs}"
echo "  SPACK_STACK_BUILDCACHE_DIR:                  ${SPACK_STACK_BUILDCACHE_DIR:-use default caches}"
echo "  SPACK_STACK_UPDATE_DEV_CACHES:               ${SPACK_STACK_UPDATE_DEV_CACHES:-false}"
echo "  SPACK_STACK_IGNORE_ENV_EXIST:                ${SPACK_STACK_IGNORE_ENV_EXIST:-false}"
echo "  SPACK_STACK_SUBMIT_TO_SCHEDULER:             ${SPACK_STACK_SUBMIT_TO_SCHEDULER:-false}"
echo "  SPACK_STACK_RUN_TESTS:                       ${SPACK_STACK_RUN_TESTS:-false}"

if [[ -z ${SPACK_STACK_MODE} ]]; then
  echo "ERROR, SPACK_STACK_MODE not defined. Provide -m MODE as argument"
  exit 1
elif [[ ! ${SPACK_STACK_MODE} == "build" && ! ${SPACK_STACK_MODE} == "install" ]]; then
  echo "ERROR, invalid mode '${SPACK_STACK_MODE}'"
  exit 1
fi

# Updating bootstrap and source caches requires role dev and mode build
if [[ ${SPACK_STACK_UPDATE_DEV_CACHES} == "true" ]]; then
  if [[ ! ${SPACK_STACK_MODE} == "build" ]]; then
    echo "ERROR, SPACK_STACK_UPDATE_DEV_CACHES requires mode 'build'"
    exit 1
  fi
fi

##################################################################################################

# Remove domain name suffices and digits and dashes [MSU] to determine hostname
SPACK_STACK_BATCH_HOST=$(echo ${HOSTNAME} | cut -d "." -f 1 | cut -d "-" -f 1)
SPACK_STACK_BATCH_HOST=${SPACK_STACK_BATCH_HOST//[0-9]/}

case ${SPACK_STACK_BATCH_HOST} in
  derecho)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2025.3.1" "gcc@=13.3.1")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/glade/work/epicufsrt/contrib/spack-stack/derecho/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/glade/work/epicufsrt/contrib/spack-stack/derecho/cargo-mirror"
    # set TMPDIR to avoid full /tmp directory on derecho login nodes
    export TMPDIR=/glade/derecho/scratch/epicufsrt
    ;;
  gaea)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2025.2.1" "gcc@=13.3.1")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/gpfs/f6/epic/proj-shared/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/gpfs/f6/epic/proj-shared/spack-stack/cargo-mirror"
    # hostname needs to match configs/sites/tier1/<host>
    SPACK_STACK_BATCH_HOST="gaea-c6"
    ;;
  hercules)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2025.3.1" "gcc@=12.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/apps/contrib/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/apps/contrib/spack-stack/cargo-mirror"
    ;;
  orion)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2025.3.1")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/apps/contrib/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/apps/contrib/spack-stack/cargo-mirror"
    ;;
  ufe)    # ursa
    SPACK_STACK_BATCH_COMPILERS=("oneapi@=2025.3.1" "oneapi@=2025.3.1-hpcx" "gcc@=12.4.0")
    SPACK_STACK_BATCH_TEMPLATES=("unified-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/contrib/spack-stack/bootstrap-mirror"
    SPACK_STACK_CARGO_MIRROR="/contrib/spack-stack/cargo-mirror"
    # hostname needs to match configs/sites/tier1/<host>
    SPACK_STACK_BATCH_HOST="ursa"
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
    derecho)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    gaea-c6)
      # no lfs command on gaea-c6
      nice -n 19 find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    hercules)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    orion)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
      ;;
    ursa)
      nice -n 19 lfs find ${dir} -type d -print0 | xargs --null chmod a+rx
      # In case the find command returns no executables
      if [[ ${executables} -eq 1 ]]; then
        sleep 30
        nice -n 19 find ${dir} -type f -executable -print0 | xargs --null chmod a+rx
        sleep 30
      fi
      nice -n 19 lfs find ${dir} -type f -print0 | xargs --null chmod a+r
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
    derecho)
      tpn=128
      ;;
    gaea-c6)
      tpn=128
      ;;
    hercules)
      tpn=80
      ;;
    orion)
      tpn=40
      ;;
    ursa)
      # occasional failures installing 'go' at tpn=128
      tpn=64
      ;;
    *)
      echo "ERROR, tasks_per_node command not configured for ${host}"
      exit 1
      ;;
  esac
  echo "${tpn}"
}

##################################################################################################

function epic_host_parameters() {
  local -n host_array=$1
  local -n epic_host=$2

  # array values: ("account" "walltime" "tasks_per_node")
  case ${epic_host} in
    derecho)
	    host_array=("NRAL0032" "12:00:00")
      ;;
    gaea-c6)
      host_array=("epic" "720")
      ;;
    hercules)
      host_array=("epic" "720")
      ;;
    orion)
      host_array=("epic" "720")
      ;;
    ursa)
      host_array=("epic" "720")
      ;;
    *)
      echo "ERROR, host_parameters command not configured for ${host}"
      exit 1
      ;;
  esac
}

##################################################################################################

function run_interactive_job() {
  host=$1
  script=$2
  reuse_build_cache=$3

  # get interactive job parameters for host
  params=()
  epic_host_parameters params host
  if [[ ${#params[@]} -lt 2 ]] ; then
    echo "Incorrect number of host-specific configuration parameters for ${host}"
    exit 1
  fi

  account=${params[0]}
  walltime=${params[1]}
  tpn=$(tasks_per_node ${host})

  echo "Starting interactive job on ${host} for account ${account} with ${tpn} tasks and a walltime of ${walltime} minutes for ${script} ..."
  case ${host} in
    derecho)
      module load ncarenv/25.10 &>/dev/null  # required for qcmd
      qcmd -l select=1:ncpus=${tpn}:mpiprocs=${tpn} -l walltime=${walltime} -j oe -q main -A ${account} -- bash ${script}
      ;;
    gaea-c6)
      salloc --exclusive --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} --qos=normal --partition=batch --clusters=c6 --account=${account} bash ${script}
      ;;
    hercules)
      salloc --exclusive --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} --qos=long --partition=development --account=${account} bash ${script}
      ;;
    orion)
      salloc --exclusive --nodes=1 --ntasks-per-node=${tpn} --time=${walltime} --qos=long --partition=development --account=${account} bash ${script}
      ;;
    ursa)
      salloc --exclusive --nodes=1 --mem=0 --ntasks-per-node=${tpn} --time=${walltime} --qos=long --account=${account} bash ${script}
      ;;
    *)
      echo "ERROR, run_interactive_job command not configured for ${host}"
      exit 1
      ;;
  esac
}

##################################################################################################

echo
echo "Welcome to EPIC SPACK-STACK BATCH INSTALL"
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
  if [[ ${SPACK_STACK_UPDATE_DEV_CACHES} == "true" ]]; then
    update_bootstrap_mirror="true"
    update_cargo_mirror="true"
    update_source_cache="true"
    update_build_cache="true"
    reuse_build_cache="false"
  else
    update_bootstrap_mirror="false"
    update_cargo_mirror="false"
    update_source_cache="false"
    update_build_cache="false"
    reuse_build_cache="true"
  fi
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
    # cylc-dev only with gcc
    if [[ "${template}" == "cylc-dev" && ! "${compiler_name}" == "gcc" ]]; then
      echo "Skipping template ${template} with compiler ${compiler}"
      continue
    # FMS compiler ICE: https://github.com/NOAA-GFDL/FMS/issues/1680
    elif [[ "${compiler_name}" == "oneapi" && "${compiler_version}" == "2025.1"* && "${template}" == "unified-dev" ]]; then
      echo "Skipping template ${template} with compiler ${compiler}"
      continue
    fi
    echo "Processing template ${template} with compiler ${compiler}"
    echo
    #############################################################

    # Build environment name. Prefices are defined here
    case ${template} in
      unified-dev)
        env_name_prefix="ue"
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
      derecho)
        umask 0022
        module purge
        case ${compiler} in
          gcc@=13.3.1)
            ;;
          oneapi@=2025.3.1)
            module use /glade/work/epicufsrt/contrib/spack-stack/derecho/installs/oneapi-2025.3.1/modulefiles
            ;;
        esac
        ;;
      gaea-c6)
        umask 0022
        module purge
        case ${compiler} in
          gcc@=13.3.1)
            ;;
          oneapi@=2025.2.1)
            ;;
        esac
        ;;
      hercules)
        umask 0022
        module purge
        case ${compiler} in
          gcc@=12.2.0)
            ;;
          oneapi@=2025.3.1)
            module use /apps/contrib/spack-stack/modulefiles
            ;;
        esac
        ;;
      orion)
        umask 0022
        module purge
        case ${compiler} in
          # not currently supported
          #gcc@=12.2.0)
          #  ;;
          oneapi@=2025.3.1)
            module use /apps/contrib/spack-stack/modulefiles
            ;;
        esac
        ;;
      ursa)
        umask 0022
        module purge
        case ${compiler} in
          gcc@=12.4.0)
            ;;
          oneapi@=2025.3.1)
            ;;
          oneapi@=2025.3.1-hpcx)
            ;;
        esac
        ;;
      *)
        echo "ERROR, host ${host} not configured for resetting environment"
        exit 1
        ;;
    esac

    # Info prints
    ulimit -a
    module list

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
      spack bootstrap mirror --binary-packages ${tmp_bootstrap_mirror_path} 2>&1 | tee log.${env_name}.bootstrap-mirror.001
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
      spack stack create env --name=${env_name} \
                             --site=${host} \
                             --compiler=${compiler_name}-${compiler_version} \
                             --template=${template} \
                             --dir=${environment_dirs} \
                             --treat-warnings-as-errors \
                             2>&1 | tee log.${env_name}.create.001
    fi
    spack env activate -p ${env_dir}

    # Not pertinent to EPIC hosts; save as an illustrative example for EPIC ParallelWorks hosts
    # and potential Enterprise GitHub or GitLab
    # Workaround for ParallelWorks (no NRL Enterprise GitHub access yet)
    #sed -i 's/+adp/~adp/g' ${env_dir}/spack.yaml

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
    spack concretize --force --fresh 2>&1 | tee log.${env_name}.concretize.001
    if [[ ! -e ${env_dir}/spack.lock ]]; then
      echo "ERROR during concretization of environment ${env_name}, spack.lock not found"
      exit 1
    fi

    # Check for duplicate packages
    ./util/show_duplicate_packages.py -i crtm -i crtm-fix -i esmf -i mapl -i neptune-env -i py-cython -i ip -i fms

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
    cat << EOF > ${install_script}
#!/usr/bin/env bash

set -e

$(declare -p test_packages)

# If no tests are required, install everything
if [[ \${#test_packages[@]} -eq 0 ]]; then
  set -o pipefail
  spack install --verbose ${buildcache_install_flags} ${parallel_install_flags} 2>&1 | tee log.${env_name}.install.001
  set +o pipefail
else
  for (( idx=0; idx<\${#test_packages[@]}; idx++ )); do
    test_package=\${test_packages[\${idx}]}
    # First, check if this package is in this environment
    set +e
    grep -e "\${test_package}@" log.concretize.001 || continue
    set -e
    idx_padded=\$(printf "%03d" "\$((idx+1))")
    set -o pipefail
    spack install --verbose ${buildcache_install_flags} ${parallel_install_flags} --only=dependencies \${test_package} \\
      2>&1 | tee log.${env_name}.install.\${idx_padded}.\${test_package}-dependencies
    spack install --verbose --no-cache --test=root \${test_package} 2>&1 | tee log.${env_name}.install.\${idx_padded}.\${test_package}
    set +o pipefail
  done
  # idx now equals the length of the array; install the rest
  idx_padded=\$(printf "%03d" "\$((idx+1))")
  set -o pipefail
  spack install --verbose ${buildcache_install_flags} ${parallel_install_flags} 2>&1 | tee log.${env_name}.install.\${idx_padded}
  set +o pipefail
fi
EOF
    chmod u+x ${install_script}
    if [[ "${submit_to_scheduler}" == "true" ]]; then
      run_interactive_job ${host} ${install_script} ${reuse_build_cache}
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
      spack module ${module_choice} refresh --yes --upstream-modules 2>&1 | tee log.${env_name}.modules.001
      spack stack setup-meta-modules 2>&1 | tee log.${env_name}.setup-meta-modules.001
    fi

    echo ; echo -n "Copying log files to ${env_dir}..."
    mv -f log.* ${env_dir} 2> /dev/null
    echo -n "done" ; echo

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
  fix_permissions ${host} ${environment_dirs} 1
fi

echo "SUCCESS"
echo

exit 0
