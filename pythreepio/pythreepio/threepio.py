import re

from typing import Tuple
from .utils import get_mapped_commands, Command
from .errors import TranslationMissing


class Threepio(object):
    def __init__(self, from_lang: str, to_lang: str, framework: object):
        self.commands = get_mapped_commands()
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.framework = framework

    def _normalize_func_name(self, name: str, lang: str) -> str:
        alpha = re.compile('[^a-zA-Z]')
        result = alpha.sub('', name).lower()

        if result in self.commands[lang]:
            return result

        raise TranslationMissing(name)

    def _order_args(self, cmd: Command, from_info: dict,
                    to_info: dict) -> Tuple[list, dict]:
        new_args = []
        new_kwargs = {}
        for i, arg in enumerate(cmd.args):
            from_arg = from_info['args'][i]
            to_arg_index = next(
                (
                    index for index, d in enumerate(
                        to_info['args']
                    )
                    if d['name'] == from_arg.get(self.to_lang, None)
                ),
                None
            )

            if to_arg_index is None:
                new_args.append(arg)
                continue

            new_args.insert(to_arg_index, arg)

        # If any kwargs are normal args, splice them in as well
        for k, v in cmd.kwargs.items():
            from_arg = [a for a in from_info['args'] if a['name'] == k][0]
            to_arg_index = next(
                (
                    index for index, d in enumerate(
                        to_info['args']
                    )
                    if d['name'] == from_arg.get(self.to_lang, {})
                ),
                None
            )

            if to_arg_index is None:
                new_kwargs[k] = v

            new_args.insert(to_arg_index, v)

        return new_args, new_kwargs

    def translate(self, cmd: Command, lookup_command: bool = False) -> Command:
        from_info = self.commands[self.from_lang][
            self._normalize_func_name(cmd.function_name, self.from_lang)
        ]
        to_info = self.commands[self.to_lang][
            self._normalize_func_name(
                from_info.get(self.to_lang),
                self.to_lang
            )
        ]

        attrs = to_info['attrs'][1:]
        translated_cmd = None
        if lookup_command:
            translated_cmd = self.framework

            while len(attrs) > 0:
                translated_cmd = getattr(translated_cmd, attrs.pop(0))

        args, kwargs = self._order_args(cmd, from_info, to_info)

        return Command(to_info['name'], args, kwargs, attrs=to_info['attrs'],
                       exec_fn=translated_cmd)
