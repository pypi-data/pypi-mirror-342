from argparse import Namespace
from logging import getLogger

from json2any.Json2AnyException import Json2AnyException
from json2any.ProviderPluginType import ProviderPluginType
from json2any.ProviderPlugins import ProviderPlugins

plugins = ProviderPlugins()
plugins.find_plugins([ProviderPluginType.DATA, ProviderPluginType.SCHEMA])

log = getLogger(__name__)


def cmd_validate_setup(subparsers):
    global plugins

    parser = subparsers.add_parser('validate', aliases=['vali'], help='Validate Data schema')

    plugins.update_arg_parser(parser)

    parser.set_defaults(func=cmd_validate_execute)


def cmd_validate_execute(args: Namespace):
    global plugins

    plugins.process_args(args)

    if len(plugins.active_data_providers) == 0:
        raise Json2AnyException("At least one data provider has to be configured")

    for data_plugin in plugins.active_data_providers:
        if not data_plugin.get_schema_id():
            raise Json2AnyException("JSONSchema id is required for data validation")

    plugins.load_data()
    log.info('Data Validation OK')
