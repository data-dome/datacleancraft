"""
mapper.py: Map fields from raw data to structured schemas.
"""

import pandas as pd
from typing import Dict, Any

class FieldMapper:
    def __init__(self, field_mapping: Dict[str, str]) -> None:
        """
        Initialize FieldMapper with a field mapping.

        Args:
            field_mapping (dict): A dictionary where keys are raw field names and values are the desired field names in the schema.
        """
        self.field_mapping = field_mapping


    def map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Map the columns in the DataFrame to the desired field names using the provided field mapping.

        Args:
            df (pd.DataFrame): Raw DataFrame with unstructured columns.

        Returns:
            pd.DataFrame: DataFrame with mapped column names.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        # Find fields that are missing from the DataFrame
        missing_fields = set(self.field_mapping.keys()) - set(df.columns)

        if missing_fields:
            raise ValueError(f"Missing required fields in input DataFrame: {', '.join(missing_fields)}")

        # Only map the available fields
        mapped_columns = {col: self.field_mapping[col] for col in df.columns if col in self.field_mapping}

        df_mapped = df.rename(columns=mapped_columns)

        return df_mapped

    def map_to_schema(self, df: pd.DataFrame, schema: Dict[str, Any]) -> pd.DataFrame:
        """
        Map raw data to a predefined schema, ensuring the data matches the expected format.

        Args:
            df (pd.DataFrame): Raw DataFrame with unstructured data.
            schema (dict): Schema that specifies the desired data types and field names.

        Returns:
            pd.DataFrame: DataFrame structured according to the schema.
        """
        # First, map the columns to match the schema field names
        df_mapped = self.map_columns(df)

        # Convert the columns to the specified types in the schema
        for field, dtype in schema.items():
            if field in df_mapped.columns:
                df_mapped[field] = df_mapped[field].astype(dtype)
            else:
                raise ValueError(f"Field '{field}' is missing in the mapped DataFrame.")

        return df_mapped

    def map_and_clean(self, df: pd.DataFrame, schema: dict) -> pd.DataFrame:
        """
        Map and clean the raw data according to the schema, handling missing or null values.

        Args:
            df (pd.DataFrame): Raw DataFrame.
            schema (dict): Schema specifying desired field names and types.

        Returns:
            pd.DataFrame: Cleaned and structured DataFrame.
        """
        # Map the DataFrame columns to the schema
        df_mapped = self.map_to_schema(df, schema)

        # Fill missing values based on the schema
        for field, dtype in schema.items():
            if field not in df_mapped.columns:
                continue

            if dtype == "int":
                # For integer columns, handle NaN explicitly by converting to nullable Int64
                df_mapped[field] = pd.to_numeric(df_mapped[field], errors='coerce')  # Ensure coercion of NaNs
                df_mapped[field] = df_mapped[field].fillna(0).astype("Int64")  # Fill NaN with 0 and convert to nullable Int64
            elif dtype == "float":
                # Handle float columns
                df_mapped[field] = pd.to_numeric(df_mapped[field], errors='coerce')  # Ensure coercion of NaNs
                df_mapped[field].fillna(0.0, inplace=True)  # Fill NaN with 0.0 for floats
            elif dtype == "str":
                # Handle string columns
                df_mapped[field].fillna('', inplace=True)  # Fill NaN with empty string for strings

        return df_mapped
