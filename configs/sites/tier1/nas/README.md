# How to build spack-stack at NAS

In the commands below some will be run on login nodes (with internet access) and some
on compute nodes as, at NAS, you aren't allowed more than 2 processes on a login node.

## Clone spack-stack

```
git clone --recursive https://github.com/JCSDA/spack-stack.git -b release/1.9.0 spack-stack-1.9.3
```

## Grab interactive node

Since NAS limits you to 2 processes on a login node, you'll need to grab an interactive node. For example:
```
qsub -I -V -X -l select=1:ncpus=128:mpiprocs=128:model=mil_ait -l walltime=12:00:00 -W group_list=s1873 -m b -N Interactive
```
will get you a Milan node for 12 hours

## Setup spack-stack on each node

We will start on a login node with internet access. This is mainly needed for the
`spack mirror create` command which downloads all the source code for the packages.

```
cd spack-stack-1.9.3
. setup.sh
```

## Create environments

We create two different environments, one for oneAPI and one for GCC. The commands below
are used to create the environments. You only need to do this once.

### oneAPI

To create the oneAPI environment, do:

```
spack stack create env --name ue-oneapi-2024.2.0 --template unified-dev --site nas --compiler oneapi
cd envs/ue-oneapi-2024.2.0
```

### GCC

To create the GCC environment, do:

```
spack stack create env --name ue-gcc-12.3.0 --template unified-dev --site nas --compiler gcc
cd envs/ue-gcc-12.3.0
```

## Activate environment

Now enter the spack environment you just created:

```
spack env activate .
```

NOTE: You need to make sure you do this in *any* terminal where you want to do any commmand
below with this environment.

## Concretize and create source cache

```
spack concretize 2>&1 | tee log.concretize
```

## Create source cache (LOGIN NODE ONLY)

Because this step downloads all the source code for all packages and all versions, it
should be done on a login node with internet access.

```
spack mirror create -a -d /nobackup/gmao_SIteam/spack-stack/source-cache
```

NOTE: Make sure you are in an environment when you run that `spack mirror create` command. Otherwise,
you will download *EVERY* package and *EVERY* version in spack!

## Install packages

Our install process will actually have (at least) three steps. This is because of the `crtm` package
which requires internet access at build time.

### Install crtm dependencies (COMPUTE NODE)

```
spack install -j 10 --verbose --fail-fast --show-log-on-error --no-check-signature --only dependencies crtm 2>&1 | tee log.install.crtm_dependencies
```

### Install crtm (LOGIN NODE)

```
spack install -j 2 --verbose --fail-fast --show-log-on-error --no-check-signature crtm 2>&1 | tee log.install.crtm
```

Note we are only using 2 processes here because NAS limits you to 2 processes on a login node.

### Install rest of packages (COMPUTE NODE)

```
spack install -j 10 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install.after_crtm
```

NOTE: You might need to run the `spack install` command multiple times because sometimes
it just fails. But then you run it more and more and it will eventually succeed.

### Packages needing internet access to build

If you encounter other packages that need internet access to build, you can install them with:

```
spack install -j 2 --verbose --fail-fast --show-log-on-error --no-check-signature <package> |& tee log.install.<package>
```

Then, once that package is built, you can go back to the compute node and run the `spack install` command again.

## Update module files and setup meta-modules

```
spack module tcl refresh -y
spack stack setup-meta-modules
```

## Deactivate environment

```
spack env deactivate
```
