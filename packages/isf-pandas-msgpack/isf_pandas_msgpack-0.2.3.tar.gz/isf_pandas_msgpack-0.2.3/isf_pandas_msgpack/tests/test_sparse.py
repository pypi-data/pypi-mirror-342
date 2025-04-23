from . import encode_decode, make_string_series
import pandas as pd
import numpy as np
from pandas.testing import (
    # assert_frame_equal,
    assert_series_equal,
)
import pytest

def _check_roundtrip(self, obj, comparator, **kwargs):

    # currently these are not implemetned
    i_rec = encode_decode(obj)
    # comparator(obj, i_rec, **kwargs)
    raise ValueError("{}\n{}".format(obj, pd.Series(i_rec)))
    with pytest.raises(NotImplementedError):
        encode_decode(obj)

@pytest.mark.skip(reason="Sparse Series are not implemented (yet): see packers.unconvert for reconsturcting sparse series.")
def test_sparse_series(self):

    s = make_string_series()
    s[3:5] = np.nan
    ss = s.astype("Sparse")
    self._check_roundtrip(ss, assert_series_equal, check_series_type=True)

    ss2 = s.astype('Sparse[int]')
    self._check_roundtrip(ss2, assert_series_equal, check_series_type=True)


# @pytest.mark.skip(reason="Sparse DataFrames are deprecated. Dataframes can however contain sparse Series.")
# def test_sparse_frame(self):

#     s = tm.makeDataFrame()
#     s.loc[3:5, 1:3] = np.nan
#     s.loc[8:10, -2] = np.nan
#     ss = s.astype("Sparse")

#     self._check_roundtrip(ss, tm.assert_frame_equal,
#                             check_frame_type=True)

#     ss2 = s.astype('Sparse[int]')
#     self._check_roundtrip(ss2, tm.assert_frame_equal,
#                             check_frame_type=True)

    # ss3 = s.to_sparse(fill_value=0)
    # self._check_roundtrip(ss3, tm.assert_frame_equal,
    #                       check_frame_type=True)