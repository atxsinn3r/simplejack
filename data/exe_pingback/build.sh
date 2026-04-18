#!/bin/bash

if [ -z "$1" ]; then
  echo "Missing URL for pingback: $1"
  exit -1
fi

vcpkg install --binarysource=clear
if test -d "build"; then rm -r build; fi
mkdir build && cd build
cmake .. "-DCMAKE_TOOLCHAIN_FILE=$VCPKG_CMAKE" "-DURL=$1"
cmake --build .
if test -f "VCPKG_TEST"; then mv VCPKG_TEST ../../bin; fi
cd ..
