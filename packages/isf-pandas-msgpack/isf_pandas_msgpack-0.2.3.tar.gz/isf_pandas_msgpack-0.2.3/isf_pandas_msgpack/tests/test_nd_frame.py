from . import encode_decode, check_arbitrary, to_msgpack, read_msgpack
import pytest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from packaging.version import Version


# class TestNDFrame(TestPackers):

def test_basic_frame(pandas_dataframe):
    for s, i in pandas_dataframe.items():
        i_rec = encode_decode(None, i)
        assert_frame_equal(i, i_rec)

@pytest.mark.skipif(
    Version(pd.__version__) < Version('1.3'), 
    reason="Prior to pandas 1.3, timezones were saved as a data attribute. This has since changed to be part of the dtype")
def test_datetime(pandas_datetime_dataframe):
    i_rec = encode_decode(None, pandas_datetime_dataframe)
    for k in pandas_datetime_dataframe.keys():
        assert_frame_equal(pandas_datetime_dataframe[k], i_rec[k])

def test_multi(pandas_dataframe):
    i_rec = encode_decode(None, pandas_dataframe)
    for k in pandas_dataframe.keys():
        assert_frame_equal(pandas_dataframe[k], i_rec[k])

    l = tuple([pandas_dataframe['float'], pandas_dataframe['float'].A,
                pandas_dataframe['float'].B, None])
    l_rec = encode_decode(None, l)
    check_arbitrary(l, l_rec)

    # this is an oddity in that packed lists will be returned as tuples
    l = [pandas_dataframe['float'], pandas_dataframe['float']
            .A, pandas_dataframe['float'].B, None]
    l_rec = encode_decode(None, l)
    assert isinstance(l_rec, tuple)
    check_arbitrary(l, l_rec)

def test_iterator(tmp_file_msg, pandas_dataframe):

    l = [pandas_dataframe['float'], pandas_dataframe['float']
            .A, pandas_dataframe['float'].B, None]

    to_msgpack(tmp_file_msg, *l)
    for i, packed in enumerate(read_msgpack(tmp_file_msg, iterator=True)):
        check_arbitrary(packed, l[i])

def tests_datetimeindex_freq_issue():

    # GH 5947
    # inferring freq on the datetimeindex
    df = pd.DataFrame([1, 2, 3], index=pd.date_range('1/1/2013', '1/3/2013'))
    result = encode_decode(None, df)
    assert_frame_equal(result, df)

    df = pd.DataFrame([1, 2], index=pd.date_range('1/1/2013', '1/2/2013'))
    result = encode_decode(None, df)
    assert_frame_equal(result, df)

def test_dataframe_duplicate_column_names():

    # GH 9618
    expected_1 = pd.DataFrame(columns=['a', 'a'])
    expected_2 = pd.DataFrame(columns=[1] * 100)
    expected_2.loc[0] = np.random.randn(100)
    expected_3 = pd.DataFrame(columns=[1, 1])
    expected_3.loc[0] = ['abc', np.nan]

    result_1 = encode_decode(None, expected_1)
    result_2 = encode_decode(None, expected_2)
    result_3 = encode_decode(None, expected_3)

    assert_frame_equal(result_1, expected_1)
    assert_frame_equal(result_2, expected_2)
    assert_frame_equal(result_3, expected_3)