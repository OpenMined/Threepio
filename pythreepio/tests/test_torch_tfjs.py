import pytest
from pythreepio.threepio import Threepio
from tests.fixtures.tfjs import abs as tfjs_abs
from tests.fixtures.tfjs import to_float as tfjs_to_float
from tests.fixtures.tfjs import rtruediv as tfjs_rtruediv


@pytest.fixture
def tfjs_threepio():
    return Threepio("torch", "tfjs", None)


def test_translates_tfjs_abs(tfjs_threepio):
    for i, input in enumerate(tfjs_abs["inputs"]):
        translations = tfjs_threepio.translate(input, lookup_command=True)
        for translation in translations:
            assert translation.attrs == tfjs_abs["answers"][i]


def test_translates_tfjs_to_float(tfjs_threepio):
    for i, input in enumerate(tfjs_to_float["inputs"]):
        translations = tfjs_threepio.translate(input, lookup_command=True)
        for translation in translations:
            assert translation.function_name == tfjs_to_float["answers"][i].function_name
            assert translation.args == tfjs_to_float["answers"][i].args
            assert translation.kwargs == tfjs_to_float["answers"][i].kwargs
            assert translation.attrs == tfjs_to_float["answers"][i].attrs


def test_translates_tfjs_rtruediv(tfjs_threepio):
    for i, input in enumerate(tfjs_rtruediv["inputs"]):
        translations = tfjs_threepio.translate(input, lookup_command=True)
        for translation in translations:
            assert translation.function_name == tfjs_rtruediv["answers"][i].function_name
            assert translation.args == tfjs_rtruediv["answers"][i].args
            assert translation.kwargs == tfjs_rtruediv["answers"][i].kwargs
            assert translation.attrs == tfjs_rtruediv["answers"][i].attrs

