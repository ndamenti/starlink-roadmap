#!/bin/bash
D=/home/claude/v2; S=$1
DUR=$(python3 -c "import json;print(json.load(open('$D/marks_seams.json'))['$S']['dur'])")
rm -rf $D/frames/$S; mkdir -p $D/frames/$S $D/clips
python3 $D/$S.py 0 $DUR > $D/frames/$S.log 2>&1
ffmpeg -v error -y -framerate 30 -i $D/frames/$S/f%05d.png -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p $D/clips/$S.mp4
echo "$S done $(ls $D/frames/$S | wc -l)"
