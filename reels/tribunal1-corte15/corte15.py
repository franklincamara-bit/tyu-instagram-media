# Trial Reel "Tribunal do Trade #1 — corte de 15 s" (TYU-69): recorte do tribunal1-final.mp4 começando pelo erro
# (stop descendo), depois réu, sentença e cartão final. Faixa de gancho "O STOP ANDOU 3 VEZES" nos 2,2 s iniciais.
# Uso: python3 corte15.py -> tribunal1-corte15-final.mp4
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "..", "tribunal1", "tribunal1-final.mp4")
SEGS = [(6.95, 12.75), (1.40, 3.85), (17.55, 23.05), (26.2, 28.6)]
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Black.otf", 70)
im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
txt = "O STOP ANDOU 3 VEZES"; w = d.textlength(txt, font=F)
x0 = (1080 - w) / 2 - 36; d.rounded_rectangle([x0, 1480, x0 + w + 72, 1480 + 112], 28, fill=(229, 72, 77, 255))
d.text(((1080 - w) / 2, 1492), txt, font=F, fill="white"); im.save(os.path.join(HERE, "hook.png"))
fc = []; n = len(SEGS)
for i, (a, b) in enumerate(SEGS):
    dur = b - a
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.06,afade=t=out:st={dur-0.08:.2f}:d=0.08[a{i}]")
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
fc.append("[vc][1:v]overlay=0:0:shortest=1:enable='between(t,0,2.2)'[vo]")
fc.append("[ac]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[ao]")
out = os.path.join(HERE, "tribunal1-corte15-final.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-loop", "1", "-t", "17", "-i", os.path.join(HERE, "hook.png"), "-filter_complex", ";".join(fc),
                "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf", "scale=720:1280", "-c:v", "libx264", "-crf", "28", "-preset", "medium",
                "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", os.path.join(HERE, "tribunal1-corte15-previa-720p.mp4")], check=True)
