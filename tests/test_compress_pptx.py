#!/usr/bin/env pytest

import os

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
