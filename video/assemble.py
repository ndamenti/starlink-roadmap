"""Assemble the film: scene clips + 1 s bridges, narration with matching gaps, loudness-normalised, faded.
Run: python3 /home/claude/v2/assemble.py            -> /home/claude/v2/starlink-mobile-explainer.mp4
     python3 /home/claude/v2/assemble.py s6 s7      -> pilot of just those scenes
Also prints the VIDEO_CHAPTERS array for index.html.
"""
import sys, json, subprocess, os
import soundfile as sf, numpy as np
D="/home/claude/v2"; ORDER=["s1","s2","s3","s4","s5","s6","s7","s8","s9"]
TITLES={"s1":"The pitch","s2":"Spectrum & the density dilemma","s3":"The physics wall","s4":"Coverage & the strip machine",
        "s5":"Fleet growth & frequency reuse","s6":"The low band — what 800 MHz buys","s7":"The ground layer — the capstone",
        "s8":"What could break it","s9":"The verdict"}
scenes=sys.argv[1:] or ORDER; outname=D+("/starlink-mobile-explainer.mp4" if not sys.argv[1:] else "/pilot-"+"-".join(scenes)+".mp4")
GAP=1.0; sr=24000
# bridge clip: 1 s of background
subprocess.run(f"ffmpeg -v error -y -f lavfi -i color=c=0x070b14:s=1920x1080:r=30 -t {GAP} -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p {D}/clips/gap.mp4",shell=True,check=True)
lines=[]; au=[]; t=0.0; chapters=[]
for i,s in enumerate(scenes):
    vdur=float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {D}/clips/{s}.mp4",shell=True))
    a,_=sf.read(f"{D}/vo_{s}.wav")
    # pad/trim audio to the clip length so sync stays frame-exact
    n=int(round(vdur*sr)); a=np.pad(a,(0,max(0,n-len(a))))[:n]
    chapters.append((t,TITLES[s])); lines.append(f"file '{D}/clips/{s}.mp4'"); au.append(a); t+=vdur
    if i<len(scenes)-1: lines.append(f"file '{D}/clips/gap.mp4'"); au.append(np.zeros(int(sr*GAP))); t+=GAP
open(f"{D}/concat.txt","w").write("\n".join(lines)+"\n"); full=np.concatenate(au); sf.write(f"{D}/full_vo.wav",full,sr)
subprocess.run(f"ffmpeg -v error -y -f concat -safe 0 -i {D}/concat.txt -c copy {D}/silent_full.mp4",shell=True,check=True)
subprocess.run(f'ffmpeg -v error -y -i {D}/silent_full.mp4 -i {D}/full_vo.wav -filter_complex "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.5,afade=t=out:st={t-1.2:.2f}:d=1.2[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart {outname}',shell=True,check=True)
print(subprocess.check_output(f"ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 {outname}",shell=True).decode())
print("const VIDEO_CHAPTERS = [")
for tc,ttl in chapters: print(f'  ["{int(tc//60)}:{int(tc%60):02d}", {tc:.1f}, "{ttl}"],')
print("];")
