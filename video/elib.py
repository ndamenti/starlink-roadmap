import sys, json; sys.path.insert(0,'/home/claude/v2')
import lib
from lib import *
lib._MARKS=json.load(open('/home/claude/v2/marks_seams.json'))
def band_strip(d,x0,y0,w,blocks,lo,hi,a,t=None,t0=0):
    """blocks: (f0,f1,label,sub,color|None,op,delay)"""
    fx=lambda f:x0+(f-lo)/(hi-lo)*w
    d.line([(fx(lo)*SS,(y0+70)*SS),(fx(hi)*SS,(y0+70)*SS)],fill=al(LINE,a),width=2*SS)
    for f0,f1,lab,sub,c,op,dl in blocks:
        aa=a*(ease(clamp((t-t0-dl)/0.6)) if t is not None else 1)
        if aa<=0.01: continue
        if c is None: d.rectangle([fx(f0)*SS,y0*SS,fx(f1)*SS,(y0+70)*SS],outline=al(TEXT,aa*0.8),width=2*SS)
        else: d.rectangle([fx(f0)*SS,y0*SS,fx(f1)*SS,(y0+70)*SS],fill=al(c,aa*op),outline=al(c,aa),width=2*SS)
        cx=(fx(f0)+fx(f1))/2; col=c or TEXT
        d.text((cx*SS,(y0+22)*SS),lab,font=mono(15,True),fill=al(TEXT,aa),anchor="mm")
        if sub: d.text((cx*SS,(y0+48)*SS),sub,font=mono(12),fill=al(DIM,aa),anchor="mm")
        d.text((fx(f0)*SS,(y0-14)*SS),str(f0),font=mono(12),fill=al(DIM,aa),anchor="mm")
    d.text((fx(hi)*SS,(y0-14)*SS),f"{hi} MHz",font=mono(12),fill=al(DIM,a),anchor="rm")
    return fx
def card(d,x,y,w,h,ttl,val,sub,c,a):
    panel(d,x,y,x+w,y+h,a); d.rounded_rectangle([x*SS,y*SS,(x+6)*SS,(y+h)*SS],3*SS,fill=al(c,a))
    d.text(((x+28)*SS,(y+22)*SS),ttl,font=mono(14),fill=al(DIM,a)); d.text(((x+28)*SS,(y+50)*SS),val,font=fnt(40,True),fill=al(c,a))
    if sub: d.text(((x+28)*SS,(y+h-36)*SS),sub,font=mono(14),fill=al(TEXT,a*0.9))
