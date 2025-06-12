# Helwan Insight

A comprehensive data analysis tool developed for Helwan students, built with Python and PyQt5. This application provides functionalities for data loading, preprocessing, exploratory data analysis (EDA), and data visualization.

---

## Project Structure

This is the organized folder structure of the `Helwan Insight` project. **Each folder marked with `__init__.py` must contain an empty file with that exact name.** This is crucial for Python to recognize them as packages.
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
