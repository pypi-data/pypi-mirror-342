from argparse import Namespace, ArgumentParser
from logging import getLogger
from typing import Optional

from jinja2 import BaseLoader, PackageLoader
from json2any_plugin.AbstractTemplateProvider import AbstractTemplateProvider

ARGS_PREFIX = 'ptp'


class PackageTemplateProvider(AbstractTemplateProvider):
    def __init__(self):
        self.log = getLogger(self.__class__.__name__)
        self.package_name: Optional[str] = None
        self.package_path: Optional[str] = None

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
        parser.add_argument(f'--{ARGS_PREFIX}-package', help='Package name where the template are located')
        parser.add_argument(f'--{ARGS_PREFIX}-path', help='Path to template  directory within the package')

    def process_args(self, args: Namespace) -> bool:
        self.package_name = args.ptp_package
        self.package_path = args.ptp_path
        return self.package_name is not None

    def init(self, template_location: str) -> None:

        # CLI arguments take precedence
        if self.package_name is None:
            self.package_name = template_location

    def get_loader(self, templates_path: Optional[str]) -> BaseLoader:

        # CLI arguments take precedence
        if self.package_path is None:
            self.package_path = templates_path

        loader = PackageLoader(self.package_name, self.package_path)
        return loader
