*  Install in dev mode (you will need Cython compiler)

        rm pandas_msgpack/msgpack/_packer.cpp
        rm pandas_msgpack/msgpack/_unpacker.cpp
        source ~/conda-py3/bin/activate
        python setup.py develop build_ext --inplace --force install

*  Testing

        pytest pandas_msgpack
        pytest -rsx -vv --color=yes pandas_msgpack/tests
