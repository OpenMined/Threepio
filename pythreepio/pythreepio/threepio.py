import re

from typing import Tuple, List
from .utils import get_mapped_commands
from .errors import TranslationMissing
from .command import Command, cmd_from_info


class Threepio(object):
    def __init__(self, from_lang: str, to_lang: str, framework: object):
        self.commands = get_mapped_commands()
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.framework = framework

    def _normalize_func_name(self, name: str, lang: str) -> str:
        alpha = re.compile("[^a-zA-Z]")
        return alpha.sub("", name).lower()

    def _order_args(
        self, cmd: Command, from_info: dict, to_info: dict
    ) -> Tuple[list, dict]:
        new_args = []
        new_kwargs = {}
        for i, arg in enumerate(cmd.args):
            from_arg = from_info["args"][i]
            to_arg_index = next(
                (
                    index
                    for index, d in enumerate(to_info["args"])
                    if d["name"] == from_arg.get(self.to_lang, None)
                ),
                None,
            )

            if to_arg_index is None:
                new_args.append(arg)
                continue

            new_args.insert(to_arg_index, arg)

        # If any kwargs are normal args, splice them in as well
        for k, v in cmd.kwargs.items():
            from_arg = [a for a in from_info["args"] if a["name"] == k][0]
            to_arg_index = next(
                (
                    index
                    for index, d in enumerate(to_info["args"])
                    if d["name"] == from_arg.get(self.to_lang, {})
                ),
                None,
            )

            if to_arg_index is None:
                new_kwargs[k] = v
                continue

            new_args.insert(to_arg_index, v)

        return new_args, new_kwargs

    def translate_multi(self, orig_cmd, commands_info):
        cmd_config = commands_info.pop(0)
        store = {}
        for i, arg in enumerate(orig_cmd.args):
            cmd_config["args"][i]["value"] = arg
            store[cmd_config["args"][i]["name"]] = arg

        new_cmds = [cmd_config]
        for from_info in commands_info:
            cmd = cmd_from_info(from_info, store)
            to_info = self.commands[self.to_lang][
                self._normalize_func_name(from_info.get(self.to_lang), self.to_lang)
            ][0]

            new_cmds.append(self.translate_command(cmd, from_info, to_info))
        return new_cmds

    def translate_command(self, cmd, from_command, to_command):
        attrs = to_command["attrs"][1:]
        translated_cmd = None
        args, kwargs = self._order_args(cmd, from_command, to_command)
        output = from_command.get("placeholder_output", None)

        return Command(
            to_command["name"],
            args,
            kwargs,
            attrs=to_command["attrs"],
            placeholder_output=output,
            exec_fn=translated_cmd,
        )

    def translate(self, cmd: Command, lookup_command: bool = False) -> List[Command]:
        from_info = self.commands[self.from_lang][
            self._normalize_func_name(cmd.function_name, self.from_lang)
        ]
        if len(from_info) > 1:
            return self.translate_multi(cmd, from_info)

        from_info = from_info[0]

        if from_info.get(self.to_lang, None) is None:
            raise TranslationMissing(cmd.function_name)

        to_info = self.commands[self.to_lang][
            self._normalize_func_name(from_info.get(self.to_lang), self.to_lang)
        ]

        return [self.translate_command(cmd, from_info, to_info[0])]
