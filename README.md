
# Helwan Insight

A comprehensive data analysis tool developed for Helwan students, built with Python and PyQt5. This application provides functionalities for data loading, preprocessing, exploratory data analysis (EDA), and data visualization.

---

helwan-insight/
├── src/
│   ├── __init__.py                ← (ملف فارغ ضروري)
│   ├── main.py                    ← نقطة تشغيل التطبيق الرئيسية

│   ├── core/                      ← وظائف منطقية أساسية
│   │   ├── __init__.py
│   │   ├── data_handler.py        ← تحميل البيانات، حفظها، والتعامل معها

│   ├── ui/                        ← واجهة المستخدم
│   │   ├── __init__.py
│   │   ├── main_window.py         ← النافذة الرئيسية وتصميمها

│   │   ├── widgets/               ← مكونات الواجهة
│   │   │   ├── __init__.py
│   │   │   ├── data_viewer.py         ← عرض الجداول
│   │   │   ├── data_preprocessing.py  ← تنظيف وتحضير البيانات
│   │   │   ├── eda_dashboard.py       ← لوحة تحليل البيانات الاستكشافية
│   │   │   └── ...                    ← أدوات أخرى

│   │   ├── dialogs/               ← النوافذ الحوارية
│   │   │   ├── __init__.py
│   │   │   ├── statistics_dialog.py  ← نافذة إدخال/عرض إحصائيات
│   │   │   └── ...

│   ├── utils/                     ← وظائف مساعدة
│   │   ├── __init__.py
│   │   ├── i18n.py                ← إعدادات الترجمة والتعريب
│   │   └── ...

│   ├── logo/                      ← شعار التطبيق
│   │   ├── __init__.py (اختياري)
│   │   └── helwan-insight.png

│   └── locale/                    ← ملفات الترجمة
│       ├── __init__.py
│       ├── ar/
│       │   └── LC_MESSAGES/
│       │       ├── helwan_insight.po  ← ملف الترجمة النصي
│       │       └── helwan_insight.mo  ← ملف الترجمة المجمع
│       ├── en/
│       │   └── LC_MESSAGES/
│       │       ├── helwan_insight.po
│       │       └── helwan_insight.mo
│       └── ...

├── helwan-insight.desktop        ← ملف تعريف التطبيق على بيئة سطح مكتب لينكس
├── PKGBUILD                      ← ملف بناء الحزمة لـ Arch Linux (AUR)
└── README.md                     ← هذا الملف



## Features

* **Data Loading:** Load datasets from CSV and Excel files.
* **Data Preprocessing:** Handle missing values, drop duplicates, change column types, rename columns.
* **Exploratory Data Analysis (EDA):** Generate various statistical plots (histograms, scatter plots, box plots, pair plots, heatmaps) to understand data distributions and relationships.
* **Data Visualization:** Interactive plotting capabilities.
* **Multi-language Support:** Currently supports Arabic and English (expandable).

---

## Requirements

To run this application, you need Python 3.x and the following libraries:

* **`PyQt5`**: For the graphical user interface.
* **`pandas`**: For data manipulation and analysis.
* **`numpy`**: For numerical operations, often a dependency of `pandas`.
* **`matplotlib`**: For basic plotting and visualization.
* **`seaborn`**: For enhanced statistical data visualization.

You can install these libraries using pip:

```bash
pip install PyQt5 pandas numpy matplotlib seaborn
```

---

## How to Run the Application (Development)

Clone the repository:

```bash
git clone https://github.com/helwan-linux/helwan-insight.git
cd helwan-insight
```

Ensure all `__init__.py` files are present: Check that an empty `__init__.py` file exists in `src/`, `src/core/`, `src/ui/`, `src/ui/widgets/`, `src/ui/dialogs/`, `src/utils/`, `src/logo/`, and `src/locale/`.

Run the application: Navigate to the root directory of the project (`helwan-insight`) and execute the `main.py` module:

```bash
python -m src.main
```

This method ensures that Python correctly recognizes all internal modules and paths.

---

## Installation (Arch Linux)

For Arch Linux and Manjaro users, you can build and install Helwan Insight as a system package using the provided `PKGBUILD`.

Ensure you are in the project's root directory (`helwan-insight`).

Create a source tarball of your project:

```bash
tar -czvf helwan-insight-1.0.0.tar.gz --exclude='./.git' --exclude='./__pycache__' --exclude='./*.pyc' .
```

(Make sure the version `1.0.0` matches `pkgver` in `PKGBUILD`).

Build the package:

```bash
makepkg -s
```

If you get a checksum error, `makepkg` will tell you the correct `sha256sum` to update in the `PKGBUILD` file.

Install the package:

```bash
sudo pacman -U helwan-insight-1.0.0-1-any.pkg.tar.zst
```

(Replace the filename with the actual package file generated).

After installation, Helwan Insight will appear in your application menu with its icon, and you can launch it directly.

---

## Contributing

We welcome contributions! Please feel free to fork the repository, make improvements, and submit pull requests.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For questions or feedback, please open an issue on the GitHub repository.
