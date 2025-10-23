# compress-pptx

[![PyPI version](https://img.shields.io/pypi/v/compress-pptx.svg)](https://pypi.org/project/compress-pptx)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Compress a PPTX or POTX file, converting all PNG/TIFF images to lossy JPEGs.

**Contents:**

- [What it does](#what-it-does)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## What it does

When copy-pasting images to PowerPoint presentations, these sometimes get inserted as lossless versions, blowing up the size of the presentation.

This script takes all PNG or TIFF images part of the presentation which are larger than a given threshold (1 MiB by default), converts them to a lossy JPEG variant, and creates a new PPTX file.

:warning: This is not the same as compressing images with PowerPoint's own functionality. You may still need to do this to reduce the size of your presentation!

**By default, PNGs containing transparency are automatically skipped** to prevent graphics issues (since JPEG doesn't support transparency). If you want to force conversion of transparent images anyway, their transparent parts will be replaced with white (although you can choose another color with `-t`).

## Requirements

- Operating system: macOS or Linux
  - Note: Under Linux, you need LibreOffice installed to convert embedded EMF files
- Python 3.9 or higher
- ImageMagick (either version 6.x with `convert`/`identify` commands or version 7.x with `magick` command)
- Optionally: `ffmpeg` for media files

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

Simply run it via [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uvx compress-pptx
```

Or install via [pipx](https://pipx.pypa.io/latest/installation/).
Or manually via pip:

```bash
pip3 install --user compress-pptx
```

## Usage

Call `compress-pptx` and point it to a PPTX or POTX file. It'll compress the images and output another compressed file next to it.

For more options, see the `-h` output:

```
usage: compress-pptx [-h] [-o OUTPUT] [-s SIZE] [-q QUALITY] [-t TRANSPARENCY]
                     [--no-skip-transparent-images] [-v] [-f] [-m] [-j] [-l]
                     [--num-cpus NUM_CPUS]
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
  --no-skip-transparent-images
                        Convert transparent images to JPEG (will replace
                        transparency with background color). By default,
                        transparent images are skipped to preserve transparency.
  -v, --verbose         Show additional info (default: False)
  -f, --force           Force overwriting output file (default: False)
  -m, --compress-media  Compress other media types such as audio and video
                        (requires ffmpeg) (default: False)
  -j, --recompress-jpeg
                        Recompress jpeg images (default: False)
  -l, --use-libreoffice
                        Use LibreOffice to compress EMF files (only way to
                        compress EMF files under Linux) (default: False)
  --num-cpus NUM_CPUS   Number of CPUs to use (default: all available CPUs)
```

For example, to compress `presentation.pptx` and output to `presentation-compressed.pptx` with a quality of 75:

```bash
compress-pptx -o presentation-compressed.pptx -q 75 presentation.pptx
```

If you have `ffmpeg` installed, you can also compress audio and video files embedded in the presentation with the `-m` flag:

```bash
compress-pptx -m presentation.pptx
```

Transparent images are automatically skipped by default to preserve transparency. If you want to **force conversion of transparent images** to JPEG (replacing transparency with a background color), use the `--no-skip-transparent-images` flag:

```bash
compress-pptx --no-skip-transparent-images presentation.pptx
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/caydey"><img src="https://avatars.githubusercontent.com/u/63204672?v=4?s=100" width="100px;" alt="caydey"/><br /><sub><b>caydey</b></sub></a><br /><a href="https://github.com/slhck/compress-pptx/commits?author=caydey" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

MIT License

Copyright (c) 2021-2025 Werner Robitza

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
