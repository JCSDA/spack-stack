CHEYENNE

module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
export MODULEPATH_ROOT=/glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules
module use /glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules/compilers

module load intel/2021.2
module load impi/2021.2
module load ncarcompilers/0.5.0
module load python/3.7.9


cd /glade/work/heinzell/jedi-stack/spack-stack-20220118
source spack/share/spack/setup-env.sh
spack env activate -p -d envs





cd /glade/work/heinzell/jedi-stack/spack-stack-20220113/
ls
rm spack*log
ls
module load python/3.7.9
module av
module li
module load git/2.33.1
module av




WITH SPACK


module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
export MODULEPATH_ROOT=/glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules
module use /glade/work/heinzell/jedi-stack/spack-stack-20220113/envs/install/modulefiles/intel/2021.2.0
module load intel-oneapi-compilers/2021.2.0
module load intel-oneapi-mpi/2021.2.0
module load python/3.7.9