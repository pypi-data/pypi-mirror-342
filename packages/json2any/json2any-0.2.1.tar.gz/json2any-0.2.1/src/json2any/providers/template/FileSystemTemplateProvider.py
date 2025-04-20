from argparse import Namespace, ArgumentParser
from logging import getLogger
from pathlib import Path
from typing import List, Optional

from jinja2 import BaseLoader, FileSystemLoader
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider

ARGS_PREFIX = 'fstp'

class FileSystemTemplateProvider(AbstractTemplateProvider):
    def __init__(self):
        self.log = getLogger(self.__class__.__name__)
        self.arg_paths: List[Path] = []
        self.template_location: Optional[Path] = None
        self.override_paths = False

    @property
    def arg_prefix(self) -> str:
        return ARGS_PREFIX

    @property
    def has_arguments(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def update_arg_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument(f'--{ARGS_PREFIX}-dir', help='Path to template  directory', type=Path,
                            action='append')
        parser.add_argument(f'--{ARGS_PREFIX}-override-paths',
                            action='store_true',
                            help='If supplied the "--fstp-dir" paths are override "rds.template_location" otherwise '
                                 'paths are appended to "rds.template_location" otherwise replaced')

    def process_args(self, args: Namespace) -> bool:
        if args.fstp_dir is None:
            return False

        self.override_paths = args.fstp_override_paths

        for template_path in args.fstp_dir:
            template_path: Path
            template_path = Path.cwd() / template_path
            template_path = template_path.resolve().absolute()

            if not template_path.is_dir():
                raise NotADirectoryError(f'{template_path} is not a directory')
            self.arg_paths.append(template_path)
        return True

    def init(self, template_location: str) -> None:
        self.template_location = Path(template_location)

    def get_loader(self, templates_path: Optional[str]) -> BaseLoader:
        paths = self.arg_paths
        if not self.override_paths and self.template_location:
            template_location = self.template_location
            if templates_path:
                template_location /= templates_path
            paths.append(template_location)

        loader = FileSystemLoader(paths)
        return loader
