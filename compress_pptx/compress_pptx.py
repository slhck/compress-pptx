import os
from pathlib import Path
import tempfile
import glob
import zipfile
from tqdm.contrib.concurrent import process_map

from .util import (
    run_command,
    file_size,
    human_readable_size,
    convert_size_to_bytes,
    which,
)


def _compress_image(args):
    cmd = [
        "magick",
        "convert",
        "-quality",
        str(args["quality"]),
        args["input"],
        args["output"],
    ]
    run_command(cmd)


def _has_transparency(input_file):
    cmd = ["magick", "identify", "-format", "%[opaque]", input_file]
    stdout, _ = run_command(cmd)
    if stdout.strip() == "False":
        return True


class CompressPptxError(SystemError):
    pass


class CompressPptx:
    DEFAULT_QUALITY = 85
    DEFAULT_SIZE = "1MiB"

    def __init__(
        self,
        input_file: str,
        output_file: str,
        size=convert_size_to_bytes(DEFAULT_SIZE),
        quality=DEFAULT_QUALITY,
        verbose=False,
    ) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.size = int(size)
        self.quality = int(quality)
        self.verbose = bool(verbose)
        self.image_list = []

        if which("magick") is None:
            raise CompressPptxError(
                "ImageMagick not found in PATH. Make sure you have installed ImageMagick and that the 'magick' command is available."
            )

        if self.quality < 0 or self.quality > 100:
            raise CompressPptxError("Quality must be between 0-100!")

        if not Path(self.input_file).exists():
            raise CompressPptxError(f"No such file: {self.input_file}")

        if not Path(self.input_file).suffix.endswith("pptx"):
            raise CompressPptxError("Input must be a PPTX file!")

        self.temp_dir = None

    def run(self) -> None:
        if self.verbose:
            print(f"Converting {self.input_file} to {self.output_file}")

        with tempfile.TemporaryDirectory() as temp_dir:
            self.temp_dir = temp_dir

            # Unzip
            self._unzip()

            # Collect compressible files
            self._find_images()

            # Compress
            self._compress_images()

            # Replace rels
            self._replace_rels()

            # Zip back
            self._zip()

        if self.verbose:
            self._print_stats()

    def _unzip(self) -> None:
        print("Extracting file ...")
        with zipfile.ZipFile(self.input_file, "r") as zip_f:
            zip_f.extractall(self.temp_dir)
            if self.verbose:
                print(f"Extracted temp files to {self.temp_dir}")

    def _find_images(self) -> None:
        if self.temp_dir is None:
            raise RuntimeError("Temp dir not created!")

        for file in glob.iglob(
            os.path.join(self.temp_dir, "ppt", "media", "*"), recursive=True
        ):
            # skip unaffected extensions
            if not (file.endswith(".png") or file.endswith(".tiff")):
                continue

            # skip files that are too small
            fsize = file_size(file)
            if fsize < self.size:
                # print(f"Skipping {Path(file).name} because it is too small")
                continue

            # skip files with transparency
            if _has_transparency(file):
                # print(f"Skipping {Path(file).name} because it contains transparency")
                continue

            if self.verbose:
                print(
                    f"{Path(file).name} added to conversion queue ({human_readable_size(fsize)})"
                )

            self.image_list.append(
                {
                    "input": file,
                    "output": Path(file).parent / (Path(file).stem + "-compressed.jpg"),
                    "input_size": fsize,
                    "output_size": None,
                    "quality": self.quality,
                }
            )

    def _compress_images(self) -> None:
        if len(self.image_list) == 0:
            print("No images to compress!")
            return

        print(f"Compressing {len(self.image_list)} file(s) ...")

        # for image in self.image_list:
        #     print(f"Compressing {image['input']} to {image['output']}")

        process_map(_compress_image, self.image_list)

        # remove borked files
        warnings = []
        for image in self.image_list:
            if not Path(image["output"]).exists:
                print(f"Warning: could not convert {image['input']}")
                warnings.append(image)

            output_size = file_size(image["output"])
            image["output_size"] = output_size

        [self.image_list.remove(w) for w in warnings]

        # delete originals
        [os.remove(f["input"]) for f in self.image_list]

    def _replace_rels(self) -> None:
        if self.temp_dir is None:
            raise RuntimeError("Temp dir not created!")

        if self.verbose:
            print("Replacing metadata ...")

        for file in glob.iglob(
            os.path.join(self.temp_dir, "ppt", "**", "*.rels"), recursive=True
        ):
            content = ""
            with open(str(file)) as f:
                content = f.read()

                for image in self.image_list:
                    original_file = Path(image["input"]).name
                    target_file = Path(image["output"]).name

                    if original_file not in content:
                        continue

                    content = content.replace(original_file, target_file)

            with open(str(file), "w") as f:
                f.write(content)

    def _zip(self) -> None:
        if self.temp_dir is None:
            raise RuntimeError("Temp dir not created!")

        src_path = Path(self.temp_dir)
        with zipfile.ZipFile(self.output_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in src_path.rglob("*"):
                zf.write(file, file.relative_to(src_path))

        print(f"Output written to: {self.output_file}")

    def _print_stats(self) -> None:
        input_size = file_size(self.input_file)
        output_size = file_size(self.output_file)
        percentage = round((input_size - output_size) / input_size * 100, 2)
        print(f"Input file:  {human_readable_size(input_size)}")
        print(
            f"Output file: {human_readable_size(output_size)} ({percentage}% reduction)"
        )
