from argparse import ArgumentParser, Namespace
from logging import getLogger
from typing import List, Optional, Dict, Any, Type

from json2any_plugin.AbstractDataProvider import AbstractDataProvider
from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider
from json2any_plugin.AbstractProvider import AbstractProvider
from json2any_plugin.AbstractSchemaProvider import AbstractSchemaProvider
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider
from jsonschema import validate
from pkg_resources import iter_entry_points

from json2any.Json2AnyException import Json2AnyException
from json2any.ProviderPluginType import ProviderPluginType
from json2any.providers.template.FileSystemTemplateProvider import FileSystemTemplateProvider
from json2any.rds import Json2AnyDescriptor


class ProviderPlugins:

    def __init__(self):
        self.log = getLogger(self.__class__.__name__)

        self.providers: List[AbstractProvider] = []
        self.active_providers: List[AbstractProvider] = []

    def find_plugins(self, plugin_types: List[ProviderPluginType] = None):

        if plugin_types is None:
            classes = [item.value for item in list(ProviderPluginType)]
        else:
            classes = [item.value for item in plugin_types]
        classes = tuple(classes)
        for entry_point in iter_entry_points(group='json2any.plugin', name=None):
            ep_class = entry_point.load()
            if not issubclass(ep_class, classes):
                continue
            try:
                self.providers.append(ep_class())
            except Exception as e:
                self.log.error(f'Helper Provider "{ep_class}" thrown exception during construction', exc_info=e)

    def update_arg_parser(self, parser: ArgumentParser):
        for provider in self.providers:
            if not provider.has_arguments:
                continue

            provider_name = 'Invalid provider'
            try:

                provider_name = provider.name
                arg_grp = parser.add_argument_group(provider_name, f'Arguments related to {provider_name}')

                provider.update_arg_parser(arg_grp)
            except Exception as e:
                self.log.error(f'Provider "{provider_name}" ({provider.__class__.__name__}) has thrown exception'
                               f' - removed', exc_info=e)
                self.providers.remove(provider)

    def process_args(self, args: Namespace):

        for provider in self.providers:
            is_active = provider.process_args(args)
            if is_active:
                self.active_providers.append(provider)

    @property
    def active_data_providers(self) -> List[AbstractDataProvider]:
        return [p for p in self.active_providers if isinstance(p, AbstractDataProvider)]

    @property
    def active_help_providers(self) -> List[AbstractHelperProvider]:
        return [p for p in self.active_providers if isinstance(p, AbstractHelperProvider)]

    @property
    def active_schema_providers(self) -> List[AbstractSchemaProvider]:
        return [p for p in self.active_providers if isinstance(p, AbstractSchemaProvider)]

    def get_default_template_provider(self) -> FileSystemTemplateProvider:
        for provider in self.providers:
            if isinstance(provider, FileSystemTemplateProvider):
                return provider

    def get_template_provider(self, rds_path: str, rds: Json2AnyDescriptor) -> AbstractTemplateProvider:

        template_location = rds.template_location
        if not template_location:
            template_location = rds_path

        # first try to find provider configured via command line args
        self.log.trace('Trying to find cmd line configured template provider ')

        atps = [p for p in self.active_providers if isinstance(p, AbstractTemplateProvider)]
        if len(atps) == 1:
            template_provider = atps[0]
            template_provider.init(template_location=template_location)
            self.log.debug('Using commandline configured Template Provider: %s', template_provider.name)
            return template_provider

        elif len(atps) > 1:
            names = [f'"{p.name}"' for p in atps]
            names_s = ', '.join(names)
            raise Json2AnyException(f'Multiple template providers selected: {names_s}')

        # secondly try one set in rds
        if rds.template_provider:
            self.log.trace('Trying to find rds selected Template Provider ')
            atps = [p for p in self.providers if
                    isinstance(p, AbstractTemplateProvider) and p.name == rds.template_provider]

            if len(atps) == 1:
                template_provider = atps[0]
                template_provider.init(template_location=template_location)
                self.log.debug('Using rds selected Template Provider: %s', template_provider.name)
                return template_provider

            elif len(atps) > 1:
                names = [f'"{p.name}"' for p in atps]
                names_s = ', '.join(names)
                raise Json2AnyException(f'Multiple template providers selected: {names_s}')

        # third choice is default one
        self.log.trace('Trying to find default Template Provider ')

        template_provider = self.get_default_template_provider()
        template_provider.init(template_location=template_location)
        self.log.debug('Using default Template Provider: %s', template_provider.name)
        return template_provider

    def get_json_schema(self, schema_id) -> Optional[Dict[str, Any]]:
        for sp in self.active_schema_providers:
            schema = sp.get_json_schema(schema_id)
            if schema is not None:
                return schema
        return None

    def get_schema_class(self, schema_id) -> Optional[Type]:
        for sp in self.active_schema_providers:
            clazz = sp.get_schema_class(schema_id)
            if clazz is not None:
                return clazz
        return None

    def get_json_schema_metadata(self, schema_id) -> Optional[Dict[str, str]]:
        for sp in self.active_schema_providers:
            mdata = sp.get_json_schema_metadata(schema_id)
            if mdata is not None:
                return mdata
        return None

    def load_data(self) -> Dict[str, Any]:
        data = {}
        for data_provider in self.active_data_providers:
            self.log.debug('Loading data using Data provider: %s', data_provider.name)
            try:
                prov_data = data_provider.load_data()
                schema_id = data_provider.get_schema_id()
                if schema_id:
                    schema = self.get_json_schema(schema_id)
                    if schema is None:
                        self.log.warning('Schema %s not found, skipping validation', schema_id)
                    else:
                        validate(instance=prov_data, schema=schema)
                data[data_provider.data_key] = prov_data

            except Exception as e:
                raise Json2AnyException(f'Failed to load data using provider "{data_provider.name}"') from e
        return data
