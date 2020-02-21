import re
import torch  # noqa: F401
import tensorflow as tf  # noqa: F401

from .utils import get_mapped_commands, Command


class Threepio(object):
    def __init__(self):
        self.commands = get_mapped_commands()

    def normalize_func_name(self, name: str):
        alpha = re.compile('[^a-zA-Z]')
        return alpha.sub('', name).lower()

    def translate(self, to_lang: str, cmd: Command):
        t = self.commands[to_lang][self.normalize_func_name(cmd.function_name)]
        translated_cmd = globals()[t['attrs'].pop(0)]
        while len(t['attrs']) > 0:
            translated_cmd = getattr(translated_cmd, t['attrs'].pop(0))

        return translated_cmd(*cmd.args, **cmd.kwargs)


if __name__ == '__main__':
    c = Threepio()
