import json
from pathlib import Path
from typing import Type, Dict, Any

from marshmallow_dataclass import class_schema
from marshmallow_jsonschema import JSONSchema

from json2any.ProviderPlugins import ProviderPlugins

plugins = ProviderPlugins()
plugins.find_plugins()


def dump_schema(data_class: Type, schema_entries: Dict[str, str]):
    schema = class_schema(data_class)()

    json_schema = JSONSchema()

    schema_d = json_schema.dump(schema)
    schema_d.update(schema_entries)

    return schema_d


def dump_schema_f(data_class: Type, file_path: Path, schema_entries: Dict[str, str], indent=4):
    schema_d = schema_d = dump_schema(data_class, schema_entries)

    with open(file_path, mode='w') as file:
        json.dump(schema_d, file, indent=indent)


def dump_schema_s(data_class: Type, schema_entries: Dict[str, str], indent=4):
    schema_d = dump_schema(data_class, schema_entries)
    return json.dumps(schema_d, indent=indent)


def load_data_w_schema(rds_file: Path, data_class: Type) -> Any:
    if not rds_file.is_file():
        raise ValueError('File: "%s" is not a file' % rds_file)

    with rds_file.open(mode='r') as f:
        j_data = json.load(f)
        schema = class_schema(data_class)()
        runs_descriptor = schema.load(j_data)
        return runs_descriptor
