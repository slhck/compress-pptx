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
  - [Extracting media](#extracting-media)
  - [FFmpeg encoding options](#ffmpeg-encoding-options)
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
                     [--num-cpus NUM_CPUS] [--extract EXTRACT]
                     [--ffmpeg-crf FFMPEG_CRF]
                     [--ffmpeg-video-codec FFMPEG_VIDEO_CODEC]
                     [--ffmpeg-audio-codec FFMPEG_AUDIO_CODEC]
                     [--ffmpeg-extra-options FFMPEG_EXTRA_OPTIONS]
                     [--ffmpeg-path FFMPEG_PATH]
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
  --extract EXTRACT     Extract all media from the presentation to the
                        specified directory (default: None)
  --ffmpeg-crf FFMPEG_CRF
                        FFmpeg CRF value for video encoding (e.g., 23 for
                        libx264) (default: None)
  --ffmpeg-video-codec FFMPEG_VIDEO_CODEC
                        FFmpeg video codec (e.g., libx264 for best PowerPoint
                        compatibility) (default: None)
  --ffmpeg-audio-codec FFMPEG_AUDIO_CODEC
                        FFmpeg audio codec (e.g., aac, libopus, libmp3lame)
                        (default: None)
  --ffmpeg-extra-options FFMPEG_EXTRA_OPTIONS
                        Extra FFmpeg options as a single string (e.g.,
                        '-preset slow -tune stillimage') (default: None)
  --ffmpeg-path FFMPEG_PATH
                        Path to ffmpeg executable (default: ffmpeg)
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

### Extracting media

To extract all media files from a presentation, use the `--extract` option with a directory path:

```bash
compress-pptx --extract ./media presentation.pptx
```

This will create the `media` directory (if it doesn't exist) and extract all images, audio, and video files from the presentation into it.

### FFmpeg encoding options

When using `-m` to compress media files, you can customize the FFmpeg encoding settings:

```bash
compress-pptx -m --ffmpeg-video-codec libx265 --ffmpeg-crf 34 presentation.pptx
```

Note that the default is `libx264` and CRF 23.

You can pass additional FFmpeg options using `--ffmpeg-extra-options`:

```bash
compress-pptx -m --ffmpeg-video-codec libx264 --ffmpeg-extra-options '-preset slow -tune stillimage' presentation.pptx
```

To see available options for a specific encoder, run:

```bash
ffmpeg -h encoder=libx264
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
