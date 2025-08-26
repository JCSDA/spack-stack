# How to build spack-stack at NAS

In the commands below some will be run on login nodes (with internet access) and some
on compute nodes as, at NAS, you aren't allowed more than 2 processes on a login node.

## Generic - Login Node

```
git clone --recursive https://github.com/JCSDA/spack-stack.git -b release/1.9.0 spack-stack-1.9.3
```

## oneapi

### Login Node

```
cd spack-stack-1.9.3
. setup.sh
spack stack create env --name ue-oneapi-2024.2.0 --template unified-dev --site nas --compiler oneapi
cd envs/ue-oneapi-2024.2.0
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack mirror create -a -d /nobackup/gmao_SIteam/spack-stack/source-cache
```

NOTE: Make sure you are in an environment when you run that `spack mirror create` command. Otherwise,
you will download *EVERY* package and *EVERY* version in spack!

### Compute Node

```
cd spack-stack-1.9.3
. setup.sh
cd envs/ue-oneapi-2024.2.0
spack env activate .
spack install -j 10 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
```

NOTE: You might need to run the `spack install` command multiple times because sometimes
it just fails. But then you run it more and more and it will eventually succeed.

```
spack module tcl refresh -y
spack stack setup-meta-modules
spack env deactivate
```

## gcc

### Login Node

```
cd spack-stack-1.9.3
. setup.sh
spack stack create env --name ue-gcc-12.3.0 --template unified-dev --site nas --compiler gcc
cd envs/ue-gcc-12.3.0
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack mirror create -a -d /nobackup/gmao_SIteam/spack-stack/source-cache
```

NOTE: Make sure you are in an environment when you run that `spack mirror create` command. Otherwise,
you will download *EVERY* package and *EVERY* version in spack!

### Compute Node

```
cd spack-stack-1.9.3
. setup.sh
cd envs/ue-gcc-12.3.0
spack env activate .
spack install -j 10 --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
```

NOTE: You might need to run the `spack install` command multiple times because sometimes
it just fails. But then you run it more and more and it will eventually succeed.

```
spack module tcl refresh -y
spack stack setup-meta-modules
spack env deactivate
```
