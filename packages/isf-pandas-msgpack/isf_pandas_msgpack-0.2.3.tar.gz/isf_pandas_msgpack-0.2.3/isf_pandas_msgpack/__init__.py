# flake8: noqa

# pandas versioning
import pandas

# from packaging.version import Version
# pv = Version(pandas.__version__)

# if pv < '0.19.0':
#     raise ValueError("pandas_msgpack requires at least pandas 0.19.0")
# _is_pandas_legacy_version = pv.version[1] == 19 and len(pv.version) == 3

from .packers import to_msgpack, read_msgpack
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("isf-pandas-msgpack")
except PackageNotFoundError:
    # package is not installed
    pass
# del get_versions, versions, pv, Version, pandas
del pandas
