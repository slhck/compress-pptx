# compress-pptx

[![PyPI version](https://img.shields.io/pypi/v/compress-pptx.svg)](https://pypi.org/project/compress-pptx)

Compress a PPTX or POTX file, converting all PNG/TIFF images to lossy JPEGs.

## What it does

When copy-pasting images to PowerPoint presentations, these sometimes get inserted as lossless versions, blowing up the size of the presentation.

This script takes all PNG or TIFF images part of the presentation which are larger than a given threshold (1 MiB by default), converts them to a lossy JPEG variant, and creates a new PPTX file.

:warning: This is not the same as compressing images with PowerPoint's own functionality. You may still need to do this to reduce the size of your presentation!

PNGs containing transparency can be skipped to prevent graphics issues. Normally their transparent parts are replaced with white (although you can choose another color).
## Requirements

- Operating system: macOS or Linux
  - Note: Under Linux, you need LibreOffice installed to convert embedded EMF files
- Python 3.7 or higher
- ImageMagick's `convert` and `identify`
- Optionally: `ffmpeg` for media files, and 

Under Ubuntu, get ImageMagick via:

```
apt install imagemagick
```

Under macOS, install it with [Homebrew](https://brew.sh):

```
brew install imagemagick
```

For ffmpeg, use the static builds from [ffmpeg.org](https://ffmpeg.org/downloads.html).

## Installation

Via pip:

```
pip3 install --user compress-pptx
```

## Usage

Call `compress-pptx` and point it to a PPTX or POTX file. It'll compress the images and output another compressed file next to it.

For more options, see the `-h` output:

```
usage: compress-pptx [-h] [-o OUTPUT] [-s SIZE] [-q QUALITY] [-t TRANSPARENCY]
                     [-k] [-v] [-f] [-m] [-j] [-l]
                     input

positional arguments:
  input

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default: None)
  -s SIZE, --size SIZE  Minimum size threshold in bytes. Also accepts the
                        suffixes k/M/G or KiB/MiB/GiB (default: 1MiB)
  -q QUALITY, --quality QUALITY
                        JPEG output quality (0-100) (default: 85)
  -t TRANSPARENCY, --transparency TRANSPARENCY
                        Replace transparency with color (default: white)
  -k, --skip-transparent-images
                        Skip converting transparent images at all (default:
                        False)
  -v, --verbose         Show additional info (default: False)
  -f, --force           Force overwriting output file (default: False)
  -m, --compress-media  Compress other media types such as audio and video
                        (requires ffmpeg) (default: False)
  -j, --recompress-jpeg
                        Recompress jpeg images (default: False)
  -l, --use-libreoffice
                        Use LibreOffice to compress EMF files (only way to
                        compress EMF files under Linux) (default: False)
```

## Bash Version

There's an unmaintained Bash version under `bash/compress-pptx.sh`.

## License

MIT License

Copyright (c) 2021-2023 Werner Robitza

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
