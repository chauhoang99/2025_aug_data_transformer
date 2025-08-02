import io
import json

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def sample_csv():
    csv_content = b"""name,status,age
John Doe,active,30
Jane Smith,inactive,25
Alice Johnson,active,35"""
    return io.BytesIO(csv_content)


def test_list_transformers():
    response = client.get("/available-transformers/")
    assert response.status_code == 200
    transformers = response.json()["available"]
    assert isinstance(transformers, dict)
    assert "filter_rows" in transformers
    assert "rename_column" in transformers
    assert "uppercase_column" in transformers
    assert "trim_whitespace" in transformers


def test_transform_data_success(sample_csv):
    pipeline = [
        {"name": "filter_rows", "params": {"column": "status", "value": "active"}},
        {"name": "uppercase_column", "params": {"column": "name"}}
    ]

    files = {"file": ("test.csv", sample_csv, "text/csv")}
    data = {"pipeline": json.dumps(pipeline)}

    response = client.post("/transform/", files=files, data=data)
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2  # Two active records
    assert all(record["status"] == "active" for record in result)
    assert all(record["name"].isupper() for record in result)


def test_transform_invalid_csv():
    # This string contains a non-ASCII character: 'é'
    # Encode it with Latin-1 (not UTF-8)
    csv_text = "invalid,csv\nname José".encode('latin-1')
    invalid_csv = io.BytesIO(csv_text)
    pipeline = [{"name": "uppercase_column", "params": {"column": "name"}}]

    files = {"file": ("test.csv", invalid_csv, "text/csv")}
    data = {"pipeline": json.dumps(pipeline)}

    response = client.post("/transform/", files=files, data=data)
    assert response.status_code == 400
    assert "Invalid CSV" in response.json()["detail"]


def test_transform_invalid_pipeline():
    csv_content = io.BytesIO(b"name,status\nJohn,active")
    files = {"file": ("test.csv", csv_content, "text/csv")}
    data = {"pipeline": "invalid json"}

    response = client.post("/transform/", files=files, data=data)
    assert response.status_code == 400
    assert "Invalid pipeline JSON" in response.json()["detail"]


def test_transform_unknown_transformer(sample_csv):
    pipeline = [{"name": "nonexistent_transformer", "params": {}}]

    files = {"file": ("test.csv", sample_csv, "text/csv")}
    data = {"pipeline": json.dumps(pipeline)}

    response = client.post("/transform/", files=files, data=data)
    assert response.status_code == 400
    assert "Unknown transformer" in response.json()["detail"]


def test_transform_pipeline_step_not_found(sample_csv):
    pipeline = [{"name": "filter_rows", "params": {"column": "status", "value": "active"}}, {"name": "rename_column", "params": {
        "old_name": "name", "new_name": "full_name"}}, {"name": "uppercase_column", "params": {"column": "full_name"}}]
    files = {"file": ("test.csv", sample_csv, "text/csv")}
    data = {"pipeline": json.dumps(pipeline)}
    response = client.post("/transform/", files=files, data=data)
    assert response.status_code == 400
    assert "Unknown pipeline param, please check again" in response.json()[
        "detail"]


def test_transform_invalid_csv_encoding():
    # Test with different CSV encoding issues
    test_cases = [
        (b"name,age\nJohn,\xff", "Invalid CSV encoding"),
        (b"no_header_row", "Invalid CSV format"),
        (b"", "Empty CSV file")
    ]

    pipeline = [{"name": "uppercase_column", "params": {"column": "name"}}]

    for csv_content, test_case in test_cases:
        invalid_csv = io.BytesIO(csv_content)
        files = {"file": ("test.csv", invalid_csv, "text/csv")}
        data = {"pipeline": json.dumps(pipeline)}

        response = client.post("/transform/", files=files, data=data)
        assert response.status_code == 400
        assert "Invalid CSV" in response.json()["detail"]


def test_transform_invalid_pipeline_formats():
    # Test various invalid pipeline formats
    test_cases = [
        ("not_json_at_all", "Invalid pipeline JSON"),
        ("{malformed_json", "Invalid pipeline JSON"),
        ("[]", "Invalid pipeline JSON"),  # Empty pipeline
        ('[{"invalid": "structure"}]', "Invalid pipeline JSON"),
    ]

    csv_content = io.BytesIO(b"name,status\nJohn,active")
    files = {"file": ("test.csv", csv_content, "text/csv")}

    for pipeline, expected_error in test_cases:
        data = {"pipeline": pipeline}
        response = client.post("/transform/", files=files, data=data)
        assert response.status_code == 400
        assert expected_error in response.json()["detail"]


def test_unknown_transformer_variations():
    # Test different scenarios of unknown transformers
    test_cases = [
        {"name": "nonexistent_transform", "params": {}},
        {"name": "UPPERCASE_COLUMN", "params": {}},  # Case sensitive check
        {"name": "filter_rows_typo", "params": {
            "column": "status", "value": "active"}},
        # Whitespace in transformer name
        {"name": " filter_rows ", "params": {}}
    ]

    csv_content = io.BytesIO(b"name,status\nJohn,active")
    files = {"file": ("test.csv", csv_content, "text/csv")}

    for transformer in test_cases:
        pipeline = [transformer]
        data = {"pipeline": json.dumps(pipeline)}
        response = client.post("/transform/", files=files, data=data)
        assert response.status_code == 400
        assert "Unknown transformer" in response.json()["detail"]


def test_invalid_pipeline_parameters():
    # Test various invalid parameter combinations
    test_cases = [
        (
            [{"name": "filter_rows", "params": {}}],  # Missing required params
            "Unknown pipeline param"
        ),
        (
            # Missing new_name
            [{"name": "rename_column", "params": {"old_name": "name"}}],
            "Unknown pipeline param"
        ),
        (
            # Wrong param name
            [{"name": "uppercase_column", "params": {"wrong_param": "name"}}],
            "Unknown pipeline param"
        ),
        (
            [{"name": "trim_whitespace", "params": None}],  # Null params
            "Unknown pipeline param"
        )
    ]

    csv_content = io.BytesIO(b"name,status\nJohn,active")
    files = {"file": ("test.csv", csv_content, "text/csv")}

    for pipeline, expected_error in test_cases:
        data = {"pipeline": json.dumps(pipeline)}
        response = client.post("/transform/", files=files, data=data)
        assert response.status_code == 400
        assert expected_error in response.json()["detail"]


def test_multiple_transformers_error_handling():
    # Test error handling in pipeline with multiple transformers
    test_cases = [
        (
            [
                {"name": "filter_rows", "params": {
                    "column": "status", "value": "active"}},
                {"name": "unknown_transformer", "params": {}}
            ],
            "Unknown transformer"
        ),
        (
            [
                {"name": "filter_rows", "params": {
                    "column": "status", "value": "active"}},
                {"name": "rename_column", "params": {"wrong_param": "name"}}
            ],
            "Unknown pipeline param"
        ),
        (
            [
                {"name": "filter_rows", "params": {
                    "column": "status", "value": "active"}},
                {"name": "rename_column", "params": {
                    "column": "name", "new_name": "full_name"}},
                {"name": "uppercase_column", "params": {"column": "wrong_name"}}
            ],
            "Column 'wrong_name' not found"
        )
    ]

    csv_content = io.BytesIO(b"name,status\nJohn,active\nJane,inactive")
    files = {"file": ("test.csv", csv_content, "text/csv")}

    for pipeline, expected_error in test_cases:
        data = {"pipeline": json.dumps(pipeline)}
        response = client.post("/transform/", files=files, data=data)
        assert response.status_code == 400
        assert expected_error in response.json()["detail"]
