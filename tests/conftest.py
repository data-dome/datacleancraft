import pytest
import pandas as pd

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Name": ["John Doe", "Jane Smith"],
        "Email": ["john.doe@example.com", "jane.smith@example.com"],
        "Phone": ["123-456-7890", "555-123-4567"],
        "Birthdate": ["1985-10-20", "1990-05-15"],
        "Salary": [55000, 67000],
        "Comments": ["Good", "Excellent"]
    })

@pytest.fixture
def field_mapping():
    return {
        "Name": "full_name",
        "Email": "email_address",
        "Phone": "phone_number",
        "Birthdate": "dob",
        "Salary": "annual_salary",
        "Comments": "notes"
    }

@pytest.fixture
def raw_dataframe():
    data = {
        "name_of_person": ["John Doe", "Jane Smith", "Alice Brown"],
        "age_years": [28, 35, 22],
        "contact": ["john.doe@example.com", "jane.smith@example.com", "alice.brown@example.com"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def field_mapping():
    return {
        "name_of_person": "name",
        "age_years": "age",
        "contact": "email"
    }

@pytest.fixture
def schema():
    return {
        "name": "str",
        "age": "int",
        "email": "str"
    }

@pytest.fixture
def sample_data():
    """Fixture for generating sample numeric data."""
    data = {
        "feature1": [0.5, 0.7, 2.0, 0.3, 99.9],
        "feature2": [1.0, 0.8, 2.1, 0.4, 98.5]
    }
    return pd.DataFrame(data)