WORD_TRANSLATIONS = {
    'tfjs': {
        'dim': 'axis',
        'input': 'a',
        'other': 'b',
        'eq': 'equal',
        't': 'transpose',
        'gt': 'greater'
    },
    'torch': {},
    'tf': {}
}

COMMAND_TRANSLATIONS = {
    'tf': {},
    'tfjs': {},
    'torch': {
        "linear": [{
            "args": [{
                "name": "linear_input",
                "kwarg": False,
                "opt": False
            }, {
                "name": "linear_weight",
                "kwarg": False,
                "opt": False
            }],
            "placeholder_output": "linear_ret"
        }, {
            "args": [
                {
                    "name": "input",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "a",
                    "placeholder_input": "linear_weight"
                }
            ],
            "attrs": [
                "torch",
                "t"
            ],
            "name": "t",
            "tfjs": "transpose",
            "tf": "transpose",
            "placeholder_output": "weight_t"
        }, {
            "args": [
                {
                    "name": "input",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "a",
                    "placeholder_input": "linear_input"
                },
                {
                    "name": "other",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "b",
                    "placeholder_input": "weight_t"
                },
                {
                    "name": "out",
                    "kwarg": True,
                    "opt": True
                }
            ],
            "attrs": [
                "torch",
                "matmul"
            ],
            "name": "matmul",
            "tfjs": "matmul",
            "tf": "matmul",
            "placeholder_output": "linear_ret"
        }],
        "truediv": [{
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
            "name": "Truediv",
            "tfjs": "div",
            "tf": "Truediv"
        }],
        "sub": [{
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
        }],
    }
}
