#!/bin/sh

# script to build and run api

make clean 
make || exit 1
./BlogAPI
