import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QAction, QFileDialog, QMessageBox, QLabel, QStackedWidget,
    QMenuBar, QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QTranslator, QLocale, QLibraryInfo
from PyQt5.QtGui import QIcon # <--- تأكد من استيراد QIcon هنا

import gettext
import os # <--- تأكد من استيراد os هنا

from core.data_handler import DataHandler
from ui.widgets.data_preview_table import DataPreviewTable
from ui.widgets.eda_dashboard import EDADashboard
from ui.dialogs.statistics_dialog import StatisticsDialog

# --- MissingValuesDialog Class ---
class MissingValuesDialog(QDialog):
    def __init__(self, df_columns: list, numerical_cols: list, categorical_cols: list, _translator_func, parent=None):
        super().__init__(parent)
        self._ = _translator_func
        self.numerical_cols = numerical_cols
        self.categorical_cols = categorical_cols

        self.setWindowTitle(self._("Handle Missing Values"))
        self.setGeometry(200, 200, 400, 250)

        self.layout = QFormLayout(self)

        self.column_combo = QComboBox()
        self.column_combo.addItem(self._("All Numerical Columns"))
        self.column_combo.addItem(self._("All Categorical Columns"))
        self.column_combo.addItem(self._("All Columns (Any Type)"))
        self.column_combo.addItems(df_columns)
        self.layout.addRow(self._("Select Column:"), self.column_combo)

        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            self._("Drop Rows (any missing)"),
            self._("Drop Rows (selected column only)"),
            self._("Fill with Mean"),
            self._("Fill with Median"),
            self._("Fill with Mode"),
            self._("Fill with Specific Value")
        ])
        self.strategy_combo.currentIndexChanged.connect(self.toggle_fill_value_input)
        self.layout.addRow(self._("Select Strategy:"), self.strategy_combo)

        self.fill_value_input = QLineEdit()
        self.fill_value_input.setPlaceholderText(self._("Enter value to fill with"))
        self.fill_value_input.setVisible(False)
        self.layout.addRow(self._("Fill Value:"), self.fill_value_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def toggle_fill_value_input(self):
        self.fill_value_input.setVisible(self.strategy_combo.currentText() == self._("Fill with Specific Value"))

    def get_selected_options(self):
        selected_column_display = self.column_combo.currentText()
        selected_strategy_display = self.strategy_combo.currentText()
        fill_val = self.fill_value_input.text() if self.fill_value_input.isVisible() else None

        strategy_map = {
            self._("Drop Rows (any missing)"): 'drop_rows_all',
            self._("Drop Rows (selected column only)"): 'drop_rows_selected',
            self._("Fill with Mean"): 'fill_mean',
            self._("Fill with Median"): 'fill_median',
            self._("Fill with Mode"): 'fill_mode',
            self._("Fill with Specific Value"): 'fill_value'
        }
        strategy = strategy_map.get(selected_strategy_display)

        column = None
        if selected_column_display == self._("All Numerical Columns"):
            column = "numerical_cols_only"
        elif selected_column_display == self._("All Categorical Columns"):
            column = "categorical_cols_only"
        elif selected_column_display == self._("All Columns (Any Type)"):
            column = "all_cols_any_type"
        else:
            column = selected_column_display

        return strategy, column, fill_val

# --- ChangeColumnTypeDialog Class ---
class ChangeColumnTypeDialog(QDialog):
    def __init__(self, df_columns: list, _translator_func, parent=None):
        super().__init__(parent)
        self._ = _translator_func
        self.setWindowTitle(self._("Change Column Type"))
        self.setGeometry(200, 200, 350, 180)

        self.layout = QFormLayout(self)

        self.column_combo = QComboBox()
        self.column_combo.addItems(df_columns)
        self.layout.addRow(self._("Select Column:"), self.column_combo)

        self.type_combo = QComboBox()
        self.type_combo.addItems([
            self._("Integer"),
            self._("Float"),
            self._("Text"),
            self._("Date/Time")
        ])
        self.layout.addRow(self._("New Type:"), self.type_combo)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def get_selected_options(self):
        column = self.column_combo.currentText()
        type_display = self.type_combo.currentText()

        type_map = {
            self._("Integer"): 'int',
            self._("Float"): 'float',
            self._("Text"): 'str',
            self._("Date/Time"): 'datetime'
        }
        new_type = type_map.get(type_display)
        
        return column, new_type

# --- RenameColumnDialog Class ---
class RenameColumnDialog(QDialog):
    def __init__(self, df_columns: list, _translator_func, parent=None):
        super().__init__(parent)
        self._ = _translator_func
        self.setWindowTitle(self._("Rename Column"))
        self.setGeometry(200, 200, 350, 180)

        self.layout = QFormLayout(self)

        self.column_combo = QComboBox()
        self.column_combo.addItems(df_columns)
        self.layout.addRow(self._("Select Column:"), self.column_combo)

        self.new_name_input = QLineEdit()
        self.new_name_input.setPlaceholderText(self._("Enter new column name"))
        self.layout.addRow(self._("New Name:"), self.new_name_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def get_selected_options(self):
        old_name = self.column_combo.currentText()
        new_name = self.new_name_input.text().strip()
        return old_name, new_name

# --- MainWindow Class ---
class MainWindow(QMainWindow):
    def __init__(self, _translator_func=None, parent=None):
        super().__init__(parent)

        if _translator_func:
            self._ = _translator_func
        else:
            self._ = lambda text: text

        self.setWindowTitle(self._("Helwan-Insight - Data Analysis Tool"))
        self.setGeometry(100, 100, 1200, 800)

        # ----------------------------------------------------
        # إضافة اللوجو هنا - المسار ديناميكي ليعمل على أي نظام تشغيل ومكان
        # تأكد من أن ملف helwan-insight.png موجود في src/logo/
        script_dir = os.path.dirname(os.path.abspath(__file__)) # مسار ملف main_window.py (الذي هو في ui)
        # نرجع خطوة للمجلد src ثم ندخل على مجلد logo
        logo_path = os.path.join(script_dir, "..", "logo", "helwan-insight.png") 
        logo_path = os.path.abspath(logo_path) # تحويل المسار لمسار مطلق لضمان المرونة

        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        else:
            print(f"Warning: Logo not found at {logo_path}. Please ensure it's at src/logo/helwan-insight.png")
            # يمكن إضافة أيقونة احتياطية هنا لو اللوجو مش موجود
        # ----------------------------------------------------

        self.df = None
        self.data_handler = None

        self.current_app_translator = None
        self.current_qt_translator = None

        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()

        self.retranslate_ui()
        self.set_status_bar_message(self._("Ready"))


    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget(self)
        self.main_layout.addWidget(self.stacked_widget)

        # تهيئة Data Preview Page
        self.data_preview_page = QWidget()
        data_preview_layout = QVBoxLayout(self.data_preview_page)
        
        self.data_preview_table = DataPreviewTable(parent=self) 
        data_preview_layout.addWidget(self.data_preview_table)
        self.stacked_widget.addWidget(self.data_preview_page)

        # تهيئة EDA Dashboard Page
        self.eda_dashboard_page = QWidget()
        eda_dashboard_layout = QVBoxLayout(self.eda_dashboard_page)
        
        self.eda_dashboard = EDADashboard(parent=self) 
        eda_dashboard_layout.addWidget(self.eda_dashboard)
        self.stacked_widget.addWidget(self.eda_dashboard_page)

        self.eda_dashboard.plot_requested.connect(self.handle_plot_request)

        self.stacked_widget.setCurrentWidget(self.data_preview_page)

    def setup_menu(self):
        menu_bar = self.menuBar()

        # 1. قائمة File
        self.file_menu = menu_bar.addMenu(self._("&File"))

        load_action = QAction(QIcon(), self._("&Load Data"), self)
        load_action.setToolTip(self._("Load data from a file"))
        load_action.setShortcut("Ctrl+L")
        load_action.triggered.connect(self.load_data)
        self.file_menu.addAction(load_action)

        # إضافة زر "View EDA Dashboard"
        view_eda_action = QAction(QIcon(), self._("&View EDA Dashboard"), self)
        view_eda_action.setToolTip(self._("Switch to the Exploratory Data Analysis Dashboard"))
        view_eda_action.setShortcut("Ctrl+E")
        view_eda_action.triggered.connect(self.show_eda_dashboard)
        self.file_menu.addAction(view_eda_action)

        # إضافة زر "Save Modified Data" (جديد)
        save_action = QAction(QIcon(), self._("&Save Modified Data"), self)
        save_action.setToolTip(self._("Save the current modified data to a new file"))
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_modified_data)
        self.file_menu.addAction(save_action)
        
        self.file_menu.addSeparator()

        # إضافة زر Save Plot as Image 
        save_plot_action = QAction(QIcon(), self._("Save Plot as &Image"), self)
        save_plot_action.setToolTip(self._("Save the current displayed plot as an image (PNG)"))
        save_plot_action.setShortcut("Ctrl+P")
        save_plot_action.triggered.connect(self.save_current_plot_as_image)
        self.file_menu.addAction(save_plot_action)

        exit_action = QAction(QIcon(), self._("E&xit"), self)
        exit_action.setToolTip(self._("Exit the application"))
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # 2. قائمة Data 
        self.data_menu = menu_bar.addMenu(self._("&Data"))
        
        # إضافة خيار "Handle Missing Values"
        handle_missing_action = QAction(QIcon(), self._("&Handle Missing Values"), self)
        handle_missing_action.setToolTip(self._("Handle missing values in the dataset"))
        handle_missing_action.triggered.connect(self.show_missing_values_dialog)
        self.data_menu.addAction(handle_missing_action)

        # إضافة خيار "Drop Duplicates"
        drop_duplicates_action = QAction(QIcon(), self._("&Drop Duplicates"), self)
        drop_duplicates_action.setToolTip(self._("Remove duplicate rows from the dataset"))
        drop_duplicates_action.triggered.connect(self.drop_duplicates_data)
        self.data_menu.addAction(drop_duplicates_action)

        # إضافة خيار "Change Column Type"
        change_type_action = QAction(QIcon(), self._("&Change Column Type"), self)
        change_type_action.setToolTip(self._("Change the data type of a selected column"))
        change_type_action.triggered.connect(self.show_change_column_type_dialog)
        self.data_menu.addAction(change_type_action)

        # إضافة خيار "Rename Column"
        rename_column_action = QAction(QIcon(), self._("&Rename Column"), self)
        rename_column_action.setToolTip(self._("Rename a selected column"))
        rename_column_action.triggered.connect(self.show_rename_column_dialog)
        self.data_menu.addAction(rename_column_action)

        # إضافة زر Generate Pair Plot 
        generate_pair_plot_action = QAction(QIcon(), self._("&Generate Pair Plot"), self)
        generate_pair_plot_action.setToolTip(self._("Generate a pair plot for numerical variables"))
        generate_pair_plot_action.triggered.connect(self.generate_pair_plot)
        self.data_menu.addAction(generate_pair_plot_action)


        # 3. قائمة Language كـ Submenu داخل File
        self.language_menu = self.file_menu.addMenu(self._("Language"))

        ar_action = QAction("العربية", self)
        ar_action.triggered.connect(lambda: self.change_language("ar"))
        self.language_menu.addAction(ar_action)

        en_action = QAction("English", self)
        en_action.triggered.connect(lambda: self.change_language("en"))
        self.language_menu.addAction(en_action)

        # 4. قائمة Help
        self.help_menu = menu_bar.addMenu(self._("&Help"))

        about_action = QAction(QIcon(), self._("&About"), self)
        about_action.setToolTip(self._("Show information about Helwan-Insight"))
        about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(about_action)

    def setup_status_bar(self):
        self.status_bar = self.statusBar()
        self.status_label = QLabel(self._("Ready"))
        self.status_bar.addWidget(self.status_label)

    def set_status_bar_message(self, message: str):
        self.status_label.setText(message)

    def load_data(self):
        self.set_status_bar_message(self._("Loading data... Please wait."))
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self._("Load Data File"),
            "",
            self._("Data Files (*.csv *.xlsx *.xls);;All Files (*)")
        )
        if file_path:
            try:
                self.data_handler = DataHandler(file_path)
                self.df = self.data_handler.load_data()
                
                self.data_preview_table.set_data(self.df)
                self.eda_dashboard.set_data(self.df, self.data_handler)

                self.stacked_widget.setCurrentWidget(self.data_preview_page)
                self.set_status_bar_message(
                    self._("Data loaded successfully! Rows: {rows}, Columns: {cols}").format(
                        rows=self.df.shape[0], cols=self.df.shape[1]
                    )
                )
            except ValueError as e:
                QMessageBox.critical(self, self._("Unsupported File Type"), self._(str(e)))
                self.set_status_bar_message(self._("Error loading data."))
            except Exception as e:
                QMessageBox.critical(self, self._("Error"), self._("Failed to load data: {e}").format(e=e))
                self.set_status_bar_message(self._("Error loading data."))
        else:
            self.set_status_bar_message(self._("Ready"))

    def save_modified_data(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Data"), self._("Please load data first to save."))
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self._("Save Modified Data"),
            "modified_data.csv",
            self._("CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)")
        )

        if file_path:
            try:
                self.data_handler.save_data(file_path) 
                QMessageBox.information(self, self._("Success"), 
                                        self._("Data saved successfully to {path}").format(path=file_path))
                self.set_status_bar_message(self._("Data saved to {path}").format(path=file_path))
            except Exception as e:
                QMessageBox.critical(self, self._("Save Error"), 
                                     self._("Failed to save data: {e}").format(e=e))
                self.set_status_bar_message(self._("Error saving data."))
        else:
            self.set_status_bar_message(self._("Save operation cancelled."))

    def save_current_plot_as_image(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Plot to Save"), self._("Please load data and generate a plot first."))
            return
        
        if self.stacked_widget.currentWidget() != self.eda_dashboard_page:
            QMessageBox.warning(self, self._("Not on Plot Page"), 
                                self._("Please navigate to the EDA Dashboard where the plot is displayed to save it."))
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            self._("Save Plot as Image"),
            "plot.png", 
            self._("PNG Image (*.png);;All Files (*)")
        )

        if file_path:
            try:
                self.eda_dashboard.plot_area.save_plot_as_image(file_path)
                QMessageBox.information(self, self._("Success"), 
                                        self._("Plot saved successfully to {path}").format(path=file_path))
                self.set_status_bar_message(self._("Plot saved to {path}").format(path=file_path))
            except Exception as e:
                QMessageBox.critical(self, self._("Save Error"), 
                                     self._("Failed to save plot: {e}").format(e=e))
                self.set_status_bar_message(self._("Error saving plot."))
        else:
            self.set_status_bar_message(self._("Save plot operation cancelled."))

    def show_eda_dashboard(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data Loaded"), self._("Please load a data file first to view the EDA Dashboard."))
            return
        if self.stacked_widget.indexOf(self.eda_dashboard_page) == -1:
            self.stacked_widget.addWidget(self.eda_dashboard_page)
        self.stacked_widget.setCurrentWidget(self.eda_dashboard_page)


    def handle_plot_request(self, plot_type: str, column: str, df: pd.DataFrame):
        if plot_type == 'heatmap':
            self.eda_dashboard.plot_area.plot_data(plot_type, None, df) 
        else:
            self.eda_dashboard.plot_area.plot_data(plot_type, column, df)
        
        if self.stacked_widget.indexOf(self.eda_dashboard_page) == -1:
            self.stacked_widget.addWidget(self.eda_dashboard_page)
        self.stacked_widget.setCurrentWidget(self.eda_dashboard_page)

    def show_about_dialog(self):
        QMessageBox.about(self, self._("About Helwan-Insight"),
                          self._("Helwan-Insight is a data analysis tool developed with PyQt5 and Pandas."))

    def apply_translation(self, locale_code: str):
        app = QApplication.instance()
        if not app:
            return

        if self.current_qt_translator and app.removeTranslator(self.current_qt_translator):
            self.current_qt_translator = None
        
        # Reload the main application translator
        # Assuming you have a setup_translation function in utils.i18n
        from utils.i18n import setup_translation
        self.current_app_translator = setup_translation(locale_code, "helwan_insight")
        
        if isinstance(self.current_app_translator, gettext.GNUTranslations):
            self._ = self.current_app_translator.gettext
        else:
            self._ = lambda text: text # Fallback if gettext translation not loaded

        # Reload Qt's own translator for standard dialogs
        self.current_qt_translator = QTranslator()
        qt_locale_name = QLocale(locale_code).name()
        if self.current_qt_translator.load("qt_" + qt_locale_name, QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
            app.installTranslator(self.current_qt_translator)
        else:
            print(f"Warning: Failed to load Qt translator for locale: {qt_locale_name}")

        self.retranslate_ui()

    def change_language(self, locale_code: str):
        self.apply_translation(locale_code)
        QMessageBox.information(self, self._("Language Change"),
                                self._("The language will be applied. Some elements might require a restart to fully update."))

    def show_missing_values_dialog(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Data"), self._("Please load data first to handle missing values."))
            return

        dialog = MissingValuesDialog(self.data_handler.get_column_names(), 
                                     self.data_handler.get_numerical_columns(), 
                                     self.data_handler.get_categorical_columns(),
                                     self._, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            strategy_type, column_to_affect, fill_value = dialog.get_selected_options()
            
            try:
                processed_count = 0
                if strategy_type == 'drop_rows_all':
                    processed_count = self.data_handler.handle_missing_values('drop_rows')
                    QMessageBox.information(self, self._("Success"), 
                                            self._("Successfully dropped {count} rows with any missing values.").format(count=processed_count))
                elif strategy_type == 'drop_rows_selected':
                    if column_to_affect in ["numerical_cols_only", "categorical_cols_only", "all_cols_any_type"]:
                        QMessageBox.warning(self, self._("Invalid Selection"), self._("Please select a specific column for 'Drop Rows (selected column only)' strategy."))
                        return
                    processed_count = self.data_handler.handle_missing_values('drop_rows', column=column_to_affect)
                    QMessageBox.information(self, self._("Success"), 
                                            self._("Successfully dropped {count} rows with missing values in column '{column}'.").format(count=processed_count, column=column_to_affect))
                
                elif strategy_type == 'fill_mean':
                    if column_to_affect == "numerical_cols_only":
                        numerical_cols = self.data_handler.get_numerical_columns()
                        for col in numerical_cols:
                            processed_count += self.data_handler.handle_missing_values('fill_mean', column=col)
                        QMessageBox.information(self, self._("Success"), 
                                                self._("Successfully filled missing values with mean in {count} numerical cells.").format(count=processed_count))
                    elif column_to_affect in ["categorical_cols_only", "all_cols_any_type"]:
                        QMessageBox.warning(self.parent, self._("Invalid Column Type"), self._("Mean filling is only applicable to numerical columns."))
                        return
                    else: # عمود محدد
                        processed_count = self.data_handler.handle_missing_values('fill_mean', column=column_to_affect)
                        QMessageBox.information(self, self._("Success"), 
                                                self._("Successfully filled {count} missing values in column '{column}' with mean.").format(count=processed_count, column=column_to_affect))

                elif strategy_type == 'fill_median':
                    if column_to_affect == "numerical_cols_only":
                        numerical_cols = self.data_handler.get_numerical_columns()
                        for col in numerical_cols:
                            processed_count += self.data_handler.handle_missing_values('fill_median', column=col)
                        QMessageBox.information(self, self._("Success"), 
                                                self._("Successfully filled missing values with median in {count} numerical cells.").format(count=processed_count))
                    elif column_to_affect in ["categorical_cols_only", "all_cols_any_type"]:
                        QMessageBox.warning(self.parent, self._("Invalid Column Type"), self._("Median filling is only applicable to numerical columns."))
                        return
                    else: # عمود محدد
                        processed_count = self.data_handler.handle_missing_values('fill_median', column=column_to_affect)
                        QMessageBox.information(self, self._("Success"), 
                                                self._("Successfully filled {count} missing values in column '{column}' with median.").format(count=processed_count, column=column_to_affect))
                
                elif strategy_type == 'fill_mode':
                    target_cols = []
                    if column_to_affect == "numerical_cols_only":
                        target_cols = self.data_handler.get_numerical_columns()
                    elif column_to_affect == "categorical_cols_only":
                        target_cols = self.data_handler.get_categorical_columns()
                    elif column_to_affect == "all_cols_any_type":
                         QMessageBox.warning(self.parent, self._("Invalid Selection"), self._("Mode filling requires selecting specific column types or a single column."))
                         return
                    else: # عمود محدد
                        target_cols = [column_to_affect]

                    for col in target_cols:
                        processed_count += self.data_handler.handle_missing_values('fill_mode', column=col)
                    QMessageBox.information(self, self._("Success"), 
                                            self._("Successfully filled missing values with mode in {count} cells.").format(count=processed_count))

                elif strategy_type == 'fill_value':
                    if not fill_value:
                        QMessageBox.warning(self.parent, self._("Missing Value"), self._("Please enter a value to fill with."))
                        return
                    
                    target_cols = []
                    if column_to_affect == "numerical_cols_only":
                        target_cols = self.data_handler.get_numerical_columns()
                    elif column_to_affect == "categorical_cols_only":
                        target_cols = self.data_handler.get_categorical_columns()
                    elif column_to_affect == "all_cols_any_type":
                         QMessageBox.warning(self.parent, self._("Invalid Selection"), self._("Filling with specific value requires selecting specific column types or a single column."))
                         return
                    else: # عمود محدد
                        target_cols = [column_to_affect]

                    for col in target_cols:
                        processed_count += self.data_handler.handle_missing_values('fill_value', column=col, fill_value=fill_value)
                    QMessageBox.information(self, self._("Success"), 
                                            self._("Successfully filled missing values with '{value}' in {count} cells.").format(value=fill_value, count=processed_count))

                # تحديث الواجهة بعد المعالجة
                self.df = self.data_handler.get_dataframe()
                self.data_preview_table.set_data(self.df)
                self.eda_dashboard.set_data(self.df, self.data_handler)

            except ValueError as e:
                QMessageBox.warning(self, self._("Error"), self._(str(e)))
            except Exception as e:
                QMessageBox.critical(self, self._("Processing Error"), self._("An unexpected error occurred: {e}").format(e=e))

    def drop_duplicates_data(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Data"), self._("Please load data first to remove duplicates."))
            return
        
        try:
            removed_count = self.data_handler.drop_duplicates()
            if removed_count > 0:
                QMessageBox.information(self, self._("Success"), 
                                        self._("Successfully removed {count} duplicate rows.").format(count=removed_count))
                self.df = self.data_handler.get_dataframe()
                self.data_preview_table.set_data(self.df)
                self.eda_dashboard.set_data(self.df, self.data_handler)
            else:
                QMessageBox.information(self, self._("No Duplicates"), self._("No duplicate rows found."))
        except ValueError as e:
            QMessageBox.warning(self, self._("Error"), self._(str(e)))
        except Exception as e:
            QMessageBox.critical(self, self._("Processing Error"), self._("An unexpected error occurred: {e}").format(e=e))

    def show_change_column_type_dialog(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Data"), self._("Please load data first to change column type."))
            return

        dialog = ChangeColumnTypeDialog(self.data_handler.get_column_names(), self._, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            column, new_type = dialog.get_selected_options()
            
            if not column or not new_type:
                QMessageBox.warning(self, self._("Missing Information"), self._("Please select a column and a new type."))
                return

            try:
                self.data_handler.change_column_type(column, new_type)
                QMessageBox.information(self, self._("Success"), 
                                        self._("Column '{column}' successfully converted to {new_type_display}.").format(
                                            column=column, new_type_display=dialog.type_combo.currentText()))
                self.df = self.data_handler.get_dataframe()
                self.data_preview_table.set_data(self.df)
                self.eda_dashboard.set_data(self.df, self.data_handler)
            except ValueError as e:
                translated_error_message = self._(str(e))
                QMessageBox.warning(self, self._("Error"), translated_error_message)
            except Exception as e:
                QMessageBox.critical(self, self._("Processing Error"), self._("An unexpected error occurred: {e}").format(e=e))

    def show_rename_column_dialog(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Data"), self._("Please load data first to rename columns."))
            return

        dialog = RenameColumnDialog(self.data_handler.get_column_names(), self._, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            old_name, new_name = dialog.get_selected_options()
            
            if not old_name or not new_name:
                QMessageBox.warning(self, self._("Missing Information"), self._("Please select a column and enter a new name."))
                return
            if old_name == new_name:
                QMessageBox.information(self, self._("No Change"), self._("The new column name is the same as the old name."))
                return

            try:
                self.data_handler.rename_column(old_name, new_name)
                QMessageBox.information(self, self._("Success"), 
                                        self._("Column '{old_name}' successfully renamed to '{new_name}'.").format(old_name=old_name, new_name=new_name))
                self.df = self.data_handler.get_dataframe()
                self.data_preview_table.set_data(self.df)
                self.eda_dashboard.set_data(self.df, self.data_handler)
            except ValueError as e:
                QMessageBox.warning(self, self._("Error"), self._(str(e)))
            except Exception as e:
                QMessageBox.critical(self, self._("Processing Error"), self._("An unexpected error occurred: {e}").format(e=e))

    def generate_pair_plot(self):
        if self.df is None:
            QMessageBox.warning(self, self._("No Data"), self._("Please load data first to generate a pair plot."))
            return

        numerical_cols = self.data_handler.get_numerical_columns()
        if not numerical_cols:
            QMessageBox.warning(self.parent, self._("No Numerical Data"), self._("No numerical columns found to generate a pair plot."))
            return
        
        self.eda_dashboard.plot_area.plot_data('pairplot', None, self.df) 
        
        self.stacked_widget.setCurrentWidget(self.eda_dashboard_page)
        self.set_status_bar_message(self._("Generated Pair Plot."))

    def retranslate_ui(self):
        self.setWindowTitle(self._("Helwan-Insight - Data Analysis Tool"))

        self.file_menu.setTitle(self._("&File"))
        self.data_menu.setTitle(self._("&Data"))
        self.help_menu.setTitle(self._("&Help"))

        for action in self.file_menu.actions():
            original_text_key = action.text().replace("&", "")
            if original_text_key == "Load Data":
                action.setText(self._("&Load Data"))
                action.setToolTip(self._("Load data from a file"))
            elif original_text_key == "View EDA Dashboard":
                action.setText(self._("&View EDA Dashboard"))
                action.setToolTip(self._("Switch to the Exploratory Data Analysis Dashboard"))
            elif original_text_key == "Save Modified Data":
                action.setText(self._("&Save Modified Data"))
                action.setToolTip(self._("Save the current modified data to a new file"))
            elif original_text_key == "Save Plot as Image":
                action.setText(self._("Save Plot as &Image"))
                action.setToolTip(self._("Save the current displayed plot as an image (PNG)"))
            elif original_text_key == "Exit":
                action.setText(self._("E&xit"))
                action.setToolTip(self._("Exit the application"))
            elif original_text_key == "Language":
                action.setText(self._("Language"))

        # ترجمة قائمة Data
        for action in self.data_menu.actions():
            original_text_key = action.text().replace("&", "")
            if original_text_key == "Handle Missing Values":
                action.setText(self._("&Handle Missing Values"))
                action.setToolTip(self._("Handle missing values in the dataset"))
            elif original_text_key == "Drop Duplicates":
                action.setText(self._("&Drop Duplicates"))
                action.setToolTip(self._("Remove duplicate rows from the dataset"))
            elif original_text_key == "Change Column Type":
                action.setText(self._("&Change Column Type"))
                action.setToolTip(self._("Change the data type of a selected column"))
            elif original_text_key == "Rename Column":
                action.setText(self._("&Rename Column"))
                action.setToolTip(self._("Rename a selected column"))
            elif original_text_key == "Generate Pair Plot":
                action.setText(self._("&Generate Pair Plot"))
                action.setToolTip(self._("Generate a pair plot for numerical variables"))


        for action in self.help_menu.actions():
            if action.text().replace("&", "") == "About":
                action.setText(self._("&About"))
                action.setToolTip(self._("Show information about Helwan-Insight"))

        self.status_label.setText(self._("Ready"))

        if self.eda_dashboard:
            self.eda_dashboard.retranslate_ui()
        if self.data_preview_table:
            self.data_preview_table.retranslate_ui()

        if isinstance(QApplication.activeModalWidget(), MissingValuesDialog):
            dialog = QApplication.activeModalWidget()
            dialog.setWindowTitle(self._("Handle Missing Values"))
            dialog.layout.labelForField(dialog.column_combo).setText(self._("Select Column:"))
            dialog.column_combo.setItemText(0, self._("All Numerical Columns"))
            dialog.column_combo.setItemText(1, self._("All Categorical Columns"))
            dialog.column_combo.setItemText(2, self._("All Columns (Any Type)"))
            current_columns_count = dialog.column_combo.count() - 3
            actual_df_cols = self.data_handler.get_column_names() if self.data_handler else []
            for i in range(len(actual_df_cols)):
                if i + 3 < current_columns_count:
                     dialog.column_combo.setItemText(i + 3, actual_df_cols[i])
                else:
                    dialog.column_combo.addItem(actual_df_cols[i])

            dialog.layout.labelForField(dialog.strategy_combo).setText(self._("Select Strategy:"))
            dialog.strategy_combo.setItemText(0, self._("Drop Rows (any missing)"))
            dialog.strategy_combo.setItemText(1, self._("Drop Rows (selected column only)"))
            dialog.strategy_combo.setItemText(2, self._("Fill with Mean"))
            dialog.strategy_combo.setItemText(3, self._("Fill with Median"))
            dialog.strategy_combo.setItemText(4, self._("Fill with Mode"))
            dialog.strategy_combo.setItemText(5, self._("Fill with Specific Value"))
            dialog.fill_value_input.setPlaceholderText(self._("Enter value to fill with"))

        if isinstance(QApplication.activeModalWidget(), ChangeColumnTypeDialog):
            dialog = QApplication.activeModalWidget()
            dialog.setWindowTitle(self._("Change Column Type"))
            dialog.layout.labelForField(dialog.column_combo).setText(self._("Select Column:"))
            current_columns_count = dialog.column_combo.count()
            actual_df_cols = self.data_handler.get_column_names() if self.data_handler else []
            dialog.column_combo.clear()
            dialog.column_combo.addItems(actual_df_cols)

            dialog.layout.labelForField(dialog.type_combo).setText(self._("New Type:"))
            dialog.type_combo.setItemText(0, self._("Integer"))
            dialog.type_combo.setItemText(1, self._("Float"))
            dialog.type_combo.setItemText(2, self._("Text"))
            dialog.type_combo.setItemText(3, self._("Date/Time"))
        
        if isinstance(QApplication.activeModalWidget(), RenameColumnDialog):
            dialog = QApplication.activeModalWidget()
            dialog.setWindowTitle(self._("Rename Column"))
            dialog.layout.labelForField(dialog.column_combo).setText(self._("Select Column:"))
            current_columns_count = dialog.column_combo.count()
            actual_df_cols = self.data_handler.get_column_names() if self.data_handler else []
            dialog.column_combo.clear()
            dialog.column_combo.addItems(actual_df_cols)

            dialog.layout.labelForField(dialog.new_name_input).setText(self._("New Name:"))
            dialog.new_name_input.setPlaceholderText(self._("Enter new column name"))
        
        if isinstance(QApplication.activeModalWidget(), StatisticsDialog):
            dialog = QApplication.activeModalWidget()
            dialog.retranslate_ui()
