#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)

pushd "$tmp"
git clone git://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
git checkout release/4.4
git rev-parse HEAD
git archive --prefix="ffmpeg-${date}/" --format=tar release/4.4 | bzip2 > "$pwd"/ffmpeg-${date}.tar.bz2
popd
