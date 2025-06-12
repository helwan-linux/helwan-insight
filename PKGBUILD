# Maintainer: Your Name <your.email@example.com>
# (تأكد من تغيير اسمك وبريدك الإلكتروني هنا)

pkgname=helwan-insight
pkgver=1.0.0 # رقم إصدار تطبيقك
pkgrel=1
pkgdesc="A comprehensive data analysis tool for Helwan students built with PyQt5 and Pandas."
arch=('any') # 'any' مناسب لتطبيقات بايثون
url="https://github.com/yourusername/helwan-insight" # رابط مشروعك على GitHub (قم بتغييره)
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

# مصدر الكود - في هذه الحالة، هو مجلد المشروع الحالي.
# هذا يعني أنك ستقوم بتشغيل makepkg من مجلد helwan-insight4 نفسه.
# إذا كنت ستقوم بتوزيع المشروع كملف مضغوط (مثلاً على GitHub Releases)، ستحتاج لتغيير هذا السطر.
# For local build from current directory:
source=("$pkgname-${pkgver}.tar.gz::file:///${PWD}/src") # هذا السطر يفترض أن 'src' هو جذر الكود في الأرشيف
# Note: For makepkg to use the local directory, you usually tar it up first or provide a 'git' source.
# A simpler way if you are building from a local copy is to adjust the build() and package() functions
# to copy from the current directory structure directly, but standard PKGBUILDs expect sources.
# Let's adjust for typical makepkg source usage (assuming you'd compress your project).
# For now, let's assume you will create a tar.gz of your project's root:
source=("${pkgname}-${pkgver}.tar.gz") # <--- هذا السطر يشير إلى ملف tar.gz للمشروع كله

# هذا سيحتاج إلى تحديث يدوياً بعد كل بناء لـ tar.gz أو استخدم 'SKIP' أثناء التطوير
sha256sums=('SKIP') 

# اسم مجلد المصدر بعد فك الضغط (غالباً هو اسم pkgname-pkgver)
_appsrcdir="${pkgname}-${pkgver}"

build() {
  # هذا الجزء يتم تنفيذه في بيئة نظيفة داخل makepkg
  # هنا، سنقوم بفك ضغط ملف المشروع المضغوط
  # makepkg سيفك الضغط تلقائياً في مجلد يسمى src/${_appsrcdir}
  cd "${srcdir}/${_appsrcdir}"
  # لا توجد خطوات بناء معقدة لتطبيقات بايثون البسيطة
}

package() {
  # هذا الجزء يقوم بنسخ الملفات إلى مجلد الوجهة المؤقت (pkg/) ليتم حزمها

  # 1. نسخ كود التطبيق كاملاً
  # ننسخ محتويات مجلد 'src' (من المصدر المفكوك) إلى /usr/share/helwan-insight/
  mkdir -p "${pkgdir}/usr/share/${pkgname}"
  cp -r "${srcdir}/${_appsrcdir}/src/"* "${pkgdir}/usr/share/${pkgname}/"
  
  # 2. نسخ ملف .desktop
  # ننسخ ملف .desktop من مجلد المصدر المفكوك إلى /usr/share/applications/
  mkdir -p "${pkgdir}/usr/share/applications"
  install -m644 "${srcdir}/${_appsrcdir}/helwan-insight.desktop" "${pkgdir}/usr/share/applications/"

  # 3. إنشاء سكربت التشغيل (Wrapper Script)
  # هذا السكربت هو الذي سيتم وضعه في /usr/bin/ وسيقوم بتشغيل التطبيق
  mkdir -p "${pkgdir}/usr/bin"
  cat <<EOF > "${pkgdir}/usr/bin/${pkgname}"
#!/bin/bash
# تعيين PYTHONPATH ليشمل مسار تطبيقك
PYTHONPATH="/usr/share/${pkgname}" python -m src.main "$@"
EOF
  # جعل السكربت قابل للتنفيذ
  chmod +x "${pkgdir}/usr/bin/${pkgname}"
}