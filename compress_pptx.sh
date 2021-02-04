#!/usr/bin/env bash
#
# PPTX compression script.
#
# Compresses all images within a PPTX input that are too large.
#
# Options are available to set JPEG quality and size threshold.
# See `-h` for more.
#
# Version: v0.1
# Copyright (c) 2021, Werner Robitza <werner.robitza@gmail.com>
# License: MIT

set -e
set -o pipefail

red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
reset=$(tput sgr0)

error() {
  echo "${red}ERR:  ${reset}$1"
}

warning() {
  echo "${yellow}WARN: ${reset}$1"
}

info() {
  echo "${green}INFO: ${reset}$1"
}

# Check necessary dependencies
for cmd in perl magick zip unzip; do
  command -v "$cmd" >/dev/null 2>&1 || { error "$cmd not found in \$PATH. Please install it!"; exit 1; }
done

usage() {
  echo "Usage:"
  echo
  echo "$0 [-s SIZE] [-q QUALITY] [-o OUTPUT] <input>"
  echo
  echo "  -s SIZE     Minimum size in for images to be compressed (default: 1M)"
  echo "              You can use 'k' for KiB or 'M' for MiB as suffix."
  echo "  -q QUALITY  JPEG quality, from 0-100 (default: 85)"
  echo "              Higher values mean better quality, larger file size."
  echo "  -o OUTPUT   Output file (default: input file with '-compressed.pptx' suffix)"
  echo
  echo "compress-pptx v0.2"
  echo "Copyright (c) 2021, Werner Robitza"
  echo "License: MIT"
  exit 1
}

output=
size="1M" # MB above which to compress a media (PNG, TIFF) file
quality="85" # JPEG quality

if [[ $# -eq 0 ]]; then
  usage;
fi

while getopts "s:q:o:" flag; do
case "$flag" in
    s) size=$OPTARG;;
    q) quality=$OPTARG;;
    o) output=$OPTARG;;
    *) usage;;
esac
done

input=${*:$OPTIND:1}
filename="$(basename "$input")"
srcDir=$(realpath "$(dirname "$input")")

# if no default was set
if [[ -z "$output" ]]; then
  output="${srcDir}/${filename%%.pptx}-compressed.pptx"
fi

# Temporary folder
tmpDir="$(mktemp -d -t tmp.XXXXXXXXXX)"
__cleanup() {
  rm -rf "$tmpDir"
}

# =============================================================

if [[ ! -f "$input" ]]; then
  error "Input file $input not found"
  exit 1
fi

info "Unzipping file to temporary directory ${tmpDir}"
unzip -q "$input" -d "$tmpDir"

info "Finding files larger than ${size}"
# TODO parallelize this if possible?
find "${tmpDir}/ppt/media" \
  -type f \
  \( -iname '*.png' -o -iname '*.tiff' \) \
  -size +"${size}" \
  -print0 | while read -r -d $'\0' file; do
  filename=$(basename -- "$file")
  dir="$(dirname -- "$file")"
  target="compressed_${filename%.*}.jpg"

  # check if image has transparency
  if [[ "$(magick identify -format '%[opaque]' "$file")" =~ "False" ]]; then
    warning "Skipping ${filename} since it contains transparency."
    continue
  fi

  info "Compressing ${filename} ($(du -h "$file" | cut -f -1 | tr -d ' '))"
  magick convert \
    -quality "${quality}" \
    "${file}" "${dir}/${target}"
  rm -- "$file"

  # replace filenames in XML
  # FIXME: this might be a bit hacky
  find "${tmpDir}/ppt/" \
    -iname '*.rels' \
    -exec perl -pi -e "s/${filename}/${target}/g" {} \+
done

pushd "$tmpDir" > /dev/null || exit
info "Writing output to $output"
zip -q -r "$output" .
popd  > /dev/null || exit

info "Done."

info "Input size:  $(du -h "$input" | cut -f -1)"
info "Output size: $(du -h "$output" | cut -f -1)"
__cleanup

trap __cleanup EXIT