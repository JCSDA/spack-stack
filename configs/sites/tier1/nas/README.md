# How to build spack-stack at NAS

In the commands below some will be run on login nodes (with internet access) and some
on compute nodes as, at NAS, you aren't allowed more than 2 processes on a login node.

## Machines

For the below you will need to login to both an `afe01` node for one step. You'll
also want to get a Rome compute node for the rest of the steps.

## Clone spack-stack

```
git clone --recurse-submodules https://github.com/mathomp4/spack-stack.git -b feature/nas_install_spack_v1 spack-stack-2.0.0-test
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
cd spack-stack-2.0.0-test
. setup.sh
```

## Create environments

We create two different environments, one for oneAPI and one for GCC. The commands below
are used to create the environments. You only need to do this once.

### oneAPI

To create the oneAPI environment, do:

```
spack stack create env --name ue-oneapi-2024.2.0 --template unified-dev --site nas --compiler=oneapi-2024.2.0
cd envs/ue-oneapi-2024.2.0
```

### GCC

To create the GCC environment, do:

```
spack stack create env --name ue-gcc-13.2.0 --template unified-dev --site nas --compiler gcc-13.2.0
cd envs/ue-gcc-13.2.0
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

NOTE: The first time you do this on a new build, you should do it on a *LOGIN* node. This is because
it might need to bootstrap things and so it will reach out to the internet.

## Create source cache (LOGIN NODE ONLY)

Because this step downloads all the source code for all packages and all versions, it
should be done on a login node with internet access.

```
spack mirror create -a -d /swbuild/gmao_SIteam/spack-stack/source-cache
```

NOTE: Make sure you are in an environment when you run that `spack mirror create` command. Otherwise,
you will download *EVERY* package and *EVERY* version in spack!

## Pre-fetch cargo packages (LOGIN NODE ONLY)

Some packages use Rust/Cargo for dependencies. These need internet access to build. So we pre-fetch them here.

We need to set `CARGO_HOME` to a location where the Cargo deps have been downloaded

```
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
../../util/fetch_cargo_deps.py
```

NOTE: `CARGO_HOME` should be set as well on the COMPUTE node!

## Install packages

Our install process will actually have (at least) three steps. This is because of the `crtm` package
which requires internet access at build time.

### Install Step 1: Dependencies of Rust codes and ecflow (COMPUTE NODE)

We currently have some codes that use rust/cargo for dependencies. And, for some reason,
even doing the "cargo dependencies" as above, they still need internet
access to build/install. 

As for ecflow, we built QT on a login node (as it was the only complete node), so we
then have to build ecflow on a login node as well.

So we first install all the dependencies of then codes.

```
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
spack install -j 16 --verbose --fail-fast --show-log-on-error --no-check-signature --only dependencies py-cryptography py-maturin py-rpds-py ecflow 2>&1 | tee log.install.deps-for-rust-and-ecflow
```

### Install Step 2: Rust Codes and ecflow (AFE LOGIN NODE)

NOTE: You *MUST* run this on an afe login node. The reason is the pfe login nodes are Sandy
Bridge but we are building Spack with `x86_64_v3` and these are too old (`_v2`). So 
you will get an illegal instruction error when the install below calls python3.

So go back to an afe login node and run:

```
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
spack install -j 2 -p 1 --verbose --fail-fast --show-log-on-error --no-check-signature py-cryptography py-maturin py-rpds-py ecflow 2>&1 | tee log.install.rust-and-ecflow
```

Note we are only using 2 processes here because NAS limits you to 2 processes on a login node.

### Install Step 3: The rest (COMPUTE NODE)

```
export CARGO_HOME=/swbuild/gmao_SIteam/spack-stack/cargo-cache
spack install -j 16 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install.after-cargo
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
spack module tcl refresh -y --delete-tree
spack stack setup-meta-modules
```

## Deactivate environment

```
spack env deactivate
```

# Debugging a package

When things go wrong, a good way to debug a failure is:

```
spack clean
spack stage <package>
spack build-env <package> -- bash --norc --noprofile
```
