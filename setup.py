#!/usr/bin/env python3

from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# read version string
with open(path.join(here, "compress_pptx", "__init__.py")) as version_file:
    version = eval(version_file.read().split(" = ")[1].strip())

# Get the long description from the README file
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

# Get the history from the CHANGELOG file
with open(path.join(here, "CHANGELOG.md")) as f:
    history = f.read()

setup(
    name="compress_pptx",
    version=version,
    description="Compress images in PPTX files",
    long_description=long_description + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Werner Robitza",
    author_email="werner.robitza@gmail.com",
    url="https://github.com/slhck/compress-pptx",
    packages=["compress_pptx"],
    include_package_data=True,
    install_requires=["tqdm"],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "MIT",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    entry_points={"console_scripts": ["compress-pptx = compress_pptx.__main__:main"]},
)
