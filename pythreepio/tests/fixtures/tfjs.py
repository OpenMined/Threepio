import torch
from pythreepio.command import Command

abs = {
    "inputs": [Command("abs", [torch.Tensor([1, -2, 3, -4])], {})],
    "answers": [["tf", "abs"]],
}

abs_torch = {
    "inputs": [Command("abs", [torch.Tensor([1, -2, 3, -4])], {})],
    "answers": [[torch.Tensor([1, 2, 3, 4])]],
}

t1 = torch.Tensor([1, -2, 3, -4])
t2 = torch.Tensor([5, 5, 5, 5])
to_float = {
    "inputs": [Command("float", [t1], {})],
    "answers": [Command("cast", [t1, "float32"], {}, ["tf", "cast"])],
}

rtruediv = {
    "inputs": [Command("rtruediv", [t2, t1], {})],
    "answers": [Command("div", [t1, t2], {}, ["tf", "div"])],
}

reshape = {
    "inputs": [Command("reshape", [t1, [2, 2]], {})],
    "answers": [Command("reshape", [t1, [2, 2]], {}, ["reshape"])],
}
