from enum import Enum

from json2any_plugin.AbstractDataProvider import AbstractDataProvider
from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider
from json2any_plugin.AbstractSchemaProvider import AbstractSchemaProvider
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider


class ProviderPluginType(Enum):
    DATA = AbstractDataProvider
    SCHEMA = AbstractSchemaProvider
    HELPER = AbstractHelperProvider
    TEMPLATE = AbstractTemplateProvider
