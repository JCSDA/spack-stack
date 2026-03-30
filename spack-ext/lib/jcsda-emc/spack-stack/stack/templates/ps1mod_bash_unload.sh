#!/usr/bin/env bash

# Restore original PS1 if we saved it
if [[ -v "$__OLD_PS1" ]]; then
  export PS1="$__OLD_PS1"
  unset __OLD_PS1
fi
