import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s6",i)
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(5)]
    # ---- beats 0-1: the phone already speaks it ----
    if t<b[2][0]+0.4:
        a=fade(t,0.2,b[2][0]+0.3,0.5)
        head(d,t,"WHY BUY FOURTEEN MEGAHERTZ OF LOW BAND?","817–824 / 862–869 MHz · the old Nextel block · Band 26 / n26",0.2,b[2][0]+0.3)
        px,py=330,600; phone_glyph(d,px*SS,py*SS,a,2.2)
        d.rounded_rectangle([(px-30)*SS,(py-62)*SS,(px+30)*SS,(py+62)*SS],4*SS,fill=al(BG,a))
        d.text(((px-26)*SS,(py-52)*SS),"B26",font=mono(18,True),fill=al(GREEN,a*fade(t,b[1][0],1e9,0.5)))
        d.text(((px-26)*SS,(py-24)*SS),"n26",font=mono(18,True),fill=al(GREEN,a*fade(t,b[1][0]+0.4,1e9,0.5)))
        d.text(((px-26)*SS,(py+8)*SS),"n252",font=mono(18,True),fill=al(RED,a*fade(t,b[1][0]+4.5,1e9,0.5)))
        d.text(((px-26)*SS,(py+34)*SS),"2027+",font=mono(13),fill=al(RED,a*fade(t,b[1][0]+5.0,1e9,0.5)))
        d.text(((px-110)*SS,(py+100)*SS),"the phone you own today",font=mono(16),fill=al(DIM,a))
        # right: two columns
        for i,(ttl,rows,c,t0) in enumerate([
            ("800 MHz · LOW BAND (pending)",["Band 26 · every current iPhone","works in today's phones","uplink + downlink · both directions","owned, not leased"],GREEN,b[1][0]),
            ("2 GHz · AWS-4 n252 (owned)",["needs new handset silicon","first phones 2027 · volume ~2029","the capacity band","owned"],AMBER,b[1][0]+4.3)]):
            x=640+i*600; aa=a*fade(t,t0-0.2,1e9,0.6); panel(d,x,300,x+560,760,aa)
            d.text(((x+30)*SS,330*SS),ttl,font=mono(15,True),fill=al(c,aa))
            for j,r in enumerate(rows):
                ra=aa*fade(t,t0+0.6+j*0.9,1e9,0.5)
                d.text(((x+30)*SS,(400+j*80)*SS),"·  "+r,font=fnt(22),fill=al(TEXT if j<3 else c,ra))
        if t>b[0][0]+2.5: d.text((90*SS,920*SS),"the phone in your pocket already speaks it",font=fnt(28),fill=al(TEXT,a*fade(t,b[0][0]+2.6,1e9,0.6)))
    # ---- beats 2-3: the cost — beam size, indoor ----
    if t>b[2][0]-0.4:
        a=fade(t,b[2][0]-0.3,1e9,0.6); im2,d2=canvas()
        head(d2,t,"WHAT LOW BAND COSTS","same antenna · longer wavelength · wider beam  (derived: λ/D, 330 km)",b[2][0]-0.3,1e9)
        cx,cy=520,560; k=ease(clamp((t-b[2][0]-1.5)/3.0))
        r2=95; r8=r2*(1+1.31*k)
        d2.ellipse([(cx-r8)*SS,(cy-r8)*SS,(cx+r8)*SS,(cy+r8)*SS],fill=al(GREEN,a*0.12),outline=al(GREEN,a*0.9),width=3*SS)
        d2.ellipse([(cx-r2)*SS,(cy-r2)*SS,(cx+r2)*SS,(cy+r2)*SS],fill=al(AMBER,a*0.18),outline=al(AMBER,a),width=3*SS)
        d2.text(((cx-50)*SS,(cy-10)*SS),"8.9 km",font=mono(16,True),fill=al(AMBER,a))
        d2.text(((cx-70)*SS,(cy+r8+16)*SS),f"{8.9*(1+1.31*k):.1f} km",font=mono(18,True),fill=al(GREEN,a*fade(t,b[2][0]+1.6,1e9,0.5)))
        d2.text(((cx-230)*SS,(cy+r8+50)*SS),"2 GHz beam (amber) vs 800 MHz beam (green)",font=mono(14),fill=al(DIM,a))
        panel(d2,900,260,1840,620,a)
        stat(d2,940,300,"BEAM WIDTH · 800 vs 2 GHz","×2.3",GREEN,60,a*fade(t,b[2][0]+2.2,1e9,0.5),"wider · 21 km instead of 9")
        stat(d2,940,430,"BEAM AREA","×5.3",GREEN,60,a*fade(t,b[2][0]+4.5,1e9,0.5),"the area · the same capacity")
        d2.text((940*SS,560*SS),"the free-space advantage cancels for a fixed antenna size (derived)",font=mono(14),fill=al(DIM,a*fade(t,b[2][0]+5.5,1e9,0.5)))
        if t>b[3][0]-0.4:
            ia=a*fade(t,b[3][0]-0.3,1e9,0.5); panel(d2,900,660,1840,900,ia)
            d2.text((940*SS,690*SS),"INDOORS · BUILDING-ENTRY LOSS (ITU-R P.2109, traditional)",font=mono(14),fill=al(DIM,ia))
            for i,(lab,v,c,t0) in enumerate([("2 GHz",15.0,AMBER,b[3][0]),("800 MHz",14.2,GREEN,b[3][0]+1.2)]):
                y=730+i*60; g=ease(clamp((t-t0)/0.9)); w=600*(v/15.0)*g
                d2.rounded_rectangle([1060*SS,y*SS,(1060+w)*SS,(y+34)*SS],4*SS,fill=al(c,ia*0.5),outline=al(c,ia),width=2*SS)
                d2.text((940*SS,(y+6)*SS),lab,font=mono(15,True),fill=al(c,ia)); d2.text(((1070+w)*SS,(y+6)*SS),f"{v*g:.1f} dB",font=mono(15),fill=al(TEXT,ia*g))
            d2.text((940*SS,860*SS),"Δ ≈ 1 dB  ·  still 1.6 dB under the decode floor  ->  no link from orbit",font=mono(15,True),fill=al(RED,ia*fade(t,b[3][0]+3.0,1e9,0.5)))
        if t>b[4][0]-0.3:
            va=fade(t,b[4][0]-0.2,1e9,0.6)
            d2.rectangle([0,930*SS,W*SS,H*SS],fill=al(BG,va*0.85))
            d2.text((90*SS,950*SS),"owned coverage in today's phones  ·  not capacity  ·  not your living room",font=fnt(26),fill=al(TEXT,va))
            d2.text((90*SS,1000*SS),"the real prize is on the ground",font=fnt(26,True),fill=al(AMBER,va*fade(t,b[4][0]+5.5,1e9,0.6)))
        im=Image.blend(im,im2,a)
    return out(im)
if __name__=="__main__": render_range(frame,"s6",float(sys.argv[1]),float(sys.argv[2]))
