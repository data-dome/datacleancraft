import pytest
import pandas as pd
from datacleancraft.structuring.standardizer import Standardizer

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "dob": ["04/24/1990", "1991-05-15", "June 1, 1992", None, "InvalidDate"],
        "created_at": ["2023-01-01", "01-02-2023", "February 5, 2023", None, "bad_date"],
        "Gender": ["M", "F", "fem", "male", "Unknown"],
        "Status": ["act", "inact", "act", "inactive", "unknown"]
    })

@pytest.fixture
def standardizer():
    return Standardizer()

def test_standardize_dates(standardizer, sample_dataframe):
    df = sample_dataframe.copy()
    result = standardizer.standardize_dates(df, date_columns=["dob", "created_at"])

    # Check correct ISO format for parsed dates
    assert result.loc[0, "dob"] == "1990-04-24"
    assert result.loc[2, "dob"] == "1992-06-01"
    assert pd.isna(result.loc[3, "dob"])  # Invalid date returns NaN
    assert result.loc[1, "created_at"] == "2023-01-02"

def test_standardize_categories(standardizer, sample_dataframe):
    df = sample_dataframe.copy()
    mapping = {
        "Gender": {"M": "Male", "F": "Female", "fem": "Female", "male": "Male"},
        "Status": {"act": "Active", "inact": "Inactive"}
    }

    result = standardizer.standardize_categories(df, category_mappings=mapping)

    # Check category mapping
    assert result.loc[0, "Gender"] == "Male"
    assert result.loc[2, "Gender"] == "Female"
    assert result.loc[4, "Gender"] == "Unknown"  # Not mapped, remains same

    assert result.loc[1, "Status"] == "Inactive"
    assert result.loc[3, "Status"] == "inactive"  # Not mapped exactly, remains same
