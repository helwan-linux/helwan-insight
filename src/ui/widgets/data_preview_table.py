import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

class DataPreviewTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._ = parent._ if parent and hasattr(parent, '_') else lambda text: text

        self.table_widget = QTableWidget()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.retranslate_ui()

    def set_data(self, df: pd.DataFrame):
        self.table_widget.clear()
        if df is None or df.empty:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            return

        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns.tolist())

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                value = df.iloc[i, j]
                if pd.isna(value):
                    item = QTableWidgetItem("")
                elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                    item = QTableWidgetItem(str(value))
                elif isinstance(value, (int, float, bool, str)):
                    item = QTableWidgetItem(str(value))
                else:
                    item = QTableWidgetItem(str(value))
                
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def retranslate_ui(self):
        pass
