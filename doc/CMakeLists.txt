cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(spack-stack VERSION 1.9.0)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules/Modules")

find_package(Sphinx REQUIRED)

# configured documentation tools and intermediate build results
set(BINARY_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/_build")
 
# Sphinx cache with pickled ReST documents
set(SPHINX_CACHE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_doctrees")
 
# HTML output directory
set(SPHINX_HTML_DIR "${CMAKE_CURRENT_BINARY_DIR}/html")
 
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/source/conf.py"
    "${BINARY_BUILD_DIR}/conf.py"
    @ONLY)

add_custom_target(spack-stack-doc-html ALL
    ${SPHINX_EXECUTABLE}
        -q -b html
        -c "${BINARY_BUILD_DIR}"
        -d "${SPHINX_CACHE_DIR}"
        "${CMAKE_CURRENT_SOURCE_DIR}/source"
        "${SPHINX_HTML_DIR}"
    COMMENT "Building HTML documentation with Sphinx")
