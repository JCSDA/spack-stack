help([[
]])

local pkgName    = myModuleName()
local pkgVersion = myModuleVersion()
local pkgNameVer = myModuleFullName()

family("MetaMPI")

-- conflicts
conflict("stack-intel-mpi")
conflict("stack-intel-oneapi-mpi")
conflict("stack-cray-mpich")
conflict("stack-mpich")
conflict("stack-mpt")

-- prerequisite modules
@MODULELOADS@
@MODULEPREREQS@

-- spack compiler module hierarchy
@MODULEPATHS@

-- mpi wrapper environment variables
setenv("MPICC",  "@MPICC@")
setenv("MPICXX", "@MPICXX@")
setenv("MPIF77", "@MPIF77@")
setenv("MPIF90", "@MPIF90@")
setenv("MPI_CC",  "@MPICC@")
setenv("MPI_CXX", "@MPICXX@")
setenv("MPI_F77", "@MPIF77@")
setenv("MPI_F90", "@MPIF90@")

-- intel specific mpi wrapper environment variables
setenv("I_MPI_CC",  os.getenv("CC"))
setenv("I_MPI_CXX", os.getenv("CXX"))
setenv("I_MPI_F77", os.getenv("F77"))
setenv("I_MPI_F90", os.getenv("FC"))
setenv("I_MPI_FC",  os.getenv("FC"))

-- compiler flags and other environment variables
@COMPFLAGS@
@ENVVARS@

-- mpi root environment variable
@MPIROOT@

-- module show info
whatis("Name: " .. pkgName)
whatis("Version: " .. pkgVersion)
whatis("Category: library")
whatis("Description: " .. pkgName .. " mpi library and module access")
