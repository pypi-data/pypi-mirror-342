import json
from argparse import Namespace
from typing import Dict, Optional, Type

from importlib_resources import files
from json2any_plugin.AbstractSchemaProvider import AbstractSchemaProvider

import json2any.rds.v1 as s_v1
import json2any.rds.v2 as s_v2
import json2any.rds.v3 as s_v3


class RdsSchemaProvider(AbstractSchemaProvider):

    def get_schema_class(self, schema_id: str) -> Optional[Type]:
        if schema_id == s_v1.JSON2ANY_SCHEMA_ID:
            return s_v1.Json2AnyDescriptor
        elif schema_id == s_v2.JSON2ANY_SCHEMA_ID:
            return s_v2.Json2AnyDescriptor
        elif schema_id == s_v3.JSON2ANY_SCHEMA_ID:
            return s_v3.Json2AnyDescriptor
        else:
            return None

    def get_json_schema_metadata(self, schema_id: str) -> Optional[Dict[str, str]]:
        if schema_id == s_v1.JSON2ANY_SCHEMA_ID:
            return s_v1.JSON2ANY_SCHEMA_METADATA
        elif schema_id == s_v2.JSON2ANY_SCHEMA_ID:
            return s_v2.JSON2ANY_SCHEMA_METADATA
        elif schema_id == s_v3.JSON2ANY_SCHEMA_ID:
            return s_v3.JSON2ANY_SCHEMA_METADATA
        else:
            return None

    def get_json_schema(self, schema_id: str) -> Optional[Dict[str, Dict]]:
        r_files = files('json2any.schema')
        for res in r_files.iterdir():
            if res.suffix != '.json':
                continue
            with res.open(mode='r') as f:
                schema = json.load(f)
                s_id = schema['$id']
                if s_id == schema_id:
                    return schema
        return None

    def get_available_schemas(self) -> Dict[str, str]:

        available_schemas = {}
        r_files = files('json2any.schema')
        for res in r_files.iterdir():
            if res.suffix != '.json':
                continue
            with res.open(mode='r') as f:
                schema = json.load(f)
                s_id = schema['$id']
                s_title = schema['title']
                available_schemas[s_id] = s_title
        return available_schemas

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def arg_prefix(self) -> str:
        return ''

    @property
    def has_arguments(self) -> bool:
        return False

    def update_arg_parser(self, parser: '_ArgumentGroup') -> None:
        # Unused
        pass

    def process_args(self, args: Namespace) -> bool:
        return True

    def init(self, **kwargs) -> None:
        # Unused
        pass
