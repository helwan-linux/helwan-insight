import pandas as pd
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QMessageBox, QApplication, QTextEdit
)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QClipboard
import numpy as np

class StatisticsDialog(QDialog):
    def __init__(self, stats_df: pd.DataFrame, _translator_func, parent=None):
        super().__init__(parent)
        self._ = _translator_func # Store the translator function
        self.stats_df = stats_df
        self.text_output = None # This will hold the QTextEdit if text output is used

        self.setWindowTitle(self._("Descriptive Statistics")) # Default title
        self.setGeometry(150, 150, 800, 500) # Set a default size

        self.main_layout = QVBoxLayout(self)

        # QTableWidget for displaying DataFrames
        self.table_widget = QTableWidget()
        self.main_layout.addWidget(self.table_widget)

        # Buttons layout
        self.button_layout = QHBoxLayout()
        self.copy_button = QPushButton(self._("Copy to Clipboard"))
        self.copy_button.clicked.connect(self.copy_table_to_clipboard) # Default connection for table
        self.button_layout.addWidget(self.copy_button)
        
        self.close_button = QPushButton(self._("Close"))
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.main_layout.addLayout(self.button_layout)

        # Populate table if a DataFrame is provided
        if self.stats_df is not None:
            self.setup_table()
        else:
            self.table_widget.setVisible(False) # Hide table if no DataFrame is passed

        self.retranslate_ui() # Initial retranslation

    def setup_table(self):
        if self.stats_df is None or self.stats_df.empty:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            QMessageBox.information(self, self._("No Data"), self._("No data to display in the table."))
            return

        # Check if it's likely a correlation matrix based on shape and index/column names
        is_correlation_matrix = (self.stats_df.index.tolist() == self.stats_df.columns.tolist() and
                                 self.stats_df.shape[0] == self.stats_df.shape[1] and
                                 pd.api.types.is_numeric_dtype(self.stats_df.values)) # Ensure it's numerical values

        # Determine table dimensions and headers
        num_rows = self.stats_df.shape[0]
        num_cols = self.stats_df.shape[1] + 1 # +1 for the index/first column

        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_cols)

        if is_correlation_matrix:
            header_labels = [self._("Variable")] + self.stats_df.columns.tolist()
            self.setWindowTitle(self._("Correlation Matrix")) # Set specific title for correlation matrix
        else: # For descriptive statistics or other general DataFrames
            header_labels = [self._("Statistic")] + self.stats_df.columns.tolist()
            self.setWindowTitle(self._("Descriptive Statistics")) # Set default title for descriptive stats

        self.table_widget.setHorizontalHeaderLabels(header_labels)

        # Populate the table with data
        for i, (index_label, row_data) in enumerate(self.stats_df.iterrows()):
            # First column is the DataFrame index (e.g., 'mean', 'std', or column name for correlation)
            item_index = QTableWidgetItem(str(index_label))
            item_index.setFlags(item_index.flags() & ~Qt.ItemIsEditable) # Make index non-editable
            self.table_widget.setItem(i, 0, item_index)

            for j, value in enumerate(row_data):
                # Format numerical values to 4 decimal places for better readability
                if isinstance(value, (float, np.float64)):
                    formatted_value = f"{value:.4f}"
                else:
                    formatted_value = str(value)
                item = QTableWidgetItem(formatted_value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable) # Make data cells non-editable
                self.table_widget.setItem(i, j + 1, item) # +1 because column 0 is for index labels

        # Adjust column widths to content
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.setVisible(True) # Ensure table is visible

    def copy_table_to_clipboard(self):
        output = []
        # Get header labels
        header = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
        output.append('\t'.join(header)) # Join with tabs for easy pasting into spreadsheets

        # Get table data
        for i in range(self.table_widget.rowCount()):
            row_data = []
            for j in range(self.table_widget.columnCount()):
                item = self.table_widget.item(i, j)
                row_data.append(item.text() if item else '')
            output.append('\t'.join(row_data))
        
        # Set text to clipboard
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText('\n'.join(output))
        clipboard.setMimeData(mime_data)
        
        QMessageBox.information(self, self._("Copied"), self._("Table data copied to clipboard."))

    def retranslate_ui(self):
        # Retranslate dialog window title based on its current content
        # If text_output is visible, it means it's showing test results, not a table
        if self.text_output and self.text_output.isVisible():
            # Title is set from the calling function (e.g., EDADashboard.perform_statistical_test)
            # No need to change window title here as it's already set dynamically
            pass 
        elif self.stats_df is not None:
            # Re-set title if it's a table based on its content (correlation or descriptive)
            is_correlation_matrix = (self.stats_df.index.tolist() == self.stats_df.columns.tolist() and
                                     self.stats_df.shape[0] == self.stats_df.shape[1] and
                                     pd.api.types.is_numeric_dtype(self.stats_df.values))
            if is_correlation_matrix:
                self.setWindowTitle(self._("Correlation Matrix"))
            else:
                self.setWindowTitle(self._("Descriptive Statistics"))
        else:
            self.setWindowTitle(self._("Statistics Result")) # Generic title if neither is applicable

        self.copy_button.setText(self._("Copy to Clipboard"))
        self.close_button.setText(self._("Close"))
        
        # Re-translate table headers if table is visible and has data
        if self.table_widget.isVisible() and self.stats_df is not None and self.table_widget.columnCount() > 0:
            is_correlation_matrix = (self.stats_df.index.tolist() == self.stats_df.columns.tolist() and
                                     self.stats_df.shape[0] == self.stats_df.shape[1] and
                                     pd.api.types.is_numeric_dtype(self.stats_df.values))
            if is_correlation_matrix:
                header_labels = [self._("Variable")] + self.stats_df.columns.tolist()
            else:
                header_labels = [self._("Statistic")] + self.stats_df.columns.tolist()
            self.table_widget.setHorizontalHeaderLabels(header_labels)
        
        # If text_output is active, ensure its copy button callback is correct
        if self.text_output:
            # The copy button's connection is managed in EDADashboard.perform_statistical_test
            # so retranslate_ui here won't change its behavior regarding text vs table.
            # We just ensure the text on the button is updated.
            pass
