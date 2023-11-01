#!/bin/bash
# Run this utility inside a spack-stack environment directory to ensure that
# permissions are set such that non-owning users/groups can use the
# installation.

path=$PWD

# Check upstream hierarchy of current directory
while [ $path != '/' ]; do
  o_perms=$(ls -ld $path | awk '{print $1}' | grep -oE "[r-][w-][x-]" | tail -1)
  if [ "${o_perms:0:1}" != 'r' ]; then
    echo "Path $path is not readable by non-owners; set o+r" 1>&2
    iret=1
  fi
  if [ "${o_perms:2:3}" != 'x' ]; then
    echo "Path $path is not accessible by non-owners; set o+x" 1>&2
    iret=1
  fi
  path=$(dirname $path)
done

# Check downstream hierarchy of current directory
n_bad_perms=$(find $PWD \( -type d -and -not -perm -005 \) -or \( -type f -and -not -perm -004 \) | wc -l)
if [ $n_bad_perms -gt 0 ]; then
  echo "There are files under this hierarchy not accessible to non-owning users/groups."
  echo 'Use "find $PWD \( -type d -a -not -perm -005 \) -o \( -type f -a -not -perm -004 \)" to identify them.'
  iret=1
fi

exit $iret
