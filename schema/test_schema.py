#!/usr/bin/env python

import json
import yaml
import os.path
from pathlib import Path

import jsonschema

testcases_dir = os.path.join(
    os.path.dirname(__file__),
    "testcases"
)

schema_path = os.path.join(os.path.dirname(__file__), "schema.json")

def load_and_validate(path: str, schema: object, expected: bool) -> bool:
    # load file
    object = None
    with open(path, "r") as testfile:
        if path.endswith(".json"):
            object = json.load(testfile)
        elif path.endswith(".yaml") or path.endswith(".yml"):
            object = yaml.safe_load(testfile)

    result = False

    try:
        jsonschema.validate(object, schema)
        if expected:
            print(f"[v] {path}: Validation succeeded when it was expected to succeed")
            return True
        else:
            print(f"[x] {path}:  Validation succeeded when it was expected to fail")
            return False
    except jsonschema.ValidationError as e:
        if expected:
            print(f"[x] {path}: Validation failed when it was expected to succeed: {e}")
            return False
        else:
            print(f"[v] {path}: Validation failed when it was expected to fail.")
            return True


if __name__ == "__main__":
    print("loading json schema...")
    
    schema = None
    with open(schema_path, "r") as schema_file:
        schema = json.load(schema_file)

    print("[i] JSON schema loaded")

    results = []

    # good cases
    for path in Path(os.path.join(testcases_dir, "good")).glob("**/*"):
        res = load_and_validate(path.__str__(), schema, True)
        results.append(res)

    # good cases
    for path in Path(os.path.join(testcases_dir, "bad")).glob("**/*"):
        res = load_and_validate(path.__str__(), schema, False)
        results.append(res)

    for res in results:
        if not res:
            exit(1)
    
    exit(0)
        

     
