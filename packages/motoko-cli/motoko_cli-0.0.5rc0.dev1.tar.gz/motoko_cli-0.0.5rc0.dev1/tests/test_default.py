import numpy as np
from motoko_cli import hello


def test_sort():
    assert np.array_equal(hello(), "Hello, World!")
