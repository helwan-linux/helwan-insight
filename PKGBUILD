# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>


pkgname=helwan-insight
pkgver=1.0.0 # رقم إصدار تطبيقك الحالي
pkgrel=1
pkgdesc="A comprehensive data analysis tool for Helwan students built with PyQt5 and Pandas."
arch=('any')
url="https://github.com/helwan-linux/helwan-insight" # رابط مشروعك على GitHub
license=('MIT')

depends=('python'
         'python-pyqt5'
         'python-pandas'
         'python-numpy'
         'python-matplotlib'
         'python-seaborn'
)

# مصدر الكود - هذا يعني أن makepkg سينزل ملف tar.gz من صفحة الإصدارات على GitHub.
# تأكد من وجود إصدار (tag) اسمه v1.0.0 (أو رقم الإصدار اللي هتكتبه في pkgver) على GitHub.
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/helwan-linux/${pkgname}/archive/v${pkgver}.tar.gz")

# هذا السطر يجب تحديثه يدوياً بقيمة الـ SHA256 sum الصحيحة لملف tar.gz بعد أول بناء.
# مبدئياً، ممكن تسيبها 'SKIP' وهتجيلك القيمة الصح لو في خطأ أثناء البناء.
sha256sums=('SKIP') 

# اسم مجلد المصدر بعد فك الضغط (غالباً هو اسم pkgname-pkgver)
_appsrcdir="${pkgname}-${pkgver}"

build() {
  # makepkg هيفك ضغط ملف السورس تلقائياً في src/${_appsrcdir}
  cd "${srcdir}/${_appsrcdir}"
}

package() {
  # نسخ كل محتويات مجلد 'src' (بما فيهم logo و locale) إلى /usr/share/helwan-insight/
  mkdir -p "${pkgdir}/usr/share/${pkgname}"
  cp -r "${srcdir}/${_appsrcdir}/src/"* "${pkgdir}/usr/share/${pkgname}/"
  
  # نسخ ملف .desktop إلى /usr/share/applications/
  mkdir -p "${pkgdir}/usr/share/applications"
  install -m644 "${srcdir}/${_appsrcdir}/helwan-insight.desktop" "${pkgdir}/usr/share/applications/"

  # إنشاء سكربت التشغيل في /usr/bin/
  mkdir -p "${pkgdir}/usr/bin"
  cat <<EOF > "${pkgdir}/usr/bin/${pkgname}"
#!/bin/bash
PYTHONPATH="/usr/share/${pkgname}" python -m src.main "$@"
EOF
  # جعل السكربت قابل للتنفيذ
  chmod +x "${pkgdir}/usr/bin/${pkgname}"
}
