#!/usr/bin/env bash

set -e

# Developer switch: create buildcaches instead of deploying environments ["true"|"false"]
# The default "false" means to deploy environments using existing buildcaches (installer mode)
SPACK_STACK_BATCH_CREATE_BUILDCACHE="false"
#SPACK_STACK_BATCH_CREATE_BUILDCACHE="true"

# A value of SPACK_STACK_BATCH_CREATE_BUILDCACHE == "true" enters developer mode. In this
# mode, one must choose between reusing existing buildcaches or rebuilding from scratch.
# This variable is meaningless in installer mode (SPACK_STACK_BATCH_CREATE_BUILDCACHE== "false")
SPACK_STACK_BATCH_REUSE_EXISTING_BUILDCACHE="true"
#SPACK_STACK_BATCH_REUSE_EXISTING_BUILDCACHE="false"

# Remove domain name suffices and digits to determine hostname
SPACK_STACK_BATCH_HOST=$(echo ${HOSTNAME} | cut -d "." -f 1)
SPACK_STACK_BATCH_HOST=${SPACK_STACK_BATCH_HOST//[0-9]/}

case ${SPACK_STACK_BATCH_HOST} in
  atlantis)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "intel@2021.6.0" "gcc@11.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="lmod"
    ;;
  narwhal)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.0" "intel@2021.10.0" "gcc@10.3.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    ;;
  nautilus)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "intel@2021.5.0" "gcc@11.2.1")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    ;;
  # DH*
  blackpearl)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2024.2.1" "gcc@13.3.0" "aocc@4.2.0")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    ;;
  bounty)
    SPACK_STACK_BATCH_COMPILERS=("oneapi@2025.0.0" "gcc@13.3.1" "aocc@5.0.0" "clang@19.1.4")
    SPACK_STACK_BATCH_TEMPLATES=("neptune-dev" "unified-dev" "cylc-dev")
    SPACK_STACK_MODULE_CHOICE="tcl"
    ;;
  # *DH
  *)
    echo "ERROR, host ${SPACK_STACK_BATCH_HOST} not configured"
    exit 1
    ;;
esac

##################################################################################################

echo "\n"
echo "Welcome to NRL SPACK-STACK BATCH INSTALL"
echo

if [[ ! -e "setup.sh" || ! -e ".spackstack" ]]; then
  echo "ERROR, this script must be executed from the top-level spack-stack directory"
  exit 1
fi

host=${SPACK_STACK_BATCH_HOST}
module_choice=${SPACK_STACK_MODULE_CHOICE}

# For Cray systems, capture the default=current environment (loaded modules)
# so that it can be restored between building stacks for different compilers
case ${host} in
  narwhal)
    module_snapshot=${PWD}/spack-stack.default-modules
    module snapshot -f ${module_snapshot}
    ;;
esac

# Create buildcaches or install environment?
case ${SPACK_STACK_BATCH_CREATE_BUILDCACHE} in
  "true")
    case ${SPACK_STACK_BATCH_REUSE_EXISTING_BUILDCACHE} in
      "false")
        echo "Developer mode: create buildcaches, and ignore existing buildcaches"
        create_buildcache="true-ignore"
        ;;
      "true")
        echo "Developer mode: create buildcaches, but reuse existing buildcaches"
        create_buildcache="true-reuse"
        ;;
      *)
      echo "ERROR, invalid value for SPACK_STACK_BATCH_REUSE_EXISTING_BUILDCACHE"
      exit 1
      ;;
    esac
    ;;
  "false")
    echo "Installer mode: deploy environments using existing buildcaches"
    create_buildcache="false"
    ;;
  *)
    echo "ERROR, invalid value for SPACK_STACK_BATCH_CREATE_BUILDCACHE"
    exit 1
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
    [[ "${create_buildcache}" == "true"* ]] && env_name=${env_name}-buildcache
    env_dir=${PWD}/envs/${env_name}

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
      # DH*
      blackpearl)
        ulimit -s unlimited
        ;;
      bounty)
        ulimit -s unlimited
        ;;
      # *DH
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
                           2>&1 | tee log.create.${env_name}.001
    spack env activate -p ${env_dir}

    # Workaround for building cylc environment on Narwhal: We need to use GNU
    # compilers without the Cray wrappers. Until we can come up with a smarter
    # solution, use this.
    if [[ ${host} == "narwhal" && ${template} == "cylc-dev" ]]; then
      echo "Applying workaround for ${template} on ${host}"
      cp -av configs/sites/tier1/narwhal/compilers.gcc-direct.tmp ${env_dir}/site/compilers.yaml
    fi

    # Check that the site has mirrors configured for local source and binary caches,
    # and extract the local path on disk. Need to strip leading "file://" from path
    result=$(spack mirror list | grep local-source) || \
        (echo "ERROR, no local source cache configured" && exit 1)
    source_mirror_path=$(echo ${result} | cut -d " " -f 3)
    source_mirror_path=${source_mirror_path:7}
    echo "Spack source mirror path: ${source_mirror_path}"
    result=$(spack mirror list | grep local-binary) || \
        (echo "ERROR, no local binary cache configured" && exit 1)
    binary_mirror_path=$(echo ${result} | cut -d " " -f 3)
    binary_mirror_path=${binary_mirror_path:7}
    echo "Spack binary mirror path: ${binary_mirror_path}"

    if [[ "${create_buildcache}" == "true"* ]]; then
      spack config add config:install_tree:padded_length:200
    fi

    # Concretize environment, and check that spack.lock is created
    spack concretize --force --fresh 2>&1 | tee log.concretize.${env_name}.001
    if [[ ! -e ${env_dir}/spack.lock ]]; then
      echo "ERROR during concretization of environment ${env_name}, spack.lock not found"
      exit 1
    fi

    # Check for duplicate packages
    ./util/show_duplicate_packages.py -i crtm -i esmf -d log.concretize.${env_name}.001

    # In developer mode, update local source cache
    if [[ "${create_buildcache}" == "true"* ]]; then
      echo "Updating local source cache ..."
      spack mirror create -a -d ${source_mirror_path}
    fi

    # Update the buildcache index if it already contains packages
    if [[ -e ${binary_mirror_path}/build_cache ]]; then
      spack buildcache update-index local-binary
    fi

    # Install the environment with the correct flags
    case ${create_buildcache} in
      "false")
        buildcache_install_flags="--no-check-signature"
        ;;
      "true-reuse")
        buildcache_install_flags="--no-check-signature"
        ;;
      "true-ignore")
        buildcache_install_flags="--no-cache"
        ;;
      *)
        echo "ERROR, unkown create_buildcache value ${create_buildcache} for setting install flags"
        exit 1
        ;;
    esac
    spack install --verbose ${buildcache_install_flags} 2>&1 | tee log.install.${env_name}.001

    # Run another spack install without redirects to catch build errors
    spack install

    # In developer mode, update local binary cache
    if [[ "${create_buildcache}" == "true"* ]]; then
      spack buildcache push -u ${binary_mirror_path}
      spack buildcache update-index local-binary
    fi

    # In installer mode, create environment modules
    if [[ "${create_buildcache}" == "false" ]]; then
      spack module ${module_choice} refresh --yes --upstream-modules 2>&1 | tee log.modules.${env_name}.001
      spack stack setup-meta-modules 2>&1 | tee log.setup-meta-modules.${env_name}.001
    fi
    
    # In installer mode, run post-install scripts if applicable
    if [[ "${create_buildcache}" == "false" ]]; then
      # On Narwhal, fix bad links to libsci
      case ${host} in
        atlantis)
          ;;
        narwhal)
          ./util/narwhal/fix_libsci.sh 2>&1 | tee log.fix_libsci.${env_name}.001
          ;;
        nautilus)
          ;;
        # DH*
        blackpearl)
          ;;
        bounty)
          ;;
        # *DH
        *)
          echo "ERROR, post-install scripts not configured for ${host}"
          exit 1
          ;;
      esac
    fi

    # Clean up
    spack clean -a
    spack env deactivate

  done

done

# Remove any module snapshots
rm -vf ${module_snapshot}

# Note. Add in the xargs stuff
# Repair permissions for environments
case ${host} in
  atlantis)
    find ./ -type d -print0 | xargs --null chmod a+rx
    find ./ -type f -executable -print0 | xargs --null chmod a+rx
    find ./ -type f -print0 | xargs --null chmod a+r
    ;;
  narwhal)
    nice -n 19 lfs find ./ -type d -print0 | xargs --null chmod a+rx
    nice -n 19 find ./ -type f -executable -print0 | xargs --null chmod a+rx
    nice -n 19 lfs find ./ -type f -print0 | xargs --null chmod a+r
    ;;
  nautilus)
    nice -n 19 lfs find ./ -type d -print0 | xargs --null chmod a+rx
    nice -n 19 find ./ -type f -executable -print0 | xargs --null chmod a+rx
    nice -n 19 lfs find ./ -type f -print0 | xargs --null chmod a+r
    ;;
  # DH*
  blackpearl)
    ;;
  bounty)
    ;;
  # *DH
  *)
    echo "ERROR, xargs-chmod command not configured for ${host}"
    exit 1
    ;;
esac

echo "NRL SPACK-STACK BATCH INSTALL SUCCESSFUL"

exit 0
