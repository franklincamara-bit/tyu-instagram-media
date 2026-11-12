# Overtrade: a curva das decisões — v2 (TYU-62)
Refeito em 12/11/2026 pelo comentário do Franklin (10/11): v1 confusa e rápida, trilha repetida.
- Storyboard desenhado (motor do VID-42), 39 s, 5 cenas: trade 1 com plano → trades 2–5 com a qualidade da decisão caindo → trade 6 (sem setup, só pressa) → a curva → a regra (limite de trades no dia).
- Narração Rafael Valente (ElevenLabs, 35 s) em `narr.mp3`; trilha lo-fi 80 bpm sintetizada nova (`mix_ot2.py`).
- Render: `node render.mjs ot2.html 39 video.mp4` → `node pen.mjs ot2.html pen.json` → `python3 mix_ot2.py` → mux com ffmpeg.
- Capa mantida da v1 (`overtrade6-v2-capa.jpg` = `../overtrade6/overtrade6-capa.jpg`).
