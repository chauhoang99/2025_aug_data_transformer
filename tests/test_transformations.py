import pytest
import pandas as pd
from transformations import (
    filter_rows,
    rename_column,
    uppercase_column,
    title_case_column,
    trim_whitespace
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'name': ['John Doe', ' Jane Smith ', 'alice johnson'],
        'status': ['active', 'inactive', 'active'],
        'age': [30, 25, 35]
    })


def test_filter_rows(sample_df):
    result = filter_rows(sample_df, 'status', 'active')
    assert len(result) == 2
    assert all(result['status'] == 'active')


def test_rename_column(sample_df):
    result = rename_column(sample_df, 'name', 'full_name')
    assert 'full_name' in result.columns
    assert 'name' not in result.columns
    assert list(result['full_name']) == list(sample_df['name'])


def test_uppercase_column(sample_df):
    result = uppercase_column(sample_df, 'name')
    expected = ['JOHN DOE', ' JANE SMITH ', 'ALICE JOHNSON']
    assert list(result['name']) == expected


def test_title_case_column(sample_df):
    result = title_case_column(sample_df, 'name')
    expected = ['John Doe', ' Jane Smith ', 'Alice Johnson']
    assert list(result['name']) == expected


def test_trim_whitespace(sample_df):
    result = trim_whitespace(sample_df, 'name')
    expected = ['John Doe', 'Jane Smith', 'alice johnson']
    assert list(result['name']) == expected


def test_transformations_with_invalid_column(sample_df):
    with pytest.raises(KeyError):
        filter_rows(sample_df, 'invalid_column', 'value')

    with pytest.raises(KeyError):
        uppercase_column(sample_df, 'invalid_column')

    with pytest.raises(KeyError):
        trim_whitespace(sample_df, 'invalid_column')
