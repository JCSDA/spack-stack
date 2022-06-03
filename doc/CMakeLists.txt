cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(spack-stack VERSION 0.0.1)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules/Modules")

option(SPHINX_OUTPUT_HTML "Build HTML documentation" ON)
option(SPHINX_OUTPUT_LATEX "Build LaTeX (PDF) documentation" OFF)

message(STATUS "SPHINX_OUTPUT_HTML: ${SPHINX_OUTPUT_HTML}")
message(STATUS "SPHINX_OUTPUT_LATEX: ${SPHINX_OUTPUT_LATEX}")

find_package(Sphinx REQUIRED)

# configured documentation tools and intermediate build results
set(BINARY_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/_build")
 
# Sphinx cache with pickled ReST documents
set(SPHINX_CACHE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_doctrees")
 
# HTML output directory
set(SPHINX_HTML_DIR "${CMAKE_CURRENT_BINARY_DIR}/html")

# LaTeX output directory
set(SPHINX_PDF_DIR "${CMAKE_CURRENT_BINARY_DIR}/pdf")
 
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/source/conf.py"
    "${BINARY_BUILD_DIR}/conf.py"
    @ONLY)

if(SPHINX_OUTPUT_HTML)
  add_custom_target(spack-stack-doc-html ALL
      ${SPHINX_EXECUTABLE}
          -q -b html
          -c "${BINARY_BUILD_DIR}"
          -d "${SPHINX_CACHE_DIR}"
          "${CMAKE_CURRENT_SOURCE_DIR}/source"
          "${SPHINX_HTML_DIR}"
      COMMENT "Building HTML documentation with Sphinx")
endif()

if(SPHINX_OUTPUT_LATEX)
  find_package(LATEX COMPONENTS PDFLATEX REQUIRED)
  set(PDF_OUTPUT_FILE "${SPHINX_PDF_DIR}/spack-stack.pdf")
  # Create LaTeX input file with Sphinx
  add_custom_command(OUTPUT "${SPHINX_PDF_DIR}"
      COMMAND "${SPHINX_EXECUTABLE}" -q -b latex
          -c "${BINARY_BUILD_DIR}"
          -d "${SPHINX_CACHE_DIR}"
          "${CMAKE_CURRENT_SOURCE_DIR}/source"
          "${SPHINX_PDF_DIR}"
      COMMENT "Running Sphinx to generate documentation (LaTeX)"
      VERBATIM
      )
  # Create PDF output file with pdflatex
  add_custom_command(OUTPUT "${PDF_OUTPUT_FILE}"
      COMMAND "${CMAKE_MAKE_PROGRAM}" all-pdf
      WORKING_DIRECTORY "${SPHINX_PDF_DIR}"
      DEPENDS "${SPHINX_PDF_DIR}"
      COMMENT "Generating PDF version of documentation"
      VERBATIM
      )
  #
  add_custom_target(spack-stack-doc-pdf ALL
      COMMENT "Generating PDF version of documentation ..."
      SOURCES "${PDF_OUTPUT_FILE}"
      VERBATIM
      )
endif()
