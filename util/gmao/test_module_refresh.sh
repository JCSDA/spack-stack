#!/usr/bin/env bash
set -e

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
refresh=$(sed -n '/^      # On TOSS5,/,/^      )$/p' "${script_dir}/batch_install.sh")
[[ -n "${refresh}" ]]

SPACK_STACK_DIR=$(mktemp -d)
mkdir "${SPACK_STACK_DIR}/logs"
trap 'rm -f "${SPACK_STACK_DIR}/logs/log.modules.test.test"; rmdir "${SPACK_STACK_DIR}/logs" "${SPACK_STACK_DIR}"' EXIT
env_name=test
LOG_TIMESTAMP=test
module_choice=tcl
spack() { printf '%s|%s\n' "$*" "$PATH"; }

PATH=:/example::/usr/bin:/bin:
original_path=$PATH
host=nas-toss5
eval "${refresh}" > /dev/null
[[ $(<"${SPACK_STACK_DIR}/logs/log.modules.test.test") == "module tcl refresh --yes --upstream-modules|/example:/usr/bin:/bin" ]]
[[ "$PATH" == "$original_path" ]]

host=nas
eval "${refresh}" > /dev/null
[[ $(<"${SPACK_STACK_DIR}/logs/log.modules.test.test") == "module tcl refresh --yes --upstream-modules|${original_path}" ]]
[[ "$PATH" == "$original_path" ]]
echo "Module refresh PATH checks passed"
