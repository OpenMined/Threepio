import pytest
import tensorflow as tf

from pythreepio.threepio import Threepio
from tests.fixtures.torch import (
    abs as torch_abs,
    add,
    add2,
    matmul,
    mean,
    mul,
    div,
    eq,
    sum as torch_sum,
    argmax,
    t,
    sub,
    truediv,
    linear,
)
from tests.util import process_tests, tf_check_answer


@pytest.fixture
def torch_threepio():
    return Threepio("torch", "tf", tf)


def test_translates_abs(torch_threepio):
    process_tests(torch_abs, torch_threepio, tf_check_answer)


def test_translates_add(torch_threepio):
    process_tests(add, torch_threepio, tf_check_answer)


def test_translates_d_add(torch_threepio):
    process_tests(add2, torch_threepio, tf_check_answer)


def test_translates_matmul(torch_threepio):
    process_tests(matmul, torch_threepio, tf_check_answer)


def test_translates_mean(torch_threepio):
    process_tests(mean, torch_threepio, tf_check_answer)


@pytest.mark.skip(reason="Requires mul -> multiply mapping")
def test_translates_mul(torch_threepio):
    process_tests(mul, torch_threepio, tf_check_answer)


@pytest.mark.skip(reason="Requires div -> truediv mapping")
def test_translates_div(torch_threepio):
    process_tests(div, torch_threepio, tf_check_answer)


@pytest.mark.skip(reason="Requires eq -> equal mapping")
def test_translates_eq(torch_threepio):
    process_tests(eq, torch_threepio, tf_check_answer)


def test_translates_sum(torch_threepio):
    process_tests(torch_sum, torch_threepio, tf_check_answer)


def test_translates_linear(torch_threepio):
    for i, input_cmd in enumerate(linear["inputs"]):
        translations = torch_threepio.translate(input_cmd, lookup_command=True)
        translations.pop(0)
        # Create a store for command outputs
        store = {}

        # Execute every translation
        for j, translation in enumerate(translations):
            result = translation.execute_routine(store)
            if translation.placeholder_output is not None:
                store[translation.placeholder_output] = result

        # Check end result
        answer = linear["answers"][i]
        tf_check_answer(result, answer)


@pytest.mark.skip(reason="Requires dim -> axis mapping")
def test_translates_argmax(torch_threepio):
    process_tests(argmax, torch_threepio, tf_check_answer)


@pytest.mark.skip(reason="Requires t -> transpose mapping")
def test_translates_transpose(torch_threepio):
    process_tests(t, torch_threepio, tf_check_answer)


@pytest.mark.skip(reason="Requires sub -> subtract mapping")
def test_translates_subtract(torch_threepio):
    process_tests(sub, torch_threepio, tf_check_answer)


def test_translates_truediv(torch_threepio):
    process_tests(truediv, torch_threepio, tf_check_answer)
