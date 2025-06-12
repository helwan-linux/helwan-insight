import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
import gettext
import os

from ui.main_window import MainWindow # <--- هذا هو سطر الاستدعاء المهم
from utils.i18n import setup_translation

def main():
    app = QApplication(sys.argv)

    initial_locale = QLocale.system().name()
    if initial_locale.startswith('ar'):
        translator_func = setup_translation("ar", "helwan_insight")
    else:
        translator_func = setup_translation("en", "helwan_insight")

    qt_translator = QTranslator()
    qt_locale_name = QLocale(initial_locale).name()
    if qt_translator.load("qt_" + qt_locale_name, QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
        app.installTranslator(qt_translator)

    main_win = MainWindow(_translator_func=translator_func)
    main_win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
