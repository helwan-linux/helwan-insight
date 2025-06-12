import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QStackedWidget, QSizePolicy, QScrollArea,
    QMessageBox, QListWidget, QAbstractItemView, QGroupBox, QTextEdit, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QClipboard

from ui.widgets.visualization import PlotArea
from core.data_handler import DataHandler
from ui.dialogs.statistics_dialog import StatisticsDialog

class EDADashboard(QWidget):
    plot_requested = pyqtSignal(str, str, pd.DataFrame)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # Get the translator function from the parent (MainWindow)
        self._ = parent._ if parent and hasattr(parent, '_') else lambda text: text

        self.df = None
        self.data_handler = None

        self.setup_ui()
        self.retranslate_ui()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)

        # Left Panel: Controls for EDA
        self.control_panel = QWidget()
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_panel.setFixedWidth(250) # Fixed width for control panel

        # Column Selection for general plots
        self.column_label = QLabel(self._("Select Column:"))
        self.column_combo = QComboBox()
        self.column_combo.currentIndexChanged.connect(self.on_column_selected)
        self.control_layout.addWidget(self.column_label)
        self.control_layout.addWidget(self.column_combo)

        # Plot Type Selection 
        self.plot_type_label = QLabel(self._("Select Plot Type:"))
        self.plot_type_combo = QComboBox()
        # Default items, will be updated based on column type
        self.plot_type_combo.addItems([
            self._("Histogram"),
            self._("Bar Chart"),
            self._("Box Plot"),
            self._("Scatter Plot"),
            self._("Line Plot"),
            self._("Pie Chart"),
            self._("Violin Plot")
        ])
        self.control_layout.addWidget(self.plot_type_label)
        self.control_layout.addWidget(self.plot_type_combo)

        # Generate Plot Button
        self.generate_plot_button = QPushButton(self._("Generate Plot"))
        self.generate_plot_button.clicked.connect(self.generate_plot)
        self.control_layout.addWidget(self.generate_plot_button)

        # Generate Heatmap Button
        self.generate_heatmap_button = QPushButton(self._("Generate Correlation Heatmap"))
        self.generate_heatmap_button.clicked.connect(self.generate_heatmap)
        self.control_layout.addWidget(self.generate_heatmap_button)


        # Statistical Analysis Section (Basic Statistics)
        self.statistical_analysis_group_box = QGroupBox(self._("Descriptive Statistics"))
        self.statistical_analysis_layout = QVBoxLayout(self.statistical_analysis_group_box)

        self.stat_column_label = QLabel(self._("Select Columns for Statistics:"))
        self.stat_column_list = QListWidget() 
        self.stat_column_list.setSelectionMode(QAbstractItemView.MultiSelection) # Allow multiple selections
        self.statistical_analysis_layout.addWidget(self.stat_column_label)
        self.statistical_analysis_layout.addWidget(self.stat_column_list)

        self.generate_stats_button = QPushButton(self._("Generate Statistics"))
        self.generate_stats_button.clicked.connect(self.generate_statistics)
        self.statistical_analysis_layout.addWidget(self.generate_stats_button)

        self.control_layout.addWidget(self.statistical_analysis_group_box)

        # Advanced Statistical Tests Section
        self.advanced_analysis_group_box = QGroupBox(self._("Advanced Statistical Tests"))
        self.advanced_analysis_layout = QVBoxLayout(self.advanced_analysis_group_box)

        self.test_type_label = QLabel(self._("Select Test Type:"))
        self.test_type_combo = QComboBox()
        self.test_type_combo.addItems([
            self._("Independent Samples T-Test"),
            self._("Chi-Square Test")
        ])
        self.test_type_combo.currentIndexChanged.connect(self.on_test_type_selected) # Update column combos based on test type
        self.advanced_analysis_layout.addWidget(self.test_type_label)
        self.advanced_analysis_layout.addWidget(self.test_type_combo)

        self.test_column1_label = QLabel(self._("Select Column 1:"))
        self.test_column1_combo = QComboBox()
        self.advanced_analysis_layout.addWidget(self.test_column1_label)
        self.advanced_analysis_layout.addWidget(self.test_column1_combo)

        self.test_column2_label = QLabel(self._("Select Column 2:"))
        self.test_column2_combo = QComboBox()
        self.advanced_analysis_layout.addWidget(self.test_column2_label)
        self.advanced_analysis_layout.addWidget(self.test_column2_combo)

        self.perform_test_button = QPushButton(self._("Perform Test"))
        self.perform_test_button.clicked.connect(self.perform_statistical_test)
        self.advanced_analysis_layout.addWidget(self.perform_test_button)

        self.control_layout.addWidget(self.advanced_analysis_group_box)

        # Correlation Analysis Section
        self.correlation_group_box = QGroupBox(self._("Correlation Analysis"))
        self.correlation_layout = QVBoxLayout(self.correlation_group_box)
        self.generate_correlation_button = QPushButton(self._("Generate Correlation Matrix"))
        self.generate_correlation_button.clicked.connect(self.generate_correlation_matrix)
        self.correlation_layout.addWidget(self.generate_correlation_button)
        self.control_layout.addWidget(self.correlation_group_box)

        # Outlier Analysis Section
        self.outlier_group_box = QGroupBox(self._("Outlier Analysis (IQR Method)"))
        self.outlier_layout = QVBoxLayout(self.outlier_group_box)

        self.outlier_column_label = QLabel(self._("Select Numerical Column:"))
        self.outlier_column_combo = QComboBox()
        self.outlier_layout.addWidget(self.outlier_column_label)
        self.outlier_layout.addWidget(self.outlier_column_combo)

        self.detect_outliers_button = QPushButton(self._("Detect Outliers"))
        self.detect_outliers_button.clicked.connect(self.detect_outliers)
        self.outlier_layout.addWidget(self.detect_outliers_button)

        self.outlier_handle_label = QLabel(self._("Handle Outliers:"))
        self.outlier_handle_combo = QComboBox()
        self.outlier_handle_combo.addItems([
            self._("Remove Outlier Rows"),
            self._("Replace with Median"),
            self._("Replace with Mean")
        ])
        self.outlier_layout.addWidget(self.outlier_handle_label)
        self.outlier_layout.addWidget(self.outlier_handle_combo)

        self.apply_outlier_handle_button = QPushButton(self._("Apply Outlier Handling"))
        self.apply_outlier_handle_button.clicked.connect(self.apply_outlier_handling)
        self.outlier_layout.addWidget(self.apply_outlier_handle_button)

        self.control_layout.addWidget(self.outlier_group_box)
        
        self.control_layout.addStretch(1) # Pushes all widgets to the top

        self.main_layout.addWidget(self.control_panel)

        # Right Panel: Plot Area
        self.plot_area = PlotArea(parent=self)
        self.main_layout.addWidget(self.plot_area)

    def set_data(self, df: pd.DataFrame, data_handler: DataHandler):
        self.df = df
        self.data_handler = data_handler
        self.update_column_combo()
        self.update_stat_column_list()
        self.update_test_column_combos()
        self.update_outlier_column_combo() # Update outlier column combo

    def update_column_combo(self):
        self.column_combo.clear()
        if self.df is not None:
            self.column_combo.addItems(self.data_handler.get_column_names())
            if self.column_combo.count() > 0:
                self.on_column_selected(0) # Trigger update of plot type options

    def update_stat_column_list(self):
        self.stat_column_list.clear()
        if self.df is not None:
            numerical_cols = self.data_handler.get_numerical_columns()
            for col in numerical_cols:
                self.stat_column_list.addItem(col)

    def update_test_column_combos(self):
        self.test_column1_combo.clear()
        self.test_column2_combo.clear()
        if self.df is not None:
            all_cols = self.data_handler.get_column_names()
            self.test_column1_combo.addItems(all_cols)
            self.test_column2_combo.addItems(all_cols)
            # Ensure the correct labels and items are shown based on the current test type
            self.on_test_type_selected(self.test_type_combo.currentIndex()) 

    def update_outlier_column_combo(self):
        self.outlier_column_combo.clear()
        if self.df is not None:
            numerical_cols = self.data_handler.get_numerical_columns()
            self.outlier_column_combo.addItems(numerical_cols)

    def on_column_selected(self, index):
        if self.df is None or index < 0:
            return 

        column_name = self.column_combo.currentText()
        if column_name:
            col_data = self.df[column_name]
            self.update_plot_type_options(column_name)

    def update_plot_type_options(self, column_name: str):
        if self.df is None:
            return

        col_data = self.df[column_name]
        col_type = self.data_handler.detect_column_type(col_data)
        
        self.plot_type_combo.clear()
        if col_type == "Numerical":
            self.plot_type_combo.addItems([
                self._("Histogram"), 
                self._("Box Plot"), 
                self._("Violin Plot"), 
                self._("Scatter Plot"),
                self._("Line Plot")
            ])
        elif col_type == "Categorical":
            self.plot_type_combo.addItems([
                self._("Bar Chart"), 
                self._("Pie Chart")
            ])
        elif col_type == "Date":
            self.plot_type_combo.addItems([
                self._("Line Plot")
            ])
        else:
            self.plot_type_combo.addItems([self._("No Supported Plots")])

    def generate_plot(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first."))
            return

        column_name = self.column_combo.currentText()
        plot_type_display = self.plot_type_combo.currentText()

        # Map display text to internal plot type identifiers
        plot_type_map = {
            self._("Histogram"): 'histogram',
            self._("Bar Chart"): 'bar',
            self._("Box Plot"): 'boxplot',
            self._("Scatter Plot"): 'scatter',
            self._("Line Plot"): 'line',
            self._("Pie Chart"): 'pie',
            self._("Violin Plot"): 'violin'
        }
        plot_type = plot_type_map.get(plot_type_display)

        if plot_type is None:
            QMessageBox.warning(self.parent, self._("Unsupported Plot Type"), 
                                self._("The selected plot type is not supported for this column type or is not recognized."))
            return

        if not column_name:
            QMessageBox.warning(self.parent, self._("Missing Information"), self._("Please select a column."))
            return
        
        # Specific check for Violin plot requiring numerical data
        if plot_type == 'violin' and not self.data_handler.detect_column_type(self.df[column_name]) == "Numerical":
             QMessageBox.warning(self.parent, self._("Plot Error"), self._("Violin plot requires a numerical column."))
             return

        self.plot_requested.emit(plot_type, column_name, self.df)

    def generate_heatmap(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first to generate a heatmap."))
            return

        numerical_cols = self.data_handler.get_numerical_columns()
        if not numerical_cols:
            QMessageBox.warning(self.parent, self._("No Numerical Data"), self._("No numerical columns found to generate a heatmap."))
            return

        self.plot_requested.emit('heatmap', None, self.df)

    def generate_statistics(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first to generate statistics."))
            return

        selected_items = self.stat_column_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.parent, self._("No Columns Selected"), self._("Please select at least one column for statistics."))
            return

        selected_columns = [item.text() for item in selected_items]

        try:
            stats_df = self.data_handler.get_basic_statistics(selected_columns)
            
            dialog = StatisticsDialog(stats_df, self._, parent=self.parent)
            dialog.exec_()

        except ValueError as e:
            QMessageBox.warning(self.parent, self._("Error"), self._(str(e)))
        except Exception as e:
            QMessageBox.critical(self.parent, self._("Statistical Analysis Error"), 
                                 self._("An unexpected error occurred during statistical analysis: {e}").format(e=e))

    def on_test_type_selected(self, index):
        test_type = self.test_type_combo.currentText()
        all_cols = self.data_handler.get_column_names() if self.data_handler and self.df is not None else []
        numerical_cols = self.data_handler.get_numerical_columns() if self.data_handler and self.df is not None else []
        categorical_cols = self.data_handler.get_categorical_columns() if self.data_handler and self.df is not None else []

        self.test_column1_combo.clear()
        self.test_column2_combo.clear()

        if test_type == self._("Independent Samples T-Test"):
            self.test_column1_combo.addItems(numerical_cols)
            self.test_column2_combo.addItems(numerical_cols)
            self.test_column1_label.setText(self._("Select Numerical Column 1:"))
            self.test_column2_label.setText(self._("Select Numerical Column 2:"))
        elif test_type == self._("Chi-Square Test"):
            self.test_column1_combo.addItems(categorical_cols)
            self.test_column2_combo.addItems(categorical_cols)
            self.test_column1_label.setText(self._("Select Categorical Column 1:"))
            self.test_column2_label.setText(self._("Select Categorical Column 2:"))
        else: # Fallback, should not happen if combo box items are well-defined
            self.test_column1_combo.addItems(all_cols)
            self.test_column2_combo.addItems(all_cols)
            self.test_column1_label.setText(self._("Select Column 1:"))
            self.test_column2_label.setText(self._("Select Column 2:"))

    def perform_statistical_test(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first to perform a test."))
            return

        test_type_display = self.test_type_combo.currentText()
        column1 = self.test_column1_combo.currentText()
        column2 = self.test_column2_combo.currentText()

        if not column1 or not column2:
            QMessageBox.warning(self.parent, self._("Missing Information"), self._("Please select two columns for the test."))
            return
        
        if column1 == column2:
            QMessageBox.warning(self.parent, self._("Invalid Selection"), self._("Please select two different columns for the test."))
            return

        test_result = None
        try:
            if test_type_display == self._("Independent Samples T-Test"):
                test_result = self.data_handler.perform_t_test(column1, column2)
            elif test_type_display == self._("Chi-Square Test"):
                test_result = self.data_handler.perform_chi_square_test(column1, column2)
            else:
                QMessageBox.warning(self.parent, self._("Unsupported Test"), self._("Selected test type is not supported."))
                return

            if test_result:
                dialog = StatisticsDialog(None, self._, parent=self.parent) # Pass None for DataFrame, as we use QTextEdit
                dialog.setWindowTitle(self._(test_result["test_type"]))
                
                result_text = []
                result_text.append(f"{self._('Test Type')}: {self._(test_result['test_type'])}")
                result_text.append(f"{self._('Column 1')}: {test_result['column1']}")
                result_text.append(f"{self._('Column 2')}: {test_result['column2']}")
                
                if test_type_display == self._("Independent Samples T-Test"):
                    result_text.append(f"{self._('T-Statistic')}: {test_result['t_statistic']:.4f}")
                    result_text.append(f"{self._('P-Value')}: {test_result['p_value']:.4f}")
                elif test_type_display == self._("Chi-Square Test"):
                    result_text.append(f"{self._('Chi2 Statistic')}: {test_result['chi2_statistic']:.4f}")
                    result_text.append(f"{self._('P-Value')}: {test_result['p_value']:.4f}")
                    result_text.append(f"{self._('Degrees of Freedom')}: {test_result['degrees_of_freedom']}")
                    result_text.append(f"\n{self._('Contingency Table')}:\n{test_result['contingency_table']}")
                    result_text.append(f"\n{self._('Expected Frequencies')}:\n{test_result['expected_frequencies']}")

                # Determine language for interpretation
                if self._("English") == "English": # Check if the translator function returns "English" for "English"
                    interpretation = test_result["interpretation"]["en"]
                elif self._("English") == "الإنجليزية": # Check if it returns the Arabic translation for "English"
                    interpretation = test_result["interpretation"]["ar"]
                else:
                    interpretation = test_result["interpretation"]["en"] # Fallback to English

                result_text.append(f"\n{self._('Interpretation')}:\n{interpretation}")
                
                dialog.table_widget.setVisible(False) # Hide the table widget for text-based results
                
                dialog.text_output = QTextEdit() # Create a QTextEdit for the result text
                dialog.text_output.setReadOnly(True)
                dialog.text_output.setText("\n".join(result_text))
                dialog.main_layout.insertWidget(0, dialog.text_output) # Insert at the top of the dialog's layout

                # Disconnect any old connections before connecting the new one for the copy button
                try:
                    dialog.copy_button.clicked.disconnect()
                except TypeError:
                    pass # No previous connection, ignore
                dialog.copy_button.clicked.connect(lambda: self.copy_text_to_clipboard(dialog.text_output.toPlainText()))
                dialog.retranslate_ui() # Retranslate dialog components after changing content

                dialog.exec_()

        except ValueError as e:
            QMessageBox.warning(self.parent, self._("Error"), self._(str(e)))
        except Exception as e:
            QMessageBox.critical(self.parent, self._("Statistical Test Error"), 
                                 self._("An unexpected error occurred during statistical test: {e}").format(e=e))

    def generate_correlation_matrix(self):
        """
        Generates and displays the correlation matrix for numerical columns.
        """
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first to generate correlation matrix."))
            return
        
        try:
            correlation_df = self.data_handler.get_correlation_matrix()
            
            if correlation_df.empty:
                QMessageBox.information(self.parent, self._("No Numerical Data"), self._("No numerical columns found to calculate correlation."))
                return

            dialog = StatisticsDialog(correlation_df, self._, parent=self.parent)
            dialog.setWindowTitle(self._("Correlation Matrix"))
            dialog.exec_()

        except ValueError as e:
            QMessageBox.warning(self.parent, self._("Error"), self._(str(e)))
        except Exception as e:
            QMessageBox.critical(self.parent, self._("Correlation Error"), 
                                 self._("An unexpected error occurred during correlation analysis: {e}").format(e=e))

    def detect_outliers(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first to detect outliers."))
            return

        column_name = self.outlier_column_combo.currentText()
        if not column_name:
            QMessageBox.warning(self.parent, self._("No Column Selected"), self._("Please select a column to detect outliers."))
            return
        
        try:
            outliers_df = self.data_handler.detect_outliers_iqr(column_name)
            
            if outliers_df.empty:
                QMessageBox.information(self.parent, self._("No Outliers"), self._("No outliers detected in the selected column using IQR method."))
                return

            dialog = StatisticsDialog(outliers_df, self._, parent=self.parent)
            dialog.setWindowTitle(self._(f"Outliers in '{column_name}'"))
            dialog.exec_()

        except ValueError as e:
            QMessageBox.warning(self.parent, self._("Error"), self._(str(e)))
        except Exception as e:
            QMessageBox.critical(self.parent, self._("Outlier Detection Error"), 
                                 self._("An unexpected error occurred during outlier detection: {e}").format(e=e))

    def apply_outlier_handling(self):
        if self.df is None:
            QMessageBox.warning(self.parent, self._("No Data"), self._("Please load data first to handle outliers."))
            return

        column_name = self.outlier_column_combo.currentText()
        if not column_name:
            QMessageBox.warning(self.parent, self._("No Column Selected"), self._("Please select a column to handle outliers."))
            return

        handle_method_display = self.outlier_handle_combo.currentText()
        method_map = {
            self._("Remove Outlier Rows"): 'remove',
            self._("Replace with Median"): 'median',
            self._("Replace with Mean"): 'mean'
        }
        method = method_map.get(handle_method_display)

        if method is None:
            QMessageBox.warning(self.parent, self._("Invalid Method"), self._("Please select a valid outlier handling method."))
            return

        try:
            rows_affected = self.data_handler.handle_outliers(column_name, method)
            if rows_affected > 0:
                QMessageBox.information(self.parent, self._("Outliers Handled"), 
                                        self._("{rows} outliers were handled in column '{col}' using '{method_display}' method.").format(
                                            rows=rows_affected, col=column_name, method_display=handle_method_display))
                # It's crucial to update data views after modifying the DataFrame
                if hasattr(self.parent, 'update_data_views'): 
                    self.parent.update_data_views() # This would trigger the main window to refresh the DataFrame display
                self.update_outlier_column_combo() # Refresh column list in case column types changed (unlikely for numerical outlier handling but good practice)
            else:
                QMessageBox.information(self.parent, self._("No Outliers"), 
                                        self._("No outliers were found or handled in column '{col}'.").format(col=column_name))

        except ValueError as e:
            QMessageBox.warning(self.parent, self._("Error"), self._(str(e)))
        except Exception as e:
            QMessageBox.critical(self.parent, self._("Outlier Handling Error"), 
                                 self._("An unexpected error occurred during outlier handling: {e}").format(e=e))

    def copy_text_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText(text)
        clipboard.setMimeData(mime_data)
        QMessageBox.information(self.parent, self._("Copied"), self._("Content copied to clipboard."))


    def retranslate_ui(self):
        self.column_label.setText(self._("Select Column:"))
        self.plot_type_label.setText(self._("Select Plot Type:"))
        self.generate_plot_button.setText(self._("Generate Plot"))
        self.generate_heatmap_button.setText(self._("Generate Correlation Heatmap"))
        
        # Re-populate plot type combo based on current column selection
        current_column_name = self.column_combo.currentText()
        if current_column_name and self.df is not None:
             self.update_plot_type_options(current_column_name)
        else: # Fallback to default items if no column is selected or data is not loaded
            self.plot_type_combo.clear()
            self.plot_type_combo.addItems([
                self._("Histogram"),
                self._("Bar Chart"),
                self._("Box Plot"),
                self._("Scatter Plot"),
                self._("Line Plot"),
                self._("Pie Chart"),
                self._("Violin Plot")
            ])
        
        # Statistical Analysis Section
        self.statistical_analysis_group_box.setTitle(self._("Descriptive Statistics"))
        self.stat_column_label.setText(self._("Select Columns for Statistics:"))
        self.generate_stats_button.setText(self._("Generate Statistics"))

        # Re-populate column list for basic statistics
        self.stat_column_list.clear()
        if self.df is not None:
            numerical_cols = self.data_handler.get_numerical_columns()
            for col in numerical_cols:
                self.stat_column_list.addItem(self._(col))
        
        # Advanced Statistical Tests Section
        self.advanced_analysis_group_box.setTitle(self._("Advanced Statistical Tests"))
        self.test_type_label.setText(self._("Select Test Type:"))
        
        # Re-translate test type combo box items
        current_test_type_index = self.test_type_combo.currentIndex()
        self.test_type_combo.clear()
        self.test_type_combo.addItems([
            self._("Independent Samples T-Test"),
            self._("Chi-Square Test")
        ])
        if current_test_type_index != -1:
            self.test_type_combo.setCurrentIndex(current_test_type_index)
        
        # Re-translate column labels based on the current test type
        self.on_test_type_selected(self.test_type_combo.currentIndex())
        
        # Re-populate test column combos
        self.update_test_column_combos()

        self.perform_test_button.setText(self._("Perform Test"))

        # Correlation Analysis Section
        self.correlation_group_box.setTitle(self._("Correlation Analysis"))
        self.generate_correlation_button.setText(self._("Generate Correlation Matrix"))

        # Outlier Analysis Section
        self.outlier_group_box.setTitle(self._("Outlier Analysis (IQR Method)"))
        self.outlier_column_label.setText(self._("Select Numerical Column:"))
        self.detect_outliers_button.setText(self._("Detect Outliers"))
        self.outlier_handle_label.setText(self._("Handle Outliers:"))
        
        # Re-translate outlier handling methods combo box
        current_outlier_handle_index = self.outlier_handle_combo.currentIndex()
        self.outlier_handle_combo.clear()
        self.outlier_handle_combo.addItems([
            self._("Remove Outlier Rows"),
            self._("Replace with Median"),
            self._("Replace with Mean")
        ])
        if current_outlier_handle_index != -1:
            self.outlier_handle_combo.setCurrentIndex(current_outlier_handle_index)

        self.apply_outlier_handle_button.setText(self._("Apply Outlier Handling"))

        # Refresh outlier column combo
        self.update_outlier_column_combo()
