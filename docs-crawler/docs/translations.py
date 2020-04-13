WORD_TRANSLATIONS = {
    'tfjs': {
        'dim': 'axis',
        'input': 'a',
        'other': 'b',
        'eq': 'equal',
        't': 'transpose',
    },
    'torch': {},
    'tf': {}
}

COMMAND_TRANSLATIONS = {
    'tf': {},
    'tfjs': {},
    'torch': {
        "truediv": {
            "args": [
                {
                    "name": "input",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "x"
                },
                {
                    "name": "other",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "y"
                },
                {
                    "name": "out",
                    "kwarg": True,
                    "opt": True
                }
            ],
            "attrs": [
                "torch",
                "div"
            ],
            "name": "truediv",
            "tfjs": "div",
            "tf": "Truediv"
        },
        "sub": {
            "args": [
                {
                    "name": "value",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "a"
                },
                {
                    "name": "other",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "b"
                },
            ],
            "attrs": [
                "torch",
                "sub"
            ],
            "name": "sub",
            "tfjs": "sub"
        },
    }
}
