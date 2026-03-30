#!/usr/bin/env bash

# Save old prompt if not already saved
if [[ -z "$__OLD_PS1" ]]; then
  export __OLD_PS1="$PS1"
fi

# Only prepend if not already present
if [[ ! "$PS1" == *"($1)"* ]]; then
  export PS1="($1) $PS1"
fi
