import pytest
import pandas as pd

@pytest.fixture(scope="session")
def sample_postal_codes():
    return ['H2X 1Y1', '12345', 'ABC123', 'K1A 0B1']

@pytest.fixture(scope="session")
def sample_dataframe():
    return pd.DataFrame({
        'postal_codes': ['H2X 1Y1', '12345', 'ABC123', 'K1A 0B1']
    })

@pytest.fixture(scope="session")
def prompt_template():
    return """Classify this {col_value} as whether it is a correctly formatted postal code. Answer only by Yes or No""" 