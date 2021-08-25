#!/bin/bash

[ -e ~/registry ] && (cd ~/registry; git pull) || git clone https://git:$1@git.dn42.dev/dn42/registry ~/registry --depth 1 --single-branch

mkdir -p ~/cache_data

python3 main.py $2 $3
