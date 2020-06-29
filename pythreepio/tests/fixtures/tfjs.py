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
