#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Bootstrap spack-stack with Miniconda installation."
   echo
   echo "options:"
   echo "-p     spack-stack installation prefix"
}

prefix=""
miniconda_ver="py39_4.12.0"

# Get the options
while getopts ":hp:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      p) # Enter a name
         prefix=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

if [[ -z "${prefix}" ]]; then
    echo "Prefix must be set - exiting"
    exit 1
fi

stack_dir=${prefix}

module_dir=${stack_dir}/modulefiles
app_dir=${stack_dir}/apps
src_dir=${stack_dir}/src

mkdir -p ${stack_dir}
mkdir -p ${app_dir}
mkdir -p ${module_dir}
mkdir -p ${src_dir}
echo "Created spack-stack dir at: ${stack_dir}"

mkdir {src_dir}/spack-stack

case "$(uname -s)" in
   Darwin)
     platform="MacOSX-x86_64"
     ;;
   Linux)
     platform="Linux-x86_64"
     ;;
esac

name=Miniconda3-${miniconda_ver}-${platform}.sh

cd ${src_dir}

echo "Installing Miniconda ${miniconda_ver}"
mkdir -p miniconda/${miniconda_ver} && cd miniconda/${miniconda_ver}
if [[ ! -f "${name}" ]]; then
    wget https://repo.anaconda.com/miniconda/${name}
fi

miniconda_prefix=${app_dir}/miniconda/${miniconda_ver}
sh ${name} -u -b -p ${miniconda_prefix}

eval "$(${miniconda_prefix}/bin/conda shell.bash hook)"
conda install -y -c conda-forge libpython-static
conda install -y poetry
mkdir -p ${module_dir}/miniconda
miniconda_module=${module_dir}/miniconda/${miniconda_ver}
cp ${SCRIPT_DIR}/templates/miniconda ${miniconda_module}
sed -i.backup "s|@MINICONDA_PREFIX@|${miniconda_prefix}|" ${miniconda_module} && rm ${miniconda_module}.backup
