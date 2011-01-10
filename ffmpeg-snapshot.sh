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
svn={$date}
svn=HEAD

cd "$tmp"
svn checkout -r $svn svn://svn.mplayerhq.hu/ffmpeg/trunk ffmpeg-$date
cd ffmpeg-$date
pushd libswscale
svn update -r $svn libswscale
popd
cd ..
tar jcf "$pwd"/ffmpeg-$date.tar.bz2 ffmpeg-$date
cd - >/dev/null
