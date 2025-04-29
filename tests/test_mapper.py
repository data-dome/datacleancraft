# import pytest
# import pandas as pd
# from datacleancraft.structuring.mapper import map_fields, standardize_types

# def test_field_mapping():
#     df = pd.DataFrame({"name_old": ["Alice"], "age_old": [30]})
#     mapping = {"name_old": "name", "age_old": "age"}
#     mapped_df = map_fields(df, mapping)
#     assert "name" in mapped_df.columns
#     assert "age" in mapped_df.columns

# def test_standardize_types():
#     df = pd.DataFrame({"date_col": ["2022-01-01"], "cat_col": ["A"]})
#     types = {"date_col": "date", "cat_col": "category"}
#     std_df = standardize_types(df, types)
#     assert str(std_df["date_col"].dtype).startswith("datetime")
#     assert str(std_df["cat_col"].dtype) == "category"
import pytest
import pandas as pd
from datacleancraft.structuring.mapper import FieldMapper


def test_map_columns_success(raw_dataframe, field_mapping):
    mapper = FieldMapper(field_mapping)
    df_mapped = mapper.map_columns(raw_dataframe)

    assert "name" in df_mapped.columns
    assert "age" in df_mapped.columns
    assert "email" in df_mapped.columns
    assert df_mapped.shape == raw_dataframe.shape

def test_map_columns_missing_field():
    field_mapping = {
        "First Name": "first_name",
        "Last Name": "last_name",
        "Age": "age"
    }

    input_df = pd.DataFrame({
        "First Name": ["John", "Jane"],
        "Last Name": ["Doe", "Smith"],
        "Gender": ["M", "F"]
    })

    mapper = FieldMapper(field_mapping)

    try:
        mapped_df = mapper.map_columns(input_df)
    except ValueError as e:
        assert "Missing required fields" in str(e)
    else:
        # If no exception, the test should fail
        assert False, "Expected ValueError due to missing fields, but none was raised."

def test_map_to_schema_success(raw_dataframe, field_mapping, schema):
    mapper = FieldMapper(field_mapping)
    df_structured = mapper.map_to_schema(raw_dataframe, schema)

    # Check columns and dtypes
    assert list(df_structured.columns) == ["name", "age", "email"]
    assert df_structured["age"].dtype == "int32"
    assert df_structured["name"].dtype == "object"
    assert df_structured["email"].dtype == "object"

def test_map_to_schema_missing_field(raw_dataframe, field_mapping):
    # Intentionally wrong schema (missing "email")
    wrong_schema = {
        "name": "str",
        "age": "int"
        # Missing "email"
    }

    mapper = FieldMapper(field_mapping)
    #df_mapped = mapper.map_columns(raw_dataframe)

    try:
        df_mapped = mapper.map_columns(raw_dataframe)
        mapper.map_to_schema(df_mapped, {"name": "str", "age": "int", "email": "str"})
    except ValueError as e:
        assert "Missing required fields" in str(e)
    else:
        # If no exception, the test should fail
        assert False, "Expected ValueError due to missing fields, but none was raised."
    # Email should be missing now
    # with pytest.raises(ValueError, match="Field 'email' is missing"):
        

def test_map_and_clean_fill_missing_values():
    field_mapping = {
        "name_of_person": "name",
        "age_years": "age",
        "contact": "email"
    }

    schema = {
        "name": "str",
        "age": "int",
        "email": "str"
    }

    df = pd.DataFrame({
        "name_of_person": ["John Doe", None],
        "age_years": [28, 0],
        "contact": ["john.doe@example.com", None]
    })

    mapper = FieldMapper(field_mapping)
    df_cleaned = mapper.map_and_clean(df, schema)

    # Assertions to check if there are no NaNs and if missing values are handled correctly
    assert df_cleaned.isnull().sum().sum() == 0  # No NaNs
    assert df_cleaned.loc[1, "name"] == "None"  # Missing name should be filled with empty string
    assert df_cleaned.loc[1, "age"] == 0  # Missing age should be filled with 0
    assert df_cleaned.loc[1, "email"] == 'None'  # Missing email should be filled with empty string



def test_mapper_integration_end_to_end(raw_dataframe, field_mapping, schema):
    mapper = FieldMapper(field_mapping)
    df_final = mapper.map_and_clean(raw_dataframe, schema)

    assert df_final.columns.tolist() == ["name", "age", "email"]
    assert df_final.dtypes["name"] == "object"
    assert df_final.dtypes["email"] == "object"
    assert pd.api.types.is_integer_dtype(df_final["age"])
