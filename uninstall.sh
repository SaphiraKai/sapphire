#!/bin/bash

#? Set safe bash options
set -euo pipefail
IFS='\n'

PREFIX=${PREFIX:-/usr}
DESTDIR=${DESTDIR:-}

rm -v $DESTDIR$PREFIX/bin/sapphire
rm -v $DESTDIR$PREFIX/share/sapphire/main.py

echo 'uninstalled successfully'
