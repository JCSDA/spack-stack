# Miniconda installation to support spack-stack Python packages

If required, miniconda can be used to provide a basic version of Python that spack-stack uses to support its Python packages.

### One-off: install miniconda python3 environment
In the following instructions, replace `/work/noaa/gsd-hpcs/dheinzel/jcsda` with the directory where your miniconda-3.9.7 directory will be installed.
```
cd /work/noaa/gsd-hpcs/dheinzel/jcsda
mkdir -p miniconda-3.9.7/src
cd miniconda-3.9.7/src
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh -u
# Accept license agreement
# Install in /work/noaa/gsd-hpcs/dheinzel/jcsda/miniconda-3.9.7
# Do not have the installer initialize Miniconda3 by running conda init
```
Create modulefile `/work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles/miniconda/3.9.7` from template `miniconda/modulefile_template` and update `MINICONDA_PATH` in this file. Then:
```
module use /work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles
module load miniconda/3.9.7
which python3
# make sure this points to the new miniconda install
which pip3
# make sure this points to the new miniconda install
pip3 install poetry
# ignore warnings/errors about pip's dependency resolver
# test:
python3 -c "import poetry"
# successful if silent
```
DOM: TEST IF THE PIP INSTALL CAN BE COMBINED WITH THIS
```
eval "$(/scratch1/BMC/gsd-hpcs/Dom.Heinzeller/spack-stack/miniconda-3.9.7/bin/conda shell.bash hook)"
conda install -c conda-forge libpython-static`
# log out to forget about the conda environment
```

### Set up the user environment for working with spack/building new software environments
This needs to be done every time before installing packages with spack or before using spack-provided modules!
```
module use /work/noaa/gsd-hpcs/dheinzel/jcsda/modulefiles
module load miniconda/3.9.7
```
