help([[
]])

local pkgName    = myModuleName()
local pkgVersion = myModuleVersion()
local pkgNameVer = myModuleFullName()

family("MetaCompiler")

-- conflicts
-- old names as of July 2025 - deprecate at some point later
conflict("stack-aocc")
conflict("stack-apple-clang")
conflict("stack-clang")
conflict("stack-gcc")
conflict("stack-intel")
conflict("stack-oneapi")
-- new names as of July 2025
conflict("stack-llvm")
conflict("stack-intel-oneapi-compilers-classic")
conflict("stack-intel-oneapi-compilers")

-- spack compiler module hierarchy
@MODULEPATHS@

-- prerequisite modules
@MODULELOADS@

-- compiler environment variables
setenv("F77", "@F77@")
setenv("FC",  "@FC@")
setenv("CC",  "@CC@")
setenv("CXX", "@CXX@")
setenv("SERIAL_F77", "@F77@")
setenv("SERIAL_FC",  "@FC@")
setenv("SERIAL_CC",  "@CC@")
setenv("SERIAL_CXX", "@CXX@")

-- compiler flags and other environment variables
@COMPFLAGS@
@ENVVARS@

-- module show info
whatis("Name: " .. pkgName)
whatis("Version: " .. pkgVersion)
whatis("Category: compiler")
whatis("Description: " .. pkgName .. " compiler family and module access")
