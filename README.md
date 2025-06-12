
# Helwan Insight

A comprehensive data analysis tool developed for Helwan students, built with Python and PyQt5. This application provides functionalities for data loading, preprocessing, exploratory data analysis (EDA), and data visualization.

---

helwan-insight4/
├── src/
│   ├── __init__.py              <-- (Empty file: Essential)
│   ├── main.py                  <-- (Main application entry point)
│
│   ├── core/
│   │   ├── __init__.py          <-- (Empty file: Essential)
│   │   ├── data_handler.py      <-- (Handles data loading, saving, and basic manipulation)
│   │   └── ...                  <-- (Other core functionalities)
│
│   ├── ui/
│   │   ├── __init__.py          <-- (Empty file: Essential)
│   │   ├── main_window.py       <-- (Defines the main application window and its layout)
│   │
│   │   ├── widgets/
│   │   │   ├── __init__.py          <-- (Empty file: Essential)
│   │   │   ├── data_viewer.py       <-- (Widget for displaying data tables)
│   │   │   ├── data_preprocessing.py<-- (Widget for data cleaning/preparation)
│   │   │   ├── eda_dashboard.py     <-- (Widget for exploratory data analysis dashboard and plots)
│   │   │   └── ...                  <-- (Other UI components)
│   │
│   │   └── dialogs/
│   │       ├── __init__.py          <-- (Empty file: Essential)
│   │       ├── statistics_dialog.py <-- (Dialogs for specific user inputs/outputs)
│   │       └── ...                  <-- (Other dialogs)
│
│   ├── utils/
│   │   ├── __init__.py          <-- (Empty file: Essential)
│   │   ├── i18n.py              <-- (Internationalization/translation setup logic)
│   │   └── ...                  <-- (Utility functions)
│
│   ├── logo/
│   │   ├── __init__.py          <-- (Empty file: Recommended)
│   │   └── helwan-insight.png   <-- (Your application logo)
│
│   └── locale/
│       ├── __init__.py          <-- (Empty file: Essential)
│       ├── ar/                  <-- Arabic translations
│       │   └── LC_MESSAGES/
│       │       ├── helwan_insight.po  <-- (Source translation file)
│       │       └── helwan_insight.mo  <-- (Compiled translation file)
│       ├── en/                  <-- English translations
│       │   └── LC_MESSAGES/
│       │       ├── helwan_insight.po
│       │       └── helwan_insight.mo
│       └── ...                  <-- (Other language folders)
│
├── helwan-insight.desktop       <-- (Desktop entry file for Linux desktop environments)
├── PKGBUILD                     <-- (Arch Linux Package Build file for AUR/pacman)
└── README.md                    <-- (This file!)


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
