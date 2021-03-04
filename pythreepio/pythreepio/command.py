import sys
from typing import Callable


class Placeholder(object):
    """
    Helper Placeholder class to hold arguments of commands.

    :param key: name of argument
    :type key: str
    :param value: value of argument
    :type value: default(None)
    """

    def __init__(self, key, value=None):
        self.key = key
        self.value = value


class Command(object):
    """
    Command Class which holds commands and its details of a certain framework.

    :param function_name: Command name in a particular framework
    :type function_name: str
    :param args: Arguments of the command For eg. Tensors to compute on
    :type args: list
    :param kwargs: Key value arguments of a command
    :type kwargs: dict
    :param attrs: Full API path of the command eg. tf.math.add
    :type attrs: dict
    :param placeholder_output: helper variable for 1->many translation
    :type placeholder_output: str
    :param exec_fn: store the command callable
    :type exec_fn: callable 
    """

    def __init__(
        self,
        function_name: str,
        args: list,
        kwargs: dict,
        attrs: list = [],
        placeholder_output: str = None,
        exec_fn: Callable = None,
    ):
        # Initialize a Command object to store command and its details of a certain framework.
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.attrs = attrs
        self.placeholder_output = placeholder_output
        self.exec_fn = exec_fn
        self.frameworks = {"tf": "tensorflow", "torch": "torch"}

    def execute_routine(self, store={}):
        """
        Executes a translated command

        :param store: Stores key value arguments of a command.
        :type store: dict
        """
        if self.exec_fn is None:
            # Copy full API Path of command
            attrs = self.attrs.copy()
            # Get module of converted framework
            translated_cmd = sys.modules[self.frameworks[attrs.pop(0)]]
            # Extract the command name from the full API Path
            while len(attrs) > 0:
                translated_cmd = getattr(translated_cmd, attrs.pop(0))
            self.exec_fn = translated_cmd

        args = []
        # Map command arguments to appropriate key value pairs
        for arg in self.args:
            if isinstance(arg, Placeholder):
                args.append(store[arg.key])
            else:
                args.append(arg)
        return self.exec_fn(*args, **self.kwargs)


def cmd_from_info(info, store: dict) -> Command:
    """
    Creates a command given info and arguments with values.

    :param info: Details of attributes of a command
    :type info: dict
    :param store: Stores key value arguments of a command.
    :type store: dict

    :return: Returns a Command object populated with args & kwargs
    :rtype:  Command
    """
    args = []
    kwargs = {}
    for arg in info["args"]:
        is_kwarg = arg["kwarg"]
        name = arg.get("placeholder_input", arg["name"])
        # Map args and kwargs from input to command argmuents
        if is_kwarg is True:
            if name in store:
                kwargs[name] = store[name]
        else:
            if name in store:
                args.append(store[name])
            else:
                # Placeholder for normal args
                args.append(Placeholder(name))

    return Command(
        info["name"],
        args,
        kwargs,
        info.get("attrs", []),
        info.get("placeholder_output", None),
    )
