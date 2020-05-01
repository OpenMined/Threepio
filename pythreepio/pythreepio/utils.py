try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources
import json
import static
from typing import Callable
from pythreepio.errors import TranslationMissing


def get_mapped_commands() -> dict:
    json_txt = pkg_resources.read_text(static, 'mapped_commands_full.json')
    return json.loads(json_txt)


class Command(object):

    def __init__(self, function_name: str, args: list,
                 kwargs: dict, attrs: list = [], exec_fn: Callable = None):
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.attrs = attrs
        self.exec_fn = exec_fn

    def execute_routine(self):
        if self.exec_fn is None:
            raise TranslationMissing(self.name)

        return self.exec_fn(*self.args, **self.kwargs)
