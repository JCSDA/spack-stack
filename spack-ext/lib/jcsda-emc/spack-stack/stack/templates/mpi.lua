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
local i_mpi_cc = os.getenv("CC")
local i_mpi_cxx = os.getenv("CXX")
local i_mpi_f77 = os.getenv("F77") or ""
local i_mpi_f90 = os.getenv("FC")
local i_mpi_fc = os.getenv("FC")

if i_mpi_cc and i_mpi_cxx and i_mpi_f90 and i_mpi_fc then
  setenv("I_MPI_CC", i_mpi_cc)
  setenv("I_MPI_CXX", i_mpi_cxx)
  setenv("I_MPI_F77", i_mpi_f77)
  setenv("I_MPI_F90", i_mpi_f90)
  setenv("I_MPI_FC",  i_mpi_fc)
end

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
