"""
detector.py: Detect data types in raw datasets.
"""

import pandas as pd
import numpy as np

class DataTypeDetector:
    def __init__(self):
        pass

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect and annotate the data types for each column.

        Args:
            df (pd.DataFrame): Raw input DataFrame.

        Returns:
            pd.DataFrame: A DataFrame with 'column' and 'detected_type'.
        """

        detection = []

        for col in df.columns:
            series = df[col]

            # Drop NaN to analyze real values
            non_null_series = series.dropna()

            if non_null_series.empty:
                detected_type = "Unknown"
            elif np.issubdtype(non_null_series.dtype, np.number):
                detected_type = "Numeric"
            elif pd.api.types.is_datetime64_any_dtype(non_null_series) or self._looks_like_datetime(non_null_series):
                detected_type = "Datetime"
            elif pd.api.types.is_bool_dtype(non_null_series):
                detected_type = "Boolean"
            elif self._looks_like_categorical(non_null_series):
                detected_type = "Categorical"
            else:
                detected_type = "Text"

            detection.append({
                "column": col,
                "detected_type": detected_type
            })

        return pd.DataFrame(detection)

    def _looks_like_datetime(self, series: pd.Series) -> bool:
        """
        Try parsing a sample of the data to datetime.
        """
        try:
            pd.to_datetime(series.sample(min(10, len(series))), errors='raise')
            return True
        except Exception:
            return False

    def _looks_like_categorical(self, series: pd.Series) -> bool:
        """
        Heuristic: if few unique values relative to number of records, it's categorical.
        """
        unique_ratio = series.nunique() / max(len(series), 1)
        return unique_ratio < 0.05  # 5% uniqueness threshold

