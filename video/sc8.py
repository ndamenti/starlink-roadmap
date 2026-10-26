import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s8",i)
RISKS=[("GRAIN 800 MHz TRANSFER","FCC consent + a rule change\nvote Oct 29 · filing due Dec 4",AMBER),
       ("ECHOSTAR CONSUMMATION","by Nov 30, 2027\n$2.4B escrow",RED),
       ("BUILDOUT MILESTONES","2 / 4 / 9 years\nor the licence ends",RED),
       ("PER-COUNTRY LICENSING","every market,\nits own approval",AMBER),
       ("DEFERRED FCC WAIVERS","20 MHz vs 45 MHz\nof satellite downlink",AMBER),
       ("UPPER C-BAND AUCTION","July 2027\nthe only exclusive city capacity",AMBER),
       ("HANDSET SILICON","phones that can hear n252\nthe one you can't buy",RED)]
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(5)]
    # narration-keyed: which cards light during beats 1-2
    lit=set()
    if b[1][0]<=t<b[2][0]: lit={0}
    elif b[2][0]<=t<b[3][0]:
        seg=(t-b[2][0])/(b[2][1]-b[2][0]); lit={1} if seg<0.22 else ({2} if seg<0.40 else ({3} if seg<0.56 else ({4} if seg<0.74 else {5})))
    show_ps=b[3][0]-0.4<t<b[4][0]-0.4
    if not show_ps and t<b[4][0]-0.4:
        head(d,t,"WHAT COULD BREAK IT","seven gates · six can be bought · one cannot",0.2,b[4][0]-0.5)
        for i,(nm,sub,c) in enumerate(RISKS):
            col,row=i%4,i//4; x,y=90+col*450,190+row*260; w=420 if i<4 else 420
            if i==6: x=90+2*450
            a=fade(t,0.5+i*0.35,b[4][0]-0.5,0.5)
            if a<=0.01: continue
            dimf=1.0 if (not lit or i in lit) else 0.38
            panel(d,x,y,x+w,y+200,a*dimf); d.rounded_rectangle([x*SS,y*SS,(x+6)*SS,(y+200)*SS],3*SS,fill=al(c,a*dimf))
            if i in lit:
                p=pulse(t); d.rounded_rectangle([(x-4-3*p)*SS,(y-4-3*p)*SS,(x+w+4+3*p)*SS,(y+204+3*p)*SS],12*SS,outline=al(c,a*0.9),width=3*SS)
            d.text(((x+30)*SS,(y+30)*SS),nm,font=mono(15,True),fill=al(c,a*dimf)); d.multiline_text(((x+30)*SS,(y+70)*SS),sub,font=fnt(19),fill=al(TEXT,a*0.92*dimf),spacing=8*SS)
    if show_ps:
        a=fade(t,b[3][0]-0.3,b[4][0]-0.5,0.6); im2,d2=canvas()
        head(d2,t,"A NEW NEIGHBOUR AT 800 MHz","public-safety radio receives at 851–861 MHz · a 1 MHz guard band · the ESMR downlink at 862–869",b[3][0]-0.3,b[4][0]-0.5)
        y=460; x0,x1=200,1720; f2x=lambda f:x0+(f-850)/(870-850)*(x1-x0)
        d2.line([(x0*SS,(y+70)*SS),(x1*SS,(y+70)*SS)],fill=al(LINE,a),width=2*SS)
        for lo,hi,lab,c,t0 in [(851,861,"PUBLIC SAFETY · B/ILT · SMR (receive)",RED,b[3][0]+0.3),(861,862,"guard",DIM,b[3][0]+1.6),(862,869,"ESMR 800 DL · SpaceX (pending)",GREEN,b[3][0]+0.8)]:
            aa=a*fade(t,t0,1e9,0.6); d2.rounded_rectangle([f2x(lo)*SS,y*SS,f2x(hi)*SS,(y+70)*SS],3*SS,fill=al(c,aa*0.4),outline=al(c,aa),width=2*SS)
            d2.text((f2x(lo)*SS,(y-30)*SS),lab,font=mono(14,True),fill=al(c,aa)); d2.text((f2x(lo)*SS,(y+84)*SS),f"{lo}",font=mono(13),fill=al(DIM,aa))
        d2.text((f2x(869)*SS-30*SS,(y+84)*SS),"869 MHz",font=mono(13),fill=al(DIM,a))
        d2.text((200*SS,640*SS),"strict liability · 24 h response · immediate shutdown on a 'clear and imminent danger' declaration  (47 CFR 90.672–674)",font=mono(15),fill=al(TEXT,a*fade(t,b[3][0]+3.5,1e9,0.6)))
        d2.text((200*SS,700*SS),"here the fight isn't spectrum — it's interference",font=fnt(30),fill=al(AMBER,a*fade(t,b[3][0]+6.0,1e9,0.6)))
        d2.text((200*SS,760*SS),"screening: at the current satellite emission limit the public-safety protection criterion is marginal; at the relaxed limits under discussion it fails (derived)",font=mono(14),fill=al(DIM,a*fade(t,b[3][0]+7.5,1e9,0.6)))
        im=Image.blend(im,im2,a)
    if t>b[4][0]-0.5:
        a=fade(t,b[4][0]-0.4,1e9,0.6); im2,d2=canvas()
        head(d2,t,"THE ONE NOBODY CAN BUY PAST","the phone in your pocket can't hear the 2 GHz spectrum yet",b[4][0]-0.4,1e9)
        d2.text((110*SS,300*SS),"HANDSET SILICON · AWS-4 n252",font=mono(18,True),fill=al(RED,a)); y0=460
        d2.line([(160*SS,y0*SS),(1760*SS,y0*SS)],fill=al(LINE,a),width=3*SS)
        for i,(yr,lab,c) in enumerate([("2026","standardised, zero phones",DIM),("2027","first handsets",AMBER),("2029","volume",GREEN)]):
            aa=a*ease(clamp((t-(b[4][0]+3.5+i*1.3))/0.7)); x=260+i*680
            d2.ellipse([(x-11)*SS,(y0-11)*SS,(x+11)*SS,(y0+11)*SS],fill=al(c,aa)); d2.text(((x-40)*SS,(y0-90)*SS),yr,font=fnt(44,True),fill=al(c,aa)); d2.text(((x-40)*SS,(y0+40)*SS),lab,font=mono(16),fill=al(DIM,aa))
        d2.text((110*SS,640*SS),"no launch cadence accelerates a chipset roadmap, or a consumer upgrade cycle",font=fnt(26),fill=al(TEXT,a*fade(t,b[4][0]+6.5,1e9,0.6)))
        la=a*fade(t,b[4][0]+9.5,1e9,0.6); panel(d2,110,730,1000,860,la)
        d2.text((150*SS,760*SS),"EXCEPT THE LOW BAND",font=mono(14),fill=al(GREEN,la)); d2.text((150*SS,790*SS),"800 MHz · Band 26 · already in your hand",font=fnt(26,True),fill=al(GREEN,la))
        im=Image.blend(im,im2,a)
    return out(im)
if __name__=="__main__": render_range(frame,"s8",float(sys.argv[1]),float(sys.argv[2]))
