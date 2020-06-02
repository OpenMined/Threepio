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


@pytest.fixture
def threepio():
    return Threepio("torch", "tf", tf)


def round(val, decimals=0):
    multiplier = tf.constant(10 ** decimals, dtype=val.dtype)
    return tf.round(val * multiplier) / multiplier


def check_answer(result, answer):
    assert tf.reduce_all(tf.equal(round(result, 3), round(answer, 3)))


def process_tests(command, threepio):
    for i, input in enumerate(command["inputs"]):
        translations = threepio.translate(input, lookup_command=True)
        for j, translation in enumerate(translations):
            result = translation.execute_routine()
            answer = command["answers"][i][j]
            check_answer(result, answer)


def test_translates_abs(threepio):
    process_tests(torch_abs, threepio)


@pytest.mark.skip(reason="Translate to keras.layers.add instead of math.add")
def test_translates_add(threepio):
    process_tests(add, threepio)


@pytest.mark.skip(reason="Translate to keras.layers.add instead of math.add")
def test_translates_d_add():
    process_tests(add2)


def test_translates_matmul(threepio):
    process_tests(matmul, threepio)


def test_translates_mean(threepio):
    process_tests(mean, threepio)


@pytest.mark.skip(reason="Requires mul -> multiply mapping")
def test_translates_mul(threepio):
    process_tests(mul, threepio)


@pytest.mark.skip(reason="Requires div -> truediv mapping")
def test_translates_div(threepio):
    process_tests(div, threepio)


@pytest.mark.skip(reason="Requires eq -> equal mapping")
def test_translates_eq(threepio):
    process_tests(eq, threepio)


def test_translates_sum(threepio):
    process_tests(torch_sum, threepio)


def test_translates_linear(threepio):
    for i, input_cmd in enumerate(linear["inputs"]):
        translations = threepio.translate(input_cmd, lookup_command=True)
        cmd_config = translations.pop(0)
        # Create a store for command outputs
        store = {}

        # Execute every translation
        for j, translation in enumerate(translations):
            result = translation.execute_routine(store)
            if translation.placeholder_output is not None:
                store[translation.placeholder_output] = result

        # Check end result
        answer = linear["answers"][i]
        check_answer(result, answer)


@pytest.mark.skip(reason="Requires dim -> axis mapping")
def test_translates_argmax(threepio):
    process_tests(argmax, threepio)


@pytest.mark.skip(reason="Requires t -> transpose mapping")
def test_translates_transpose(threepio):
    process_tests(t, threepio)


@pytest.mark.skip(reason="Requires sub -> subtract mapping")
def test_translates_subtract(threepio):
    process_tests(sub, threepio)


def test_translates_truediv(threepio):
    process_tests(truediv, threepio)
