import sys; sys.path.insert(0,'/home/claude/v2'); from elib import *
B=lambda i: beat("e3",i)
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(3)]; a=fade(t,0.2,1e9,0.5)
    head(d,t,"WHERE THE NEIGHBOR IS LISTENING, THE FENCE IS 500× STRICTER","the lower seam around the n252 uplink · to scale",0.2,1e9)
    y=300; blocks=[(1980,1990,"PCS A–F DL","Big-3",DIM,0.25,0),(1990,1995,"G","T-Mobile",GREEN,0.3,0.1),(1995,2000,"H DL","SpaceX",AMBER,0.35,0.2),(2000,2020,"n252 UPLINK","SpaceX · owned",AMBER,0.5,0.3),(2020,2025,"J — VACANT","never sold",None,0,0.4),(2025,2031,"BAS","broadcast aux",PURPLE,0.25,0.5)]
    fx=band_strip(d,160,y,1600,blocks,1978,2032,a,t,0)
    # mask ramp annotation
    if t>b[0][0]+1.5:
        ra=fade(t,b[0][0]+1.6,1e9,0.5); d.line([(fx(1995)*SS,(y+90)*SS),(fx(2000)*SS,(y+90)*SS)],fill=al(RED,ra),width=4*SS)
        d.text((fx(1997.5)*SS,(y+112)*SS),"−40 → −13 dBm/MHz ramp",font=mono(13,True),fill=al(RED,ra),anchor="mm")
        card(d,160,480,520,170,"HARDENED EDGE · BELOW 1995 MHz","−40 dBm/MHz","70 + 10·log₁₀(P) · §27.53(h) · 500× stricter",RED,ra)
    if t>b[1][0]-0.2:
        ha=fade(t,b[1][0],1e9,0.5); card(d,720,480,520,170,"WRITTEN 2012 FOR","DISH ↔ H-block","a hostile boundary · now both sides SpaceX",AMBER,ha)
        d.text((720*SS,690*SS),"binds in both directions — §27.53(h)(2)(iv): H fires back at −40 into 2005–2020",font=mono(14),fill=al(TEXT,ha*fade(t,b[1][0]+5,1e9,0.5)))
        # arrows both ways across 2000
        for s_,dl in ((-1,0),(1,0.6)):
            aa=ha*fade(t,b[1][0]+7+dl,1e9,0.4); x=fx(2000); d.line([(x*SS,(y-40)*SS),((x+s_*60)*SS,(y-40)*SS)],fill=al(RED,aa),width=4*SS); d.polygon([((x+s_*60)*SS,(y-48)*SS),((x+s_*60)*SS,(y-32)*SS),((x+s_*76)*SS,(y-40)*SS)],fill=al(RED,aa))
    if t>b[2][0]-0.2:
        ja=fade(t,b[2][0],1e9,0.5); p=pulse(t); d.rectangle([fx(2020)*SS-3*SS,(y-6)*SS,fx(2025)*SS+3*SS,(y+76)*SS],outline=al(TEXT,ja*(0.5+0.5*p)),width=3*SS)
        card(d,1280,480,580,170,"THE ONLY TRUE GUARD BAND","J · 2020–2025","5 MHz the FCC never sold · protects by accident",TEXT,ja)
        d.text((160*SS,800*SS),"one accident, zero design — everything else is masks",font=fnt(28),fill=al(TEXT,ja*fade(t,b[2][0]+5,1e9,0.5)))
    return out(im)
if __name__=="__main__": render_range(frame,"e3",float(sys.argv[1]),float(sys.argv[2]))
