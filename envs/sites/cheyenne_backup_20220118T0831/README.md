module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
export MODULEPATH_ROOT=/glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules
module use /glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules/compilers

module load intel/19.1.1
### module load ncarcompilers/0.5.0 ???
module load impi/2019.7.217
module load python/3.7.9
module av
module li

# spack

cd /glade/work/heinzell/jedi-stack/spack-stack-20220118
source spack/share/spack/setup-env.sh
spack env activate -p -d envs

# fv3-bundle

cd /glade/scratch/heinzell/fv3-bundle-spack-stack-20220118/fv3-bundle-feature-ufs-20220113/buildscripts

module use /glade/work/heinzell/jedi-stack/spack-stack-20220118/envs/install/modulefiles/intel/2020.1.217
module use /glade/work/heinzell/jedi-stack/spack-stack-20220118/envs/install/modulefiles/intel-mpi/2019.7.217-eovmnfj/intel/2020.1.217
module av
module li





# OLD

WITH SPACK


module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
module use /glade/work/heinzell/jedi-stack/spack-stack-20220113/envs/install/modulefiles/intel/2021.2.0
module load intel-oneapi-compilers/2021.2.0
module load intel-oneapi-mpi/2021.2.0
module load python/3.7.9