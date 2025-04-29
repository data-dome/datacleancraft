import pytest
from datacleancraft.ingestion.reader import read_file
import pandas as pd

def test_read_csv(tmp_path):
    p = tmp_path / "test.csv"
    p.write_text("col1,col2\nval1,val2\n")
    df = read_file(p)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 2)

def test_unsupported_format(tmp_path):
    p = tmp_path / "test.unsupported"
    p.write_text("some content")
    with pytest.raises(ValueError):
        read_file(p)
