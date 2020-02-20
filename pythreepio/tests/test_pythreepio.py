import torch
import tensorflow as tf

from pythreepio import __version__
from pythreepio.threepio import Threepio
from pythreepio.utils import Command

def test_version():
    assert __version__ == '0.1.0'

def test_tf_torch_matmul():
    tensor_a = torch.tensor([[1, 2], [5, 6]])
    tensor_b = torch.tensor([[1, 2], [5, 6]])
    expected_answer = torch.tensor([[11, 14], [35, 46]])

    c = Command('tf.linalg.matmul(a, b)', 'matmul', [tensor_a, tensor_b], {})
    t = Threepio()
    r = t.translate('torch', c)

    assert torch.equal(r, expected_answer)

def test_torch_tf_matmul():
    tensor_a = tf.constant([[1, 2], [5, 6]])
    tensor_b = tf.constant([[1, 2], [5, 6]])
    expected_answer = tf.constant([[11, 14], [35, 46]])

    c = Command('torch.matmul(a, b)', 'matmul', [tensor_a, tensor_b], {})
    t = Threepio()
    r = t.translate('tf', c)
    assert tf.reduce_all(tf.equal(r, expected_answer))