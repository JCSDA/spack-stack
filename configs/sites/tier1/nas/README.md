# How to build spack-stack at NAS

## Generic

```
git clone --recursive https://github.com/JCSDA/spack-stack.git -b release/1.9.0 spack-stack-1.9.1
```

## oneapi

```
cd spack-stack-1.9.1
. setup.sh
spack stack create env --name ue-oneapi-2024.2.0 --template unified-dev --site nas --compiler oneapi
cd envs/ue-oneapi-2024.2.0
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
```

NOTE: You might need to run the `spack install` command multiple times because sometimes
it just fails. But then you run it more and more and it will eventually succeed.

```
spack module tcl refresh -y
spack stack setup-meta-modules
spack env deactivate
```

## gcc

```
cd spack-stack-1.9.1
. setup.sh
spack stack create env --name ue-gcc-12.3.0 --template unified-dev --site nas --compiler gcc
cd envs/ue-gcc-12.3.0
spack env activate .
spack concretize 2>&1 | tee log.concretize
spack install --verbose --fail-fast --show-log-on-error --no-check-signature 2>&1 | tee log.install
```

NOTE: You might need to run the `spack install` command multiple times because sometimes
it just fails. But then you run it more and more and it will eventually succeed.

```
spack module tcl refresh -y
spack stack setup-meta-modules
spack env deactivate
```
