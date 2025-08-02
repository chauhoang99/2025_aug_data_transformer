import pandas as pd
import pytest

from exceptions import ColumnNotFound
from transformations import (
    filter_rows,
    rename_column,
    titlecase_column,
    trim_whitespace,
    uppercase_column,
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


def test_titlecase_column(sample_df):
    result = titlecase_column(sample_df, 'name')
    expected = ['John Doe', ' Jane Smith ', 'Alice Johnson']
    assert list(result['name']) == expected


def test_trim_whitespace(sample_df):
    result = trim_whitespace(sample_df, 'name')
    expected = ['John Doe', 'Jane Smith', 'alice johnson']
    assert list(result['name']) == expected


def test_transformations_with_invalid_column(sample_df):
    with pytest.raises(ColumnNotFound):
        filter_rows(sample_df, 'invalid_column', 'value')

    with pytest.raises(ColumnNotFound):
        uppercase_column(sample_df, 'column is not in data')

    with pytest.raises(ColumnNotFound):
        trim_whitespace(sample_df, 'column is not in data')


def test_column_not_found_error_message():
    df = pd.DataFrame({'name': ['John']})
    with pytest.raises(ColumnNotFound) as exc_info:
        filter_rows(df, 'status', 'active')
    assert "Column 'status' not found" == exc_info.value.detail


def test_rename_column_source_validation(sample_df):
    with pytest.raises(ColumnNotFound) as exc_info:
        rename_column(sample_df, 'nonexistent', 'new_name')
    assert "Column 'nonexistent' not found" == exc_info.value.detail


def test_multiple_transformations_error_handling(sample_df):
    # Test that errors are raised appropriately when chaining transformations
    with pytest.raises(ColumnNotFound) as exc_info:
        # First transformation succeeds, second fails
        df = uppercase_column(sample_df, 'name')
        titlecase_column(df, 'nonexistent')
    assert "Column 'nonexistent' not found" == exc_info.value.detail


def test_empty_dataframe_column_validation():
    empty_df = pd.DataFrame(columns=['name'])
    with pytest.raises(ColumnNotFound) as exc_info:
        uppercase_column(empty_df, 'status')
    assert "Column 'status' not found" == exc_info.value.detail


def test_case_sensitive_column_validation(sample_df):
    # Test that column validation is case sensitive
    with pytest.raises(ColumnNotFound) as exc_info:
        uppercase_column(sample_df, 'Name')  # 'Name' vs 'name'
    assert "Column 'Name' not found" == exc_info.value.detail


def test_whitespace_column_validation(sample_df):
    # Test that column names with whitespace are handled correctly
    with pytest.raises(ColumnNotFound) as exc_info:
        uppercase_column(sample_df, ' name ')  # Extra whitespace
    assert "Column ' name ' not found" == exc_info.value.detail
