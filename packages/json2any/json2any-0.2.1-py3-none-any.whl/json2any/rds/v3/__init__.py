from json2any.rds.v3.CopyJobDescriptor import CopyJobDescriptor
from json2any.rds.v3.JobDescriptor import JobDescriptor
from json2any.rds.v3.Json2AnyDescriptor import Json2AnyDescriptor
from json2any.rds.v3.RenderJobDescriptor import RenderJobDescriptor

JSON2ANY_SCHEMA_NAME = 'https://gitlab.com/json2any/json2any/rds'
JSON2ANY_SCHEMA_VERSION = 3
JSON2ANY_SCHEMA_ID = f'{JSON2ANY_SCHEMA_NAME}_v{JSON2ANY_SCHEMA_VERSION}'
JSON2ANY_SCHEMA_METADATA = {
    '$id': JSON2ANY_SCHEMA_ID,
    'title': 'json2any Runs description schema',
    'description': 'Describes how the templates and data are put together to generate output'
}

__all__ = ['JSON2ANY_SCHEMA_VERSION', 'JSON2ANY_SCHEMA_ID', 'JSON2ANY_SCHEMA_METADATA', 'Json2AnyDescriptor',
           'JobDescriptor', 'CopyJobDescriptor', 'RenderJobDescriptor']
