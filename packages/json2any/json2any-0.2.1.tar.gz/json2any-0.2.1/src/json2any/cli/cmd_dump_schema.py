import importlib
import json
from argparse import Namespace
from logging import getLogger
from pathlib import Path

import json2any.rds.v1 as rds_v1
import json2any.rds.v2 as rds_v2
import json2any.rds.v3 as rds_v3
from json2any.ProviderPluginType import ProviderPluginType
from json2any.ProviderPlugins import ProviderPlugins
from json2any.rds.schema_utils import dump_schema, dump_schema_f

plugins = ProviderPlugins()
plugins.find_plugins([ProviderPluginType.SCHEMA])

log = getLogger(__name__)


def schema_import(name):
    components = name.split('.')
    clazz_name = components[-1]
    module = importlib.import_module('.'.join(components[:-1]))
    clazz = getattr(module, clazz_name)
    mdata = getattr(module, 'CENUM_SCHEMA_METADATA')

    return clazz, mdata


def cmd_dump_schema_setup(subparsers):
    global plugins

    parser = subparsers.add_parser('dump-schema', aliases=['ds'], help='dump JSONSchema')
    parser.add_argument('schema_id', help='$id of JSONSchema')


    parser.add_argument('--regenerate', help='Attempt to generate schema from class', action='store_true')
    parser.add_argument('-pp', '--pretty-print', help='Pretty print json schema', action='store_true')
    parser.add_argument('-of', '--output-file', help='Write schema to file')

    plugins.update_arg_parser(parser)

    parser.set_defaults(func=cmd_dump_schema_execute)


def cmd_dump_schema_execute(args: Namespace):
    global plugins

    plugins.process_args(args)
    out_file = args.output_file

    if args.schema_id == 'rds':
        schema_dir = Path(__file__).resolve().parent.parent

        out_file = schema_dir / 'schema' / f'rds.schema_v{rds_v3.JSON2ANY_SCHEMA_VERSION}.json'
        dump_schema_f(rds_v3.Json2AnyDescriptor, out_file, rds_v3.JSON2ANY_SCHEMA_METADATA)

        out_file = schema_dir / 'schema' / f'rds.schema_v{rds_v2.JSON2ANY_SCHEMA_VERSION}.json'
        dump_schema_f(rds_v2.Json2AnyDescriptor, out_file, rds_v2.JSON2ANY_SCHEMA_METADATA)

        out_file = schema_dir / 'schema' / f'rds.schema_v{rds_v1.JSON2ANY_SCHEMA_VERSION}.json'
        dump_schema_f(rds_v1.Json2AnyDescriptor, out_file, rds_v1.JSON2ANY_SCHEMA_METADATA)

        return

    schema_id = args.schema_id

    if args.regenerate:
        clazz = plugins.get_schema_class(schema_id)
        mdata = plugins.get_json_schema_metadata(schema_id)
        schema = dump_schema(clazz, mdata)
    else:
        schema = plugins.get_json_schema(schema_id)

    if args.pretty_print:
        schema_s = json.dumps(schema, indent=4)
    else:
        schema_s = json.dumps(schema)

    if out_file:
        with open(out_file, mode='w') as f:
            f.write(schema_s)
    else:
        log.info(schema_s)
