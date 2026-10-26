import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s7",i)
dens,midx,STATES,CPATH,GW,GH,CELL=conus()
MW,MH=5140.0,2760.0; MSC=min(1150/MW,640/MH); OX=64; OY=200
def P2(x,y): return (SS*(OX+x*MSC),SS*(OY+y*MSC))
base=Image.new('RGBA',(W*SS,H*SS),(0,0,0,0)); bd=ImageDraw.Draw(base)
for st in STATES:
    for r in parse_path(st['d'],P2): bd.line(r+[r[0]],fill=(138,152,176,80),width=2)
for r in parse_path(CPATH,P2): bd.line(r+[r[0]],fill=(150,170,200,170),width=3)
DCOL=[(20,42,69),(31,75,122),(61,122,181),(230,179,87),(230,126,76),(214,69,69)]
SCOL=[(214,69,69),(230,126,76),(230,179,87),(168,201,76),(47,191,113)]
land=dens>0; servDens=1.2
frac_sat=np.where(land,np.minimum(1.0,servDens/np.maximum(dens,1e-9)),0)
def rgbmap(mode,nmetro=0):
    o=np.zeros((GH,GW,3))
    for j in range(GH):
        for i in range(GW):
            if dens[j,i]<0: continue
            if mode=='d':
                v=dens[j,i]*2.59; k=0 if v<1 else 1 if v<10 else 2 if v<50 else 3 if v<250 else 4 if v<1000 else 5; o[j,i]=DCOL[k]
            else:
                f=0.9 if (nmetro and midx[j,i]<nmetro) else frac_sat[j,i]; k=0 if f<0.05 else 1 if f<0.2 else 2 if f<0.5 else 3 if f<0.999 else 4; o[j,i]=SCOL[k]
    return o
D_RGB=rgbmap('d'); S_RGB=rgbmap('s'); H10=rgbmap('s',10); cw=CELL*MSC*SS
metro=(midx<10)&land
def cells(rgb,a):
    img=Image.fromarray(rgb.astype('uint8'),'RGB').resize((int(GW*cw),int(GH*cw)),Image.NEAREST)
    m=Image.fromarray((np.where(land,a,0)*255).astype('uint8'),'L').resize((int(GW*cw),int(GH*cw)),Image.NEAREST); img.putalpha(m); return img
def tower(d,x,y,h,c,a):
    d.line([(x*SS,y*SS),((x-h*0.22)*SS,(y+h)*SS)],fill=al(c,a),width=3*SS); d.line([(x*SS,y*SS),((x+h*0.22)*SS,(y+h)*SS)],fill=al(c,a),width=3*SS)
    for k in (0.35,0.65,0.95): d.line([((x-h*0.22*k)*SS,(y+h*k)*SS),((x+h*0.22*k)*SS,(y+h*k)*SS)],fill=al(c,a),width=2*SS)
    d.line([((x-10)*SS,(y-8)*SS),((x+10)*SS,(y-8)*SS)],fill=al(c,a),width=4*SS)
def spec_blocks(d,x,y,a,t,b):
    # owned ground spectrum: H-block 5/5 + 800 2x7 pending
    d.text((x*SS,y*SS),"OWNED GROUND SPECTRUM",font=mono(14),fill=al(DIM,a))
    items=[("H-block",5,"5 / 5 MHz · owned",BLUE,b[2][0]+2.0,False),("800 MHz",14,"2×7 MHz · pending Grain",GREEN,b[2][0]+5.0,True)]
    xx=x
    for lab,w,sub,c,t0,pend in items:
        aa=a*fade(t,t0,1e9,0.6); ww=w*24
        if pend:
            d.rectangle([xx*SS,(y+30)*SS,(xx+ww)*SS,(y+80)*SS],fill=al(c,aa*0.22),outline=al(c,aa),width=2*SS)
            for k in range(0,ww+50,10): d.line([(max(xx,xx+k-50)*SS,(y+80 if k>=50 else y+30+(50-k))*SS),(min(xx+k,xx+ww)*SS,(y+30 if k<=ww else y+30+(k-ww))*SS)],fill=al(c,aa*0.5),width=1*SS)
        else: d.rounded_rectangle([xx*SS,(y+30)*SS,(xx+ww)*SS,(y+80)*SS],4*SS,fill=al(c,aa*0.45),outline=al(c,aa),width=2*SS)
        d.text((xx*SS,(y+90)*SS),lab,font=mono(15,True),fill=al(c,aa)); d.text((xx*SS,(y+112)*SS),sub,font=mono(13),fill=al(DIM,aa)); xx+=ww+30
    d.text((x*SS,(y+150)*SS),"= a licensed floor · thin, but owned · nobody can turn it off",font=mono(15,True),fill=al(TEXT,a*fade(t,b[3][0]+0.5,1e9,0.6)))
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(8)]
    # ---------------- phase A: the map (beats 0-1, map persists to beat 5) ----------------
    if t<b[6][0]+0.5:
        a=fade(t,0.2,b[6][0]+0.4,0.6)
        if t<b[1][0]+1.0: rgb,ttl,sub=D_RGB,"WHERE PEOPLE ACTUALLY ARE","census · population density"
        elif t<b[5][0]: rgb,ttl,sub=S_RGB,"WHAT ORBIT ALONE CAN CARRY","share of local population served · satellite only · company's own numbers"
        else:
            k=ease(clamp((t-b[5][0]-0.5)/2.4)); rgb=S_RGB*(1-k)+H10*k; ttl,sub="ADD THE GROUND LAYER — TOP 10 METROS","~2.1M mixed rooftop / pole small cells · 800 MHz floor on the macro grid"
        # the map shrinks to the left once the spectrum story starts (beat 2)
        head(d,t,ttl,sub,0.2,1e9)
        la=np.where(land,ease(clamp((t-0.4)/1.2)),0)
        layer=cells(rgb,la*a); im.paste(layer,(int(OX*SS),int(OY*SS)),layer); bb=base.copy(); bb.putalpha(bb.split()[3].point(lambda v:int(v*a))); im.paste(bb,(0,0),bb); d=ImageDraw.Draw(im,'RGBA')
        # "every city is red" pulse
        if b[1][0]+7.5<t<b[2][0]:
            p=pulse(t,0.9); 
            for j in range(GH):
                for i in range(GW):
                    if metro[j,i]: x0=OX*SS+i*cw; y0=OY*SS+j*cw; d.rectangle([x0,y0,x0+cw,y0+cw],outline=al(RED,0.9*p),width=2*SS)
        RX=1300
        if t>b[1][0]+0.7:
            pa=fade(t,b[1][0]+0.8,1e9,0.5)
            if t<b[5][0]: val=9.0e6*ease(clamp((t-b[1][0]-1.0)/1.6)); col=AMBER; pct=val/336e6*100
            else: val=9.0e6+(94e6-9.0e6)*ease(clamp((t-b[5][0]-0.5)/2.6)); col=GREEN; pct=val/336e6*100
            d.text((RX*SS,210*SS),"PEOPLE THE NETWORK CAN CARRY",font=mono(14),fill=al(DIM,pa))
            d.text((RX*SS,242*SS),f"{val/1e6:.0f}M",font=fnt(72,True),fill=al(col,pa))
            d.text((RX*SS,340*SS),f"of 336M  ·  {pct:.1f}%" if val<20e6 else f"of 336M  ·  {pct:.0f}%",font=mono(20),fill=al(DIM,pa))
        if b[1][0]+3.0<t<b[2][0]:
            aa=fade(t,b[1][0]+3.2,b[2][0]-0.1,0.5)
            d.text((RX*SS,430*SS),"LAND AREA FULLY GREEN",font=mono(14),fill=al(DIM,aa)); d.text((RX*SS,462*SS),"21%",font=fnt(46,True),fill=al(TEXT,aa))
            d.text((RX*SS,530*SS),"a fifth of the land — almost none of the people",font=mono(15),fill=al(DIM,aa))
            d.text((RX*SS,580*SS),"every city is red",font=mono(17,True),fill=al(RED,fade(t,b[1][0]+7.3,b[2][0]-0.1,0.4)))
        # beats 2-3: owned spectrum + towers over the map's right side
        if b[2][0]-0.3<t<b[5][0]:
            sa=fade(t,b[2][0]-0.2,b[5][0]-0.1,0.5); panel(d,1260,400,1870,790,sa); spec_blocks(d,1300,430,sa,t,b)
            if t>b[3][0]-0.3:
                ta=sa*fade(t,b[3][0]-0.2,1e9,0.6)
                for i in range(3): tower(d,1330+i*110,640,100,GREEN,ta*fade(t,b[3][0]+i*0.5,1e9,0.5))
                d.text((1660*SS,690*SS),"macro\ntowers",font=mono(14),fill=al(DIM,ta))
        # beat 4: CBRS
        if b[4][0]-0.3<t<b[6][0]+0.5:
            ca=fade(t,b[4][0]-0.2,b[6][0]+0.4,0.5); panel(d,1260,400 if t<b[5][0] else 400,1870,790 if t<b[5][0] else 790,ca) if t>=b[5][0]-0.2 else None
            if t>=b[5][0]-0.2 or True:
                d.rectangle([1260*SS,400*SS,1870*SS,790*SS],fill=al(PANEL,ca)) 
                d.rounded_rectangle([1260*SS,400*SS,1870*SS,790*SS],10*SS,outline=al(LINE,ca),width=2*SS)
                d.text((1300*SS,430*SS),"CAPACITY · CBRS 3.5 GHz",font=mono(14),fill=al(PURPLE,ca))
                for j,r in enumerate(["shared spectrum · not SpaceX's","priority access, not exclusivity","a referee (SAS) can shuffle the channels","never the coverage anchor"]):
                    d.text((1300*SS,(470+j*48)*SS),"·  "+r,font=fnt(20),fill=al(TEXT,ca*fade(t,b[4][0]+0.6+j*1.1,1e9,0.5)))
                if t>b[5][0]-0.3:
                    ha=ca*fade(t,b[5][0]-0.2,1e9,0.5)
                    boxes=2.1e6*ease(clamp((t-b[5][0]-0.3)/2.2))
                    d.text((1300*SS,680*SS),"SMALL CELLS · TOP 10 METROS",font=mono(14),fill=al(DIM,ha)); d.text((1300*SS,708*SS),f"{boxes/1e6:.1f}M",font=fnt(48,True),fill=al(BLUE,ha))
                    d.text((1480*SS,730*SS),"rooftop + pole · on CBRS, over the 800 floor",font=mono(13),fill=al(DIM,ha))
    # ---------------- phase B: with / without CBRS (beat 6) ----------------
    if t>b[6][0]-0.4:
        a=fade(t,b[6][0]-0.3,b[7][0]+0.4,0.6); im2,d2=canvas()
        head(d2,t,"THE CITY LAYER, WITH AND WITHOUT CBRS","same ~2.1M boxes · same 94M reached · the difference is headroom",b[6][0]-0.3,b[7][0]+0.4)
        for i,(ttl,c,reach,hr,note,t0) in enumerate([
            ("WITH CBRS  ·  H-block 5/5 + 15 MHz shared",GREEN,"94M","×3.6","throughput ceiling ~339M subscribers  ·  extra MHz buys margin",b[6][0]-0.2),
            ("OWNED ONLY  ·  H-block 5/5, no CBRS",RED,"94M","×1.1","ceiling ~106M vs 95M metro population  ·  at its limit — any growth chokes",b[6][0]+1.6)]):
            x=120+i*880; aa=a*fade(t,t0,1e9,0.6); panel(d2,x,200,x+800,720,aa)
            d2.rounded_rectangle([x*SS,200*SS,(x+8)*SS,720*SS],3*SS,fill=al(c,aa))
            d2.text(((x+40)*SS,235*SS),ttl,font=mono(15,True),fill=al(c,aa))
            stat(d2,x+40,300,"PEOPLE REACHED (orbit + ground)",reach,TEXT,56,aa,"of 336M · 28%")
            stat(d2,x+40,440,"CAPACITY HEADROOM",hr,c,56,aa*fade(t,t0+1.5,1e9,0.6))
            d2.text(((x+40)*SS,600*SS),note,font=mono(14),fill=al(DIM,aa*fade(t,t0+2.5,1e9,0.6)))
            # headroom bar
            g=ease(clamp((t-t0-1.2)/1.0)); wmax=560; wv=wmax*min(float(hr[1:]),3.6)/3.6*g
            d2.rounded_rectangle([(x+40)*SS,650*SS,(x+40+wv)*SS,680*SS],4*SS,fill=al(c,aa*0.5),outline=al(c,aa),width=2*SS)
            d2.line([((x+40+wmax/3.6)*SS,640*SS),((x+40+wmax/3.6)*SS,690*SS)],fill=al(TEXT,aa*0.7),width=2*SS); d2.text(((x+40+wmax/3.6+8)*SS,692*SS),"×1 = ceiling",font=mono(12),fill=al(DIM,aa))
        d2.text((120*SS,800*SS),"the floor stands either way — the capacity doesn't",font=fnt(26),fill=al(TEXT,a*fade(t,b[6][0]+6.5,1e9,0.6)))
        d2.text((120*SS,850*SS),"the only exclusive mid-band on the table: the Upper C-band auction · July 2027",font=mono(17),fill=al(AMBER,a*fade(t,b[6][0]+11.0,1e9,0.6)))
        im=Image.blend(im,im2,a)
    # ---------------- phase C: the towers (beat 7) ----------------
    if t>b[7][0]-0.4:
        a=fade(t,b[7][0]-0.3,1e9,0.6); im3,d3=canvas()
        head(d3,t,"REMEMBER — NOT A SINGLE CELL TOWER?","Bloomberg, Oct 22 2026 · reported · nothing signed",b[7][0]-0.3,1e9)
        sa=a*fade(t,b[7][0]+0.2,1e9,0.5)
        d3.text((90*SS,300*SS),"without building a single cell tower",font=fnt(40),fill=al(DIM,sa))
        wln=d3.textlength("without building a single cell tower",font=fnt(40)); k=ease(clamp((t-b[7][0]-1.4)/0.8))
        d3.line([(90*SS,324*SS),(90*SS+wln*k,324*SS)],fill=al(RED,sa),width=4*SS)
        ta=a*fade(t,b[7][0]+2.6,1e9,0.6); n=int(80000*ease(clamp((t-b[7][0]-2.6)/2.4)))
        d3.text((90*SS,420*SS),f"{n:,}",font=fnt(120,True),fill=al(GREEN,ta)); d3.text((90*SS,570*SS),"tower sites reportedly in talks · about half the US tower base · Crown Castle et al.",font=mono(18),fill=al(TEXT,ta))
        rng=np.random.default_rng(9); cnt=int(60*ease(clamp((t-b[7][0]-2.6)/4.0)))
        for i in range(cnt):
            x=1180+rng.uniform(0,640); y=300+rng.uniform(0,420); tower(d3,x,y,40,GREEN,ta*0.8)
        d3.text((90*SS,700*SS),"nothing signed",font=mono(22,True),fill=al(AMBER,a*fade(t,b[7][0]+7.0,1e9,0.5)))
        d3.text((90*SS,780*SS),"that's what an 800 MHz floor looks like when you build it",font=fnt(30),fill=al(TEXT,a*fade(t,b[7][0]+8.6,1e9,0.6)))
        d3.text((94*SS,830*SS),"DISH–Crown Castle 2020 (20,000 towers) is the quarter-scale precedent",font=mono(15),fill=al(DIM,a*fade(t,b[7][0]+10.0,1e9,0.6)))
        im=Image.blend(im,im3,a)
    return out(im)
if __name__=="__main__": render_range(frame,"s7",float(sys.argv[1]),float(sys.argv[2]))
