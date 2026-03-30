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
      cmd = [[
        if [ -z "$__OLD_PS1" ]; then
          export __OLD_PS1="$PS1"
        fi
        case "$PS1" in
          *"(@VENV_NAME@)"*) ;;
          *) export PS1="(@VENV_NAME@) $PS1" ;;
        esac
        ]]
    }
  elseif (mode() == "unload") then
    execute{
      cmd = [[
        if [ ! -z "$__OLD_PS1" ]; then
          export PS1="$__OLD_PS1"
          unset __OLD_PS1
        fi
      ]]
    }
  end
end