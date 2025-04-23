from . import encode_decode
from pandas._testing import assert_categorical_equal

def test_basic(pandas_categorical_data):
    # run multiple times here
    for _ in range(10):
        for s, i in pandas_categorical_data.items():
            i_rec = encode_decode(None, i)
            assert_categorical_equal(i, i_rec)