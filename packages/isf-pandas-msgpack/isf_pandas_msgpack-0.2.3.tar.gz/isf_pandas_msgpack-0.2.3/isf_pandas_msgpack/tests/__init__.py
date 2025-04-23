import pandas as pd
from isf_pandas_msgpack import to_msgpack, read_msgpack
from pandas._testing import (
    assert_frame_equal,
    assert_series_equal,
    assert_index_equal,
)

def encode_decode(path, x, compress=None, **kwargs):
    if path is None:
        # returns the msgpack string
        s = to_msgpack(None, x, compress=compress, **kwargs)
        return read_msgpack(s, **kwargs)
    else:
        to_msgpack(path, x, compress=compress, **kwargs)
        return read_msgpack(path, **kwargs)


def check_arbitrary(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        assert(len(a) == len(b))
        for a_, b_ in zip(a, b):
            check_arbitrary(a_, b_)
    elif isinstance(a, pd.DataFrame):
        assert_frame_equal(a, b)
    elif isinstance(a, pd.Series):
        assert_series_equal(a, b)
    elif isinstance(a, pd.Index):
        assert_index_equal(a, b)
    elif a is pd.NaT:
        assert b is pd.NaT
    elif isinstance(a, pd.Timestamp):
        assert a == b
        assert a.freq == b.freq
    else:
        assert(a == b)


def make_string_index(length):
    """
    Create a string index of the given length.
    """
    return pd.Index([str(i) for i in range(length)])


def make_integer_index(length):
    """
    Create an integer index of the given length.
    """
    return pd.Index(range(length))


def make_float_index(length):
    """
    Create a float index of the given length.
    """
    return pd.Index([float(i) for i in range(length)])


def make_datetime_index(length):
    """
    Create a datetime index of the given length.
    """ 
    return pd.date_range(start='2020-01-01', periods=length, freq='D')

def make_timedelta_index(length):
    """
    Create a timedelta index of the given length.
    """
    return pd.to_timedelta(pd.date_range(start='2020-01-01',
                                          periods=length, freq='D') - pd.Timestamp('2020-01-01'))
    
    
def make_boolean_index(length):
    """
    Create a boolean index of the given length.
    """
    return pd.Index([True if i % 2 == 0 else False for i in range(length)])


def make_categorical_index(length):
    """
    Create a categorical index of the given length.
    """
    return pd.CategoricalIndex([str(i) for i in range(length)])


def make_range_index(length):
    """
    Create a range index of the given length.
    """
    return pd.RangeIndex(start=0, stop=length, step=1)

    

def make_interval_index(length):
    """
    Create an interval index of the given length.
    """
    return pd.IntervalIndex.from_breaks(range(0, length * 2, 2))


def make_period_index(length):
    """
    Create a period index of the given length.
    """
    return pd.PeriodIndex(pd.date_range(start='2020-01-01',
                                         periods=length, freq='D').to_period('D'))

def make_string_series(length=10):
    """
    Create a string series of the given length.
    """
    return pd.Series([str(i) for i in range(length)], index=make_string_index(length))