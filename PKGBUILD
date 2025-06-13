# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>

pkgname=hel-insight
pkgver=1.0.0
pkgrel=1
pkgdesc="A comprehensive data analysis tool for Helwan students built with PyQt5 and Pandas."
arch=('any')
url="https://github.com/helwan-linux/helwan-insight"
license=('MIT')

depends=(
  'python'
  'python-pyqt5'
  'python-pandas'
  'python-numpy'
  'python-matplotlib'
  'python-seaborn'
)

# بنختار تحميل نسخة مضغوطة من الريبو
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/helwan-linux/helwan-insight/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('SKIP')

# اسم مجلد الريبو بعد الفك
_appsrcdir="helwan-linux-helwan-insight-${pkgver}"

build() {
  cd "${srcdir}/${_appsrcdir}"
  # لا أجزاء بناء لأن بايثون فقط
}

package() {
  cd "${srcdir}/${_appsrcdir}"

  install -d "${pkgdir}/usr/share/${pkgname}"
  cp -r src/* "${pkgdir}/usr/share/${pkgname}/"

  install -d "${pkgdir}/usr/share/applications"
  install -m644 helwan-insight.desktop "${pkgdir}/usr/share/applications/helwan-insight.desktop"

  install -d "${pkgdir}/usr/share/pixmaps"
  install -m644 src/logo/helwan-insight.png "${pkgdir}/usr/share/pixmaps/helwan-insight.png"

  install -d "${pkgdir}/usr/bin"
  cat <<EOF > "${pkgdir}/usr/bin/${pkgname}"
#!/bin/bash
exec python /usr/share/${pkgname}/main.py "\$@"
EOF
  chmod +x "${pkgdir}/usr/bin/${pkgname}"
}
