import sys; sys.path.insert(0,'/home/claude/v2'); from elib import *
B=lambda i: beat("e1",i)
def frame(t):
    im,d=canvas(); b=[B(i) for i in range(3)]; a=fade(t,0.2,1e9,0.5)
    d.text((90*SS,200*SS),"HOW ADJACENT SPECTRUM",font=fnt(72,True),fill=al(TEXT,a)); d.text((90*SS,290*SS),"IS PROTECTED",font=fnt(72,True),fill=al(AMBER,a))
    d.text((94*SS,400*SS),"a four-minute companion to Spectrum → The seams",font=mono(20),fill=al(DIM,a))
    # two neighbours, no gap, pulsing boundary
    y=600; fx=band_strip(d,300,y,1320,[(0,10,"NEIGHBOR A","",BLUE,0.35,0.8),(10,20,"NEW TRANSMITTER","",AMBER,0.45,0.8)],0,20,a,t,0)
    if b[1][0]<t<b[2][0]:
        k=ease(clamp((t-b[1][0])/1.5)); g=k*2.0  # a guard gap that appears then is crossed out
        d.rectangle([fx(10-g/2)*SS,(y-4)*SS,fx(10+g/2)*SS,(y+74)*SS],fill=al(BG,1),outline=al(TEXT,0.8),width=2*SS)
        d.text((fx(10)*SS,(y+35)*SS),"guard band?",font=mono(14),fill=al(TEXT,a),anchor="mm")
        xa=fade(t,b[1][0]+4.2,1e9,0.4); d.line([(fx(8.6)*SS,(y-20)*SS),(fx(11.4)*SS,(y+90)*SS)],fill=al(RED,xa),width=6*SS); d.line([(fx(11.4)*SS,(y-20)*SS),(fx(8.6)*SS,(y+90)*SS)],fill=al(RED,xa),width=6*SS)
        d.text((300*SS,740*SS),"not how the US band plan works — and hasn't been for twenty years",font=fnt(26),fill=al(TEXT,xa))
    if t>b[2][0]-0.2:
        p=pulse(t); d.line([(fx(10)*SS,(y-30)*SS),(fx(10)*SS,(y+100)*SS)],fill=al(RED,0.5+0.5*p),width=4*SS)
        d.text((300*SS,740*SS),"every number that follows is a rule you can look up",font=fnt(26),fill=al(TEXT,fade(t,b[2][0],1e9,0.5)))
    return out(im)
if __name__=="__main__": render_range(frame,"e1",float(sys.argv[1]),float(sys.argv[2]))
