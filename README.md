# compress-pptx

[![PyPI version](https://img.shields.io/pypi/v/compress-pptx.svg)](https://img.shields.io/pypi/v/compress-pptx)

Compress a PPTX file, converting all PNG/TIFF images to lossy JPEGs.

## What it does

When copy-pasting images to PowerPoint presentations, these sometimes get inserted as lossless versions, blowing up the size of the presentation.

This script takes all PNG or TIFF images part of the presentation which are larger than a given threshold (1 MiB by default), converts them to a lossy JPEG variant, and creates a new PPTX file.

PNGs containing transparency will be skipped to prevent graphics issues.
## Requirements

- Python 3.5 or higher
- ImageMagick's `magick`, which calls `convert` and `identify`

Under Ubuntu, get ImageMagick via:

```
apt install imagemagick
```

## Installation

Via pip:

```
pip3 install --user compress-pptx
```

## Usage

Call `compress_pptx` and point it to a PPTX file. It'll compress the images and output another compressed file next to it.

For more options, see the `-h` output:

```
compress_pptx [-h] [-o OUTPUT] [-s SIZE] [-q QUALITY] [-v] input

positional arguments:
  input

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file
  -s SIZE, --size SIZE  Minimum size threshold in bytes. Also accepts the suffixes k/M/G or KiB/MiB/GiB
  -q QUALITY, --quality QUALITY
                        JPEG output quality (0-100)
  -v, --verbose         Show additional info
```

## Bash Version

There's an unmaintained Bash version under `bash/compress-pptx.sh`.

## License

MIT License

Copyright (c) 2021 Werner Robitza

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
