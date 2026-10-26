import sys, math; sys.path.insert(0,'/home/claude/v2'); from elib import *
B=lambda i: beat("e4",i)
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(3)]; a=fade(t,0.2,1e9,0.5)
    head(d,t,"SATELLITES ARE DIFFERENT","a beam cannot stop at a line on a map · so the rule moves to the ground",0.2,1e9)
    # ground with two licence areas, beam cone from above spilling across the boundary
    gy=700; d.line([(120*SS,gy*SS),(1100*SS,gy*SS)],fill=al(LINE,a),width=3*SS)
    d.rectangle([120*SS,(gy+4)*SS,610*SS,(gy+40)*SS],fill=al(AMBER,a*0.35)); d.rectangle([610*SS,(gy+4)*SS,1100*SS,(gy+40)*SS],fill=al(BLUE,a*0.35))
    d.text((365*SS,(gy+22)*SS),"SpaceX's block / area",font=mono(13),fill=al(TEXT,a),anchor="mm"); d.text((855*SS,(gy+22)*SS),"neighbor's",font=mono(13),fill=al(TEXT,a),anchor="mm")
    d.line([(610*SS,(gy-30)*SS),(610*SS,(gy+60)*SS)],fill=al(TEXT,a*0.8),width=3*SS); d.text((610*SS,(gy+80)*SS),"license boundary",font=mono(13),fill=al(TEXT,a),anchor="mm")
    sx,sy=480,230; sat_glyph(d,sx*SS,sy*SS,a)
    k=ease(clamp((t-0.8)/2.0)); half=60+300*k
    d.polygon([(sx*SS,(sy+14)*SS),((sx-half*0.6)*SS,gy*SS),((sx+half)*SS,gy*SS)],fill=al(AMBER,a*0.16)); d.line([(sx*SS,(sy+14)*SS),((sx+half)*SS,gy*SS)],fill=al(AMBER,a*0.7),width=2*SS); d.line([(sx*SS,(sy+14)*SS),((sx-half*0.6)*SS,gy*SS)],fill=al(AMBER,a*0.7),width=2*SS)
    if k>0.9: d.text((850*SS,(gy-60)*SS),"spill — unavoidable",font=mono(14,True),fill=al(RED,a*fade(t,3.2,1e9,0.5)),anchor="mm")
    if t>b[1][0]-0.2:
        ca=fade(t,b[1][0],1e9,0.5); card(d,1180,200,700,190,"THE SCS CAP · 47 CFR §25.202(k)(1)","−120 dBW/m²/MHz","aggregate · all satellites · outside the band",BLUE,ca)
        for i,(txt,dl) in enumerate([("measured 1.5 m above the ground — at phone height","3.5"),("totaled across the ENTIRE fleet, not per satellite","6.5"),("a ceiling on interference DELIVERED, not a promise at the transmitter","9.0")]):
            d.text((1180*SS,(420+i*40)*SS),"·  "+txt,font=fnt(19),fill=al(TEXT,ca*fade(t,b[1][0]+float(dl),1e9,0.5)))
        # pfd meter at 1.5m
        ma=ca*fade(t,b[1][0]+3.5,1e9,0.5); mx=760; d.line([(mx*SS,(gy-30)*SS),(mx*SS,gy*SS)],fill=al(BLUE,ma),width=3*SS); d.ellipse([(mx-8)*SS,(gy-38)*SS,(mx+8)*SS,(gy-22)*SS],fill=al(BLUE,ma)); d.text(((mx+16)*SS,(gy-34)*SS),"1.5 m",font=mono(12),fill=al(BLUE,ma))
    if t>b[2][0]-0.2:
        ta=fade(t,b[2][0],1e9,0.5); im2,d2=canvas()
        head(d2,t,"WHAT −120 dBW/m²/MHz MEANS AT THE RADIO","power flux on the ground  →  power in a phone-sized antenna  →  compared with the receiver's own noise (derived)",b[2][0],1e9)
        steps=[("−120 dBW/m²/MHz","the cap on the ground",BLUE,0.3),("× phone antenna (0 dBi, λ²/4π)","−20 dB·m² at 856 MHz",DIM,2.0),("÷ 1 MHz → 25 kHz channel","−16 dB",DIM,3.5),("= −126 dBm per 25 kHz","interference arriving in the receiver",AMBER,5.0)]
        for i,(v,s_,c,dl) in enumerate(steps):
            aa=ta*fade(t,b[2][0]+dl,1e9,0.5); y=220+i*110; d2.text((120*SS,y*SS),v,font=fnt(34,True),fill=al(c,aa)); d2.text((122*SS,(y+48)*SS),s_,font=mono(14),fill=al(DIM,aa))
        # bars: interference vs noise floor
        ba=ta*fade(t,b[2][0]+7.5,1e9,0.6); x0,y0=1050,300; d2.text((x0*SS,(y0-40)*SS),"dBm in a 25 kHz channel  (higher = louder)",font=mono(13),fill=al(DIM,ba))
        for i,(lab,v,c) in enumerate([("satellite interference, worst case",-126.1,AMBER),("receiver thermal noise kTB + 5 dB NF",-125.0,DIM),("public-safety radio signal at the §90.672 threshold",-101.0,GREEN)]):
            y=y0+i*110; w=(v+140)/40*700; d2.rounded_rectangle([x0*SS,y*SS,(x0+w)*SS,(y+44)*SS],5*SS,fill=al(c,ba*0.45),outline=al(c,ba),width=2*SS)
            d2.text((x0*SS,(y-22)*SS),lab,font=mono(13),fill=al(TEXT,ba)); d2.text(((x0+w+14)*SS,(y+10)*SS),f"{v:.0f} dBm",font=mono(16,True),fill=al(c,ba))
        d2.text((120*SS,760*SS),"the cap is pinned to the level where the satellite is no louder than the noise the radio already lives with",font=fnt(26),fill=al(TEXT,ta*fade(t,b[2][0]+11,1e9,0.6)))
        im=Image.blend(im,im2,ta)
    return out(im)
if __name__=="__main__": render_range(frame,"e4",float(sys.argv[1]),float(sys.argv[2]))
