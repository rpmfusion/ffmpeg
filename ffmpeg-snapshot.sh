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
svn=$(date +%Y%m%d)
svn=20080908

cd "$tmp"
svn checkout -r {$svn} svn://svn.mplayerhq.hu/ffmpeg/trunk ffmpeg-$svn
cd ffmpeg-$svn/libswscale
svn update -r {$svn}
cd ..
./version.sh . version.h
find . -type d -name .svn -print0 | xargs -0r rm -rf
sed -i -e '/^\.PHONY: version\.h$/d' Makefile
cd ..
tar jcf "$pwd"/ffmpeg-$svn.tar.bz2 ffmpeg-$svn
cd - >/dev/null
