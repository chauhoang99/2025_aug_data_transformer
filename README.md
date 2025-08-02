# Introduction

- Flexible transformation pipeline
- Pluggable transformation steps
- Support for multiple data operations:
  - Filter rows based on column values
  - Rename columns
  - Convert text to uppercase
  - Convert text to title case
  - Trim whitespace
- Error handling for invalid inputs
- Easy to extend with new transformations

# Setup

## Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Docker (optional)

## 1. Without Docker

```
git clone https://github.com/chauhoang99/2025_aug_data_transformer.git
cd .\2025_aug_data_transformer\
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## 2. With Docker

```
git clone https://github.com/chauhoang99/2025_aug_data_transformer.git
cd .\2025_aug_data_transformer\
docker compose up -d
```

# The APIs

## The Transform Endpoint
`POST /transform/`

### Parameters:
- `file`: CSV file to transform
- `pipeline`: JSON array of transformation steps

### Example:
```bash
curl -X POST http://127.0.0.1:8000/transform/ \
  -H "X-API-Key: supersecretkey123" \
  -F "file=@test.csv" \
  -F 'pipeline=[
    {"name": "filter_rows", "params": {"column": "status", "value": "active"}},
    {"name": "rename_column", "params": {"column": "name", "new_name": "full_name"}},
    {"name": "uppercase_column", "params": {"column": "full_name"}}
  ]'
```
What it does it that it will send the test.csv file in the repo to the transformer, the pipeline is defined by the "pipeline" parameter.

## The Available Transformers Endpoint

`GET /available-transformers/`

Returns a list of available transformation operations.

For testing, the already repo includes a test.csv file. The endpoint also can accept any other csv file.

# What can be better:

In this version the authorization method is very simple and just for the purpose of Proof of Concept only, in real life we can replace it with a more robust authentication/authorization method like JWT or SSO.
