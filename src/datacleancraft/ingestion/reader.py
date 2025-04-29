# reader.py: Load JSON, CSV, XML, text
"""
Reader module for loading different data formats.
"""

import pandas as pd
import json
import xmltodict
from pathlib import Path
from typing import Union

def read_file(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Detect file format and load into a pandas DataFrame.
    
    Args:
        file_path (str or Path): Path to the input data file.

    Returns:
        pd.DataFrame: Loaded data.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

    suffix = file_path.suffix.lower()

    if suffix == ".json":
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.json_normalize(data)
    
    elif suffix == ".csv":
        return pd.read_csv(file_path)
    
    elif suffix == ".xml":
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_data = xmltodict.parse(f.read())
        return pd.json_normalize(xml_data)
    
    elif suffix in (".txt", ".text"):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return pd.DataFrame({'text': [line.strip() for line in lines]})
    
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
"""
reader.py - Module for reading structured data from various formats (CSV, JSON).
"""


def load_data(input_path: Union[str, Path], format: str = "csv") -> pd.DataFrame:
    """
    Load data into a DataFrame from disk.

    Args:
        input_path (str or Path): Path to the input file.
        format (str): Format to read ('csv' or 'json').

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file {input_path} does not exist.")

    format = format.lower()

    if format == "csv":
        return pd.read_csv(input_path)
    elif format == "json":
        return pd.read_json(input_path, orient='records', lines=True)
    else:
        raise ValueError(f"Unsupported input format: {format}")
