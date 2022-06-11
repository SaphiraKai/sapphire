#!/bin/bash

#? Set safe bash options
set -euo pipefail
IFS='\n'

PREFIX=${PREFIX:-/usr}
DESTDIR=${DESTDIR:-}

install -Dvm 755 sapphire.sh  $DESTDIR$PREFIX/bin/sapphire
install -Dvm 755 main.py      $DESTDIR$PREFIX/share/sapphire/main.py

echo 'installed successfully'
