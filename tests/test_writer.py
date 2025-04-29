import os
import pandas as pd
import pytest

from datacleancraft.export.writer import export_data

def test_export_csv(tmp_path, sample_dataframe):
    file_path = tmp_path / "test_output.csv"
    export_data(sample_dataframe, file_path, format="csv")

    # Assert file was created
    assert file_path.exists()

    # Assert content is correct
    df_read = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df_read, sample_dataframe)

def test_export_json(tmp_path, sample_dataframe):
    file_path = tmp_path / "test_output.json"
    export_data(sample_dataframe, file_path, format="json")

    # Assert file was created
    assert file_path.exists()

    # Assert content is correct
    df_read = pd.read_json(file_path, lines=True)
    pd.testing.assert_frame_equal(df_read, sample_dataframe)

def test_unsupported_format(tmp_path, sample_dataframe):
    file_path = tmp_path / "test_output.unsupported"

    with pytest.raises(ValueError, match="Unsupported export format"):
        export_data(sample_dataframe, file_path, format="unsupported")
