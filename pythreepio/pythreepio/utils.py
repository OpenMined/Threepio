import json

COMMANDS_FILE_PATH = '../static/mapped_commands.json'

def get_mapped_commands() -> dict:
    commands = {}
    with open(COMMANDS_FILE_PATH, 'r') as f:
        commands = json.load(f)
    return commands


class Command(object):
    def __init__(self, code: str, function_name:str, args:list, kwargs: dict):
        self.code = code
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs

    