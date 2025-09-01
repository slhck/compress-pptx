import glob
import os
import tempfile
import zipfile
from pathlib import Path
from typing import List, Optional, TypedDict

from tqdm.contrib.concurrent import process_map

from .util import (
    convert_size_to_bytes,
    file_size,
    human_readable_size,
    run_command,
    which,
)


class FileObj(TypedDict):
    is_image: bool
    input: str
    output: str
    input_size: int
    output_size: Optional[int]
    quality: int
    transparency: str
    verbose: bool


def _compress_file(file: FileObj):
    if file["is_image"]:
        # image, use convert (imagemagick)
        cmd = [
            "magick",
            "convert",
            "-quality",
            str(file["quality"]),
            "-background",
            "white",
            "-alpha",
            "remove",
            "-alpha",
            "off",
            file["input"] + "[0]",  # add [0] to use only the first page of TIFFs
            file["output"],
        ]
    else:
        # video, use ffmpeg
        cmd = ["ffmpeg", "-i", file["input"], file["output"]]
    run_command(cmd, verbose=file["verbose"])


def _has_transparency(input_file: str, verbose=False) -> bool:
    cmd = ["magick", "identify", "-format", "%[opaque]", input_file]
    stdout, _ = run_command(cmd, verbose=verbose)
    if stdout is not None and stdout.strip() == "False":
        return True
    return False


class CompressPptxError(SystemError):
    pass


class CompressPptx:
    DEFAULT_QUALITY = 85
    DEFAULT_SIZE = "1MiB"
    DEFAULT_TRANSPARENCY = "white"

    temp_dir: Optional[str]

    def __init__(
        self,
        input_file: str,
        output_file: str,
        size=convert_size_to_bytes(DEFAULT_SIZE),
        quality=DEFAULT_QUALITY,
        transparency=DEFAULT_TRANSPARENCY,
        skip_transparent_images=False,
        verbose=False,
        force=False,
        compress_media=False,
        recompress_jpeg=False,
        use_libreoffice=False,
        num_cpus=1,
    ) -> None:
        """
        Compress images in a PowerPoint file.

        Args:
            input_file (str): Path to input file
            output_file (str): Path to output file
            size (int, optional): Minimum size of images to compress. Defaults to 1MiB.
            quality (int, optional): JPEG quality to use. Defaults to 85.
            transparency (str, optional): Color to replace transparency with. Defaults to "white".
            skip_transparent_images (bool, optional): Skip converting transparent images. Defaults to False.
            verbose (bool, optional): Show additional info. Defaults to False.
            force (bool, optional): Force overwriting output file. Defaults to False.
            compress_media (bool, optional): Compress other media types such as audio and video (requires ffmpeg). Defaults to False.
            recompress_jpeg (bool, optional): Recompress jpeg images. Defaults to False.
            use_libreoffice (bool, optional): Use LibreOffice to compress EMF files (only way to compress EMF files under Linux). Defaults to False.
            num_cpus (int, optional): Number of CPUs to use for parallel processing. Defaults to 1.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.size = int(size)
        self.quality = int(quality)
        self.transparency = str(transparency)
        self.skip_transparent_images = bool(skip_transparent_images)
        self.verbose = bool(verbose)
        self.force = bool(force)
        self.compress_media = compress_media
        self.use_libreoffice = use_libreoffice
        self.num_cpus = num_cpus

        # file extensions and conversions
        self.image_extensions = [".png", ".emf", ".tiff"]
        if recompress_jpeg:
            self.image_extensions.extend([".jpg", ".jpeg"])
        self.converted_image_extension = ".jpg"

        self.video_extensions = [".mov", ".avi", ".mp4"]
        self.converted_video_extensions = ".mp4"
        self.audio_extensions = [".mp3", ".wav"]
        self.converted_audio_extensions = ".mp3"

        self.file_list: List[FileObj] = []

        required_executables = ["magick"]
        # add ffmpeg to required executables if user wants media files to be compressed
        if self.compress_media:
            required_executables.append("ffmpeg")
        # add "unoconv" (libreoffice package) to required executables of user wants emf files compressed
        if self.use_libreoffice:
            required_executables.append("unoconv")

        for expected_cmd in required_executables:
            if which(expected_cmd) is None:
                raise CompressPptxError(
                    f"ImageMagick '{expected_cmd}' not found in PATH. Make sure you have installed ImageMagick and that the '{expected_cmd}' command is available."
                )

        if self.quality < 0 or self.quality > 100:
            raise CompressPptxError("Quality must be between 0-100!")

        if not Path(self.input_file).exists():
            raise CompressPptxError(f"No such file: {self.input_file}")

        if not (
            Path(self.input_file).suffix.endswith("pptx")
            or Path(self.input_file).suffix.endswith("potx")
        ):
            raise CompressPptxError("Input must be a PPTX or POTX file!")

        if Path(self.output_file).exists() and not self.force:
            raise CompressPptxError(
                f"Output file {self.output_file} already exists. Use -f/--force to force overwriting."
            )

        self.temp_dir = None

    def run(self) -> None:
        if self.verbose:
            print(f"Converting {self.input_file} to {self.output_file}")

        with tempfile.TemporaryDirectory() as temp_dir:
            self.temp_dir = temp_dir

            # Unzip
            self._unzip()

            # Collect compressible files
            self._find_files()

            # Compress
            self._compress_files()

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

    def _check_endswith(self, filename: str, extensions: List[str]) -> bool:
        for ext in extensions:
            if filename.endswith(ext):
                return True
        return False

    def _find_files(self) -> None:
        if self.temp_dir is None:
            raise RuntimeError("Temp dir not created!")

        for file in glob.iglob(
            os.path.join(self.temp_dir, "ppt", "media", "*"), recursive=True
        ):
            is_image = True
            output_extension = self.converted_image_extension
            # skip unaffected extensions
            if not (
                self._check_endswith(file, self.image_extensions)
            ):  # is not an image
                if (
                    self.compress_media
                ):  # and is also not a media (and compressing media enabled)
                    is_image = False
                    if self._check_endswith(file, self.video_extensions):
                        output_extension = self.converted_video_extensions
                    elif self._check_endswith(file, self.audio_extensions):
                        output_extension = self.converted_audio_extensions
                    else:
                        continue  ## file is not a media file
                else:
                    continue  ## file is not an image

            # skip files that are too small
            fsize = file_size(file)
            if fsize < self.size:
                # print(f"Skipping {Path(file).name} because it is too small")
                continue

            if is_image:  # image file
                # skip files with transparency
                if self.skip_transparent_images and _has_transparency(
                    file, self.verbose
                ):
                    if self.verbose:
                        print(
                            f"Skipping {Path(file).name} because it contains transparency"
                        )
                    continue

            if self.verbose:
                print(
                    f"{Path(file).name} added to conversion queue ({human_readable_size(fsize)})"
                )

            file_obj: FileObj = {
                "is_image": is_image,
                "input": file,
                "output": (
                    Path(file).parent
                    / (Path(file).stem + "-compressed" + output_extension)
                ).as_posix(),
                "input_size": fsize,
                "output_size": None,
                "quality": self.quality,
                "transparency": self.transparency,
                "verbose": self.verbose,
            }

            self.file_list.append(file_obj)

    def _libreoffice_compress_files(self, files: List[FileObj]):
        for file in files:
            cmd = [
                "unoconv",
                "-f",
                "jpg",
                "-o",
                file["output"],
                file["input"],
            ]
            run_command(cmd, verbose=file["verbose"])

    def _compress_files(self) -> None:
        if len(self.file_list) == 0:
            print("No Files to compress!")
            return

        for file in self.file_list:
            if self.verbose:
                print(f"Compressing {file['input']} to {file['output']}")

        # compress files with "magick convert" and "ffmpeg" in parallel
        non_emf_files = [f for f in self.file_list if not f["input"].endswith(".emf")]
        print(f"Compressing {len(non_emf_files)} file(s) ...")
        if self.num_cpus > 1:
            process_map(_compress_file, non_emf_files, max_workers=self.num_cpus)
        else:
            for file in non_emf_files:
                _compress_file(file)

        emf_files = [f for f in self.file_list if f["input"].endswith(".emf")]
        if len(emf_files) > 0:
            print(f"Compressing {len(emf_files)} .EMF file(s) ...")
            if self.use_libreoffice:
                # compress ".emf" (microsoft) files using libreoffice sequentially
                # (idk why, but it dosent work in parallel)
                self._libreoffice_compress_files(emf_files)
            else:
                # compress ".emf" files using "magick convert" which works only on windows
                if self.num_cpus > 1:
                    process_map(_compress_file, emf_files, max_workers=self.num_cpus)
                else:
                    for file in emf_files:
                        _compress_file(file)

        # remove borked files
        warnings = []
        for file in self.file_list:
            if not Path(file["output"]).exists():
                print(f"Warning: could not convert {file['input']}")
                warnings.append(file)
            else:
                output_size = file_size(file["output"])
                file["output_size"] = output_size

        for w in warnings:
            self.file_list.remove(w)

        # delete originals
        for f in self.file_list:
            os.remove(f["input"])

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

                for compress_file in self.file_list:
                    original_file = Path(compress_file["input"]).name
                    target_file = Path(compress_file["output"]).name

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
