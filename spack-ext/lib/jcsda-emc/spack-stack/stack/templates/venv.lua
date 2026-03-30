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

-- Prompt modification (bash only)
if (myShellName() == "bash") then
  if (mode() == "load") then
    execute{
      cmd = [[ source @VENV_MODULEDIR@/ps1mod_bash_load.sh @VENV_NAME@ ]]
    }
  elseif (mode() == "unload") then
    execute{
      cmd = [[ source @VENV_MODULEDIR@/ps1mod_bash_unload.sh @VENV_NAME@ ]]
    }
  end
end
