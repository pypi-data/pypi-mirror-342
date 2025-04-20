from argparse import Namespace
from logging import getLogger

from json2any.ProviderPluginType import ProviderPluginType
from json2any.ProviderPlugins import ProviderPlugins

plugins = ProviderPlugins()
plugins.find_plugins([ProviderPluginType.SCHEMA])

log = getLogger(__name__)


def cmd_list_schemas_setup(subparsers):
    global plugins

    parser = subparsers.add_parser('list-schemas', aliases=['ls'], help='List available JSONSchema')

    plugins.update_arg_parser(parser)

    parser.set_defaults(func=cmd_list_schemas_execute)


def cmd_list_schemas_execute(args: Namespace):
    global plugins

    plugins.process_args(args)

    for plg in plugins.active_schema_providers:
        for s_id, s_title in plg.get_available_schemas().items():
            log.info(f' $id: {s_id}: "{s_title}"')
