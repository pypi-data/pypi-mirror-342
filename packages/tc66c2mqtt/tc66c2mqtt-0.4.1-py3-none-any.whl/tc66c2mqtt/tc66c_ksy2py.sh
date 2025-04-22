#!/bin/bash

# Creates Python parser `tc66c.py` from Kaitai Struct YAML file `tc66c.ksy`.
#
# Needs installed: https://github.com/kaitai-io/kaitai_struct_compiler
# See: https://kaitai.io/#download

set -x

kaitai-struct-compiler -t python tc66c.ksy
