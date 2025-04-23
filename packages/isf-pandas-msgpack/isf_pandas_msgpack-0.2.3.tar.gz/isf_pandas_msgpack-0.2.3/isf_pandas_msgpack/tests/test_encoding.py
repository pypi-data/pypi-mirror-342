from pandas.testing import assert_frame_equal
from . import encode_decode, to_msgpack

UTF_ENCODINGS = ['utf8', 'utf16', 'utf32']

def test_utf(pandas_dataframe):
    # GH10581
    for encoding in UTF_ENCODINGS:
        for frame in pandas_dataframe.values():
            result = encode_decode(None, frame, encoding=encoding)
            assert_frame_equal(result, frame)

def test_default_encoding(pandas_dataframe):
    for frame in pandas_dataframe.values():
        result = to_msgpack(frame)
        expected = to_msgpack(frame, encoding='utf8')
        assert result == expected
        result = encode_decode(None, frame)
        assert_frame_equal(result, frame)