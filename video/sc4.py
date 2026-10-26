import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s4",i)
def hexlat(n,R):
    a=R*math.sqrt(2*math.pi/(max(n,1)*math.sqrt(3))); rows=int(R/(a*math.sqrt(3)/2))+2; cols=int(R/a)+2; pts=[]
    for j in range(-rows,rows+1):
        for i in range(-cols,cols+1):
            x=(i+(0.5 if j%2 else 0))*a; y=j*a*math.sqrt(3)/2; pts.append((x,y,x*x+y*y))
    pts.sort(key=lambda p:p[2]); return [(x,y) for x,y,_ in pts[:n]]
LAT=hexlat(700,300)
# ---- strip machine (Panel 6 redrawn): 5 strips · 83 beams · 7 handsets · x10 ----
NSTRIP,NBEAM,NHAND,SPEED=5,83,7,10
STRIPC=[AMBER,GREEN,BLUE,PURPLE,(236,112,99)]
rng=np.random.default_rng(42); HANDS=[(rng.uniform(0.08,0.92),rng.uniform(0.12,0.88)) for _ in range(NHAND)]
def strip_machine(d,t0,t,x,y,w,h,a):
    # satellites stream "south" (down) across an Earth-fixed grid; each strip's beam cluster colours the ground it lights
    panel(d,x,y,x+w,y+h,a)
    d.text(((x+20)*SS,(y+16)*SS),"THE STRIP MACHINE · 5 strips · 83 beams · 7 handsets · ×10",font=mono(13,True),fill=al(TEXT,a))
    d.text(((x+20)*SS,(y+38)*SS),"handover = colour change",font=mono(13),fill=al(AMBER,a))
    gx,gy,gw,gh=x+20,y+66,w-40,h-86
    # fixed ground grid
    for i in range(0,13):
        xx=gx+gw*i/12; d.line([(xx*SS,gy*SS),(xx*SS,(gy+gh)*SS)],fill=al(LINE,a*0.9),width=1*SS)
    for j in range(0,8):
        yy=gy+gh*j/7; d.line([(gx*SS,yy*SS),((gx+gw)*SS,yy*SS)],fill=al(LINE,a*0.9),width=1*SS)
    # strips: each satellite's footprint is a band of height fh moving down at SPEED; period so handover every ~7 s screen time
    per=7.0; fh=gh/NSTRIP*1.0
    owner=[None]*NHAND
    for s in range(NSTRIP):
        c=STRIPC[s]; ph=(t-t0)/per+s/NSTRIP
        cy=gy+((ph*gh*1.0)%(gh+fh))-fh/2
        # footprint rectangle clipped
        y0,y1=max(cy-fh/2,gy),min(cy+fh/2,gy+gh)
        if y1>y0:
            d.rectangle([gx*SS,y0*SS,(gx+gw)*SS,y1*SS],fill=al(c,a*0.13))
            # beam dots across the strip
            nb=NBEAM//NSTRIP+1
            for k in range(nb):
                bx=gx+gw*(k+0.5)/nb; by=cy
                if gy<=by<=gy+gh: d.ellipse([(bx-3)*SS,(by-3)*SS,(bx+3)*SS,(by+3)*SS],fill=al(c,a*0.8))
            sx=gx+gw+0; 
        for i,(hx,hy) in enumerate(HANDS):
            px,py=gx+hx*gw,gy+hy*gh
            if cy-fh/2<=py<=cy+fh/2: owner[i]=s
    for i,(hx,hy) in enumerate(HANDS):
        px,py=gx+hx*gw,gy+hy*gh; c=STRIPC[owner[i]] if owner[i] is not None else DIM
        d.rounded_rectangle([(px-6)*SS,(py-10)*SS,(px+6)*SS,(py+10)*SS],2*SS,fill=al(TEXT,a))
        d.ellipse([(px-14)*SS,(py-18)*SS,(px+14)*SS,(py+18)*SS],outline=al(c,a),width=3*SS)
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(4)]
    a=fade(t,0.3,1e9,0.6); strip=t>b[2][0]-0.3
    head(d,t,"HOW COVERAGE ACTUALLY WORKS","one satellite · ~700 beams · ~8.9 km each at nadir",0.2,1e9)
    cx,cy=(560 if strip else 780),560
    d.ellipse([(cx-320)*SS,(cy-320)*SS,(cx+320)*SS,(cy+320)*SS],outline=al(LINE,a),width=2*SS)
    d.text(((cx-330)*SS,(cy+335)*SS),"~1,000 km of ground visible from 330 km",font=mono(15),fill=al(DIM,a))
    k=ease(clamp((t-0.8)/4.5)); n=int(700*k); dx=0.0
    if t>b[1][0]-0.2: dx=ease(clamp((t-b[1][0])/(b[3][0]-b[1][0])))*300-150
    for i in range(n):
        x,y=LAT[i]
        if (x+dx)**2+y**2>320**2: continue
        px,py=(cx+x+dx)*SS,(cy+y)*SS; s=2.6*SS; col=BLUE if (t<b[2][0] or i%3) else GREEN
        d.ellipse([px-s,py-s,px+s,py+s],fill=al(col,a*0.85))
    sat_glyph(d,(cx+dx)*SS,(cy-430)*SS,a); d.line([((cx+dx)*SS,(cy-418)*SS),((cx+dx)*SS,(cy-320)*SS)],fill=al(BLUE,a*0.4),width=2*SS)
    if not strip:
        panel(d,1300,200,1840,700,a)
        stat(d,1340,240,"BEAMS PER SATELLITE",count(700*k),TEXT,54,a); stat(d,1340,380,"BEAM WIDTH ON THE GROUND","~8.9 km",BLUE,42,a)
        if t>b[1][0]-0.3:
            aa=fade(t,b[1][0]-0.2,1e9,0.5); stat(d,1340,510,"ORBITAL SPEED","27,000 km/h",AMBER,36,aa); d.text((1340*SS,620*SS),"overhead for about four minutes",font=mono(17),fill=al(DIM,aa))
    else:
        sa=fade(t,b[2][0]-0.2,1e9,0.5); strip_machine(d,b[2][0],t,960,150,880,560,sa)
        panel(d,960,740,1840,900,sa)
        d.text((1000*SS,770*SS),"CELLS STAY FIXED TO THE GROUND",font=mono(15),fill=al(DIM,sa)); d.text((1000*SS,800*SS),"handover every 1–2 minutes",font=fnt(26,True),fill=al(GREEN,sa)); d.text((1000*SS,850*SS),"the satellites sweep; the cells don't move",font=mono(15),fill=al(DIM,sa))
    if t>b[3][0]-0.2: d.text((90*SS,980*SS),"continuous coverage — stitched from moving parts",font=fnt(28),fill=al(TEXT,fade(t,b[3][0]-0.1,1e9,0.5)))
    return out(im)
if __name__=="__main__": render_range(frame,"s4",float(sys.argv[1]),float(sys.argv[2]))
