"""'How adjacent spectrum is protected' — a short companion film (v1, Oct 2026).
Renders vo_e*.wav and marks_seams.json.  Run: python3 /home/claude/v2/narration_seams.py [e1 e2 …]
"""
from kokoro_onnx import Kokoro
import soundfile as sf, numpy as np, json, sys, os
ROOT="/home/claude/v2"
k=Kokoro(f"{ROOT}/voices/kokoro-v1.0.onnx", f"{ROOT}/voices/voices-v1.0.bin")

SC={
"e1":[
 "A fair question about any new transmitter: what stops it from stomping on the neighbors?",
 "Most people expect the answer in megahertz of empty spectrum. A guard band. That is not how the American band plan works... and hasn't been for twenty years.",
 "This is four minutes on what actually protects adjacent spectrum. Every number is a rule you can look up."],
"e2":[
 "Think of it as property fences and a noise ordinance. Adjacent yards, no buffer strip between them. You can be as loud as you like inside your own yard — but measured at the fence, your noise has to fall below a ceiling.",
 "That ceiling is called an emission mask. The standard one is forty-three plus ten log P decibels of attenuation outside your block — which works out to minus thirteen dBm per megahertz at the edge.",
 "That is the fence every carrier in America runs on today. AT&T sits beside Verizon with zero vacant megahertz between them. Vacant spectrum is wasted money, so the regulator engineers the protection into how sharply a signal must stop."],
"e3":[
 "Where the neighbor is delicate — frequencies where phones are listening, not talking — the fence is five hundred times stricter. Minus forty dBm per megahertz.",
 "That rule was written in twenty twelve for a hostile boundary: DISH's uplink against a stranger's H-block. SpaceX now owns both sides of that line, and the rule still binds — in both directions.",
 "There is exactly one true guard band in the neighborhood: the J block, five megahertz the FCC never managed to sell. It protects by accident, and SpaceX doesn't own it."],
"e4":[
 "Satellites are different. A beam from orbit cannot stop at a license boundary drawn on a map — any more than a floodlight on a helicopter can stop at your fence.",
 "So the rule changes. Instead of a fence at the transmitter, it is a ceiling on interference power arriving on the ground: minus one hundred twenty decibel-watts per square meter per megahertz, measured a meter and a half above the ground, and totaled across the entire fleet.",
 "Translate that into a phone's antenna and it is roughly minus one hundred twenty-six dBm in a narrowband channel — about where the receiver's own thermal noise already sits. The rule is pinned to the level at which the satellite is no louder than the noise the radio already lives with."],
"e5":[
 "Now the hard case. The pending eight-hundred-megahertz block sits one megahertz above the receivers of every public-safety radio system in the country.",
 "Here the protection isn't a mask at all. It's a receiver test. Section ninety point six seven two: if a police radio's signal is at least minus one hundred one dBm and its carrier-to-interference ratio drops below twenty decibels, that is unacceptable interference — and the interferer is strictly liable. Twenty-four hours to respond. Forty-eight to fix. Immediate shutdown on a sworn declaration of danger.",
 "Run the satellite cap through that test. At minus one hundred twenty, the public-safety radio keeps a ratio of about twenty to twenty-one and a half decibels — it passes, barely. At the relaxed limits now being floated, it fails. That arithmetic is on the site, with its assumptions labeled.",
 "So the strictest protection in the entire stack is the one SpaceX is about to buy into — and the Cellular band next door already carries an AST satellite grant that imports exactly these rules. The template exists."],
"e6":[
 "Three things follow, and none of them is an opinion.",
 "One. Adjacent spectrum is protected by enforceable numbers, not by empty space — and that has been the design of the whole band plan since the nineties.",
 "Two. For satellites, the protection is measured at the victim, on the ground, across the whole fleet. It does not depend on trusting the transmitter.",
 "Three. The record shows the regulator saying no. SpaceX asked for nine point four decibels of relief and got it only in two five-megahertz slivers, over the objections of AT&T, Verizon and EchoStar — with a claw-back if interference appears.",
 "If you believe the neighbors are unprotected... say which number is wrong."],
}
GAP=0.7; SR=24000; MARKS={}
if __name__=="__main__":
    want=sys.argv[1:] or list(SC)
    if os.path.exists(f"{ROOT}/marks_seams.json"): MARKS.update(json.load(open(f"{ROOT}/marks_seams.json")))
    for name,beats in SC.items():
        if name not in want: continue
        out=[]; marks=[]; t=0.0
        for i,b in enumerate(beats):
            a,_=k.create(b,voice="af_heart",speed=0.96,lang="en-us")
            marks.append([round(t,2),round(t+len(a)/SR,2)]); out.append(a); t+=len(a)/SR
            g=GAP if i<len(beats)-1 else 0.4; out.append(np.zeros(int(SR*g),dtype=a.dtype)); t+=g
        au=np.concatenate(out); sf.write(f"{ROOT}/vo_{name}.wav",au,SR); MARKS[name]={"dur":round(len(au)/SR,2),"beats":marks}
        print(f"{name}: {MARKS[name]['dur']:>6.2f}s")
    json.dump(MARKS,open(f"{ROOT}/marks_seams.json","w"),indent=1)
    print("TOTAL",round(sum(m["dur"] for m in MARKS.values()),1))
