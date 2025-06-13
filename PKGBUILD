# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>

pkgname=hel-insight
pkgver=1.0.0
pkgrel=1
pkgdesc="A comprehensive data analysis tool for students."
arch=('any')
url="https://github.com/helwan-linux/helwan-insight"
license=('MIT')
depends=('python' 'python-pyqt5' 'python-pandas' 'python-numpy' 'python-matplotlib' 'python-seaborn')
source=("hel-insight.tar.gz::https://github.com/helwan-linux/helwan-insight/archive/refs/heads/main.tar.gz")
sha256sums=('SKIP')

build() {
  cd "$srcdir/helwan-insight-main"
}

package() {
  cd "$srcdir/helwan-insight-main/helwan-insight"

  # نسخ الملفات إلى /usr/share
  install -d "$pkgdir/usr/share/hel-insight"
  cp -r src locales "$pkgdir/usr/share/hel-insight/"

  # تثبيت أيقونة
  install -Dm644 src/logo/helwan-insight.png "$pkgdir/usr/share/pixmaps/helwan-insight.png"

  # ملف سطح المكتب
  install -Dm644 helwan-insight.desktop "$pkgdir/usr/share/applications/hel-insight.desktop"

  # سكريبت التشغيل
  install -d "$pkgdir/usr/bin"
  cat <<EOF > "$pkgdir/usr/bin/hel-insight"
#!/bin/bash
# هذا السطر تم تعديله لتشغيل main.py مباشرة مع PYTHONPATH الصحيح
PYTHONPATH="/usr/share/hel-insight/src" python3 /usr/share/hel-insight/src/main.py "\$@"
EOF
  chmod +x "$pkgdir/usr/bin/hel-insight"
}
