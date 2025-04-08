#!/bin/bash
# This script is used by the GitHub Actions util-test workflow.

# This functions runs a command and checks the return code.
function run_and_check(){
  expected=$1
  label=$2
  shift 2
  echo "Running '$*' in $PWD"
  eval "$*" &> /tmp/output.$$
  if [ $? -ne $expected ]; then
    echo "Test $label failed! Output:"
    cat /tmp/output.$$
    rm /tmp/output.$$
    echo
    fail=1
  fi
}

echo "umask:" $(umask)
chmod o+rX $HOME
mkdir -p ${SPACK_STACK_DIR}/util/checks
cd ${SPACK_STACK_DIR}/util/checks

## Check check_permissions.sh
mkdir -p perm_check1/perm_check2/perm_check3
cd perm_check1/perm_check2
chmod 777 ../../perm_check1
chmod 777 .
chmod 777 ./perm_check3
run_and_check 0 "check_permissions A" ${SPACK_STACK_DIR}/util/check_permissions.sh
chmod 776 ../../perm_check1
run_and_check 1 "check_permissions B" ${SPACK_STACK_DIR}/util/check_permissions.sh
chmod 773 ../../perm_check1
run_and_check 1 "check_permissions C" ${SPACK_STACK_DIR}/util/check_permissions.sh
chmod 770 ../../perm_check1
run_and_check 1 "check_permissions D" ${SPACK_STACK_DIR}/util/check_permissions.sh
chmod 777 ../../perm_check1
chmod 776 perm_check3
run_and_check 1 "check_permissions E" ${SPACK_STACK_DIR}/util/check_permissions.sh
chmod 773 perm_check3
run_and_check 1 "check_permissions F" ${SPACK_STACK_DIR}/util/check_permissions.sh
chmod 770 perm_check3
run_and_check 1 "check_permissions G" ${SPACK_STACK_DIR}/util/check_permissions.sh

## Check show_duplicate_packages.py
cd ${SPACK_STACK_DIR}/util/checks
echo '{"concrete_specs": {"a2yzf2cdwz7ajifuqacnzfde5wulwyke": {"name": "w3emc", "version": "2.10.0"}, "ks553jzmi3kmx4g76t6mfeb6gpmxa5n4": {"name": "w3emc", "version": "2.11.0"}}}' > spack.lock
run_and_check 1 "show_duplicate_packages.py, should find duplicates" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py
run_and_check 0 "show_duplicate_packages.py, should not find duplicates" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i w3emc

exit $fail
