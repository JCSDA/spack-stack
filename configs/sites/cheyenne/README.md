# Cheyenne

## General instructions/prerequisites

### Set up the user environment for working with spack/building new software environments
```
module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
export MODULEPATH_ROOT=/glade/work/jedipara/cheyenne/spack-stack/modulefiles
module use /glade/work/jedipara/cheyenne/spack-stack/modulefiles/compilers
module load python/3.7.9
module load git/2.33.1
git lfs install
```
