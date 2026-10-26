# Film pipeline — Starlink Mobile explainer (v2, Oct 2026)

Everything needed to re-cut `starlink-mobile-explainer.mp4`. Narration is fixed first; the visuals are cut to its beat marks.

## Layout
- `narration.py` — the script (nine scenes, `SC` dict) and the Kokoro voice renderer. Writes `vo_s*.wav` + `marks.json`.
- `lib.py` — palette, fonts, easing, beat lookup, CONUS map loader (reads `US_DENS` / `US_MIDX` / `US_STATES` / `CONUS_PATH` out of `index.html`).
- `sc1.py … sc9.py` — one renderer per scene; `python3 scN.py <t0> <t1>` renders frames for that time range.
- `render.sh <scene>` — renders a whole scene and encodes `clips/<scene>.mp4`.
- `verify.py <scene>…` — checks every frame decodes, re-renders bad ones, re-encodes.
- `assemble.py [scenes…]` — concatenates clips with 1 s bridges, muxes the narration (loudnorm −16 LUFS), prints `VIDEO_CHAPTERS`.

## One-time setup (Linux/WSL; ~360 MB)
    pip install kokoro-onnx soundfile pillow numpy
    mkdir -p voices fonts
    curl -L -o voices/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
    curl -L -o voices/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
    curl -L -o fonts/inter.zip https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip ; unzip -q fonts/inter.zip -d fonts/inter
    curl -L -o fonts/jbm.zip https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip ; unzip -q fonts/jbm.zip -d fonts/jbm
    # ffmpeg must be on PATH

## Paths
Scripts are absolute-pathed to `/home/claude/v2` (the build container) and the site at `/home/claude/starlink-roadmap/index.html`.
To run elsewhere, replace those two strings once:
    sed -i 's#/home/claude/v2#/your/path/video#g; s#/home/claude/starlink-roadmap/index.html#/your/path/index.html#g' *.py render.sh

## Re-cut
    python3 narration.py            # or: python3 narration.py s7   (one scene)
    for s in s1 s2 s3 s4 s5 s6 s7 s8 s9; do ./render.sh $s; done   # ~0.15–0.3 s per frame, single core
    python3 verify.py s1 s2 s3 s4 s5 s6 s7 s8 s9
    python3 assemble.py             # -> starlink-mobile-explainer.mp4 + VIDEO_CHAPTERS for index.html
Poster: any frame, e.g. frames/s1/f00120.png -> video-poster.jpg.

## Numbers
Scene 7's headline figures are the site's Canonical Serviceability dials at v144 (800 layer on): 9.0M / 2.7% orbit-alone,
21% land green, 94M / 28% hybrid on ~2.1M small cells; CBRS none -> throughput headroom ×1.1 (vs ×3.6). Re-read them off the
live tab before voicing if the model changes.

## Companion short — "How adjacent spectrum is protected" (4:31)
Same pipeline, separate script and beat marks: `narration_seams.py` → `vo_e*.wav` + `marks_seams.json`; renderers `e1.py…e6.py`
(they import `elib.py`, which points `lib` at the seams marks); `render_e.sh <scene>`; then concatenate `clips/e1…e6.mp4` with 1 s
bridges and mux `full_e.wav` exactly as `assemble.py` does for the main film. Output: `adjacent-spectrum-explainer.mp4`, poster
`seams-poster.jpg`, chapters in `SEAMS_CHAPTERS` in index.html.
