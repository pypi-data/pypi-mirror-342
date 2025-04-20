from argparse import Namespace, ArgumentParser
from pathlib import Path
from typing import Any, Dict

from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider


class ExampleHelper:

    def min(self, a, b):
        r = min(a, b)
        return r

    def max(self, a, b):
        r = max(a, b)
        return r

    def to_upper(self, s: str):
        return s.upper()

    def get_cwd(self):
        return Path.cwd()

    def include_raw(self, path: str):
        if path is None or str.strip(path) == "":
            return ""

        path = Path(path)
        if path.is_file():
            return path.read_text()
        else:
            raise FileNotFoundError(path)


def filter_splitlines(input: str):
    if not input:
        return None
    return input.splitlines()


class ExampleHelperProvider(AbstractHelperProvider):

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def arg_prefix(self) -> str:
        return ''

    @property
    def has_arguments(self) -> bool:
        return False

    def update_arg_parser(self, parser: ArgumentParser) -> None:
        # argparser not used
        pass

    def process_args(self, args: Namespace) -> bool:
        return True

    def init(self, **kwargs) -> None:
        # unused
        pass

    def get_helper_object(self) -> Any:
        return ExampleHelper()

    def get_filters(self) -> Dict[str, Any]:
        return {
            'splitlines': filter_splitlines
        }

    def get_helper_ns(self) -> str:
        return "example"
