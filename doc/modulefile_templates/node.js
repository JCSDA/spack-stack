#%Module1.0

module-whatis "Provides an node.js-20.10.0 installation for use with spack."

# Only allow one instance of compiler to load
conflict ecflow

proc ModulesHelp { } {
puts stderr "Provides an node.js-20.10.0 installation for use with spack."
}

if { [ module-info mode load ] && ![ is-loaded gcc/10.3.0 ] } {
    module load gcc/10.3.0
}

# Set this value
set NODEJS_PATH "/p/app/projects/NEPTUNE/spack-stack/node-js-20.10.0/gcc-10.3.0"

prepend-path PATH "${NODEJS_PATH}/bin"
prepend-path LD_LIBRARY_PATH "${NODEJS_PATH}/lib"
prepend-path LIBRARY_PATH "${NODEJS_PATH}/lib"
prepend-path CPATH "${NODEJS_PATH}/include"
prepend-path CMAKE_PREFIX_PATH "${NODEJS_PATH}"
