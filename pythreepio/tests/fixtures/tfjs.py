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

t1 = torch.Tensor([[[1,2], [3,4]], [[5,6], [7,8]]])
select = {
  "inputs": [Command("select", [
    t1,
    0,
    1
  ],
                     {})],
  "answers": [Command("gather", [t1, 1, 0], {}, ["tf", "gather"])],
}

t1 = torch.Tensor([1, -2, 3, -4])
t2 = torch.Tensor([5, 5, 5, 5])
to_float = {
    "inputs": [Command("float", [t1], {})],
    "answers": [Command("cast", [t1, "float32"], {}, ["tf", "cast"])],
}

rsub = {
    "inputs": [Command("__rsub__", [t1, 1], {})],
    "answers": [Command("sub", [1, t1], {}, ["tf", "sub"])],
}

rtruediv = {
    "inputs": [Command("rtruediv", [t2, t1], {})],
    "answers": [Command("div", [t1, t2], {}, ["tf", "div"])],
}

reshape = {
    "inputs": [Command("reshape", [t1, [2, 2]], {})],
    "answers": [Command("reshape", [t1, [2, 2]], {}, ["reshape"])],
}
