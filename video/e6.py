import sys; sys.path.insert(0,'/home/claude/v2'); from elib import *
B=lambda i: beat("e6",i)
CL=[("1","PROTECTED BY NUMBERS, NOT EMPTY SPACE","−13 dBm/MHz standard · −40 at hardened edges · zero vacant MHz by design since the 1990s · 47 CFR §27.53, §90.691",TEXT),
    ("2","MEASURED AT THE VICTIM, ON THE GROUND","−120 dBW/m²/MHz · 1.5 m above ground · aggregate across the whole fleet · §25.202(k)(1) · and §90.672's receiver test at 800 MHz",BLUE),
    ("3","THE RECORD SHOWS THE REGULATOR SAYING NO","SpaceX asked 9.4 dB · got it in two 5 MHz slivers only · over AT&T, Verizon, EchoStar · claw-back to −120 on interference · DA 25-197",AMBER)]
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(5)]; a=fade(t,0.2,1e9,0.5)
    head(d,t,"THREE THINGS FOLLOW — NONE OF THEM AN OPINION","",0.2,1e9)
    for i,(n,ttl,sub,c) in enumerate(CL):
        aa=a*fade(t,b[i+1][0],1e9,0.6); y=190+i*200; panel(d,120,y,1800,y+170,aa); d.rounded_rectangle([120*SS,y*SS,126*SS,(y+170)*SS],3*SS,fill=al(c,aa))
        d.text((160*SS,(y+30)*SS),n,font=fnt(56,True),fill=al(c,aa)); d.text((250*SS,(y+36)*SS),ttl,font=fnt(30,True),fill=al(TEXT,aa)); d.text((250*SS,(y+92)*SS),sub,font=mono(15),fill=al(DIM,aa*fade(t,b[i+1][0]+2.0,1e9,0.5)))
        if b[i+1][0]<=t<b[min(i+2,4)][0]: p=pulse(t); d.rounded_rectangle([(116-3*p)*SS,(y-4-3*p)*SS,(1804+3*p)*SS,(y+174+3*p)*SS],12*SS,outline=al(c,aa*0.8),width=3*SS)
    if t>b[4][0]-0.2:
        fa=fade(t,b[4][0],1e9,0.6); d.rectangle([0,800*SS,W*SS,H*SS],fill=al(BG,fa*0.9))
        d.text((120*SS,830*SS),"if you believe the neighbors are unprotected —",font=fnt(34),fill=al(TEXT,fa)); d.text((120*SS,890*SS),"say which number is wrong.",font=fnt(44,True),fill=al(AMBER,fa*fade(t,b[4][0]+2.2,1e9,0.5)))
        d.text((120*SS,990*SS),"every figure: Spectrum → The seams · starlink-roadmap-production.up.railway.app",font=mono(15),fill=al(DIM,fa*fade(t,b[4][0]+3.5,1e9,0.5)))
    return out(im)
if __name__=="__main__": render_range(frame,"e6",float(sys.argv[1]),float(sys.argv[2]))
