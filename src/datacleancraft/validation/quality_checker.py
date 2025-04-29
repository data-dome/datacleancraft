# """
# quality_checker.py: Basic data quality checks.
# """

# import pandas as pd

# class DataQualityChecker:
#     def __init__(self, max_null_threshold: float = 0.4):
#         """
#         Args:
#             max_null_threshold (float): Maximum allowed fraction of missing values in a column before it's flagged.
#         """
#         self.max_null_threshold = max_null_threshold

#     def validate(self, df: pd.DataFrame) -> None:
#         """
#         Run basic quality checks on the DataFrame.

#         Args:
#             df (pd.DataFrame): Data to validate.

#         Raises:
#             ValueError: If critical quality issues are found.
#         """

#         self._check_missing_values(df)
#         self._check_duplicate_rows(df)
#         self._check_constant_columns(df)

#     def _check_missing_values(self, df: pd.DataFrame) -> None:
#         missing_fraction = df.isnull().mean()
#         problematic_columns = missing_fraction[missing_fraction > self.max_null_threshold]

#         if not problematic_columns.empty:
#             raise ValueError(f"Columns with too many missing values (> {self.max_null_threshold*100}%):\n{problematic_columns}")

#     def _check_duplicate_rows(self, df: pd.DataFrame) -> None:
#         duplicate_count = df.duplicated().sum()

#         if duplicate_count > 0:
#             raise ValueError(f"Data contains {duplicate_count} duplicate rows.")

#     def _check_constant_columns(self, df: pd.DataFrame) -> None:
#         constant_columns = [col for col in df.columns if df[col].nunique(dropna=True) <= 1]

#         if constant_columns:
#             raise ValueError(f"Constant-value columns detected (only one unique value): {constant_columns}")
import pandas as pd
from typing import List, Dict

class DataQualityChecker:
    def __init__(self, max_null_threshold: float = 0.4):
        """
        Args:
            max_null_threshold (float): Maximum allowed fraction of missing values in a column before it's flagged.
        """
        self.max_null_threshold = max_null_threshold

    def validate(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """
        Run basic quality checks on the DataFrame and return the issues found.

        Args:
            df (pd.DataFrame): Data to validate.

        Returns:
            List[Dict[str, str]]: List of issues found during validation.
        """
        issues = []
        
        issues.extend(self._check_missing_values(df))
        issues.extend(self._check_duplicate_rows(df))
        issues.extend(self._check_constant_columns(df))
        
        return issues

    def _check_missing_values(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        missing_fraction = df.isnull().mean()
        problematic_columns = missing_fraction[missing_fraction > self.max_null_threshold]

        if not problematic_columns.empty:
            return [{"issue": "Too many missing values", "columns": str(problematic_columns)}]
        return []

    def _check_duplicate_rows(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        duplicate_count = df.duplicated().sum()

        if duplicate_count > 0:
            return [{"issue": f"Duplicate rows detected", "count": str(duplicate_count)}]
        return []

    def _check_constant_columns(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        constant_columns = [col for col in df.columns if df[col].nunique(dropna=True) <= 1]

        if constant_columns:
            return [{"issue": "Constant-value columns detected", "columns": str(constant_columns)}]
        return []
