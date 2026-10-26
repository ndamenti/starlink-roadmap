#!/bin/bash
# usage: render.sh <scene>  — renders all frames of a scene in N parallel chunks, then encodes a silent clip
S=$1; D=/home/claude/v2; N=${2:-4}
DUR=$(python3 -c "import json;print(json.load(open('$D/marks.json'))['$S']['dur'])")
rm -rf $D/frames/$S; mkdir -p $D/frames/$S $D/clips
for i in $(seq 0 $((N-1))); do
  A=$(python3 -c "print($DUR*$i/$N)"); B=$(python3 -c "print($DUR*($i+1)/$N if $i<$N-1 else $DUR)")
  python3 $D/sc${S#s}.py $A $B > $D/frames/$S.log.$i 2>&1 &
done
wait
ffmpeg -v error -y -framerate 30 -i $D/frames/$S/f%05d.png -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p $D/clips/$S.mp4
echo "$S done $(ls $D/frames/$S | wc -l) frames"
