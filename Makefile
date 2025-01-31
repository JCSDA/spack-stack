
MAKEFILE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

# BUILD_DIR defines the location of the spack environments
# when building packages and creating buildcaches. The default
# location is subdirectory envs/build in the directory of this
# Makefile, and each environment underneath has a unique name:
#   PREFIX-COMPILER-COMPILER-VERSION
#   ne-oneapi-2024.2.1-build # neptune env, oneapi@2024.1.1
#   ce-gcc-13.3.1-build      # cylc env, gcc@13.3.1
#
# INSTALL_DIR defines the location of the spack environment
# for deployments. The default location is subdirectory
# envs/install in the direcotry of this Makefile, and
# each environment underneath has a unique name:
#   PREFIX-COMPILER-COMPILER-VERSION
#   ne-oneapi-2024.2.1 # neptune env, oneapi@2024.1.1
#   ce-gcc-13.3.1      # cylc env, gcc@13.3.1
#
# BUILDCACHE_DIR defines the location of the build (binary)
# cache created during the 'build' step. This directory should
# remain the same for all versions of spack-stack, for example:
#     /home/fnmoc/spack-stack/build-cache
# Identical versions of packages are shared and reused, and each
# package (version, build options, dependencies) is uniquely
# identified by a Merkel hash. The default location is subdirectory
# build-cache in the directory of this Makefile, i.e. not shared
# between deployments of spack-stack.

BUILD_DIR      ?= $(MAKEFILE_DIR)/envs/build
INSTALL_DIR    ?= $(MAKEFILE_DIR)/envs/install
BUILDCACHE_DIR ?= $(MAKEFILE_DIR)/build-cache

default_target : build

# The 'build' target
build:
	@echo "Building spack-stack in $(BUILD_DIR) ..."
	mkdir -p $(BUILD_DIR)
	time ./util/nrl/batch_install.sh \
	    -b $(BUILD_DIR) \
	    -c $(BUILDCACHE_DIR) \
	    -r ops
	touch $(BUILD_DIR)/complete.flag
	@echo "Build complete."

# The 'install' target
install:
	@echo "Installing spack-stack in $(INSTALL_DIR) ..."
	mkdir -p $(INSTALL_DIR)
	time ./util/nrl/batch_install.sh \
	    -i $(INSTALL_DIR) \
	    -c $(BUILDCACHE_DIR) \
	    -r ops
	touch $(INSTALL_DIR)/complete.flag
	@echo "Installation complete."

# The 'clean' target
clean:
	@echo "Cleaning spack-stack build environments in $(BUILD_DIR) ..."
	rm -fr $(BUILD_DIR)/*

.PHONY: build install clean
