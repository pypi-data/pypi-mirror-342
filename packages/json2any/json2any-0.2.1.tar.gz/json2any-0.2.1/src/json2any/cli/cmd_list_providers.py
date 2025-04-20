import os
from argparse import Namespace
from logging import getLogger

from json2any_plugin.AbstractDataProvider import AbstractDataProvider
from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider
from json2any_plugin.AbstractSchemaProvider import AbstractSchemaProvider
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider

from json2any.ProviderPluginType import ProviderPluginType
from json2any.ProviderPlugins import ProviderPlugins

plugins = ProviderPlugins()
plugins.find_plugins()

log = getLogger(__name__)


def cmd_list_providers_setup(subparsers):
    global plugins

    parser = subparsers.add_parser('list-providers', aliases=['lp'], help='List available providers')

    plugins.update_arg_parser(parser)

    parser.set_defaults(func=cmd_list_providers_execute)


def cmd_list_providers_execute(args: Namespace):
    global plugins

    plugins.process_args(args)

    log.info(f'{os.linesep}Schema Data Providers')
    for provider in plugins.providers:
        if isinstance(provider, AbstractDataProvider):
            log.info(f' * class: {provider.__class__.__module__}{provider.__class__.__name__}: {provider.name}')

    log.info(f'{os.linesep}Schema Helper Providers')
    for provider in plugins.providers:
        if isinstance(provider, AbstractHelperProvider):
            log.info(f' * class: {provider.__class__.__module__}{provider.__class__.__name__}: {provider.name}')

    log.info(f'{os.linesep}Schema Info Providers')
    for provider in plugins.providers:
        if isinstance(provider, AbstractSchemaProvider):
            log.info(f' * class: {provider.__class__.__module__}{provider.__class__.__name__}: {provider.name}')

    log.info(f'{os.linesep}Template Providers')
    for provider in plugins.providers:
        if isinstance(provider, AbstractTemplateProvider):
            log.info(f' * class: {provider.__class__.__module__}{provider.__class__.__name__}: {provider.name}')
