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
date=20100425
svn={$date}

cd "$tmp"
svn checkout -r $svn svn://svn.mplayerhq.hu/ffmpeg/trunk ffmpeg-$date
cd ffmpeg-$date
pushd libswscale
svn update -r $svn libswscale
popd
./version.sh . version.h
find . -type d -name .svn -print0 | xargs -0r rm -rf
sed -i -e '/^\.PHONY: version\.h$/d' Makefile
cd ..
tar jcf "$pwd"/ffmpeg-$date.tar.bz2 ffmpeg-$date
cd - >/dev/null
