#!/usr/bin/env bash

# This script is supposed to be called from fetch_cargo_deps.py

set -ex

WORKDIR=${1}
export RUSTUP_HOME=${CARGO_HOME}/rustup

mkdir -p ${WORKDIR}
cd ${WORKDIR}
curl https://sh.rustup.rs -sSf > install.sh
chmod u+x install.sh
./install.sh --no-modify-path -y --default-toolchain stable --quiet 

export PATH=${CARGO_HOME}/bin
rustup default stable
