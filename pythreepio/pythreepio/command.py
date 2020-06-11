import sys
from typing import Callable
from pythreepio.errors import TranslationMissing


class Placeholder(object):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value


class Command(object):
    def __init__(
        self,
        function_name: str,
        args: list,
        kwargs: dict,
        attrs: list = [],
        placeholder_output: str = None,
        exec_fn: Callable = None,
    ):
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.attrs = attrs
        self.placeholder_output = placeholder_output
        self.exec_fn = exec_fn
        self.frameworks = {"tf": "tensorflow"}

    def execute_routine(self, store={}):
        if self.exec_fn is None:
            attrs = self.attrs.copy()
            translated_cmd = sys.modules[self.frameworks[attrs.pop(0)]]
            while len(attrs) > 0:
                translated_cmd = getattr(translated_cmd, attrs.pop(0))
            self.exec_fn = translated_cmd

        args = []
        for arg in self.args:
            if isinstance(arg, Placeholder):
                args.append(store[arg.key])
            else:
                args.append(arg)

        return self.exec_fn(*args, **self.kwargs)


def cmd_from_info(info, store: dict) -> Command:
    args = []
    kwargs = {}
    for arg in info["args"]:
        is_kwarg = arg["kwarg"]
        name = arg.get("placeholder_input", arg["name"])
        if is_kwarg is True:
            if name in store:
                kwargs[name] = store[name]
        else:
            if name in store:
                args.append(store[name])
            else:
                args.append(Placeholder(name))

    return Command(
        info["name"],
        args,
        kwargs,
        info.get("attrs", []),
        info.get("placeholder_output", None),
    )
