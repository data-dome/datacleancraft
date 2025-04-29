# writer.py: Write CSV, SQL dump, JSON
"""
Module for writing structured data into supported formats.
"""

import pandas as pd
from pathlib import Path
from typing import Union

def export_data(df: pd.DataFrame, output_path: Union[str, Path], format: str = "csv") -> None:
    """
    Export DataFrame to disk.

    Args:
        df (pd.DataFrame): Data to save.
        output_path (str or Path): Destination path.
        format (str): Output format (csv, json).
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    format = format.lower()

    if format == "csv":
        df.to_csv(output_path, index=False)
    elif format == "json":
        df.to_json(output_path, orient='records', lines=True)
    else:
        raise ValueError(f"Unsupported export format: {format}")
