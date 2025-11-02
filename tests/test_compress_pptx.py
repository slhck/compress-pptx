#!/usr/bin/env pytest

import os
import tempfile

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
