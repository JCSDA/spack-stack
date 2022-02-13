# Generating Site Configs

```
source ./setup.sh
mkdir <site-name> && cd <site-name>
# Output the files here
export SPACK_SYSTEM_CONFIG_PATH=`pwd`
spack external find --scope system
spack compiler find --scope system
```

## External Packages


Run `spack external find` to locate common external packages such as git, Perl, CMake, etc.

## Compilers

Run `spack compiler find` to locate compilers in your path. Compilers with modules need to be added manually. 
