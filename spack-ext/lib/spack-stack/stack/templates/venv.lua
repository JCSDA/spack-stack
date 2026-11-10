-- spack-stack virtual environment meta module

help([[
This modulefile defines the @VENV_NAME@ environment meta module for spack-stack
]])

whatis("spack-stack virtual environment meta module")

-- conflicts
conflict("stack-venv")

-- prerequisite modules
@MODULELOADS@

-- environment
setenv("PYTHONHOME", "@VENV_ROOT@")
prepend_path("PATH", "@VENV_ROOT@/bin")
prepend_path("LD_LIBRARY_PATH", "@VENV_ROOT@/lib")
prepend_path("LD_LIBRARY_PATH", "@VENV_ROOT@/lib64")
