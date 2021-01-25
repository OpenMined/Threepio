import re

from typing import Tuple, List
from .utils import get_mapped_commands
from .errors import TranslationMissing
from .command import Command, cmd_from_info


class Threepio(object):
    """
    Threepio Class to translate a command from one framework to another.

    :param from_lang: Framework to convert from
    :type from_lang: str
    :param to_lang: Framework to convert to
    :type to_lang: str
    :param framework: Reference to package that represents to_lang
    :type framework: object
    """

    def __init__(self, from_lang: str, to_lang: str, framework: object):
        """Initialize a Threepio object to translate commands."""

        # Fetch a dictionary of mapped commands between frameworks
        self.commands = get_mapped_commands()
        # Assert framework to convert from is present in mapped commands
        assert from_lang in self.commands, f"\"{from_lang}\" is not in the mapped commands."
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.framework = framework

    def _normalize_func_name(self, name: str) -> str:
        """Normalizes a function name to lower case and keep only alphabets

        :param name: function name to normalize
        :type name: str

        :return: returns a string converted to lowercase keeping only alphabets
        :rtype: str
        """
        alpha = re.compile("[^a-zA-Z]")
        return alpha.sub("", name).lower()

    def _order_args(
        self, cmd: Command, from_info: dict, to_info: dict
    ) -> Tuple[list, dict]:
        """Extracts and orders the args and kwargs according to translated command

        :param cmd: command to be translated
        :type cmd: Command
        :param from_info: Dictionary of info for the command for the `from` framework
        :type from_info: dict
        :param to_info: Dictionary of info for the command for the `to` framework
        :type to_info: dict

        :return: Returns ordered - args and kwargs
        :rtype:  Tuple[list, dict]
        """
        new_args = []
        new_kwargs = {}

        def get_to_arg_index(from_arg):
            """Returns index for the original argument in the translated command arguments list

            :param from_arg: info of ith argument of 'from' framework
            :type from_arg: dict

            :return: returns the index of original argument or None
            :rtype:  int or None
            """
            return next(
                (
                    index
                    for index, d in enumerate(to_info["args"])
                    if d["name"] == from_arg.get(self.to_lang, None)
                ),
                None,
            )

        # Loop through the command arguments For eg. Tensors to perform operation to
        for i, arg in enumerate(cmd.args):
            # Extract the info of ith argument of `from` framework
            from_arg = from_info["args"][i]
            # Check if the same name argument is present in `to` framework
            # If yes, get its index
            to_arg_index = get_to_arg_index(from_arg)

            # Append arguments which don't have same name between frameworks
            if to_arg_index is None:
                new_args.append(arg)
                continue

            # Append arguments with same names at the proper position of the `to` framework
            new_args.insert(to_arg_index, arg)

        # Add static args, if any
        for from_arg in from_info["args"]:
            if "value" in from_arg:
                to_arg_index = get_to_arg_index(from_arg)
                if to_arg_index is not None:
                    new_args.insert(to_arg_index, from_arg["value"])

        # If any kwargs are normal args, splice them in as well
        for k, v in cmd.kwargs.items():
            # Map kwargs similarly if provided
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
        """Translates command which has multiple translated chained commands

        :param orig_cmd: command to be translated
        :type orig_cmd: Command
        :param commands_info: chained commmands with info
        :type commands_info: list

        :return: Returns translated commands
        :rtype:  list
        """
        cmd_config = commands_info.pop(0)
        store = {}
        for i, arg in enumerate(orig_cmd.args):
            # Store the command arguments
            cmd_config["args"][i]["value"] = arg
            store[cmd_config["args"][i]["name"]] = arg

        new_cmds = [cmd_config]
        for from_info in commands_info:
            # Creates a command given info and arguments with values
            cmd = cmd_from_info(from_info, store)

            # Get the info of the command for the framework we want to convert to with the new alias of the command
            to_info = self.commands[self.to_lang][
                self._normalize_func_name(from_info.get(self.to_lang))
            ][0]

            new_cmds.append(self.translate_command(cmd, from_info, to_info))
        return new_cmds

    def translate_command(self, cmd, from_command, to_command):
        """Translates a Command Object after knowing it exists in both frameworks

        :param cmd: command to be translated
        :type cmd: Command
        :param from_command: Dictionary of info for the command for the `from` framework
        :type from_command: dict
        :param to_command: Dictionary of info for the command for the `to` framework
        :type to_command: dict

        :return: returns a list of translated commands
        :rtype: list
        """

        translated_cmd = None
        # Extracts and orders the args and kwargs according to translated command
        args, kwargs = self._order_args(cmd, from_command, to_command)
        output = from_command.get("placeholder_output", None)
        # Return a new Command object created after translation with ordered args and kwargs
        return Command(
            to_command["name"],
            args,
            kwargs,
            attrs=to_command["attrs"],
            placeholder_output=output,
            exec_fn=translated_cmd,
        )

    def translate(self, cmd: Command) -> List[Command]:
        """Translates a Command Object

        :param cmd: command to be translated
        :type cmd: Command

        :return: returns a list of translated command/s
        :rtype: list
        """

        # Normalize the function name
        normalized_func_name = self._normalize_func_name(cmd.function_name)
        # Get the info of the command from the framework to be translated from
        from_info = self.commands[self.from_lang].get(normalized_func_name)
        # Throw Exception if the command does not exist in the framework to be translated from
        if from_info is None:
            raise TranslationMissing(cmd.function_name)
        # Check if translated command has multiple chained commands
        if len(from_info) > 1:
            return self.translate_multi(cmd, from_info)

        # Extract the info since there is only one command
        from_info = from_info[0]

        # Check if the alias of the command exists in the framework to translate to
        if from_info.get(self.to_lang, None) is None:
            raise TranslationMissing(cmd.function_name)

        # Get the info of the command for the framework we want to convert to with the new alias of the command
        to_info = self.commands[self.to_lang][
            self._normalize_func_name(from_info.get(self.to_lang))
        ]

        return [self.translate_command(cmd, from_info, to_info[0])]
