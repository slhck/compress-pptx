#!/usr/bin/env pytest

import os
import tempfile
from pathlib import Path

import compress_pptx.compress_pptx as compressor
from compress_pptx.compress_pptx import CompressPptx


def test_conversion():
    here = os.path.dirname(__file__)
    input_file = os.path.join(here, "test.pptx")
    output_file = os.path.join(here, "test-compressed.pptx")
    if os.path.isfile(output_file):
        os.remove(output_file)
    CompressPptx(input_file, output_file).run()
    assert os.path.isfile(output_file)
    os.remove(output_file)


def test_extract():
    here = os.path.dirname(__file__)
    input_file = os.path.join(here, "test.pptx")

    with tempfile.TemporaryDirectory() as temp_dir:
        extract_dir = os.path.join(temp_dir, "media")
        CompressPptx(input_file, input_file, extract_dir=extract_dir).run()

        # Check that the directory was created
        assert os.path.isdir(extract_dir)

        # Check that media files were extracted
        extracted_files = os.listdir(extract_dir)
        assert len(extracted_files) > 0

        # Check that at least one file exists
        for file in extracted_files:
            file_path = os.path.join(extract_dir, file)
            assert os.path.isfile(file_path)


def test_extract_creates_directory():
    here = os.path.dirname(__file__)
    input_file = os.path.join(here, "test.pptx")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Use a nested directory that doesn't exist
        extract_dir = os.path.join(temp_dir, "nested", "media")
        CompressPptx(input_file, input_file, extract_dir=extract_dir).run()

        # Check that the directory was created
        assert os.path.isdir(extract_dir)

        # Check that media files were extracted
        extracted_files = os.listdir(extract_dir)
        assert len(extracted_files) > 0


def test_transparency_check_skips_emf(monkeypatch, tmp_path):
    media_dir = tmp_path / "ppt" / "media"
    media_dir.mkdir(parents=True)
    (media_dir / "image.emf").write_bytes(b"emf")
    (media_dir / "image.png").write_bytes(b"png")
    checked = []

    def has_transparency(path, identify_cmd, verbose):
        checked.append(Path(path).suffix)
        return False

    monkeypatch.setattr(compressor, "which", lambda command: "/usr/bin/magick")
    monkeypatch.setattr(compressor, "_has_transparency", has_transparency)
    input_file = Path(__file__).with_name("test.pptx")
    job = CompressPptx(
        str(input_file),
        str(tmp_path / "output.pptx"),
        size=0,
        skip_transparent_images=True,
    )
    job.temp_dir = str(tmp_path)

    job._find_files()

    assert checked == [".png"]
    assert [Path(file["input"]).name for file in job.file_list] == ["image.png"]
