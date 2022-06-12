#!/bin/bash

#? Set safe bash options
set -euo pipefail
IFS='\n'

PREFIX=${PREFIX:-/usr}
DESTDIR=${DESTDIR:-}

rm -v  $DESTDIR$PREFIX/bin/sapphire
rm -rv $DESTDIR$PREFIX/share/sapphire/

echo
echo 'uninstalled successfully'
