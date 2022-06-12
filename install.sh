#!/bin/bash

#? Set safe bash options
set -euo pipefail
IFS='\n'

PREFIX=${PREFIX:-/usr}
DESTDIR=${DESTDIR:-}

install -Dvm 755 sapphire.sh  $DESTDIR$PREFIX/bin/sapphire
install -Dvm 755 main.py      $DESTDIR$PREFIX/share/sapphire/main.py
install -Dvm 644 functions.py $DESTDIR$PREFIX/share/sapphire/functions.py
install -Dvm 644 colors.py    $DESTDIR$PREFIX/share/sapphire/colors.py
install -Dvm 644 voice.py     $DESTDIR$PREFIX/share/sapphire/voice.py
install -Dvm 644 errors.py    $DESTDIR$PREFIX/share/sapphire/errors.py
mkdir -p                      $DESTDIR$PREFIX/share/sapphire/voice/
install -Dvm 644 voice/*.ogg  $DESTDIR$PREFIX/share/sapphire/voice/

echo
echo 'installed successfully'
