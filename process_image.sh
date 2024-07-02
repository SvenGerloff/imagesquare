#!/bin/bash

file=$1
output_dir=$2
keyOut=$3

mkdir -p "$output_dir"
magick "$file" -background white -gravity center -resize 600x600 -extent 1000x1000 "$output_dir/$keyOut"
