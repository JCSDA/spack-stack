#!/usr/bin/env bash

set -e

##################################################################################################
# Options                                                                                        #
##################################################################################################

usage() {
  set +x
  echo
  echo "Usage: $0 -b <BUILD_DIR> | -i <INSTALL_DIR> | -r <role> | -c <BUILDCACHE_DIR>"
  echo
  echo "  -b  Build environments in BUILD_DIR and update build caches"
  echo "  -i  Install environments in INSTALL_DIR using build caches"
  echo "  -r  Set role, can be 'ops' or 'dev'"
  echo "  -c  Provide location of build caches as BUILDCACHE_DIR"
  echo "      Must be set if and only if role is 'ops'"
  echo "  -h  display this help"
  echo
}

while getopts b:c:i:r:h flag
do
  case "${flag}" in
    b)
      SPACK_STACK_MODE="build"
      SPACK_STACK_ENVIRONMENT_DIRS=${OPTARG}
      ;;
    c)
      SPACK_STACK_BUILDCACHE_DIR=${OPTARG}
      ;;
    i)
      SPACK_STACK_MODE="install"
      SPACK_STACK_ENVIRONMENT_DIRS=${OPTARG}
      ;;
    r)
      SPACK_STACK_ROLE=${OPTARG}
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
echo "  SPACK_STACK_ENVIRONMENT_DIRS:                ${SPACK_STACK_ENVIRONMENT_DIRS:-not set}"
echo "  SPACK_STACK_BUILDCACHE_DIR:                  ${SPACK_STACK_BUILDCACHE_DIR:-not set}"

if [[ ${SPACK_STACK_ROLE} == "ops" ]]; then
  if [[ -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
    echo "ERROR, SPACK_STACK_BUILDCACHE_DIR not defined. Provide -c BUILDCACHE_DIR as argument when role is 'ops'."
    exit 1
  fi
elif [[ ${SPACK_STACK_ROLE} == "dev" ]]; then
  if [[ ! -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
    echo "ERROR, SPACK_STACK_BUILDCACHE_DIR must not be set if role is 'dev'."
    exit 1
  fi
else
  echo "ERROR, invalid role '${SPACK_STACK_ROLE}'"
  exit 1
fi

if [[ ${SPACK_STACK_MODE} == "build" ]]; then
  if [[ -z ${SPACK_STACK_ENVIRONMENT_DIRS} ]]; then
    echo "ERROR, SPACK_STACK_ENVIRONMENT_DIRS not defined. Provide -b BUILD_DIR as argument."
    exit 1
  fi
elif [[ ${SPACK_STACK_MODE} == "install" ]]; then
  if [[ -z ${SPACK_STACK_ENVIRONMENT_DIRS} ]]; then
    echo "ERROR, SPACK_STACK_ENVIRONMENT_DIRS not defined. Provide -i INSTALL_DIR as argument."
    exit 1
  fi
else
  echo "ERROR, invalid mode '${SPACK_STACK_MODE}'"
  exit 1
fi

##################################################################################################

# Remove domain name suffices and digits to determine hostname
SPACK_STACK_BATCH_HOST=$(echo ${HOSTNAME} | cut -d "." -f 1)
SPACK_STACK_BATCH_HOST=${SPACK_STACK_BATCH_HOST//[0-9]/}

case ${SPACK_STACK_BATCH_HOST} in
  atlantis)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "intel@2021.6.0" "gcc@11.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    SPACK_STACK_BOOTSTRAP_MIRROR="/neptune_diagnostics/spack-stack/bootstrap-mirror"
    ;;
  cole)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "gcc@12.3.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/work1/heinzell/spack-stack/bootstrap-mirror"
    ;;
  narwhal)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.0" "intel@2021.10.0" "gcc@10.3.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/bootstrap-mirror"
    ;;
  nautilus)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "intel@2021.5.0" "gcc@11.2.1")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/cwfs/projects/NEPTUNE/spack-stack/bootstrap-mirror"
    ;;
  tusk)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.0" "gcc@12.1.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/p/work1/heinzell/spack-stack/bootstrap-mirror"
    ;;
  blackpearl)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "gcc@13.3.0" "aocc@4.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/home/dom/prod/spack-bootstrap-mirror"
    ;;
  bounty)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2025.0.0" "gcc@13.3.1" "aocc@5.0.0" "clang@19.1.4")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    SPACK_STACK_BOOTSTRAP_MIRROR="/home/dom/prod/spack-bootstrap-mirror"
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

if [[ -z ${SPACK_STACK_ENVIRONMENT_DIRS} ]]; then
  environment_dirs=${PWD}/envs
else
  environment_dirs=${SPACK_STACK_ENVIRONMENT_DIRS}
fi
mkdir -p ${environment_dirs}

if [[ ! -z ${SPACK_STACK_BUILDCACHE_DIR} ]]; then
  buildcache_dir=${SPACK_STACK_BUILDCACHE_DIR}
  mkdir -p ${buildcache_dir}
fi

if [[ "${SPACK_STACK_MODE}" == "install" ]]; then
  update_bootstrap_mirror="false"
  update_source_cache="false"
  update_build_cache="false"
  reuse_build_cache="true"
elif [[ "${SPACK_STACK_MODE}" == "build" ]]; then
  if [[ "${SPACK_STACK_ROLE}" == "ops" ]]; then
    update_bootstrap_mirror="false"
    update_source_cache="false"
  elif [[ "${SPACK_STACK_ROLE}" == "dev" ]]; then
    update_bootstrap_mirror="true"
    update_source_cache="true"
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

# For Cray systems, capture the default=current environment (loaded modules)
# so that it can be restored between building stacks for different compilers
case ${host} in
  atlantis)
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

  compiler_name=$(echo ${compiler} | cut -d "@" -f 1)
  compiler_version=$(echo ${compiler} | cut -d "@" -f 2)

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
      echo "ERROR, environment ${env_dir} already exists"
      exit 1
    fi

    # Reset environment
    echo "Resetting environment ..."
    case ${host} in
      atlantis)
        umask 0022
        module purge
        ;;
      cole)
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
          oneapi@2024.2.1)
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
          gcc@12.3.0)
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
          oneapi@2024.2.0)
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
          intel@2021.10.0)
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
          gcc@10.3.0)
            module purge
            module load PrgEnv-gnu/8.4.0
            module unload gcc
            module load gcc/10.3.0
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
          oneapi@2024.2.0)
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
          gcc@12.1.0)
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

    spack stack create env --name=${env_name} \
                           --site=${host} \
                           --compiler=${compiler_name} \
                           --template=${template} \
                           --dir=${environment_dirs} \
                           2>&1 | tee log.create.${env_name}.001
    spack env activate -p ${env_dir}

    # Workaround for building cylc environment on Narwhal: We need to use GNU
    # compilers without the Cray wrappers. Until we can come up with a smarter
    # solution, use this.
    if [[ ${host} == "narwhal" && ${template} == "cylc-dev" ]]; then
      echo "Applying workaround for ${template} on ${host}"
      cp -av configs/sites/tier1/narwhal/compilers.gcc-direct.tmp ${env_dir}/site/compilers.yaml
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
      rsync -av ${tmp_bootstrap_mirror_path}/ ${bootstrap_mirror_path}/
      rm -fr ${tmp_bootstrap_mirror_path}
      # Update buildcache index
      spack buildcache update-index ${bootstrap_mirror_path}/bootstrap_cache
    fi

    echo "Registering bootstrap mirror ${bootstrap_mirror_path} ..."
    if [[ ! -d ${bootstrap_mirror_path} ]]; then
      echo "ERROR, directory ${bootstrap_mirror_path} not found"
      exit 1
    fi
    spack bootstrap add --trust local-sources ${bootstrap_mirror_path}/metadata/sources
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
    spack concretize --force --fresh 2>&1 | tee log.concretize.${env_name}.001
    if [[ ! -e ${env_dir}/spack.lock ]]; then
      echo "ERROR during concretization of environment ${env_name}, spack.lock not found"
      exit 1
    fi

    # Check for duplicate packages
    ./util/show_duplicate_packages.py -i crtm -i esmf -d log.concretize.${env_name}.001

    # Update local source cache if requested
    if [[ "${update_source_cache}" == "true"* ]]; then
      echo "Updating local source cache ..."
      spack mirror create -a -d ${source_mirror_path}
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
      # On Narwhal, fix bad links to libsci
      case ${host} in
        atlantis)
          ;;
        cole)
          ;;
        narwhal)
          ./util/narwhal/fix_libsci.sh 2>&1 | tee log.fix_libsci.${env_name}.001
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
    
    # Clean up
    spack clean -a
    spack env deactivate

  done

done

# Remove any module snapshots
rm -vf ${module_snapshot}

# Repair permissions for environments if in installer mode
if [[ "${update_build_cache}" == "false" ]]; then
  # Also search for exectuables
  fix_permissions ${host} ${PWD} 1
fi

echo "SUCCESS"
echo

exit 0
