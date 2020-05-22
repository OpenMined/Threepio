import pytest
import torch
import tensorflow as tf

from pythreepio.threepio import Threepio
from pythreepio.utils import Command


@pytest.fixture
def threepio_tf():
    return Threepio('torch', 'tf', tf)


@pytest.fixture
def threepio_torch():
    return Threepio('tf', 'torch', torch)


def test_tf_torch_matmul(threepio_torch):
    tensor_a = torch.tensor([[1, 2], [5, 6]])
    tensor_b = torch.tensor([[1, 2], [5, 6]])
    expected_answer = torch.tensor([[11, 14], [35, 46]])

    c = threepio_torch.translate(
        Command('matmul', [tensor_a, tensor_b], {}),
        lookup_command=True
    )
    r = c.execute_routine()

    assert torch.equal(r, expected_answer)


def test_torch_tf_matmul(threepio_tf):
    tensor_a = tf.constant([[1, 2], [5, 6]])
    tensor_b = tf.constant([[1, 2], [5, 6]])
    expected_answer = tf.constant([[11, 14], [35, 46]])

    c = threepio_tf.translate(
        Command('matmul', [tensor_a, tensor_b], {}),
        lookup_command=True
    )
    r = c.execute_routine()

    assert tf.reduce_all(tf.equal(r, expected_answer))
