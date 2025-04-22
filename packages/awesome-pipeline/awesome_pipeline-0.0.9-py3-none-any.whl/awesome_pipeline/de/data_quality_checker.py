import pandas as pd
import numpy as np
from scipy.stats import zscore, skew, kurtosis


class DataQualityChecker:
    """
    A class to perform advanced data quality checks on a pandas DataFrame.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the DataQualityChecker with a DataFrame.

        :param dataframe: pd.DataFrame to be checked.
        """
        self.df = dataframe

    def check_missing_values(self):
        """
        Check for missing values in the DataFrame.

        :return: DataFrame with the count and percentage of missing values for each column.
        """
        missing_count = self.df.isnull().sum()
        missing_percentage = (missing_count / len(self.df)) * 100
        return pd.DataFrame(
            {"Missing Count": missing_count, "Missing Percentage": missing_percentage}
        ).sort_values(by="Missing Count", ascending=False)

    def check_duplicates(self):
        """
        Check for duplicate rows in the DataFrame.

        :return: Number of duplicate rows.
        """
        return self.df.duplicated().sum()

    def check_data_types(self):
        """
        Check data types of each column.

        :return: Series with data types of each column.
        """
        return self.df.dtypes

    def check_outliers(self, method: str = "IQR", threshold: float = 3):
        """
        Detect outliers in numerical columns using the specified method.

        :param method: Method to detect outliers. Options are "IQR" or "z-score".
        :param threshold: Threshold for outlier detection. Default is 3 for z-score.
        :return: Dictionary with column names as keys and lists of outlier indices as values.
        """
        outliers = {}
        numeric_cols = self.df.select_dtypes(include=np.number).columns

        if method == "IQR":
            for col in numeric_cols:
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                outliers[col] = self.df[
                    (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                ].index.tolist()
        elif method == "z-score":
            z_scores = self.df[numeric_cols].apply(zscore)
            for col in numeric_cols:
                outliers[col] = z_scores[abs(z_scores[col]) > threshold].index.tolist()
        else:
            raise ValueError("Invalid method. Choose 'IQR' or 'z-score'.")

        return outliers

    def get_summary_statistics(self):
        """
        Get summary statistics for numerical columns.

        :return: DataFrame with summary statistics for numerical columns.
        """
        numeric_cols = self.df.select_dtypes(include=np.number)
        if numeric_cols.empty:
            return (
                "No numeric columns in the DataFrame to calculate summary statistics."
            )

        summary = numeric_cols.describe()
        summary.loc["skew"] = numeric_cols.apply(skew, nan_policy="omit")
        summary.loc["kurtosis"] = numeric_cols.apply(kurtosis, nan_policy="omit")
        return summary

    def check_unique_values(self):
        """
        Check the count of unique values in each column.

        :return: DataFrame with unique value counts for each column.
        """
        unique_counts = self.df.nunique()
        return pd.DataFrame({"Unique Values": unique_counts}).sort_values(
            by="Unique Values", ascending=False
        )

    def detect_constant_columns(self):
        """
        Detect columns with a single unique value (constant columns).

        :return: List of column names that are constant.
        """
        return [col for col in self.df.columns if self.df[col].nunique() == 1]

    def check_correlations(self, method: str = "pearson", threshold: float = 0.8):
        """
        Check for highly correlated numerical features.

        :param method: Correlation method ("pearson", "spearman", or "kendall").
        :param threshold: Correlation threshold to consider features as highly correlated.
        :return: List of tuples containing pairs of highly correlated columns and their correlation coefficient.
        """
        numeric_cols = self.df.select_dtypes(include=np.number)
        if numeric_cols.empty:
            return (
                "No numeric columns in the DataFrame to calculate summary statistics."
            )

        corr_matrix = numeric_cols.corr(method=method)
        correlated_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    correlated_pairs.append(
                        (
                            corr_matrix.columns[i],
                            corr_matrix.columns[j],
                            corr_matrix.iloc[i, j],
                        )
                    )
        return correlated_pairs

    def check_category_balance(self, column: str):
        """
        Check the balance of categorical values in a specified column.

        :param column: Column to analyze.
        :return: DataFrame with counts and percentages of each category.
        """
        value_counts = self.df[column].value_counts()
        percentage = (value_counts / len(self.df)) * 100
        return pd.DataFrame({"Count": value_counts, "Percentage": percentage})

    def detect_date_columns(self):
        """
        Detect columns with datetime data type or that can be inferred as dates.

        :return: List of column names with datetime data.
        """
        date_columns = []
        for col in self.df.columns:
            if np.issubdtype(self.df[col].dtype, np.datetime64):
                date_columns.append(col)
            else:
                try:
                    pd.to_datetime(self.df[col])
                    date_columns.append(col)
                except (ValueError, TypeError):
                    pass
        return date_columns

    def check_column_coverage(self, column: str, reference: list):
        """
        Check if all values in a column are covered in a given reference list.

        :param column: Column to check.
        :param reference: List of valid values.
        :return: DataFrame with counts of matching and non-matching values.
        """
        match = self.df[column].isin(reference).sum()
        non_match = len(self.df) - match
        return pd.DataFrame({"Match": [match], "Non-Match": [non_match]})

    def detect_imbalanced_columns(self, threshold: float = 0.1):
        """
        Detect columns with imbalanced categorical values.

        :param threshold: Minimum percentage for a category to be considered balanced.
        :return: List of column names with imbalance issues.
        """
        imbalanced_columns = []
        for col in self.df.select_dtypes(include="object").columns:
            value_counts = self.df[col].value_counts(normalize=True)
            if (value_counts < threshold).any():
                imbalanced_columns.append(col)
        return imbalanced_columns

    def generate_report(self):
        """
        Generate a comprehensive data quality report.

        :return: Dictionary containing data quality metrics.
        """
        report = {}
        checks = {
            "Missing Values": self.check_missing_values,
            "Duplicate Rows": self.check_duplicates,
            "Data Types": self.check_data_types,
            "Outliers (IQR Method)": lambda: self.check_outliers(method="IQR"),
            "Summary Statistics": self.get_summary_statistics,
            "Unique Values": self.check_unique_values,
            "Constant Columns": self.detect_constant_columns,
            "High Correlations": self.check_correlations,
            "Date Columns": self.detect_date_columns,
            "Imbalanced Columns": self.detect_imbalanced_columns,
        }

        for check_name, check_func in checks.items():
            try:
                report[check_name] = check_func()
            except Exception as e:
                report[check_name] = f"Failed: {e}"

        return report
