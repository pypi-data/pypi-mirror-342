import datetime, pytest, sys
import numpy as np
import pandas as pd
from . import encode_decode

def test_timestamp():
    for i in [pd.Timestamp(
        '20130101'), pd.Timestamp('20130101', tz='US/Eastern'),
            pd.Timestamp('201301010501')]:
        i_rec = encode_decode(None, i)
        assert i == i_rec

def test_nat():
    nat_rec = encode_decode(None, pd.NaT)
    assert pd.isnull(nat_rec)

@pytest.mark.skipif(
    sys.version_info < (2, 7),
    reason='datetime64 broken in 2.6')
def test_datetimes():
    for i in [datetime.datetime(2013, 1, 1),
                datetime.datetime(2013, 1, 1, 5, 1),
                datetime.date(2013, 1, 1),
                np.datetime64(datetime.datetime(2013, 1, 5, 2, 15))]:
        i_rec = encode_decode(None, i)
        assert i == i_rec

def test_timedeltas():
    for i in [datetime.timedelta(days=1),
                datetime.timedelta(days=1, seconds=10),
                np.timedelta64(1000000)]:
        i_rec = encode_decode(None, i)
        assert i == i_rec 