import pandas as pd
import numpy as np
import scipy.stats as stats
import io

class DataHandler:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        if not self.file_path:
            raise ValueError("File path not provided to load data.")

        if self.file_path.endswith('.csv'):
            try:
                self.df = pd.read_csv(self.file_path)
            except Exception as e:
                raise ValueError(f"Failed to load CSV file: {e}")
        elif self.file_path.endswith(('.xlsx', '.xls')):
            try:
                self.df = pd.read_excel(self.file_path)
            except Exception as e:
                raise ValueError(f"Failed to load Excel file: {e}")
        else:
            raise ValueError("Unsupported file type. Please load a .csv, .xlsx, or .xls file.")
        
        if self.df is None or self.df.empty:
            raise ValueError("The loaded file is empty or contains no valid data.")
        
        return self.df

    def get_dataframe(self) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("No data has been loaded yet. Please call load_data() first.")
        return self.df

    def get_column_names(self) -> list:
        if self.df is None:
            raise ValueError("No data has been loaded yet.")
        return self.df.columns.tolist()

    def get_numerical_columns(self) -> list:
        if self.df is None:
            raise ValueError("No data has been loaded yet.")
        numerical_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        return numerical_cols

    def get_categorical_columns(self) -> list:
        if self.df is None:
            raise ValueError("No data has been loaded yet.")
        categorical_cols = self.df.select_dtypes(exclude=np.number).columns.tolist()
        return categorical_cols

    def detect_column_type(self, column_data: pd.Series) -> str:
        if pd.api.types.is_numeric_dtype(column_data):
            # Heuristic for categorical vs numerical for integers/numbers
            # If unique values are less than 10% of total length and also less than or equal to 50 unique values,
            # it might be treated as categorical, otherwise numerical.
            if column_data.nunique() < len(column_data) * 0.1 and column_data.nunique() <= 50:
                return "Categorical"
            return "Numerical"
        
        if pd.api.types.is_datetime64_any_dtype(column_data):
            return "Date"
        
        if pd.api.types.is_object_dtype(column_data) or pd.api.types.is_string_dtype(column_data):
            return "Categorical"

        return "Categorical" # Default for anything else

    def get_dataframe_head(self, n: int = 5) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("No data has been loaded yet.")
        return self.df.head(n)

    def get_dataframe_info(self):
        if self.df is None:
            raise ValueError("No data has been loaded yet.")
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()


    def get_dataframe_describe(self) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("No data has been loaded yet.")
        return self.df.describe()

    def handle_missing_values(self, strategy: str, column: str = None, fill_value=None):
        if self.df is None:
            raise ValueError("No data loaded to handle missing values.")

        if strategy == 'drop_rows':
            if column:
                original_rows = self.df.shape[0]
                self.df.dropna(subset=[column], inplace=True)
                return original_rows - self.df.shape[0]
            else:
                original_rows = self.df.shape[0]
                self.df.dropna(inplace=True)
                return original_rows - self.df.shape[0]

        elif strategy.startswith('fill_'):
            if not column:
                raise ValueError("Column must be specified for fill strategies.")
            
            if column not in self.df.columns:
                raise ValueError(f"Column '{column}' not found.")

            col_data = self.df[column]
            initial_missing = col_data.isnull().sum()

            if initial_missing == 0:
                return 0

            if strategy == 'fill_mean':
                if pd.api.types.is_numeric_dtype(col_data):
                    self.df[column].fillna(col_data.mean(), inplace=True)
                else:
                    raise ValueError(f"Column '{column}' is not numeric for 'fill_mean' strategy.")
            elif strategy == 'fill_median':
                if pd.api.types.is_numeric_dtype(col_data):
                    self.df[column].fillna(col_data.median(), inplace=True)
                else:
                    raise ValueError(f"Column '{column}' is not numeric for 'fill_median' strategy.")
            elif strategy == 'fill_mode':
                self.df[column].fillna(col_data.mode()[0], inplace=True)
            elif strategy == 'fill_value':
                if fill_value is None:
                    raise ValueError("Fill value must be provided for 'fill_value' strategy.")
                try:
                    # Attempt to convert fill_value to the column's dtype
                    if pd.api.types.is_numeric_dtype(col_data):
                        fill_value = pd.to_numeric(fill_value)
                    elif pd.api.types.is_datetime64_any_dtype(col_data):
                        fill_value = pd.to_datetime(fill_value)
                except ValueError:
                    pass # If conversion fails, use original fill_value

                self.df[column].fillna(fill_value, inplace=True)
            
            return initial_missing

        else:
            raise ValueError(f"Unsupported missing value strategy: {strategy}")

    def get_missing_values_summary(self) -> pd.DataFrame:
        if self.df is None:
            return pd.DataFrame(columns=['Column', 'Missing Count', 'Percentage'])
        
        missing_data = self.df.isnull().sum()
        missing_data = missing_data[missing_data > 0]
        
        if missing_data.empty:
            return pd.DataFrame(columns=['Column', 'Missing Count', 'Percentage'])
        
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Percentage': (missing_data.values / len(self.df)) * 100
        })
        return missing_df.reset_index(drop=True)

    def drop_duplicates(self) -> int:
        if self.df is None:
            raise ValueError("No data loaded to remove duplicates.")
        
        original_rows = self.df.shape[0]
        self.df.drop_duplicates(inplace=True)
        return original_rows - self.df.shape[0]

    def change_column_type(self, column: str, new_type: str):
        if self.df is None:
            raise ValueError("No data loaded to change column type.")
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found.")

        try:
            if new_type == 'int':
                # Convert to numeric first, then to int. Coerce errors to NaN.
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
                # Check for any remaining NaNs after numeric conversion
                if self.df[column].isnull().any():
                     raise ValueError("Cannot convert column to integer: contains non-numeric or missing values. Please handle them first.")
                self.df[column] = self.df[column].astype(int)
            elif new_type == 'float':
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
            elif new_type == 'str':
                self.df[column] = self.df[column].astype(str)
            elif new_type == 'datetime':
                self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
                # Check for NaT (Not a Time) values introduced by errors
                if self.df[column].isnull().any():
                    num_errors = self.df[column].isnull().sum()
                    raise ValueError(f"Cannot convert column to datetime: {num_errors} values could not be parsed as dates. Please check data format.")
            else:
                raise ValueError(f"Unsupported new type: {new_type}")
        except Exception as e:
            raise ValueError(f"Error converting column '{column}' to '{new_type}': {e}")
            
    def rename_column(self, old_column_name: str, new_column_name: str):
        if self.df is None:
            raise ValueError("No data loaded to rename columns.")
        if old_column_name not in self.df.columns:
            raise ValueError(f"Column '{old_column_name}' not found.")
        # Prevent renaming to an existing column unless it's the same column (case-sensitive check)
        if new_column_name in self.df.columns and new_column_name != old_column_name:
            raise ValueError(f"New column name '{new_column_name}' already exists.")
        
        try:
            self.df.rename(columns={old_column_name: new_column_name}, inplace=True)
        except Exception as e:
            raise ValueError(f"Error renaming column '{old_column_name}' to '{new_column_name}': {e}")

    def get_basic_statistics(self, columns: list = None) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("No data loaded to generate statistics.")
        
        if not columns:
            target_df = self.df.select_dtypes(include=np.number)
        else:
            for col in columns:
                if col not in self.df.columns:
                    raise ValueError(f"Column '{col}' not found in the DataFrame.")
                if not pd.api.types.is_numeric_dtype(self.df[col]):
                    raise ValueError(f"Column '{col}' is not numerical. Please select numerical columns for basic statistics.")
            target_df = self.df[columns]
        
        if target_df.empty:
            raise ValueError("No numerical columns available for statistical analysis.")
            
        return target_df.describe()

    def perform_t_test(self, column1: str, column2: str) -> dict:
        if self.df is None:
            raise ValueError("No data loaded to perform t-test.")
        
        if not all(col in self.df.columns for col in [column1, column2]):
            raise ValueError(f"One or both columns ('{column1}', '{column2}') not found.")
        
        if not (pd.api.types.is_numeric_dtype(self.df[column1]) and 
                pd.api.types.is_numeric_dtype(self.df[column2])):
            raise ValueError("Both columns must be numerical for t-test.")
        
        # Drop rows with NaN in either of the two columns for the test
        clean_df = self.df[[column1, column2]].dropna()
        if clean_df.empty:
            raise ValueError("No common non-missing data points for selected columns to perform t-test.")

        # Perform Independent Samples T-Test (Welch's t-test, which does not assume equal variances)
        t_statistic, p_value = stats.ttest_ind(clean_df[column1], clean_df[column2], equal_var=False)
        
        return {
            "test_type": "Independent Samples T-Test",
            "column1": column1,
            "column2": column2,
            "t_statistic": t_statistic,
            "p_value": p_value,
            "interpretation": {
                "en": f"The p-value ({p_value:.4f}) is {('less than' if p_value < 0.05 else 'greater than')} 0.05. Therefore, we {'reject' if p_value < 0.05 else 'fail to reject'} the null hypothesis. This suggests {'a significant difference' if p_value < 0.05 else 'no significant difference'} between the means of '{column1}' and '{column2}'.",
                "ar": f"قيمة P ({p_value:.4f}) {'أقل من' if p_value < 0.05 else 'أكبر من'} 0.05. لذلك، نحن {'نرفض' if p_value < 0.05 else 'نفشل في رفض'} الفرضية الصفرية. هذا يشير إلى {'وجود فرق جوهري' if p_value < 0.05 else 'عدم وجود فرق جوهري'} بين متوسطي '{column1}' و '{column2}'."
            }
        }

    def perform_chi_square_test(self, column1: str, column2: str) -> dict:
        if self.df is None:
            raise ValueError("No data loaded to perform Chi-Square test.")
        
        if not all(col in self.df.columns for col in [column1, column2]):
            raise ValueError(f"One or both columns ('{column1}', '{column2}') not found.")
        
        # Ensure both columns are categorical
        if not (self.detect_column_type(self.df[column1]) == "Categorical" and
                self.detect_column_type(self.df[column2]) == "Categorical"):
            raise ValueError(f"Both columns ('{column1}', '{column2}') must be categorical for Chi-Square test.")
            
        # Create a contingency table (cross-tabulation)
        contingency_table = pd.crosstab(self.df[column1], self.df[column2])
        
        if contingency_table.empty:
            raise ValueError("Contingency table is empty. Check data for selected columns.")

        # Perform Chi-Square test of independence
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        return {
            "test_type": "Chi-Square Test of Independence",
            "column1": column1,
            "column2": column2,
            "chi2_statistic": chi2,
            "p_value": p_value,
            "degrees_of_freedom": dof,
            "contingency_table": contingency_table.to_string(), # Convert to string for display
            "expected_frequencies": pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns).to_string(), # Convert to string for display
            "interpretation": {
                "en": f"The p-value ({p_value:.4f}) is {('less than' if p_value < 0.05 else 'greater than')} 0.05. Therefore, we {'reject' if p_value < 0.05 else 'fail to reject'} the null hypothesis. This suggests {'a significant association' if p_value < 0.05 else 'no significant association'} between '{column1}' and '{column2}'.",
                "ar": f"قيمة P ({p_value:.4f}) {'أقل من' if p_value < 0.05 else 'أكبر من'} 0.05. لذلك، نحن {'نرفض' if p_value < 0.05 else 'نفشل في رفض'} الفرضية الصفرية. هذا يشير إلى {'وجود علاقة جوهرية' if p_value < 0.05 else 'عدم وجود علاقة جوهرية'} بين '{column1}' و '{column2}'."
            }
        }
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        Calculates the Pearson correlation matrix for all numerical columns.
        Returns a DataFrame representing the correlation matrix.
        """
        if self.df is None:
            raise ValueError("No data loaded to calculate correlation.")
        
        numerical_df = self.df.select_dtypes(include=np.number)
        
        if numerical_df.empty:
            raise ValueError("No numerical columns found to calculate correlation.")
        
        # Pearson correlation is the default for .corr()
        correlation_matrix = numerical_df.corr(method='pearson')
        return correlation_matrix

    # --- دوال جديدة للتعامل مع القيم المتطرفة (Outliers) ---
    def detect_outliers_iqr(self, column: str) -> pd.DataFrame:
        """
        Detects outliers in a numerical column using the IQR method.
        Returns a DataFrame containing the detected outliers.
        """
        if self.df is None:
            raise ValueError("No data loaded to detect outliers.")
        
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found.")
        
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' is not numerical. Outlier detection requires a numerical column.")
        
        # Calculate Q1, Q3, and IQR
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Filter for outliers
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        # Return only the outlier values from the specified column
        if not outliers.empty:
            # Create a new DataFrame with just the outlier values and their original index
            # This is helpful for the user to see which specific values are outliers
            return outliers[[column]].copy()
        return pd.DataFrame() # Return an empty DataFrame if no outliers are found

    def handle_outliers(self, column: str, method: str):
        """
        Handles outliers in a numerical column using the IQR method.
        Method can be 'remove' (drops rows), 'median' (replaces with median), or 'mean' (replaces with mean).
        Returns the number of rows/values affected.
        """
        if self.df is None:
            raise ValueError("No data loaded to handle outliers.")
        
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found.")
        
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' is not numerical. Outlier handling requires a numerical column.")
        
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        initial_rows = self.df.shape[0]
        rows_affected = 0

        # Create a boolean mask for identifying outliers
        outlier_mask = (self.df[column] < lower_bound) | (self.df[column] > upper_bound)

        if method == 'remove':
            self.df = self.df[~outlier_mask].copy() # Use .copy() to avoid SettingWithCopyWarning
            rows_affected = initial_rows - self.df.shape[0]
        elif method == 'median':
            median_val = self.df[column].median()
            rows_affected = outlier_mask.sum()
            self.df.loc[outlier_mask, column] = median_val
        elif method == 'mean':
            mean_val = self.df[column].mean()
            rows_affected = outlier_mask.sum()
            self.df.loc[outlier_mask, column] = mean_val
        else:
            raise ValueError(f"Unsupported outlier handling method: {method}")
        
        return rows_affected # Return the number of affected rows/values

    def save_data(self, output_file_path: str):
        if self.df is None:
            raise ValueError("No data loaded to save.")
        
        if output_file_path.endswith('.csv'):
            try:
                self.df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
            except Exception as e:
                raise IOError(f"Failed to save CSV file: {e}")
        elif output_file_path.endswith(('.xlsx', '.xls')):
            try:
                self.df.to_excel(output_file_path, index=False)
            except Exception as e:
                raise IOError(f"Failed to save Excel file: {e}")
        else:
            raise ValueError("Unsupported file type for saving. Please specify .csv or .xlsx.")
