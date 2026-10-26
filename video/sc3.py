import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s3",i)
RUNGS=[("MEASURED  ·  live service today",0.62,RED,"12 Mbps"),("CLAIM-ANCHORED  ·  planning target",2.48,AMBER,"50 Mbps"),("HEADLINE CLAIM  ·  single-user peak",7.5,GREEN,"150 Mbps")]
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(4)]
    if t<b[1][0]+0.3:
        a=fade(t,0.2,b[1][0]+0.2,0.5)
        head(d,t,"THE PHYSICS WALL","a quarter-watt phone · a satellite 330 km up",0.2,b[1][0]+0.2)
        px,py=260*SS,780*SS; phone_glyph(d,px,py,a,1.1); sx,sy=1560*SS,320*SS; sat_glyph(d,sx,sy,a)
        k=ease(clamp((t-1.0)/3.5)); steps=40
        for i in range(steps):
            f0,f1=i/steps,(i+1)/steps
            if f1>k: break
            x0,y0=px+(sx-px)*f0,py+(sy-py)*f0; x1,y1=px+(sx-px)*f1,py+(sy-py)*f1
            aa=a*(1.0-f0)**2.4; d.line([(x0,y0),(x1,y1)],fill=al(BLUE,max(aa,0.04)),width=int(max(1,(1-f0)*9)*SS))
        d.text((640*SS,600*SS),f"-{150*k:.0f} dB",font=fnt(72,True),fill=al(AMBER,a))
        d.text((644*SS,690*SS),"free-space loss at 2 GHz · ~480 km slant path",font=mono(18),fill=al(DIM,a))
        if t>4.5: d.text((644*SS,740*SS),"the signal arrives about a million billion times weaker",font=fnt(22),fill=al(TEXT,a*fade(t,4.6,1e9,0.6)))
    if t>b[1][0]-0.4:
        a=fade(t,b[1][0]-0.3,1e9,0.6); im2,d2=canvas()
        head(d2,t,"SO HOW FAST IS IT, REALLY?","throughput = spectrum × spectral efficiency  ·  at 20 MHz",b[1][0]-0.3,1e9)
        d2.text((90*SS,180*SS),"bits per second, per hertz",font=mono(16),fill=al(DIM,a)); maxv=8.0
        # narration-keyed: which rung is active during beat 2
        act=-1
        if b[2][0]<=t<b[3][0]:
            seg=(t-b[2][0])/(b[2][1]-b[2][0]); act=0 if seg<0.33 else (1 if seg<0.66 else 2)
        for i,(lab,v,c,mb) in enumerate(RUNGS):
            aa=a*ease(clamp((t-(b[2][0]-0.4+i*1.5))/0.8))
            if aa<=0.01: continue
            dimf=1.0 if act<0 or act==i else 0.42
            y=300+i*180; wfull=1350*(v/maxv); grow=ease(clamp((t-(b[2][0]-0.3+i*1.5))/1.1))
            d2.rounded_rectangle([300*SS,y*SS,(300+wfull*grow)*SS,(y+72)*SS],5*SS,fill=al(c,aa*0.42*dimf),outline=al(c,aa*dimf),width=2*SS)
            if act==i:
                p=pulse(t); d2.rounded_rectangle([(296-4*p)*SS,(y-4-4*p)*SS,(304+wfull*grow+4*p)*SS,(y+76+4*p)*SS],7*SS,outline=al(c,aa*0.9),width=3*SS)
            d2.text((90*SS,(y+6)*SS),f"{v}",font=fnt(40,True),fill=al(c,aa*dimf))
            d2.text((90*SS,(y+56)*SS),"bps/Hz",font=mono(13),fill=al(DIM,aa*dimf))
            d2.text((320*SS,(y+10)*SS),lab,font=mono(16,True),fill=al(TEXT,aa*dimf))
            d2.text((320*SS,(y+42)*SS),mb+" per beam",font=mono(15),fill=al(DIM,aa*dimf))
        if t>b[3][0]-0.3:
            ba=fade(t,b[3][0]-0.2,1e9,0.5)
            d2.line([(250*SS,300*SS),(250*SS,672*SS)],fill=al(TEXT,ba*0.7),width=3*SS)
            for yy in (300,672): d2.line([(230*SS,yy*SS),(270*SS,yy*SS)],fill=al(TEXT,ba*0.7),width=3*SS)
            d2.text((90*SS,900*SS),"these are the endpoints of a bracket — not competing facts",font=fnt(26),fill=al(TEXT,ba))
            d2.text((94*SS,948*SS),"every figure on the site is labelled with which end it holds",font=mono(17),fill=al(DIM,ba))
        im=Image.blend(im,im2,a)
    return out(im)
if __name__=="__main__": render_range(frame,"s3",float(sys.argv[1]),float(sys.argv[2]))
