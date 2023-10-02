import argparse
import os
import sys

from .compress_pptx import CompressPptx, CompressPptxError
from .util import convert_size_to_bytes


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="compress-pptx"
    )
    parser.add_argument("input")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument(
        "-s",
        "--size",
        help="Minimum size threshold in bytes. Also accepts the suffixes k/M/G or KiB/MiB/GiB",
        type=str,
        default=CompressPptx.DEFAULT_SIZE,
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        help="JPEG output quality (0-100)",
        default=CompressPptx.DEFAULT_QUALITY,
    )
    parser.add_argument(
        "-t",
        "--transparency",
        type=str,
        help="Replace transparency with color",
        default=CompressPptx.DEFAULT_TRANSPARENCY,
    )
    parser.add_argument(
        "-k",
        "--skip-transparent-images",
        action="store_true",
        help="Skip converting transparent images at all",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show additional info"
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Force overwriting output file"
    )
    parser.add_argument(
        "-m",
        "--compress-media",
        action="store_true",
        help="Compress other media types such as audio and video (requires ffmpeg)",
    )
    parser.add_argument(
        "-j", "--recompress-jpeg", action="store_true", help="Recompress jpeg images"
    )
    parser.add_argument(
        "-l",
        "--use-libreoffice",
        action="store_true",
        help="Use LibreOffice to compress EMF files (only way to compress EMF files under Linux)",
    )
    cli_args = parser.parse_args()

    basename, _ = os.path.splitext(cli_args.input)
    output = (
        cli_args.output
        if cli_args.output is not None
        else basename + "-compressed.pptx"
    )

    size_bytes = convert_size_to_bytes(cli_args.size)

    try:
        CompressPptx(
            input_file=cli_args.input,
            output_file=output,
            size=size_bytes,
            quality=cli_args.quality,
            transparency=cli_args.transparency,
            skip_transparent_images=cli_args.skip_transparent_images,
            verbose=cli_args.verbose,
            force=cli_args.force,
            compress_media=cli_args.compress_media,
            recompress_jpeg=cli_args.recompress_jpeg,
            use_libreoffice=cli_args.use_libreoffice,
            num_cpus=os.cpu_count(),
        ).run()
    except CompressPptxError as e:
        print(f"Error: {e}")
    except Exception as e:
        raise e


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
