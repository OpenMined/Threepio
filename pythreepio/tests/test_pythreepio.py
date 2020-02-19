import torch

from pythreepio import __version__
from pythreepio.threepio import Threepio
from pythreepio.utils import Command

def test_version():
    assert __version__ == '0.1.0'

def test_tf_torch_matmul():
    tensor_a = torch.tensor([[1, 2], [5, 6]])
    tensor_b = torch.tensor([[1, 2], [5, 6]])
    c = Command('tf.linalg.matmul(a, b)', 'matmul', [tensor_a, tensor_b], {})
    t = Threepio()
    t.translate('torch', c)

def test_torch_tf_matmul():
    tensor_a = torch.tensor([[1, 2], [5, 6]])
    tensor_b = torch.tensor([[1, 2], [5, 6]])
    c = Command('tf.linalg.matmul(a, b)', 'matmul', [tensor_a, tensor_b], {})
    t = Threepio()
    t.translate('torch', c)