import torch
import tensorflow as tf
from pythreepio.command import Command

abs = {
    "inputs": [Command("abs", [tf.constant([1, -2, 3, -4])], {})],
    "answers": [[tf.constant([1, 2, 3, 4])]],
}

add = {
    "inputs": [
        Command(
            "add", [tf.constant([[1, 0], [0, 1]]), tf.constant([[0, 1], [1, 0]])], {}
        )
    ],
    "answers": [[tf.constant([[1, 1], [1, 1]])]],
}

add2 = {
    "inputs": [
        Command(
            "__add__",
            [tf.constant([[1, 0], [0, 1]]), tf.constant([[0, 1], [1, 0]])],
            {},
        )
    ],
    "answers": [[tf.constant([[1, 1], [1, 1]])]],
}

matmul = {
    "inputs": [
        Command(
            "matmul",
            [tf.constant([[1, 0], [0, 1]]), tf.constant([[0, 1], [1, 0]])],
            {},
        )
    ],
    "answers": [[tf.constant([[0, 1], [1, 0]])]],
}

mean = {
    "inputs": [Command("mean", [tf.constant([0.2294, -0.5481, 1.3288])], {})],
    "answers": [[tf.constant(0.3367)]],
}

mul = {
    "inputs": [Command("mul", [tf.constant([10, 20, 30]), 100], {})],
    "answers": [[tf.constant([1000, 2000, 3000])]],
}

div = {
    "inputs": [Command("div", [tf.constant([10, 20, 30, 40]), 0.5], {})],
    "answers": [[tf.constant([20, 40, 60, 80])]],
}

eq = {
    "inputs": [
        Command(
            "eq", [tf.constant([[1, 2], [3, 4]]), tf.constant([[1, 1], [4, 4]])], {}
        )
    ],
    "answers": [[tf.constant([[1, 0], [0, 1]])]],
}

sum = {
    "inputs": [Command("sum", [tf.constant([1, 2, 3])], {})],
    "answers": [[tf.constant([6])]],
}

argmax = {
    "inputs": [
        Command(
            "argmax", [tf.constant([[0, 10, 2], [1, 20, 30], [10, 0, 0]])], {"dim": -1}
        )
    ],
    "answers": [[tf.constant([1, 2, 0])]],
}

t = {
    "inputs": [Command("t", [tf.constant([[1, 2, 3], [4, 5, 6]])], {})],
    "answers": [[tf.constant([[1, 4], [2, 5], [3, 6]])]],
}

softmax = {
    "inputs": [
        Command(
            "softmax",
            [tf.constant([[2, 1, 0.1], [2, 1, 0.1], [2, 1, 0.1]])],
            {"dim": -1},
        )
    ],
    "answers": [
        tf.constant(
            [[0.659, 0.2424, 0.0985], [0.659, 0.2424, 0.0985], [0.659, 0.2424, 0.0985]]
        )
    ],
}

relu = {
    "inputs": [Command("relu", [[1, -2, 3]], [])],
    "answers": [tf.constant([1, 0, 3])],
}

sub = {
    "inputs": [Command("sub", [[1, 2, 3], [1, 2, 3]], {})],
    "answers": [[tf.constant([0, 0, 0])]],
}

truediv = {
    "inputs": [Command("truediv", [[1, 2, 3], [1, 2, 3]], {})],
    "answers": [[tf.constant([1, 1, 1])]],
}

linear = {
    "inputs": [
        Command(
            "linear", [tf.constant([[0, 0], [1, 1]]), tf.constant([[1, 1], [0, 0]])], {}
        )
    ],
    "answers": [tf.constant([[0, 0], [2, 0]])],
}
