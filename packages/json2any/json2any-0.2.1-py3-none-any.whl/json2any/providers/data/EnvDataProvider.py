import os
from argparse import ArgumentParser, Namespace
from logging import getLogger
from typing import Dict, Any, Optional

from json2any_plugin.AbstractDataProvider import AbstractDataProvider


class EnvDataProvider(AbstractDataProvider):

    def __init__(self):
        self.log = getLogger(self.__class__.__name__)
        super().__init__(data_key='env')

    @property
    def arg_prefix(self) -> str:
        return 'env'

    @property
    def has_arguments(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def update_arg_parser(self, parser: ArgumentParser):
        super().update_arg_parser(parser)
        parser.add_argument('--env-data', action='store_true',
                            help='')

    def process_args(self, args: Namespace) -> bool:
        super().process_args(args)

        return args.env_data

    def init(self, **kwargs):
        self.log.debug('EnvDataProvider initialised')

    def load_data(self) -> Dict[str, Any]:
        return os.environ.copy()

    def get_schema_id(self) -> Optional[str]:
        return None
