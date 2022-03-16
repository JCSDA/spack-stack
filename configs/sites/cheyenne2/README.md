# Cheyenne

## General instructions/prerequisites

### Set up the user environment for working with spack/building new software environments
```
module purge
module unuse /glade/u/apps/ch/modulefiles/default/compilers
#export MODULEPATH_ROOT=/glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules
#module use /glade/p/ral/jntp/GMTB/tools/compiler_mpi_modules/compilers
module load python/3.7.9
```

wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18487/l_BaseKit_p_2022.1.2.146.sh
sh l_BaseKit_p_2022.1.2.146.sh
# install to /glade/work/heinzell/intel-oneapi-2022.1.1

wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18479/l_HPCKit_p_2022.1.2.117.sh
sh l_HPCKit_p_2022.1.2.117.sh
# install to /glade/work/heinzell/intel-oneapi-2022.1.1


source /glade/work/heinzell/intel-oneapi-2022.1.1/compiler/2022.0.2/env/vars.sh

source /glade/work/heinzell/intel-oneapi-2022.1.1/mpi/2021.5.1/env/vars.sh
