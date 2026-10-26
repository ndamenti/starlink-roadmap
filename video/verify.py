"""Verify every scene's frame set is complete and decodable; re-render bad/missing frames; re-encode the clip."""
import os, sys, json, subprocess, importlib
sys.path.insert(0,'/home/claude/v2'); from PIL import Image
D='/home/claude/v2'; M=json.load(open(f'{D}/marks.json'))
for s in sys.argv[1:]:
    n=int(M[s]['dur']*30); d=f'{D}/frames/{s}'; mod=importlib.import_module('sc'+s[1:]); bad=0
    for i in range(n):
        p=f'{d}/f{i:05d}.png'
        try: Image.open(p).verify()
        except Exception: mod.frame(i/30).save(p,compress_level=1); bad+=1
    subprocess.run(f'ffmpeg -v error -y -framerate 30 -i {d}/f%05d.png -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p {D}/clips/{s}.mp4',shell=True,check=True)
    dur=float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {D}/clips/{s}.mp4',shell=True))
    print(s,'frames',n,'fixed',bad,'clip',round(dur,2),'vo',M[s]['dur'])
