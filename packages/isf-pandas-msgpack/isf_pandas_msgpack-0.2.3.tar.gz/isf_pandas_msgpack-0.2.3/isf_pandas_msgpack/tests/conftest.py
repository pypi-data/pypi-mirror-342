import pandas as pd
import numpy as np
import pytest, random, string, os, datetime

from . import (
    make_string_index,
    make_integer_index,
    make_float_index,
    make_datetime_index,
    make_categorical_index,
    make_range_index,
)
    

@pytest.fixture
def pandas_data():
    d = {
        'string': make_string_index(100),
        'date': make_datetime_index(100),
        'int': make_integer_index(100),
        'rng': make_range_index(100),
        'float': make_float_index(100),
        'empty': pd.Index([]),
        'tuple': pd.Index(zip(['foo', 'bar', 'baz'], [1, 2, 3])),
        'period': pd.Index(pd.period_range('2012-1-1', freq='M', periods=3)),
        'date2': pd.Index(pd.date_range('2013-01-1', periods=10)),
        'bdate': pd.Index(pd.bdate_range('2013-01-02', periods=10)),
        'cat': make_categorical_index(100)
    }

    return d

@pytest.fixture
def pandas_multi_index():
    mi = {
        'reg': pd.MultiIndex.from_tuples(
            [('bar', 'one'), ('baz', 'two'),
            ('foo', 'two'),
            ('qux', 'one'), ('qux', 'two')],
            names=['first', 'second']),
        }
    return mi


@pytest.fixture
def pandas_categorical_data():
    d = {}
    d['plain_str'] = pd.Categorical(['a', 'b', 'c', 'd', 'e'])
    d['plain_str_ordered'] = pd.Categorical(['a', 'b', 'c', 'd', 'e'], ordered=True)
    d['plain_int'] = pd.Categorical([5, 6, 7, 8])
    d['plain_int_ordered'] = pd.Categorical([5, 6, 7, 8], ordered=True)
    return d


@pytest.fixture
def pandas_dataframe():

    # data = {
    #     'A': [0., 1., 2., 3., np.nan],
    #     'B': [0, 1, 0, 1, 0],
    #     'C': ['foo1', 'foo2', 'foo3', 'foo4', 'foo5'],
    #     'D': pd.date_range('1/1/2009', periods=5),
    #     'E': [0., 1, pd.Timestamp('20100101'), 'foo', 2.],
    #     'H': pd.Categorical(['a', 'b', 'c', 'd', 'e']),
    #     'I': pd.Categorical(['a', 'b', 'c', 'd', 'e'], ordered=True),
    # }
    data = {
        'A': [u'\u2019'] * 1000,
        'B': np.arange(1000, dtype=np.int32),
        'C': list(100 * 'abcdefghij'),
        'D': pd.date_range(datetime.datetime(2015, 4, 1), periods=1000),
        'E': [datetime.timedelta(days=x) for x in range(1000)],
        'G': [400] * 1000
    }
    frame = {
        'float': pd.DataFrame(dict(A=data['A'], B=pd.Series(data['A']))),
        'int': pd.DataFrame(dict(A=data['B'], B=pd.Series(data['B']))),
        'mixed': pd.DataFrame(data)}
    return frame

@pytest.fixture
def pandas_datetime_dataframe():
    datetime_frame = {
        "datetime": pd.DataFrame({
        'F': [pd.Timestamp('20130102', tz='US/Eastern')] * 5,
        'G': [pd.Timestamp('20130603', tz='CET')] * 5,
    })}
    return datetime_frame

def random_string(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def tmp_file_msg(tmp_path):
    """
    Create a temporary file with the `.msg` extension.
    """
    f = '__%s__.msg' % random_string(10)
    return os.path.join(tmp_path, f)