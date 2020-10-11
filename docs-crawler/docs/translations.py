"""
.. module:: docs
   :synopsis: Contains dictionary containing keys and values for translating words & commands between frameworks
"""

# dictionary containing values for translating words
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

# dictionary containing values for translating commands
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
            }, {
                "name": "linear_bias",
                "kwarg": True,
                "opt": True
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
                    "tfjs": "a"
                },
                {
                    "name": "other",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "b"
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
        "rtruediv": [{
            "args": [
                {
                    "name": "input",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "b"
                },
                {
                    "name": "other",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "a"
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
            "name": "rtruediv",
            "tfjs": "div",
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
        "rsub": [{
            "args": [
                {
                    "name": "other",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "b"
                },
                {
                    "name": "value",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "a"
                },
            ],
            "attrs": [
                "__rsub__"
            ],
            "name": "rsub",
            "tfjs": "sub"
        }],
        "copy": [{
            "args": [
                {
                    "name": "value",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "x"
                },
            ],
            "attrs": [
                "copy"
            ],
            "name": "copy",
            "tfjs": "clone"
        }],
        "float": [{
            "args": [
                {
                    "name": "value",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "x"
                },
                {
                    "name": "dtype",
                    "kwarg": False,
                    "opt": False,
                    "value": "float32",
                    "tfjs": "dtype"
                },
            ],
            "attrs": [
                "float"
            ],
            "name": "float",
            "tfjs": "cast"
        }],
        "select": [{
            "args": [
                {
                    "name": "value",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "x",
                },
                {
                    "name": "dim",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "axis",
                },
                {
                    "name": "index",
                    "kwarg": False,
                    "opt": False,
                    "tfjs": "indices",
                },
            ],
            "attrs": [
                "select"
            ],
            "name": "select",
            "tfjs": "gather",
        }],
    }
}
