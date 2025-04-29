# """
# Standardizer Module

# Functions to normalize dates, categorical values, and other common field formats.
# """

# import pandas as pd
# import numpy as np
# from typing import List, Dict, Union
# from dateutil import parser as date_parser

# class Standardizer:
#     def __init__(self):
#         pass

#     def standardize_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
#         """
#         Standardize date columns to ISO 8601 format (YYYY-MM-DD).

#         Args:
#             df (pd.DataFrame): Input dataframe.
#             date_columns (List[str]): List of columns to standardize.

#         Returns:
#             pd.DataFrame: DataFrame with standardized date columns.
#         """
#         for col in date_columns:
#             df[col] = df[col].apply(self._parse_date)
#         return df

#     def _parse_date(self, value: Union[str, pd.Timestamp]) -> Union[str, float]:
#         """
#         Helper to parse individual date value.

#         Args:
#             value: Input date value.

#         Returns:
#             str or np.nan: Standardized ISO date string or np.nan if invalid.
#         """
#         if pd.isnull(value):
#             return np.nan
#         try:
#             parsed = date_parser.parse(str(value), fuzzy=True)
#             return parsed.date().isoformat()
#         except Exception:
#             return np.nan

#     def standardize_categories(self, df: pd.DataFrame, category_mappings: Dict[str, Dict[str, str]]) -> pd.DataFrame:
#         """
#         Standardize categorical columns using mapping dictionaries.

#         Args:
#             df (pd.DataFrame): Input dataframe.
#             category_mappings (Dict[str, Dict[str, str]]): 
#                 Column-wise mappings. 
#                 Example: {"Gender": {"M": "Male", "F": "Female"}}

#         Returns:
#             pd.DataFrame: DataFrame with standardized categories.
#         """
#         for col, mapping in category_mappings.items():
#             if col in df.columns:
#                 df[col] = df[col].map(mapping).fillna(df[col])
#         return df
#     def standardize(self, df: pd.DataFrame, date_columns: List[str], category_mappings: Dict[str, Dict[str, str]]) -> pd.DataFrame:
#         """
#         Standardize the DataFrame by applying date and category standardizations.

#         Args:
#             df (pd.DataFrame): Input dataframe.
#             date_columns (List[str]): List of columns to standardize as dates.
#             category_mappings (Dict[str, Dict[str, str]]): Column-wise mappings for categories.

#         Returns:
#             pd.DataFrame: Fully standardized DataFrame.
#         """
#         df = self.standardize_dates(df, date_columns)
#         df = self.standardize_categories(df, category_mappings)
#         return df

import pandas as pd
import numpy as np
from typing import List, Dict, Union
from dateutil import parser as date_parser

class Standardizer:
    def __init__(self):
        pass

    def standardize_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """
        Standardize date columns to ISO 8601 format (YYYY-MM-DD).
        
        Args:
            df (pd.DataFrame): Input dataframe.
            date_columns (List[str]): List of columns to standardize.
        
        Returns:
            pd.DataFrame: DataFrame with standardized date columns.
        """
        for col in date_columns:
            df[col] = df[col].apply(self._parse_date)
        return df

    def _parse_date(self, value: Union[str, pd.Timestamp]) -> Union[str, float]:
        """
        Helper to parse individual date value.
        
        Args:
            value: Input date value.
        
        Returns:
            str or np.nan: Standardized ISO date string or np.nan if invalid.
        """
        if pd.isnull(value):
            return np.nan
        try:
            # Attempt to parse the date
            parsed = date_parser.parse(str(value), fuzzy=True)
            return parsed.date().isoformat()
        except Exception:
            # If parsing fails, return the value as is
            return value

    def standardize_categories(self, df: pd.DataFrame, category_mappings: Dict[str, Dict[str, str]]) -> pd.DataFrame:
        """
        Standardize categorical columns using mapping dictionaries.

        Args:
            df (pd.DataFrame): Input dataframe.
            category_mappings (Dict[str, Dict[str, str]]): 
                Column-wise mappings. 
                Example: {"Gender": {"M": "Male", "F": "Female"}}

        Returns:
            pd.DataFrame: DataFrame with standardized categories.
        """
        for col, mapping in category_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping).fillna(df[col])
        return df

    def detect_date_columns(self, df: pd.DataFrame) -> List[str]:
        """
        Automatically detect columns that should be treated as dates.
        
        Args:
            df (pd.DataFrame): Input dataframe.
        
        Returns:
            List[str]: List of columns to treat as dates.
        """
        date_columns = []
        for col in df.columns:
            # Check if column is of string type or datetime-like
            if pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_datetime64_any_dtype(df[col]):
                # Try to parse a sample value to check if it's a date
                if df[col].apply(lambda x: self._parse_date(x) != np.nan).any():
                    date_columns.append(col)
        return date_columns

    def detect_category_columns(self, df: pd.DataFrame, max_unique_values: int = 20) -> Dict[str, Dict[str, str]]:
        """
        Automatically detect columns that should be treated as categorical.
        
        Args:
            df (pd.DataFrame): Input dataframe.
            max_unique_values (int): Threshold to classify a column as categorical.
        
        Returns:
            Dict[str, Dict[str, str]]: Dictionary of column names and their value mappings.
        """
        category_mappings = {}
        for col in df.columns:
            unique_vals = df[col].nunique()
            if unique_vals <= max_unique_values and pd.api.types.is_object_dtype(df[col]):
                # Map each category to its own value (this can be customized)
                category_mappings[col] = {val: val for val in df[col].dropna().unique()}
        return category_mappings

    def standardize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize the DataFrame by applying auto-detected date and category standardizations.
        
        Args:
            df (pd.DataFrame): Input dataframe.
        
        Returns:
            pd.DataFrame: Fully standardized DataFrame.
        """
        # Automatically detect date columns
        date_columns = self.detect_date_columns(df)

        # Automatically detect category columns and create mapping
        category_mappings = self.detect_category_columns(df)

        # Apply standardization
        df = self.standardize_dates(df, date_columns)
        df = self.standardize_categories(df, category_mappings)

        return df
# 