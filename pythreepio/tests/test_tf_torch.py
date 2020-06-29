import pytest
import torch

from pythreepio.threepio import Threepio
from tests.fixtures.tf import abs as tf_abs
from tests.util import process_tests, torch_check_answer


@pytest.fixture
def tf_threepio():
    return Threepio("tf", "torch", torch)


def test_translates_tf_abs(tf_threepio):
    process_tests(tf_abs, tf_threepio, torch_check_answer)
