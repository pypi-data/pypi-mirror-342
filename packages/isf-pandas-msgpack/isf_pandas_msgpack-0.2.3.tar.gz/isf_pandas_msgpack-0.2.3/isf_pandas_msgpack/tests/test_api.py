import pytest
import pandas as pd
import numpy as np
from . import to_msgpack, read_msgpack
from pandas.testing import assert_frame_equal

def test_string_io(tmp_file_msg):

    df = pd.DataFrame(np.random.randn(10, 2))

    s = to_msgpack(None, df)
    result = read_msgpack(s)
    assert_frame_equal(result, df)

    # s = to_msgpack(None, df)
    # result = read_msgpack(s)
    # tm.assert_frame_equal(result, df)

    to_msgpack(str(tmp_file_msg), df)
    with open(tmp_file_msg, 'rb') as fh:
        result = read_msgpack(s)
    assert_frame_equal(result, df)

    # s = to_msgpack(self.path, df)
    # result = read_msgpack(s)
    # tm.assert_frame_equal(result, df)

    s = to_msgpack(None, df)
    with open(tmp_file_msg, 'wb') as fh:
        fh.write(s)
    result = read_msgpack(tmp_file_msg)
    assert_frame_equal(result, df)

def test_iterator_with_string_io():

    dfs = [pd.DataFrame(np.random.randn(10, 2)) for i in range(5)]
    s = to_msgpack(None, *dfs)
    for i, result in enumerate(read_msgpack(s, iterator=True)):
        assert_frame_equal(result, dfs[i])

def test_invalid_arg():
    # GH10369
    class A(object):
        def __init__(self):
            self.read = 0

    with pytest.raises(ValueError):
        read_msgpack(path_or_buf=None)
    with pytest.raises(ValueError):
        read_msgpack(path_or_buf={})
    with pytest.raises(ValueError):
        read_msgpack(path_or_buf=A())