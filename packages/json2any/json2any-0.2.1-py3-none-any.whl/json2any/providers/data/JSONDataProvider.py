import json
from argparse import ArgumentParser, Namespace
from logging import getLogger
from pathlib import Path
from typing import Dict, Any, Optional

from json2any_plugin.AbstractDataProvider import AbstractDataProvider


class JSONDataProvider(AbstractDataProvider):

    def __init__(self):
        self.log = getLogger(self.__class__.__name__)
        super().__init__()
        self.json_file_path: Optional[Path] = None
        self.schema_id: Optional[str] = None

    @property
    def arg_prefix(self) -> str:
        return 'json'

    @property
    def has_arguments(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def update_arg_parser(self, parser: ArgumentParser):
        super().update_arg_parser(parser)
        parser.add_argument('--json-data', type=Path,
                            help='Data Loader: input JSON file: "--json-data /path/to/file.json"')

        parser.add_argument('--json-schema-id', type=str,
                            help='JSONSchema $id used to validate data loaded')

    def process_args(self, args: Namespace) -> bool:
        super().process_args(args)

        if args.json_data is None:
            return False

        self.schema_id = args.json_schema_id

        if not args.json_data.is_file():
            raise ValueError(f'Input JSON file "{args.json_data}" is not a file.')
        self.json_file_path = args.json_data

        return True

    def init(self, **kwargs):
        self.log.debug('JSONDataProvider initialised; data path: %s', str(self.json_file_path))

    def load_data(self) -> Dict[str, Any]:
        with self.json_file_path.open(mode='r') as f:
            data = json.load(f)
            return data

    def get_schema_id(self) -> Optional[str]:
        return self.schema_id
