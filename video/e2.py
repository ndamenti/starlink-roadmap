import sys, math; sys.path.insert(0,'/home/claude/v2'); from elib import *
B=lambda i: beat("e2",i)
def mask(d,x0,y0,w,h,a,k,hard=False):
    # power vs frequency: flat in-block, then the mask ceiling outside; y maps dBm/MHz from +30 (top) to -60 (bottom)
    ymap=lambda v:y0+h*(30-v)/90
    edge=x0+w*0.5
    d.line([(x0*SS,ymap(-13)*SS),((x0+w)*SS,ymap(-13)*SS)],fill=al(LINE,a),width=1*SS)
    for v in (30,0,-13,-40): d.text(((x0-14)*SS,ymap(v)*SS),f"{v:+d}" if v else "0",font=mono(12),fill=al(DIM,a),anchor="rm")
    d.text(((x0-14)*SS,(y0-16)*SS),"dBm/MHz",font=mono(12),fill=al(DIM,a),anchor="rm")
    # in-block power
    d.rectangle([x0*SS,ymap(26)*SS,edge*SS,ymap(-60)*SS],fill=al(AMBER,a*0.35))
    d.text(((x0+w*0.25)*SS,(y0+h*0.55)*SS),"YOUR BLOCK\nas loud as you like",font=mono(14,True),fill=al(TEXT,a),anchor="mm",align="center")
    # mask line outside: steps to -13 (or -40) within ~ first segment
    lvl=-40 if hard else -13
    pts=[(edge,26),(edge+w*0.02,lvl),(x0+w,lvl)]
    pts=[(px*SS,ymap(pv)*SS) for px,pv in pts]
    n=max(2,int(len(pts)*k+1)); d.line(pts[:n] if k>=1 else [pts[0],(pts[0][0]+(pts[-1][0]-pts[0][0])*k,pts[0][1]+(pts[-1][1]-pts[0][1])*min(1,k*8) if k<0.12 else pts[1][1])],fill=al(RED,a),width=5*SS)
    d.text(((edge+w*0.27)*SS,(ymap(lvl)-26)*SS),f"the fence · {lvl} dBm/MHz ceiling",font=mono(14,True),fill=al(RED,a*ease(clamp((k-0.5)/0.4))),anchor="mm")
    d.text(((edge+w*0.27)*SS,(y0+h*0.75)*SS),"NEIGHBOR'S BLOCK",font=mono(14,True),fill=al(BLUE,a),anchor="mm")
    d.line([(edge*SS,y0*SS),(edge*SS,(y0+h)*SS)],fill=al(TEXT,a*0.8),width=3*SS); d.text((edge*SS,(y0+h+20)*SS),"license edge · zero vacant MHz",font=mono(13),fill=al(TEXT,a),anchor="mm")
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(3)]; a=fade(t,0.2,1e9,0.5)
    head(d,t,"FENCES, NOT GAPS","adjacent yards · no buffer strip · a ceiling measured at the fence",0.2,1e9)
    k=ease(clamp((t-b[1][0]+0.5)/2.5)); mask(d,260,220,1100,520,a,k)
    if b[1][0]<t: 
        ca=fade(t,b[1][0]+1.5,1e9,0.5); card(d,1420,220,440,150,"THE STANDARD MASK","43 + 10·log₁₀(P)","dB of attenuation outside the block",TEXT,ca)
        card(d,1420,400,440,150,"AT THE BLOCK EDGE","−13 dBm/MHz","47 CFR §27.53(h) · §90.691(a)",RED,ca*fade(t,b[1][0]+6.5,1e9,0.5))
    if t>b[2][0]-0.2:
        sa=fade(t,b[2][0],1e9,0.5); y=850; fx=band_strip(d,260,y,1100,[(0,10,"AT&T","PCS",BLUE,0.35,0),(10,20,"VERIZON","PCS",PURPLE,0.35,0.4),(20,30,"T-MOBILE","PCS",GREEN,0.35,0.8)],0,30,sa,t,b[2][0])
        d.text((260*SS,(y+90)*SS),"every carrier in America, today · vacant spectrum is wasted money",font=mono(15),fill=al(TEXT,sa*fade(t,b[2][0]+4,1e9,0.5)))
    return out(im)
if __name__=="__main__": render_range(frame,"e2",float(sys.argv[1]),float(sys.argv[2]))
