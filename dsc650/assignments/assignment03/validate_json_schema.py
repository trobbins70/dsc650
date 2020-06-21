from pathlib import Path
import json
from jsonschema import validate
import gzip
from dsc650.assignments.assignment03.util import (
    SCHEMA_DIR, RESULTS_DIR, PROCESSED_DATA_DIR
)

def read_jsonl_data():
    src_data_path = PROCESSED_DATA_DIR.joinpath('openflights').joinpath('routes.jsonl.gz')
    with gzip.open(src_data_path, 'rb') as f:
        records = [json.loads(line) for line in f.readlines()]
    return records


def validate_jsonl_data(records):
    schema_path = SCHEMA_DIR.joinpath('routes-schema.json')
    with open(schema_path) as f:
        schema = json.load(f)
    for i, record in enumerate(records):
        validate(instance=record, schema=schema)
    # validation_csv_path = RESULTS_DIR.joinpath('validation-results.csv')



def main():
    records = read_jsonl_data()
    validate_jsonl_data(records)


if __name__ == '__main__':
    main()
