"""Starlink Mobile explainer — v2 narration (Oct 2026, site build v144).

Renders every scene's beats with Kokoro (af_heart), writes vo_<scene>.wav and
marks.json (beat start/end seconds). The visuals are cut to these marks:
the narration is fixed, the visuals serve it.

Run:  python3 /home/claude/v2/narration.py
Numbers are the site's canonical dials at v144 (Serviceability, Canonical
scenario, 800 MHz layer on): orbit-alone 9.0M / 2.7%, 21% land green,
hybrid 94M / 28% with ~2.1M small cells; CBRS none -> headroom x1.1.
"""
from kokoro_onnx import Kokoro
import soundfile as sf, numpy as np, json

ROOT = "/home/claude/v2"
k = Kokoro(f"{ROOT}/voices/kokoro-v1.0.onnx", f"{ROOT}/voices/voices-v1.0.bin")

SC = {
"s1": [
 "SpaceX wants to be America's fourth mobile carrier — without building a single cell tower.",
 "The towers are satellites. Fifteen thousand of them, talking to the phone already in your pocket. No app. No attachment. No special hardware.",
 "That's the pitch. This site asks a harder question. How much of it is physics... and how much is a press release?"],
"s2": [
 "Start with the asset. Nineteen billion dollars bought sixty-five megahertz of radio spectrum from EchoStar. Exclusive lanes on an invisible highway.",
 "Then, this October, a second piece. Fourteen megahertz of low band from Grain Management — about eight billion dollars, by report, and not yet approved. Seventy-nine megahertz, if it closes.",
 "And the band can do two jobs. Pointed up, it's a satellite link over the countryside. Pointed sideways, it feeds small cells in a city.",
 "But why would a city need its own network at all? Density.",
 "One satellite beam is about nine kilometers across — sixty-odd square kilometers — and everyone underneath it shares it. Out in farm country, that's a few dozen people. In a city, it's tens of thousands.",
 "The satellite layer can carry about one subscriber per square kilometer. Urban density runs hundreds of times higher.",
 "No fleet size fixes that. Satellites sell coverage. They can't sell capacity where people are stacked.",
 "So cities need a ground layer... and only once that layer exists can the satellite hand over the band. The handover isn't a trick. It's a sequence."],
"s3": [
 "Now the hard part. A phone talking to a satellite three hundred and thirty kilometers up is shouting at an airplane with a quarter-watt voice. The signal arrives a million billion times weaker.",
 "So how fast is it, really? Throughput is spectrum times efficiency... and the efficiency number is the whole argument.",
 "Measured today: nought point six two. The company's planning target: four times that. Their headline claim: twelve times that.",
 "Those aren't contradictions. They're a bracket... and everything on this site is labeled with which end it's holding."],
"s4": [
 "A satellite sees a thousand kilometers of ground. But it doesn't light all of it at once. It paints it... in about seven hundred beams, each about nine kilometers wide.",
 "And it's moving. Twenty-seven thousand kilometers an hour. Which means your tower is overhead for about four minutes.",
 "Cells stay fixed to the ground while the satellites sweep across them, handing your phone off every minute or two.",
 "Continuous coverage... stitched from moving parts."],
"s5": [
 "Now watch what happens as the fleet grows.",
 "With only a few hundred satellites, the one serving you sits low on the horizon. Its beam arrives at a slant... smeared into a long ellipse that spills onto its neighbors.",
 "So the network has to ration. Neighboring cells take turns on different slices of the band — and your cell gets about a third of the spectrum. Ten megabits, not fifty.",
 "Add satellites, and the one serving you climbs higher in the sky. The beam lands square, compact, and isolated. Now every cell can use the whole band at once. That's full frequency reuse.",
 "The typical cell crosses that line around six thousand satellites. Every cell — even the worst-placed one — gets there around fifteen thousand.",
 "So the advertised fifty megabits isn't wrong. It's just what the network delivers after it's finished being built. Fleet growth doesn't only add capacity... it deletes the bad geometry."],
"s6": [
 "So why pay billions for fourteen megahertz? Because the phone in your pocket already speaks it.",
 "It's Band twenty-six — in every current iPhone, and most Androids. The new two-gigahertz spectrum needs chips that don't ship until twenty twenty-seven. The eight-hundred band works in the phone you own today, in both directions, on spectrum SpaceX would own instead of lease.",
 "But low band costs something. On the same antenna, a longer wavelength makes a wider beam. Two point three times wider — twenty-one kilometers instead of nine. Five times the area... the same capacity.",
 "And indoors? Lower frequencies do get through walls better. By about one decibel. Still no link from orbit.",
 "So eight hundred megahertz buys owned coverage, in today's phones. It doesn't buy capacity, and it doesn't buy your living room. The real prize is on the ground."],
"s7": [
 "So how many people can this actually carry? The site does the division.",
 "Using the company's own optimistic numbers, the satellite layer serves about nine million Americans. Under three percent. It greens a fifth of the land — and almost none of the people. Every city is red.",
 "So what does SpaceX actually own on the ground? Five megahertz of H-block. And if the Grain deal closes, fourteen more at eight hundred — the low band every carrier builds its city coverage on.",
 "Put those on macro towers and you have a licensed floor. Carrier-grade coverage, in phones people already carry. Thin — a dozen megahertz is coverage, not capacity — but owned. Nobody can turn it off.",
 "Capacity is the other problem, and owned spectrum doesn't solve it. The candidate is CBRS: shared spectrum, where SpaceX would hold priority, not exclusivity — and a referee can shuffle the channels.",
 "Pour two million small cells on CBRS over that floor, across the top ten metros, and the hybrid network reaches ninety-four million people. Twenty-eight percent.",
 "Lose CBRS, and the floor still stands. The same boxes reach the same people — but on five megahertz, the city layer runs at its ceiling. One point one times headroom. Any growth, and it chokes... until the C-band auction in twenty twenty-seven offers the only exclusive mid-band on the table.",
 "And remember... not a single cell tower? In October, SpaceX was reported in talks for eighty thousand tower sites. Half the towers in the country. Nothing signed. But that's what an eight-hundred-megahertz floor looks like when you build it."],
"s8": [
 "Seven things decide whether this works.",
 "The Grain transfer needs FCC consent — and a rule change, because satellites aren't allowed in that band yet. The vote is October twenty-ninth. The filing is due December fourth.",
 "The EchoStar deal has to consummate by November twenty twenty-seven, against a two point four billion dollar escrow. Buildout milestones, or the license terminates. Every foreign market, its own license. The FCC still has to release the full forty-five megahertz from orbit. And the C-band auction decides whether the city network ever gets exclusive capacity.",
 "At eight hundred megahertz there's a new neighbor, too. Public safety radio, one megahertz below. There, the fight isn't spectrum. It's interference.",
 "But the one nobody can buy their way past... is that the phone in your pocket can't hear the two-gigahertz spectrum yet. First handsets, twenty twenty-seven. Volume, around twenty twenty-nine. Only the low band is already in your hand."],
"s9": [
 "So. Physics, or press release?",
 "Both, honestly. The physics works. What it describes is a coverage product with a city ground layer — not a fourth carrier that looks like the other three.",
 "The timeline is the bet. And the timeline now runs through the FCC... and through the tower leases.",
 "Every number here is sourced, labeled, and yours to move. Go argue with it."],
}

GAP = 0.7; SR = 24000; MARKS = {}
if __name__ == "__main__":
    import sys, os
    want = sys.argv[1:] or list(SC)
    if os.path.exists(f"{ROOT}/marks.json"): MARKS.update(json.load(open(f"{ROOT}/marks.json")))
    for name, beats in SC.items():
        if name not in want: continue
        out = []; marks = []; t = 0.0
        for i, b in enumerate(beats):
            a, _ = k.create(b, voice="af_heart", speed=0.96, lang="en-us")
            marks.append([round(t, 2), round(t + len(a) / SR, 2)]); out.append(a); t += len(a) / SR
            g = GAP if i < len(beats) - 1 else 0.4
            out.append(np.zeros(int(SR * g), dtype=a.dtype)); t += g
        au = np.concatenate(out); sf.write(f"{ROOT}/vo_{name}.wav", au, SR)
        MARKS[name] = {"dur": round(len(au) / SR, 2), "beats": marks}
        print(f"{name}: {MARKS[name]['dur']:>6.2f}s  beats={len(beats)}")
    json.dump(MARKS, open(f"{ROOT}/marks.json", "w"), indent=1)
    tot = sum(m["dur"] for m in MARKS.values())
    print("TOTAL SPOKEN:", round(tot, 1), "s  + 8 gaps =", round(tot + 8, 1), "s")
