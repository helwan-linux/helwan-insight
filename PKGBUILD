# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com.com>
# (تأكد من تغيير اسمك وبريدك الإلكتروني هنا)

pkgname=helwan-insight
pkgver=1.0.0 # رقم إصدار تطبيقك
pkgrel=1
pkgdesc="A comprehensive data analysis tool for Helwan students built with PyQt5 and Pandas."
arch=('any') # 'any' مناسب لتطبيقات بايثون
url="https://github.com/helwan-linux/helwan-insight" # <--- رابط مشروعك على GitHub (محدث)
license=('MIT') # نوع الترخيص الخاص بك (أو قم بتغييره)

# الاعتماديات (المكتبات) التي يحتاجها تطبيقك
# تأكد من أن كل مكتبة بايثون تبدأ بـ 'python-'
depends=('python'
         'python-pyqt5'
         'python-pandas'
         'python-numpy'
         'python-matplotlib'
         'python-seaborn'
         # أضف هنا أي مكتبات بايثون أخرى يستخدمها مشروعك
)

# مصدر الكود - هذا يشير إلى ملف tar.gz لإصدار من مشروعك على GitHub.
# تأكد من أن هذا الإصدار (v1.0.0 في هذه الحالة) موجود على GitHub.
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/helwan-linux/${pkgname}/archive/v${pkgver}.tar.gz")

# هذا سيحتاج إلى تحديث يدوياً بعد كل إصدار جديد أو استخدام SHA256 sum صحيح
sha256sums=('SKIP') 

# اسم مجلد المصدر بعد فك الضغط (غالباً هو اسم pkgname-pkgver)
_appsrcdir="${pkgname}-${pkgver}"

build() {
  # هذا الجزء يتم تنفيذه في بيئة نظيفة داخل makepkg.
  # makepkg سيفك الضغط تلقائياً في مجلد src/${_appsrcdir}.
  cd "${srcdir}/${_appsrcdir}"
  # لا توجد خطوات بناء معقدة لتطبيقات بايثون البسيطة.
}

package() {
  # هذا الجزء يقوم بنسخ الملفات إلى مجلد الوجهة المؤقت (pkg/) ليتم حزمها.

  # 1. نسخ كود التطبيق كاملاً.
  # ننسخ محتويات مجلد 'src' (من المصدر المفكوك) إلى /usr/share/helwan-insight/.
  mkdir -p "${pkgdir}/usr/share/${pkgname}"
  cp -r "${srcdir}/${_appsrcdir}/src/"* "${pkgdir}/usr/share/${pkgname}/"
  
  # 2. نسخ ملف .desktop.
  # ننسخ ملف .desktop من مجلد المصدر المفكوك إلى /usr/share/applications/.
  mkdir -p "${pkgdir}/usr/share/applications"
  install -m644 "${srcdir}/${_appsrcdir}/helwan-insight.desktop" "${pkgdir}/usr/share/applications/"

  # 3. إنشاء سكربت التشغيل (Wrapper Script).
  # هذا السكربت هو الذي سيتم وضعه في /usr/bin/ وسيقوم بتشغيل التطبيق.
  mkdir -p "${pkgdir}/usr/bin"
  cat <<EOF > "${pkgdir}/usr/bin/${pkgname}"
#!/bin/bash
# تعيين PYTHONPATH ليشمل مسار تطبيقك
PYTHONPATH="/usr/share/${pkgname}" python -m src.main "$@"
EOF
  # جعل السكربت قابل للتنفيذ.
  chmod +x "${pkgdir}/usr/bin/${pkgname}"
}
