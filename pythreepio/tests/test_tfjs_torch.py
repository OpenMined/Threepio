import pytest
import torch

from pythreepio.threepio import Threepio
from tests.fixtures.tfjs import abs_torch
from tests.util import process_tests, torch_check_answer


@pytest.fixture
def tf_threepio():
    return Threepio("tfjs", "torch", torch)


def test_translates_tf_abs(tf_threepio):
    process_tests(abs_torch, tf_threepio, torch_check_answer)
