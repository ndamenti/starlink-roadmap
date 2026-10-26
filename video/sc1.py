import sys, math; sys.path.insert(0,'/home/claude/v2')
from lib import *
B=lambda i: beat("s1",i)
def frame(t):
    im,d=canvas(); b0,b1=B(0); c0,c1=B(1); e0,e1=B(2)
    a=fade(t,0.3,e0-0.2,0.7)
    if a>0.01:
        d.text((90*SS,300*SS),"STARLINK",font=fnt(96,True),fill=al(TEXT,a))
        w=d.textlength("STARLINK ",font=fnt(96,True))
        d.text((90*SS+w,300*SS),"MOBILE",font=fnt(96,True),fill=al(AMBER,a))
        d.text((94*SS,430*SS),"the fourth carrier — without a single cell tower",font=mono(22),fill=al(DIM,a*fade(t,1.2,e0,0.6)))
    if t>c0-0.6:
        ca=fade(t,c0-0.5,e0-0.1,0.6); k=ease(clamp((t-c0)/5.0)); n=int(260*k); cx,cy=1360*SS,470*SS
        for i in range(n):
            ang=(i*137.508)*math.pi/180.0; r=(i/260.0)**0.5*300*SS
            x,y=cx+r*math.cos(ang),cy+r*math.sin(ang)*0.55; s=2.2*SS
            d.ellipse([x-s,y-s,x+s,y+s],fill=al(BLUE,ca*(0.35+0.65*(i/260.0))))
        d.text((1160*SS,800*SS),"D2C SATELLITES PLANNED",font=mono(15),fill=al(DIM,ca))
        d.text((1160*SS,830*SS),count(15000*k),font=fnt(64,True),fill=al(TEXT,ca))
        px,py=300*SS,760*SS; phone_glyph(d,px,py,ca)
        d.line([(px,py-34*SS),(cx-140*SS,cy+120*SS)],fill=al(BLUE,ca*0.55),width=2*SS)
        for i,s in enumerate(["no app","no attachment","no special hardware"]):
            aa=ca*fade(t,c0+1.6+i*0.8,e0,0.5)
            d.text((100*SS,(560+i*40)*SS),"·  "+s,font=mono(20),fill=al(TEXT,aa))
    if t>e0-0.4:
        qa=fade(t,e0-0.3,1e9,0.6); im2,d2=canvas()
        d2.text((90*SS,420*SS),"PHYSICS?",font=fnt(84,True),fill=al(TEXT,qa))
        d2.text((90*SS,540*SS),"OR PRESS RELEASE?",font=fnt(84,True),fill=al(AMBER,qa))
        d2.text((94*SS,690*SS),"every number that follows is labelled: measured  ·  claimed  ·  derived",font=mono(20),fill=al(DIM,qa*fade(t,e0+1.0,1e9,0.6)))
        im=Image.blend(im,im2,qa)
    return out(im)
if __name__=="__main__": render_range(frame,"s1",float(sys.argv[1]),float(sys.argv[2]))
