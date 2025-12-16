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
conflict("stack-openmpi")

-- spack compiler module hierarchy
@MODULEPATHS@

-- prerequisite modules
@MODULELOADS@

-- mpi wrapper environment variables
setenv("MPICC",  "@MPICC@")
setenv("MPICXX", "@MPICXX@")
setenv("MPIF77", "@MPIF77@")
setenv("MPIF90", "@MPIF90@")

-- underlying compilers for mpi distributions
setenv("I_MPI_CC",  "@CC@")
setenv("I_MPI_CXX", "@CXX@")
setenv("I_MPI_F77", "@F77@")
setenv("I_MPI_F90", "@FC@")
setenv("I_MPI_FC",  "@FC@")
setenv("OMPI_CC",  "@CC@")
setenv("OMPI_CXX", "@CXX@")
setenv("OMPI_F77", "@F77@")
setenv("OMPI_F90", "@FC@")
setenv("OMPI_FC",  "@FC@")
setenv("MPICH_CC",  "@CC@")
setenv("MPICH_CXX", "@CXX@")
setenv("MPICH_F77", "@F77@")
setenv("MPICH_F90", "@FC@")
setenv("MPICH_FC",  "@FC@")

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
