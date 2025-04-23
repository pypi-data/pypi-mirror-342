"""See https://github.com/pandas-dev/pandas/pull/9783
"""
from . import encode_decode
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.errors import PerformanceWarning
import pytest
import numpy as np
from unittest.mock import patch
from numpy.testing import assert_array_equal as assert_numpy_array_equal

try:
    from sqlalchemy import create_engine
    _create_sql_engine = create_engine
except ImportError:
    _SQLALCHEMY_INSTALLED = False
else:
    _SQLALCHEMY_INSTALLED = True
try:
    import blosc  # NOQA
except ImportError:
    _BLOSC_INSTALLED = False
else:
    _BLOSC_INSTALLED = True

try:
    import zlib  # NOQA
except ImportError:
    _ZLIB_INSTALLED = False
else:
    _ZLIB_INSTALLED = True


def test_plain(pandas_dataframe):
    i_rec = encode_decode(None, pandas_dataframe)
    for k in pandas_dataframe.keys():
        assert_frame_equal(pandas_dataframe[k], i_rec[k])

def _test_compression(pandas_dataframe, compress):
    i_rec = encode_decode(None, pandas_dataframe, compress=compress)
    for k in pandas_dataframe.keys():
        value = i_rec[k]
        expected = pandas_dataframe[k]
        assert_frame_equal(value, expected)
        # make sure that we can write to the new frames
        for block in value._mgr.blocks:
            if isinstance(block.values, np.ndarray):
                assert block.values.flags.writeable
            else:
                # e.g. DatetimeArray
                # Access underlying _data array
                if hasattr(block.values, '_data'):
                    assert block.values._data.flags.writeable
                else:
                    # DatetimeArrays are still experimental with changing API - just pass... - Bjorge 2025-03-24
                    pass

@pytest.mark.skipif(not _ZLIB_INSTALLED, reason="zlib not installed")
def test_compression_zlib(pandas_dataframe):
    _test_compression(pandas_dataframe, 'zlib')

@pytest.mark.skipif(not _BLOSC_INSTALLED, reason="blosc not installed")
def test_compression_blosc(pandas_dataframe):
    _test_compression(pandas_dataframe, 'blosc')

def _test_compression_warns_when_decompress_caches(pandas_dataframe, compress):
    not_garbage = []
    control = []  # copied data

    compress_module = globals()[compress]
    real_decompress = compress_module.decompress

    def decompress(ob):
        """mock decompress function that delegates to the real
        decompress but caches the result and a copy of the result.
        """
        res = real_decompress(ob)
        not_garbage.append(res)  # hold a reference to this bytes object
        control.append(bytearray(res))  # copy the data here to check later
        return res

    # types mapped to values to add in place.
    rhs = {
        np.dtype('float64'): 1.0,
        np.dtype('int32'): 1,
        np.dtype('object'): 'a',
        np.dtype('datetime64[ns]'): np.timedelta64(1, 'ns'),
        np.dtype('timedelta64[ns]'): np.timedelta64(1, 'ns'),
    }

    with patch(f"{compress}.decompress", decompress), pytest.raises(PerformanceWarning) as excinfo:

        i_rec = encode_decode(
            None,
            pandas_dataframe, 
            compress=compress
            )
        for k in pandas_dataframe.keys():
            value = i_rec[k]
            expected = pandas_dataframe[k]
            assert_frame_equal(value, expected)
            # make sure that we can write to the new frames even though
            # we needed to copy the data
            for block in value._mgr.blocks:
                if isinstance(block.values, np.ndarray):
                    assert block.values.flags.writeable
                    # mutate the data in some way
                    block.values[0] += rhs[block.dtype]
                else:
                    # e.g. DatetimeArray
                    # Access underlying _data array
                    assert block.values._data.flags.writeable
                    block.values._data[0] += rhs[block.dtype]

    assert excinfo.match('copying data after decompressing; this may mean that decompress is caching its result')
    for buf, control_buf in zip(not_garbage, control):
        # make sure none of our mutations above affected the
        # original buffers
        assert buf == control_buf

@pytest.mark.skipif(not _ZLIB_INSTALLED, reason="zlib not installed")
def test_compression_warns_when_decompress_caches_zlib(pandas_dataframe):
    _test_compression_warns_when_decompress_caches(pandas_dataframe, 'zlib')

@pytest.mark.skipif(not _BLOSC_INSTALLED, reason="blosc not installed")
def test_compression_warns_when_decompress_caches_blosc(pandas_dataframe):
    _test_compression_warns_when_decompress_caches(pandas_dataframe, 'blosc')

def _test_small_strings_no_warn(compress):
    empty = np.array([], dtype='uint8')
    empty_unpacked = encode_decode(None, empty, compress=compress)

    assert_numpy_array_equal(empty_unpacked, empty)
    # Ensure that the unpacked array is writable
    assert empty_unpacked.flags.writeable

    char = np.array([ord(b'a')], dtype='uint8')
    char_unpacked = encode_decode(None, char, compress=compress)

    assert_numpy_array_equal(char_unpacked, char)
    assert char_unpacked.flags.writeable
    # if this test fails I am sorry because the interpreter is now in a
    # bad state where b'a' points to 98 == ord(b'b').
    char_unpacked[0] = ord(b'b')

    # we compare the ord of bytes b'a' with unicode u'a' because the should
    # always be the same (unless we were able to mutate the shared
    # character singleton in which case ord(b'a') == ord(b'b').
    assert ord(b'a') == ord(u'a')
    assert_numpy_array_equal(
        char_unpacked,
        np.array([ord(b'b')], dtype='uint8'),
    )

@pytest.mark.skipif(not _ZLIB_INSTALLED,reason="zlib not installed")
def test_small_strings_no_warn_zlib():
    _test_small_strings_no_warn('zlib')

@pytest.mark.skipif(not _BLOSC_INSTALLED, reason="blosc not installed")
def test_small_strings_no_warn_blosc():
    _test_small_strings_no_warn('blosc')

@pytest.mark.skipif(not _BLOSC_INSTALLED, reason="blosc not installed")
def test_readonly_axis_blosc():
    # GH11880
    df1 = pd.DataFrame({'A': list('abcd')})
    df2 = pd.DataFrame(df1, index=[1., 2., 3., 4.])
    assert 1 in encode_decode(None, df1['A'], compress='blosc')
    assert 1. in encode_decode(None, df2['A'], compress='blosc')

def test_readonly_axis_zlib():
    # GH11880
    df1 = pd.DataFrame({'A': list('abcd')})
    df2 = pd.DataFrame(df1, index=[1., 2., 3., 4.])
    assert 1 in encode_decode(None, df1['A'], compress='zlib')
    assert 1. in encode_decode(None, df2['A'], compress='zlib')

@pytest.mark.skipif(not _SQLALCHEMY_INSTALLED, reason="sqlalchemy not installed")
@pytest.mark.skipif(not _BLOSC_INSTALLED, reason="blosc not installed")
def test_readonly_axis_blosc_to_sql():
    # GH11880
    expected = pd.DataFrame({'A': list('abcd')})
    df = encode_decode(None, expected, compress='blosc')
    eng = _create_sql_engine("sqlite:///:memory:")
    df.to_sql('test', eng, if_exists='append')
    result = pd.read_sql_table('test', eng, index_col='index')
    result.index.names = [None]
    assert_frame_equal(expected, result)


@pytest.mark.skipif(not _SQLALCHEMY_INSTALLED, reason="sqlalchemy not installed")
@pytest.mark.skipif(not _ZLIB_INSTALLED, reason="zlib not installed")
def test_readonly_axis_zlib_to_sql():
    # GH11880
    expected = pd.DataFrame({'A': list('abcd')})
    df = encode_decode(None, expected, compress='zlib')
    eng = _create_sql_engine("sqlite:///:memory:")
    df.to_sql('test', eng, if_exists='append')
    result = pd.read_sql_table('test', eng, index_col='index')
    result.index.names = [None]
    assert_frame_equal(expected, result)