import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt
import seaborn as sns 

class PlotArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._ = parent._ if parent and hasattr(parent, '_') else lambda text: text

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.setContentsMargins(0, 0, 0, 0)
        plt.tight_layout()

    def plot_data(self, plot_type: str, column: str, df: pd.DataFrame):
        if plot_type not in ['pairplot', 'violin']: 
            self.ax.clear()

        if df is None or df.empty:
            QMessageBox.warning(self.parent, self._("No Data"), self._("No data available to plot."))
            return
        
        if column is not None and column not in df.columns: 
            QMessageBox.warning(self.parent, self._("Invalid Column"), self._("Selected column does not exist in the data."))
            return

        col_data = df[column] if column else None

        try:
            if plot_type == 'histogram':
                col_data.hist(ax=self.ax, bins=20)
                self.ax.set_title(self._("Histogram of {column}").format(column=column))
                self.ax.set_xlabel(self._(column))
                self.ax.set_ylabel(self._("Frequency"))
            elif plot_type == 'bar':
                if col_data.nunique() > 10:
                    top_values = col_data.value_counts().nlargest(10)
                    self.ax.bar(top_values.index.astype(str), top_values.values)
                    self.ax.set_title(self._("Bar Chart of Top 10 {column}").format(column=column))
                else:
                    value_counts = col_data.value_counts()
                    self.ax.bar(value_counts.index.astype(str), value_counts.values)
                    self.ax.set_title(self._("Bar Chart of {column}").format(column=column))
                self.ax.set_xlabel(self._(column))
                self.ax.set_ylabel(self._("Count"))
                self.figure.autofmt_xdate(rotation=45)
            elif plot_type == 'boxplot':
                col_data.plot.box(ax=self.ax)
                self.ax.set_title(self._("Box Plot of {column}").format(column=column))
                self.ax.set_ylabel(self._(column))
            elif plot_type == 'scatter':
                if pd.api.types.is_numeric_dtype(col_data):
                    self.ax.scatter(df.index, col_data)
                    self.ax.set_title(self._("Scatter Plot of {column}").format(column=column))
                    self.ax.set_xlabel(self._("Index"))
                    self.ax.set_ylabel(self._(column))
                else:
                    QMessageBox.warning(self.parent, self._("Plot Error"), 
                                        self._("Scatter plot requires numerical data for the selected column."))
            elif plot_type == 'line':
                if pd.api.types.is_datetime64_any_dtype(col_data):
                    self.ax.plot(col_data, df.index)
                    self.ax.set_xlabel(self._(column))
                    self.ax.set_ylabel(self._("Index"))
                else:
                    self.ax.plot(df.index, col_data)
                    self.ax.set_xlabel(self._("Index"))
                    self.ax.set_ylabel(self._(column))
                self.ax.set_title(self._("Line Plot of {column}").format(column=column))
                self.figure.autofmt_xdate()
            elif plot_type == 'pie':
                if not pd.api.types.is_numeric_dtype(col_data) or col_data.nunique() < len(col_data):
                    value_counts = col_data.value_counts()
                    self.ax.pie(value_counts, labels=value_counts.index.astype(str), autopct='%1.1f%%', startangle=90)
                    self.ax.set_title(self._("Pie Chart of {column}").format(column=column))
                    self.ax.axis('equal')
                else:
                    QMessageBox.warning(self.parent, self._("Plot Error"),
                                        self._("Pie chart is best suited for categorical or discrete numerical data."))
            elif plot_type == 'heatmap':
                numerical_df = df.select_dtypes(include=['number'])
                if numerical_df.empty:
                    QMessageBox.warning(self.parent, self._("Plot Error"), self._("No numerical data available for heatmap."))
                    return
                
                correlation_matrix = numerical_df.corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=self.ax)
                self.ax.set_title(self._("Correlation Heatmap"))
                self.figure.tight_layout()
            
            elif plot_type == 'pairplot':
                numerical_df = df.select_dtypes(include=['number'])
                if numerical_df.empty:
                    QMessageBox.warning(self.parent, self._("Plot Error"), self._("No numerical data available for pair plot."))
                    return
                
                plt.close(self.figure)
                g = sns.pairplot(numerical_df)
                
                self.figure = g.fig
                
                self.layout.removeWidget(self.canvas)
                self.canvas.deleteLater()
                self.canvas = FigureCanvas(self.figure)
                self.layout.addWidget(self.canvas)
                
                self.canvas.draw_idle()
                return
            
            elif plot_type == 'violin':
                if not pd.api.types.is_numeric_dtype(col_data):
                    QMessageBox.warning(self.parent, self._("Plot Error"), 
                                        self._("Violin plot requires a numerical column."))
                    return
                
                sns.violinplot(y=col_data, ax=self.ax, inner='quartile') 
                self.ax.set_title(self._("Violin Plot of {column}").format(column=column))
                self.ax.set_ylabel(self._(column))

            else:
                QMessageBox.warning(self.parent, self._("Unsupported Plot Type"), 
                                    self._("The selected plot type '{plot_type}' is not yet supported for '{column}'.").format(plot_type=plot_type, column=column))
                return

            self.figure.canvas.draw_idle()

        except Exception as e:
            QMessageBox.critical(self.parent, self._("Plotting Error"), 
                                 self._("An error occurred while plotting: {e}").format(e=e))
            self.ax.clear()
            self.figure.canvas.draw_idle()

    def save_plot_as_image(self, file_path: str):
        try:
            self.figure.savefig(file_path, bbox_inches='tight', dpi=300)
        except Exception as e:
            raise IOError(f"Failed to save plot to {file_path}: {e}")

    def retranslate_ui(self):
        pass
