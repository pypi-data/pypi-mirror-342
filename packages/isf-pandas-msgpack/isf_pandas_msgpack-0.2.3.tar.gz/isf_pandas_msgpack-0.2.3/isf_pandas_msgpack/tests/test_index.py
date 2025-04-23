from . import encode_decode, make_string_index
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal, assert_index_equal

def test_basic_index(pandas_data):

    for s, i in pandas_data.items():
        i_rec = encode_decode(None, i)
        assert_index_equal(i, i_rec)

    # datetime with no freq (GH5506)
    i = pd.Index([pd.Timestamp('20130101'), pd.Timestamp('20130103')])
    i_rec = encode_decode(None, i)
    assert_index_equal(i, i_rec)

    # datetime with timezone
    i = pd.Index([pd.Timestamp('20130101 9:00:00'), pd.Timestamp(
        '20130103 11:00:00')]).tz_localize('US/Eastern')
    i_rec = encode_decode(None, i)
    assert_index_equal(i, i_rec)

def test_multi_index(pandas_multi_index):

    for s, i in pandas_multi_index.items():
        i_rec = encode_decode(None, i)
        assert_index_equal(i, i_rec)

def test_str_index():
    i = make_string_index(100)

    i_rec = encode_decode(None, i)
    assert_index_equal(i, i_rec)

def test_categorical_index():
    # GH15487
    df = pd.DataFrame(np.random.randn(10, 2))
    df = df.astype({0: 'category'}).set_index(0)
    result = encode_decode(None, df)
    assert_frame_equal(result, df)