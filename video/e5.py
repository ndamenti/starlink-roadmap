import sys; sys.path.insert(0,'/home/claude/v2'); from elib import *
B=lambda i: beat("e5",i)
ROWS=[("−120 · current SCS cap",21.5,19.6,BLUE),("−114 · floated in draft NPRM",17.9,17.0,AMBER),("−110.6 · SpaceX's PCS waiver level",15.1,14.6,RED)]
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(4)]; a=fade(t,0.2,1e9,0.5)
    head(d,t,"THE HARD CASE — 800 MHz AND PUBLIC SAFETY","assumes SpaceX acquires Grain's 800 MHz licenses (pending) · 851–874 MHz to scale",0.2,1e9)
    y=230; blocks=[(851,854,"NPSPAC","public safety RX",RED,0.45,0),(854,860,"INTERLEAVED","PS · B/ILT · SMR RX",RED,0.3,0.2),(860,861,"EXP","",RED,0.3,0.4),(861,862,"GB","1 MHz",None,0,0.6),(862,869,"ESMR 800 DL","SpaceX · pending",GREEN,0.5,0.8),(869,874,"CELLULAR A","AST SCS grant",DIM,0.25,1.0)]
    fx=band_strip(d,160,y,1600,blocks,849,876,a,t,0)
    if 2.5<t<b[1][0]: p=pulse(t); d.line([(fx(861)*SS,(y-10)*SS),(fx(862)*SS,(y-10)*SS)],fill=al(RED,0.5+0.5*p),width=5*SS); d.text((fx(861.5)*SS,(y-28)*SS),"1 MHz",font=mono(13,True),fill=al(RED,1),anchor="mm")
    if b[1][0]-0.2<t<b[2][0]:
        ca=fade(t,b[1][0],b[2][0],0.5); card(d,160,360,560,170,"47 CFR §90.672 · A RECEIVER TEST","−101 dBm · 20 dB","signal ≥ −101 dBm and C/(I+N) < 20 dB = unacceptable",RED,ca)
        d.text((160*SS,560*SS),"not a mask at the transmitter — a condition measured at the victim's radio",font=mono(15),fill=al(TEXT,ca*fade(t,b[1][0]+6,1e9,0.5)))
        for i,(ttl,v,c,dl) in enumerate([("STRICTLY LIABLE","the interferer",AMBER,9.0),("24 h","to respond",AMBER,11.0),("48 h","corrective action",AMBER,12.0),("SHUTDOWN","on a sworn 'clear and imminent danger' declaration",RED,13.5)]):
            aa=ca*fade(t,b[1][0]+dl,1e9,0.5); x=780+(i%2)*540; yy=360+(i//2)*170; card(d,x,yy,520,150,"§90.673–674" if i else "§90.673",v if i==0 else ttl,"" if i==0 else v,c,aa)
            if i==0: d.text(((x+28)*SS,(yy+110)*SS),ttl,font=mono(14),fill=al(TEXT,aa))
    if t>b[2][0]-0.2:
        ta=fade(t,b[2][0],1e9,0.5); im2,d2=canvas()
        head(d2,t,"RUN THE SATELLITE CAP THROUGH THE TEST (derived)","0 dBi portable at −101 dBm · full aggregate OOBE placed in one 25 kHz channel · receiver noise figure swept 5–8 dB",b[2][0],1e9)
        x0,y0=160,260; sc=lambda v:x0+v/30*1400
        d2.line([(sc(20)*SS,(y0-30)*SS),(sc(20)*SS,(y0+360)*SS)],fill=al(TEXT,ta*0.8),width=3*SS); d2.text((sc(20)*SS,(y0-46)*SS),"§90.672 criterion · 20 dB",font=mono(14,True),fill=al(TEXT,ta),anchor="mm")
        for i,(lab,v5,v8,c) in enumerate(ROWS):
            aa=ta*fade(t,b[2][0]+1.0+i*3.0,1e9,0.6); y=y0+i*120
            d2.text((x0*SS,(y-26)*SS),lab,font=mono(14,True),fill=al(c,aa))
            for j,(v,nf) in enumerate(((v5,"NF 5 dB"),(v8,"NF 8 dB"))):
                yy=y+j*36; ok=v>=20; col=GREEN if ok else RED; g=ease(clamp((t-(b[2][0]+1.2+i*3.0+j*0.5))/0.9))
                d2.rounded_rectangle([x0*SS,yy*SS,(x0+(sc(v)-x0)*g)*SS,(yy+28)*SS],4*SS,fill=al(col,aa*0.4),outline=al(col,aa),width=2*SS)
                d2.text(((sc(v)+14)*SS,(yy+14)*SS),f"{v:.1f} dB · {nf} · {'passes' if ok else 'FAILS'}",font=mono(14,True),fill=al(col,aa*g),anchor="lm")
        d2.text((160*SS,660*SS),"C/(I+N) at the public-safety radio",font=mono(13),fill=al(DIM,ta))
        d2.text((160*SS,720*SS),"the current cap passes by 0–1.5 dB · every relaxation on the table fails",font=fnt(28),fill=al(TEXT,ta*fade(t,b[2][0]+10,1e9,0.6)))
        d2.text((162*SS,770*SS),"screening arithmetic, not a coexistence study — the noise figures are assumptions, and the arithmetic is on the site",font=mono(14),fill=al(DIM,ta*fade(t,b[2][0]+12,1e9,0.6)))
        if t>b[3][0]-0.2:
            pa=fade(t,b[3][0],1e9,0.5); panel(d2,160,830,1760,990,pa)
            d2.text((196*SS,858*SS),"THE TEMPLATE EXISTS",font=mono(14),fill=al(GREEN,pa))
            d2.text((196*SS,888*SS),"FCC DA 26-391 (Apr 2026): AST's satellite grant on the Cellular band next door imports §§22.970–973 — the same public-safety protections — as a condition of the licence.",font=fnt(20),fill=al(TEXT,pa*fade(t,b[3][0]+5,1e9,0.5)))
            d2.text((196*SS,940*SS),"the strictest protection in the stack is the one SpaceX is buying into",font=fnt(22,True),fill=al(AMBER,pa*fade(t,b[3][0]+1.5,1e9,0.5)))
        im=Image.blend(im,im2,ta)
    return out(im)
if __name__=="__main__": render_range(frame,"e5",float(sys.argv[1]),float(sys.argv[2]))
