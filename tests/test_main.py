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
    pipeline = [ { "name": "filter_rows", "params": { "column": "status", "value": "active" }}, { "name": "rename_column", "params": { "old_name": "name", "new_name": "full_name" }}, { "name": "uppercase_column", "params": { "column": "full_name" }}]
    files = {"file": ("test.csv", sample_csv, "text/csv")}
    data = {"pipeline": json.dumps(pipeline)}
    response = client.post("/transform/", files=files, data=data)
    assert response.status_code == 400
    assert "Unknown pipeline param, please check again" in response.json()["detail"]
