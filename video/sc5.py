import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s5",i)
TBL=[(650,28),(2000,44),(3000,50),(4000,54),(5000,57),(6000,60),(7000,62),(8000,63),(10000,66),(15000,70)]
def elev(f):
    if f<=650: return 28.0
    for (f0,e0),(f1,e1) in zip(TBL,TBL[1:]):
        if f<=f1: k=(math.log(f)-math.log(f0))/(math.log(f1)-math.log(f0)); return e0+k*(e1-e0)
    return 70.0
usable=lambda e: 20.0 if e>=60 else (40/3 if e>=42 else 20/3)
regime=lambda e: ("REUSE-1 · FULL POOL",GREEN,3) if e>=60 else (("TRANSITIONAL",AMBER,2) if e>=42 else ("REUSE-3 · RATIONED",RED,1))
mbps=lambda e: usable(e)*2.48*math.sin(math.radians(e))
dens,midx,STATES,CPATH,GW,GH,CELL=conus()
MW,MH=5140.0,2760.0; ISC=min(440/MW,240/MH)
def mkmap(ox,oy):
    P=lambda x,y:(SS*(ox+x*ISC),SS*(oy+y*ISC)); base=Image.new('RGBA',(W*SS,H*SS),(0,0,0,0)); bd=ImageDraw.Draw(base)
    for r in parse_path(CPATH,P): bd.polygon(r,fill=(14,22,38,255)); bd.line(r+[r[0]],fill=(150,170,200,170),width=2)
    return base
def fleet_at(t,b):
    if t<b[3][0]: return 650
    if t<b[4][0]: k=ease(clamp((t-b[3][0]-0.5)/9.5)); return math.exp(math.log(650)+k*(math.log(6200)-math.log(650)))
    if t<b[5][0]: k=ease(clamp((t-b[4][0]-0.5)/7.0)); return math.exp(math.log(6200)+k*(math.log(15000)-math.log(6200)))
    return 15000
rng=np.random.default_rng(3); SATS=rng.random((400,2))
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(6)]; f=fleet_at(t,b); e=elev(f); reg,rcol,lanes=regime(e); mb=mbps(e)
    head(d,t,"FLEET GROWTH CHANGES THE GEOMETRY","higher satellites  ->  rounder beams  ->  more spectrum per cell",0.2,1e9)
    gx,gy,gw=90*SS,640*SS,900*SS; d.line([(gx,gy),(gx+gw,gy)],fill=al(LINE,1),width=3*SS)
    px=gx+gw*0.30; R=430*SS; ang=math.radians(e); sx,sy=px+R*math.cos(ang),gy-R*math.sin(ang)
    half=min((8.9/math.sin(ang)**2)/8.9*26*SS,250*SS)
    d.polygon([(sx,sy),(px-half,gy),(px+half,gy)],fill=(91,168,255,42)); d.line([(sx,sy),(px,gy)],fill=BLUE+(190,),width=2*SS)
    d.arc([px-90*SS,gy-90*SS,px+90*SS,gy+90*SS],-e,0,fill=AMBER+(200,),width=2*SS); d.text((px+100*SS,gy-52*SS),f"{e:.0f}°",font=mono(22,True),fill=AMBER)
    sat_glyph(d,sx,sy,1.0); phone_glyph(d,px,gy-10*SS,1.0,0.45); d.text((gx,gy+26*SS),"GROUND",font=mono(13),fill=DIM)
    cx,cy=gx+gw*0.72,830*SS
    showmap=t>b[3][1]+0.3
    if not showmap:
        d.text((cx-150*SS,cy-155*SS),"BEAM FOOTPRINT · TOP-DOWN",font=mono(14),fill=DIM)
        along=8.9/math.sin(ang)**2; cross=8.9/math.sin(ang); sc=105*SS/max(along,8.9); a2,b2=along*sc,cross*sc
        d.ellipse([cx-a2/2,cy-b2/2,cx+a2/2,cy+b2/2],fill=(91,168,255,55),outline=BLUE+(190,),width=2*SS)
        d.text((cx-a2/2,cy+b2/2+14*SS),f"{along:.0f} km along  x  {cross:.0f} km across",font=mono(14),fill=BLUE)
        if e<60:
            for s in (-1,1): d.ellipse([cx+s*a2*0.92-a2/2,cy-b2/2,cx+s*a2*0.92+a2/2,cy+b2/2],outline=(214,69,69,110),width=2*SS)
            if t>b[1][0]+1: d.text((cx-150*SS,cy+b2/2+40*SS),"spilling into neighbouring cells",font=mono(14),fill=RED)
        else: d.text((cx-150*SS,cy+b2/2+40*SS),"isolated — neighbours reuse the same MHz",font=mono(14),fill=GREEN)
    else:
        ma=fade(t,b[3][1]+0.4,1e9,0.8); ox,oy=560,690; base=mkmap(ox,oy); 
        base.putalpha(base.split()[3].point(lambda v:int(v*ma))); im.paste(base,(0,0),base); d=ImageDraw.Draw(im,'RGBA')
        d.text((ox*SS,(oy-24)*SS),"CONUS · satellites overhead as the fleet thickens",font=mono(14),fill=al(DIM,ma))
        nsat=int(f/15000*330)  # ~330 over CONUS at 15k
        P=lambda x,y:(ox+x*ISC,oy+y*ISC)
        polys=parse_path(CPATH,lambda x,y:(x,y))
        from PIL import ImagePath
        for i in range(min(nsat,400)):
            X,Y=SATS[i,0]*MW,SATS[i,1]*MH
            # clip to landmass by point-in-polygon on the largest ring
            ring=max(polys,key=len); inside=False; n=len(ring); j=n-1
            for q in range(n):
                xi,yi=ring[q]; xj,yj=ring[j]
                if ((yi>Y)!=(yj>Y)) and (X<(xj-xi)*(Y-yi)/(yj-yi+1e-9)+xi): inside=not inside
                j=q
            if not inside: continue
            x,y=P(X,Y); s=2.2*SS; d.ellipse([x*SS-s,y*SS-s,x*SS+s,y*SS+s],fill=al(BLUE,ma*0.9))
    RX=1120*SS; panel(d,1120,150,1830,930)
    d.text((RX+40*SS,190*SS),"D2C FLEET",font=mono(15),fill=DIM); d.text((RX+40*SS,222*SS),f"{int(round(f/50)*50):,}",font=fnt(60,True),fill=TEXT)
    d.text((RX+40*SS,320*SS),"TYPICAL SERVING ELEVATION",font=mono(15),fill=DIM); d.text((RX+40*SS,352*SS),f"{e:.0f}°",font=fnt(48,True),fill=AMBER)
    d.text((RX+40*SS,440*SS),"SPECTRUM AVAILABLE TO YOUR CELL",font=mono(15),fill=DIM)
    for i in range(3):
        x0=RX+40*SS+i*175*SS; lit=i<lanes
        d.rounded_rectangle([x0,478*SS,x0+155*SS,522*SS],5*SS,fill=(rcol+(150,)) if lit else (30,42,62,255),outline=(rcol if lit else LINE),width=2*SS)
    d.text((RX+40*SS,540*SS),reg,font=mono(17,True),fill=rcol); d.text((RX+400*SS,540*SS),f"{usable(e):.1f} of 20 MHz",font=mono(17),fill=DIM)
    d.text((RX+40*SS,640*SS),"CELL DOWNLINK THROUGHPUT",font=mono(15),fill=DIM); col=GREEN if e>=60 else (AMBER if e>=42 else RED)
    d.text((RX+40*SS,672*SS),f"{mb:.0f}",font=fnt(96,True),fill=col); wpx=d.textlength(f"{mb:.0f}",font=fnt(96,True)); d.text((RX+52*SS+wpx,760*SS),"Mbps",font=mono(26),fill=DIM)
    d.text((RX+40*SS,830*SS),"shared by everyone in the cell",font=mono(15),fill=DIM)
    if b[4][0]-0.4<t<b[5][0]+0.3:
        a=fade(t,b[4][0]-0.3,b[5][0]+0.2,0.5); d.rounded_rectangle([RX+40*SS,868*SS,RX+660*SS,908*SS],6*SS,fill=(47,191,113,int(255*a*0.20)),outline=al(GREEN,a),width=2*SS)
        d.text((RX+56*SS,876*SS),"FULL REUSE:  TYPICAL CELL ~6,000 SATELLITES",font=mono(16,True),fill=al(GREEN,a))
    if t>=b[5][0]-0.3:
        a=fade(t,b[5][0]-0.2,1e9,0.5); d.rounded_rectangle([RX+40*SS,868*SS,RX+700*SS,908*SS],6*SS,fill=(47,191,113,int(255*a*0.20)),outline=al(GREEN,a),width=2*SS)
        d.text((RX+56*SS,876*SS),"EVERY CELL, WORST CASE:  ~15,000 SATELLITES",font=mono(16,True),fill=al(GREEN,a))
    if t>b[5][0]+4.0: d.text((90*SS,980*SS),"the advertised 50 Mbps is an end-state, not a launch-day figure",font=fnt(22),fill=al(TEXT,fade(t,b[5][0]+4.2,1e9,0.6)))
    return out(im)
if __name__=="__main__": render_range(frame,"s5",float(sys.argv[1]),float(sys.argv[2]))
