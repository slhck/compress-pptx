import argparse
import os
import sys
from .compress_pptx import CompressPptx, CompressPptxError
from .util import convert_size_to_bytes


def main():
    parser = argparse.ArgumentParser()
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
        "-v", "--verbose", action="store_true", help="Show additional info"
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
            verbose=cli_args.verbose,
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
