import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s9",i)
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(4)]
    a=fade(t,0.1,b[1][0]+0.2,0.5)
    if a>0.01:
        d.text((90*SS,420*SS),"PHYSICS?",font=fnt(80,True),fill=al(TEXT,a)); d.text((90*SS,540*SS),"OR PRESS RELEASE?",font=fnt(80,True),fill=al(AMBER,a))
    if t>b[1][0]-0.4:
        a2=fade(t,b[1][0]-0.3,1e9,0.6); im2,d2=canvas()
        d2.text((90*SS,240*SS),"THE PHYSICS WORKS.",font=fnt(64,True),fill=al(GREEN,a2*fade(t,b[1][0]+1.0,1e9,0.6)))
        d2.text((90*SS,340*SS),"a coverage product with a city ground layer —",font=fnt(30),fill=al(TEXT,a2*fade(t,b[1][0]+3.0,1e9,0.6)))
        d2.text((90*SS,390*SS),"not a fourth carrier that looks like the other three",font=fnt(30),fill=al(DIM,a2*fade(t,b[1][0]+4.5,1e9,0.6)))
        d2.text((90*SS,500*SS),"THE TIMELINE IS THE BET.",font=fnt(64,True),fill=al(AMBER,a2*fade(t,b[2][0]-0.2,1e9,0.6)))
        for i,(lab,c) in enumerate([("the FCC",AMBER),("the tower leases",GREEN)]):
            aa=a2*fade(t,b[2][0]+2.6+i*1.4,1e9,0.5); x=90+i*420; panel(d2,x,600,x+380,680,aa); d2.text(((x+30)*SS,622*SS),"·  "+lab,font=fnt(26),fill=al(c,aa))
        aa=a2*fade(t,b[3][0]-0.2,1e9,0.5)
        d2.text((90*SS,780*SS),"every number is sourced, labelled, and yours to move",font=fnt(26),fill=al(TEXT,aa))
        d2.text((90*SS,840*SS),"starlink-roadmap-production.up.railway.app",font=mono(24),fill=al(BLUE,aa)); d2.line([(90*SS,890*SS),(940*SS,890*SS)],fill=al(BLUE,aa*0.5),width=2*SS)
        d2.text((90*SS,930*SS),"site build v144 · Oct 2026 · 800 MHz base case: assumes SpaceX acquires Grain's licences (pending)",font=mono(13),fill=al(DIM,aa))
        im=Image.blend(im,im2,a2)
    return out(im)
if __name__=="__main__": render_range(frame,"s9",float(sys.argv[1]),float(sys.argv[2]))
