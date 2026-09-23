#!/usr/bin/env pytest

import os
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import compress_pptx.compress_pptx as compressor
from compress_pptx.compress_pptx import CompressPptx


def test_conversion(tmp_path):
    here = os.path.dirname(__file__)
    input_file = os.path.join(here, "test.pptx")
    output_file = tmp_path / "test-compressed.pptx"
    CompressPptx(input_file, str(output_file), num_cpus=1).run()

    with zipfile.ZipFile(output_file) as archive:
        names = set(archive.namelist())
        assert "ppt/media/image1-compressed.jpg" in names
        assert "ppt/media/image1.png" not in names
        manifest = ElementTree.fromstring(archive.read("[Content_Types].xml"))
        namespace = "http://schemas.openxmlformats.org/package/2006/content-types"
        overrides = {
            element.get("PartName"): element.get("ContentType")
            for element in manifest.findall(f"{{{namespace}}}Override")
        }
        assert overrides["/ppt/media/image1-compressed.jpg"] == "image/jpeg"
        assert "/ppt/media/image1.png" not in overrides


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
