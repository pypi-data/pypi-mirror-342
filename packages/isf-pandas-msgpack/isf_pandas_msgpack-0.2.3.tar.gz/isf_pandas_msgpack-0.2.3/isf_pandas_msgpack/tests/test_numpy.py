import numpy as np
import pytest
from . import encode_decode

def test_numpy_scalar_float(tmp_file_msg):
    x = np.float32(np.random.rand())
    x_rec = encode_decode(tmp_file_msg, x)
    assert x == pytest.approx(x_rec)

def test_numpy_scalar_complex(tmp_file_msg):
    x = np.complex64(np.random.rand() + 1j * np.random.rand())
    x_rec = encode_decode(tmp_file_msg, x)
    assert np.allclose(x, x_rec)

def test_scalar_float(tmp_file_msg):
    x = np.random.rand()
    x_rec = encode_decode(tmp_file_msg, x)
    assert x == pytest.approx(x_rec)

def test_scalar_complex(tmp_file_msg):
    x = np.random.rand() + 1j * np.random.rand()
    x_rec = encode_decode(tmp_file_msg, x)
    assert np.allclose(x, x_rec)

def test_list_numpy_float(tmp_file_msg):
    x = [np.float32(np.random.rand()) for i in range(5)]
    x_rec = encode_decode(tmp_file_msg, x)
    # current msgpack cannot distinguish list/tuple
    assert tuple(x) == pytest.approx(x_rec)

    x_rec = encode_decode(tmp_file_msg, tuple(x))
    assert tuple(x) == pytest.approx(x_rec)

def test_list_numpy_float_complex(tmp_file_msg):
    if not hasattr(np, 'complex128'):
        pytest.skip('numpy cant handle complex128')

    x = [np.float32(np.random.rand()) for i in range(5)] + \
        [np.complex128(np.random.rand() + 1j * np.random.rand())
            for i in range(5)]
    x_rec = encode_decode(tmp_file_msg, x)
    assert np.allclose(x, x_rec)

def test_list_float(tmp_file_msg):
    x = [np.random.rand() for i in range(5)]
    x_rec = encode_decode(tmp_file_msg, x)
    # current msgpack cannot distinguish list/tuple
    assert tuple(x) == pytest.approx(x_rec)

    x_rec = encode_decode(tmp_file_msg, tuple(x))
    assert tuple(x) == pytest.approx(x_rec)

def test_list_float_complex(tmp_file_msg):
    x = [np.random.rand() for i in range(5)] + \
        [(np.random.rand() + 1j * np.random.rand()) for i in range(5)]
    x_rec = encode_decode(tmp_file_msg, x)
    assert np.allclose(x, x_rec)

def test_dict_float(tmp_file_msg):
    x = {'foo': 1.0, 'bar': 2.0}
    x_rec = encode_decode(tmp_file_msg, x)
    assert x == pytest.approx(x_rec)

def test_dict_complex(tmp_file_msg):
    x = {'foo': 1.0 + 1.0j, 'bar': 2.0 + 2.0j}
    x_rec = encode_decode(tmp_file_msg, x)
    assert x == x_rec
    for key in x:
        assert type(x[key]) == type(x_rec[key])

def test_dict_numpy_float(tmp_file_msg):
    x = {'foo': np.float32(1.0), 'bar': np.float32(2.0)}
    x_rec = encode_decode(tmp_file_msg, x)
    assert x == pytest.approx(x_rec)

def test_dict_numpy_complex(tmp_file_msg):
    x = {'foo': np.complex128(1.0 + 1.0j),
            'bar': np.complex128(2.0 + 2.0j)}
    x_rec = encode_decode(tmp_file_msg, x)
    assert x == x_rec
    for key in x:
        assert type(x[key]) == type(x_rec[key])

def test_numpy_array_float(tmp_file_msg):
    # run multiple times
    for _ in range(10):
        x = np.random.rand(10)
        for dtype in ['float32', 'float64']:
            x = x.astype(dtype)
            x_rec = encode_decode(tmp_file_msg, x)
            assert x == pytest.approx(x_rec)

def test_numpy_array_complex(tmp_file_msg):
    x = (np.random.rand(5) + 1j * np.random.rand(5)).astype(np.complex128)
    x_rec = encode_decode(tmp_file_msg, x)
    assert all(map(lambda x, y: x == y, x, x_rec)) and x.dtype == x_rec.dtype

def test_list_mixed(tmp_file_msg):
    x = [1.0, np.float32(3.5), np.complex128(4.25), u'foo']
    x_rec = encode_decode(tmp_file_msg, x)
    # current msgpack cannot distinguish list/tuple
    assert tuple(x) == pytest.approx(x_rec)

    x_rec = encode_decode(tmp_file_msg, tuple(x))
    assert tuple(x) == pytest.approx(x_rec)