# LZF Python

Python bindings for the LZF compression library. This package provides Python wrappers for the LZF compression and decompression functions.

## Requirements

- Python 3.6+
- SWIG
- C++ compiler (with C++11 support)

## Installation

```bash
pip install lzf-python
```

Or install from source:

```bash
git clone https://github.com/author/lzf-python.git
cd lzf-python
pip install .
```

## Usage

```python
import lzf
import io

# Compress data
with open('input_file', 'rb') as input_file, open('compressed_file', 'wb') as output_file:
    lzf.lzf_compress(output_file, input_file)

# Decompress data
with open('compressed_file', 'rb') as input_file, open('decompressed_file', 'wb') as output_file:
    lzf.lzf_decompress(output_file, input_file)
```

## License

MIT 