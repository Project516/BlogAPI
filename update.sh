#!/bin/sh

# script to update mongoose files

# remove old files
rm include/mongoose.h
rm src/mongoose.c

# save latest files
wget -O include/mongoose.h https://raw.githubusercontent.com/cesanta/mongoose/master/mongoose.h
wget -O src/mongoose.c https://raw.githubusercontent.com/cesanta/mongoose/master/mongoose.c
