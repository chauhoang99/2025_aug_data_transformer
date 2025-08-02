## Introduction

A small data pipeline that receives input csv file from an API endpoint and then perform data transformation.
The transformation steps are pluggable and allow flexibility to add or remove any step.

## Setup

git clone https://github.com/chauhoang99/2025_aug_data_transformer.git
cd .\2025_aug_data_transformer\
pip install -r requirements.txt
python -m uvicorn main:app --reload

## Test the API

For testing the API please run this command: 
curl -X POST http://127.0.0.1:8000/transform/ -F "file=@test.csv" -F "pipeline=[{\"name\":\"filter_rows\",\"params\":{\"column\":\"status\",\"value\":\"active\"}},{\"name\":\"rename_column\",\"params\":{\"column\":\"name\",\"new_name\":\"full_name\"}},{\"name\":\"uppercase_column\",\"params\":{\"column\":\"full_name\"}}]"
