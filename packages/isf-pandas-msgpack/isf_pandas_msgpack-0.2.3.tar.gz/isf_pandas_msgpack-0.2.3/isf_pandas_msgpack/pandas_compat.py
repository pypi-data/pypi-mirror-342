import pandas as pd
from packaging.version import Version
import sys

PANDAS_ST_200 = Version(pd.__version__).release < (2, 0, 0)
PANDAS_ST_210 = Version(pd.__version__).release < (2, 1, 0)
PANDAS_ST_120 = Version(pd.__version__).release < (1, 2, 0)
PANDAS_GE_210 = Version(pd.__version__).release >= (2, 1, 0)
PANDAS_GE_300 =  Version(pd.__version__).major >= 3
PY3 = (sys.version_info[0] >= 3)
STRING_TYPES = (str,)


if PANDAS_ST_120:
    from pandas.core.internals import _safe_reshape
    from pandas.io.common import get_filepath_or_buffer as _get_filepath_or_buffer
    def get_filepath_or_buffer(*args, **kwargs):
        fpb, encoding, compression, _ = _get_filepath_or_buffer(*args, **kwargs)
        return fpb, encoding, compression
else:
    from pandas.io.common import _get_filepath_or_buffer
    def get_filepath_or_buffer(*args, **kwargs):
        io_args = _get_filepath_or_buffer(*args, **kwargs)
        fpb, encoding, compression = io_args.filepath_or_buffer, io_args.encoding, io_args.compression
        return fpb, encoding, compression
    def _safe_reshape(arr, new_shape):
        """
        If possible, reshape `arr` to have shape `new_shape`,
        with a couple of exceptions (see gh-13012):

        1) If `arr` is a ExtensionArray or Index, `arr` will be
        returned as is.
        2) If `arr` is a Series, the `_values` attribute will
        be reshaped and returned.

        Parameters
        ----------
        arr : array-like, object to be reshaped
        new_shape : int or tuple of ints, the new shape
        """
        if isinstance(arr, ABCSeries):
            arr = arr._values
        if not is_extension_array_dtype(arr.dtype):
            # Note: this will include TimedeltaArray and tz-naive DatetimeArray
            # TODO(EA2D): special case will be unnecessary with 2D EAs
            arr = np.asarray(arr).reshape(new_shape)
        return arr

if PANDAS_ST_210:
    from pandas.core.arrays.sparse import SparseDtype
else:
    from pandas import SparseDtype

    
if PY3:
    def u(s):
        return s

    def u_safe(s):
        return s
else:
    def u(s):
        return unicode(s, "unicode_escape")

    def u_safe(s):
        try:
            return unicode(s, "unicode_escape")
        except:
            return s