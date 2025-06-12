helwan-insight/
├── src/
│   ├── __init__.py           <-- (ملف فارغ: أساسي)
│   ├── main.py               <-- (ملف التشغيل الرئيسي)
│   │
│   ├── core/
│   │   ├── __init__.py       <-- (ملف فارغ: أساسي)
│   │   ├── data_handler.py
│   │   └── ... (أي ملفات core أخرى)
│   │
│   ├── ui/
│   │   ├── __init__.py       <-- (ملف فارغ: أساسي)
│   │   ├── main_window.py    <-- (ملف تعريف كلاس MainWindow)
│   │   ├── widgets/
│   │   │   ├── __init__.py   <-- (ملف فارغ: أساسي)
│   │   │   ├── data_viewer.py
│   │   │   ├── data_preprocessing.py
│   │   │   ├── eda_dashboard.py
│   │   │   └── ... (أي ملفات widgets أخرى)
│   │   │
│   │   └── dialogs/
│   │       ├── __init__.py   <-- (ملف فارغ: أساسي)
│   │       ├── statistics_dialog.py
│   │       └── ... (أي ملفات dialogs أخرى)
│   │
│   ├── utils/
│   │   ├── __init__.py       <-- (ملف فارغ: أساسي)
│   │   ├── i18n.py           <-- (منطق إعداد الترجمة)
│   │   └── ... (أي ملفات utils أخرى)
│   │
│   ├── logo/                 <-- (مجلد اللوجو داخل src)
│   │   ├── __init__.py       <-- (ملف فارغ: يفضل إضافته)
│   │   └── helwan-insight.png <-- (ملف اللوجو الخاص بك)
│   │
│   └── locale/               <-- (مجلد الترجمة داخل src)
│       ├── __init__.py       <-- (ملف فارغ: أساسي)
│       ├── ar/               <-- ترجمة عربية
│       │   ├── LC_MESSAGES/
│       │   │   └── helwan_insight.mo
│       │   │   └── helwan_insight.po
│       │   └── ...
│       │
│       ├── en/               <-- ترجمة إنجليزية (إذا كانت الملفات منفصلة)
│       │   ├── LC_MESSAGES/
│       │   │   └── helwan_insight.mo
│       │   │   └── helwan_insight.po
│       │   └── ...
│       └── ... (مجلدات اللغات الأخرى مثل fr/, es/ إلخ.)
│
├── helwan-insight.desktop  <-- (ملف اختصار التطبيق على سطح المكتب)
├── PKGBUILD                <-- (ملف بناء الحزمة لـ Arch Linux)
└── README.md               <-- (ملف اختياري لمعلومات المشروع)
