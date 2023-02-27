# Maintainer: Saphira Kai
pkgname=sapphire
pkgver=r11.6eb221c
pkgrel=1
epoch=
pkgdesc="An actually helpful personal assistant using GPT-3"
arch=(any)
url="https://github.com/SaphiraKai/sapphire"
license=('GPLv2')
groups=()
depends=('bash' 'python' 'python-openai' 'python-speechrecognition' 'python-gtts' 'mpv')
makedepends=()
checkdepends=()
optdepends=()
provides=('sapphire')
conflicts=()
replaces=()
backup=()
options=()
install=
changelog=

pkgver() {
	(
		set -o pipefail
		git describe --long 2>/dev/null | sed 's/\([^-]*-g\)/r\1/;s/-/./g' ||
		printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
	)
}

source=("src-$(pkgver).tar")
noextract=()
sha256sums=('SKIP')
validpgpkeys=()

#prepare() {}

#build() {}

#check() {}

package() {
	cd "$srcdir"
	DESTDIR="$pkgdir/" ./install.sh
}
