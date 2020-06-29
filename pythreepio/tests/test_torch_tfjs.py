import pytest
from pythreepio.threepio import Threepio
from tests.fixtures.tfjs import abs as tfjs_abs


@pytest.fixture
def tfjs_threepio():
    return Threepio("torch", "tfjs", None)


def test_translates_tfjs_abs(tfjs_threepio):
    for i, input in enumerate(tfjs_abs["inputs"]):
        translations = tfjs_threepio.translate(input, lookup_command=True)
        for translation in translations:
            assert translation.attrs == tfjs_abs["answers"][i]
