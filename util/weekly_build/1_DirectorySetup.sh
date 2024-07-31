#!/bin/bash

set -e

echo Base directory: ${2?"Second arg: base directory for build"}

mkdir -p $2
