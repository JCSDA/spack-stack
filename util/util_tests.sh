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
echo -e " -  abcdefg hdf6@1.2.3%intel\n -  tuvwxyz hdf6@1.2.3%gcc" > fakeconcrete.A
run_and_check 1 "show_duplicate_packages.py A1" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.A
run_and_check 1 "show_duplicate_packages.py A2" "cat fakeconcrete.A | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py"
run_and_check 0 "show_duplicate_packages.py A3" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -c fakeconcrete.A
run_and_check 0 "show_duplicate_packages.py A4" "cat fakeconcrete.A | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -c"
echo -e " -  abcdefg hdf6@1.2.3\n -  tuvwxyz hdf6@1.2.4" > fakeconcrete.B
run_and_check 1 "show_duplicate_packages.py B1" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.B
run_and_check 1 "show_duplicate_packages.py B2" "cat fakeconcrete.B | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py"
echo -e " -  abcdefg hdf6@1.2.3\n[+] abcdefg hdf6@1.2.3" > fakeconcrete.C
run_and_check 0 "show_duplicate_packages.py C1" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.C
run_and_check 0 "show_duplicate_packages.py C2" "cat fakeconcrete.C | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py"
echo -e " -  abcdefg hdf6@1.2.3\n -  tuvwxyz hdf6@1.2.3\n -  hijklmn mypackage@1.1.1\n[+] opqrstu mypackage@1.1.1" > fakeconcrete.D
run_and_check 0 "show_duplicate_packages.py D1" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.D -i hdf6 -i mypackage
run_and_check 0 "show_duplicate_packages.py D2" ${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.D -i mypackage -i hdf6
run_and_check 0 "show_duplicate_packages.py D3" "cat fakeconcrete.D | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i hdf6 -i mypackage"
run_and_check 0 "show_duplicate_packages.py D4" "cat fakeconcrete.D | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i mypackage -i hdf6"
run_and_check 1 "show_duplicate_packages.py D5" "cat fakeconcrete.D | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i hdf6"
run_and_check 1 "show_duplicate_packages.py D6" "cat fakeconcrete.D | ${SPACK_STACK_DIR}/util/show_duplicate_packages.py -i mypackage"

cmd="${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.A 2>/dev/null | uniq | grep -c hdf6"
echo "Running '$cmd' in $PWD"
if [ $(eval "$cmd") -ne 2 ] ; then
  echo "show_duplicate_packages.py E failed!"
  fail=1
fi

cmd="${SPACK_STACK_DIR}/util/show_duplicate_packages.py fakeconcrete.F -d 2>/dev/null | uniq | grep -c hdf6"
echo -e " -  abcdefg hdf6@1.2.3\n -  tuvwxyz hdf6@1.2.3\n -  a1b2c3d other@1.1.1" > fakeconcrete.F
if [ $(eval "$cmd") -ne 2 ] ; then
  echo "show_duplicate_packages.py F failed!"
  fail=1
fi

## Check check_package_config.py
export SPACK_ENV=${SPACK_STACK_DIR}/util/test_env
export SPACK_ROOT=${SPACK_STACK_DIR}/spack
output_checksum=$(${SPACK_STACK_DIR}/util/check_package_config.py | sort | md5sum)
reference_checksum=$(cat ${SPACK_STACK_DIR}/util/test_env/package_check_baseline.txt | md5sum)
if [[ "$output_checksum" != "$reference_checksum" ]]; then
  echo "check_package_config.py check A failed!"
  fail=1
fi
# Test ignoring packages
count=$(${SPACK_STACK_DIR}/util/check_package_config.py -i sp --ignore cmake | wc -l)
if [ "$count" -ne 0 ]; then
  echo "check_package_config.py check B failed!"
  fail=1
fi

exit $fail
