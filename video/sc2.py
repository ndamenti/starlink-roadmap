import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s2",i)
BLOCKS=[(1695,1710,"AWS-3 UL","15",PURPLE),(1915,1920,"H UL","5",BLUE),(1995,2000,"H DL","5",BLUE),(2000,2020,"AWS-4 low","20",AMBER),(2180,2200,"AWS-4 high","20",AMBER)]
ESMR=[(817,824,"800 UL","7",GREEN),(862,869,"800 DL","7",GREEN)]
# broken axis: 800-880 on the left segment, 1680-2215 on the right
def fx(f):
    if f<1000: return 130+(f-800)/(880-800)*330
    return 560+(f-1680)/(2215-1680)*1230
def hatch(d,x0,y0,x1,y1,c,a,step=10):
    d.rectangle([x0,y0,x1,y1],fill=al(c,a*0.22),outline=al(c,a),width=2*SS)
    h=y1-y0; x=x0-h
    while x<x1:
        xa,xb=x,x+h  # line from (xa,y1) to (xb,y0), clip to [x0,x1]
        la,lb=max(xa,x0),min(xb,x1)
        if lb>la:
            ya=y1-(la-xa); yb=y1-(lb-xa)
            d.line([(la,ya),(lb,yb)],fill=al(c,a*0.5),width=1*SS)
        x+=step*SS
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(8)]
    ba=fade(t,b[0][0]-0.4,b[3][0]+0.6,0.6)
    if ba>0.01:
        two=t>b[1][0]-0.3
        head(d,t,"WHAT THE MONEY BOUGHT" if two else "WHAT NINETEEN BILLION DOLLARS BOUGHT","65 MHz owned (EchoStar) · + 14 MHz low band pending (Grain, Oct 2026) · broken axis" if two else "65 MHz of exclusive spectrum · EchoStar transaction",b[0][0]-0.3,b[3][0]+0.4)
        y=420
        d.line([(fx(1680)*SS,(y+70)*SS),(fx(2215)*SS,(y+70)*SS)],fill=al(LINE,ba),width=2*SS)
        for f in (1700,1800,1900,2000,2100,2200): d.text((fx(f)*SS-14*SS,(y+120)*SS),str(f),font=mono(12),fill=al(DIM,ba*0.7))
        for i,(lo,hi,nm,mhz,c) in enumerate(BLOCKS):
            ap=ba*ease(clamp((t-(b[0][0]+0.6+i*0.45))/0.7))
            if ap<=0.01: continue
            x0,x1=fx(lo)*SS,fx(hi)*SS; wpx=max(x1-x0,26*SS)
            d.rounded_rectangle([x0,y*SS,x0+wpx,(y+70)*SS],4*SS,fill=al(c,ap*0.45),outline=al(c,ap),width=2*SS)
            d.text((x0,(y+82)*SS),f"{lo}-{hi}",font=mono(13),fill=al(DIM,ap)); d.text((x0,(y-26)*SS),nm,font=mono(14,True),fill=al(c,ap)); d.text((x0,(y+100)*SS),mhz+" MHz",font=mono(13),fill=al(c,ap*0.8))
        tot=ba*ease(clamp((t-(b[0][0]+3.0))/0.8))
        if not two:
            d.text((560*SS,600*SS),"65 MHz owned",font=fnt(46,True),fill=al(TEXT,tot))
            d.text((562*SS,668*SS),"exclusive lanes on an invisible highway",font=mono(18),fill=al(DIM,tot))
        else:
            ga=ba*fade(t,b[1][0]-0.2,1e9,0.6)
            d.line([(fx(800)*SS,(y+70)*SS),(fx(880)*SS,(y+70)*SS)],fill=al(LINE,ga),width=2*SS)
            # axis break marks
            for xx in (fx(880)+14,fx(1680)-14): d.line([((xx-6)*SS,(y+58)*SS),((xx+6)*SS,(y+82)*SS)],fill=al(DIM,ga),width=2*SS)
            for f in (820,850,870): d.text((fx(f)*SS-12*SS,(y+120)*SS),str(f),font=mono(12),fill=al(DIM,ga*0.7))
            for i,(lo,hi,nm,mhz,c) in enumerate(ESMR):
                ap=ga*ease(clamp((t-(b[1][0]+0.8+i*0.5))/0.7))
                x0,x1=fx(lo)*SS,fx(hi)*SS
                hatch(d,x0,y*SS,x1,(y+70)*SS,c,ap)
                d.text((x0,(y+82)*SS),f"{lo}-{hi}",font=mono(13),fill=al(DIM,ap)); d.text((x0,(y-26)*SS),nm,font=mono(14,True),fill=al(c,ap)); d.text((x0,(y+100)*SS),mhz+" MHz · pending",font=mono(13),fill=al(c,ap*0.8))
            d.text((130*SS,600*SS),"65",font=fnt(46,True),fill=al(TEXT,ga))
            w=d.textlength("65 ",font=fnt(46,True))
            d.text((130*SS+w,600*SS),"→ 79 MHz",font=fnt(46,True),fill=al(GREEN,ga*fade(t,b[1][0]+5.5,1e9,0.6)))
            d.text((132*SS,668*SS),"~$8B reported for the low band · FCC consent pending · satellites not yet allowed in the band",font=mono(16),fill=al(DIM,ga*fade(t,b[1][0]+2.5,1e9,0.6)))
    if b[2][0]-0.4<t<b[3][0]+0.4:
        a=fade(t,b[2][0]-0.3,b[3][0]+0.2,0.5)
        for i,(lab,sub,c,up) in enumerate([("COUNTRYSIDE","satellite  ->  phone",AMBER,True),("CITY","rooftop small cell  ->  phone",BLUE,False)]):
            x=200+i*900; panel(d,x,720,x+700,960,a)
            d.text((x*SS+30*SS,745*SS),lab,font=mono(16,True),fill=al(c,a)); d.text((x*SS+30*SS,790*SS),sub,font=fnt(24),fill=al(TEXT,a)); d.text((x*SS+30*SS,850*SS),"same band · different job",font=mono(15),fill=al(DIM,a))
            ax=x+600
            if up: d.line([(ax*SS,930*SS),(ax*SS,780*SS)],fill=al(c,a),width=3*SS); d.polygon([(ax*SS-9*SS,790*SS),(ax*SS+9*SS,790*SS),(ax*SS,768*SS)],fill=al(c,a))
            else: d.line([(ax*SS-70*SS,860*SS),(ax*SS+40*SS,860*SS)],fill=al(c,a),width=3*SS); d.polygon([(ax*SS+30*SS,851*SS),(ax*SS+30*SS,869*SS),(ax*SS+52*SS,860*SS)],fill=al(c,a))
    if t>b[3][0]-0.5:
        a=fade(t,b[3][0]-0.4,b[7][0]+0.3,0.6)
        head(d,t,"WHY CITIES ARE A DIFFERENT PROBLEM","one beam · ~8.9 km across · about 62 square kilometres",b[3][0]-0.3,b[7][0]+0.2)
        for i,(lab,ppl,col,dots) in enumerate([("FARM COUNTRY",150,GREEN,60),("A CITY",250000,RED,900)]):
            cx=460+i*980; cy=520; aa=a*ease(clamp((t-(b[4][0]-0.2+i*1.1))/0.8))
            if aa<=0.01: continue
            d.ellipse([(cx-190)*SS,(cy-190)*SS,(cx+190)*SS,(cy+190)*SS],fill=al(BLUE,aa*0.10),outline=al(BLUE,aa*0.55),width=2*SS)
            k=ease(clamp((t-(b[4][0]+0.4+i*1.1))/2.2)); n=int(dots*k); rng=np.random.default_rng(7+i); pts=rng.random((dots,2))
            for j in range(n):
                ang=2*math.pi*pts[j,0]; r=190*math.sqrt(pts[j,1]); x,y=cx+r*math.cos(ang),cy+r*math.sin(ang); s=(2.6 if i==0 else 1.5)*SS
                d.ellipse([x*SS-s,y*SS-s,x*SS+s,y*SS+s],fill=al(col,aa*0.9))
            if i==1 and b[5][0]<t<b[7][0]:
                p=pulse(t); d.ellipse([(cx-196-4*p)*SS,(cy-196-4*p)*SS,(cx+196+4*p)*SS,(cy+196+4*p)*SS],outline=al(RED,aa*0.8*p),width=3*SS)
            d.text(((cx-190)*SS,(cy+205)*SS),lab,font=mono(16,True),fill=al(col,aa))
            d.text(((cx-190)*SS,(cy+235)*SS),f"~{count(ppl*k)} people under one beam",font=mono(15),fill=al(DIM,aa))
            sh=50.0/max(ppl*k,1)
            d.text(((cx-190)*SS,(cy+262)*SS),f"50 Mbps shared  ->  {sh*1000:.0f} kbps each" if sh<0.1 else f"50 Mbps shared  ->  {sh:.2f} Mbps each",font=mono(15,True),fill=al(col,aa*fade(t,b[4][0]+2.0+i*1.1,1e9,0.5)))
        if t>b[5][0]-0.3:
            ca=fade(t,b[5][0]-0.2,b[7][0]+0.2,0.5); panel(d,470,850,1450,1010,ca)
            d.text((505*SS,872*SS),"SATELLITE CAPACITY CEILING",font=mono(15),fill=al(DIM,ca)); d.text((505*SS,898*SS),"~1",font=fnt(46,True),fill=al(AMBER,ca)); d.text((580*SS,932*SS),"subscriber per km²",font=mono(17),fill=al(DIM,ca))
            d.text((880*SS,898*SS),"urban density runs 100–1,000× higher",font=mono(16),fill=al(RED,ca*fade(t,b[5][0]+1.6,1e9,0.5)))
            d.text((880*SS,932*SS),"no fleet size fixes that",font=mono(16,True),fill=al(RED,ca*fade(t,b[6][0]+0.4,1e9,0.5)))
    if t>b[7][0]-0.4:
        a=fade(t,b[7][0]-0.3,1e9,0.6); im2,d2=canvas()
        head(d2,t,"SO THE CITIES NEED A GROUND LAYER","and the band can only be handed over once that layer exists",b[7][0]-0.3,1e9)
        for i,(n,s,c) in enumerate([("1","build the ground layer",BLUE),("2","subscribers arrive",BLUE),("3","satellite hands over the band",AMBER)]):
            aa=a*ease(clamp((t-(b[7][0]+0.3+i*1.2))/0.7)); x=180+i*580; panel(d2,x,400,x+480,540,aa)
            d2.text((x*SS+30*SS,425*SS),n,font=fnt(30,True),fill=al(c,aa)); d2.text((x*SS+30*SS,480*SS),s,font=fnt(22),fill=al(TEXT,aa))
            if i<2: ax=x+500; d2.polygon([(ax*SS,462*SS),(ax*SS+22*SS,470*SS),(ax*SS,478*SS)],fill=al(DIM,aa))
        d2.text((180*SS,700*SS),"the handover isn't a trick — it's a sequence",font=fnt(28),fill=al(TEXT,a*fade(t,b[7][0]+4.0,1e9,0.6)))
        im=Image.blend(im,im2,a)
    return out(im)
if __name__=="__main__": render_range(frame,"s2",float(sys.argv[1]),float(sys.argv[2]))
