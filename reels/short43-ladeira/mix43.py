# Trilha do Short VID-43: efeitos sintetizados (geradores do mix60.py) + cama sonora + narração, −14 LUFS, MP4 final 30 fps.
# Uso: python3 mix43.py raw43.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "short60"))
import mix60 as X            # pop, whoosh, impact, riser, chime, lp, st
sys.path.insert(0, HERE)
import short43 as S

SR = X.SR
W = S.load_words()
def wt(txt, start=0):
    for i in range(start, len(W)):
        if W[i][0] == txt: return i
    raise KeyError(txt)
t = lambda i: W[i][1]
iP2 = wt("Perdeu", 1); iP3 = wt("Perdeu", iP2 + 1); iP4 = wt("Perdeu", iP3 + 1)
M = dict(l1=t(wt("10%")), g1=t(wt("11%.")), l2=t(iP2 + 1), g2=t(wt("25%.")), l3=t(iP3 + 1), g3=t(wt("43%.")), l4=t(iP4 + 1), g4=t(wt("dobrar")),
         bIn=t(wt("descida") - 1) - 0.15, esc=t(wt("escada.")), lad=t(wt("ladeira.")), cIn=t(wt("E")) - 0.2, dob=t(wt("dobra")), des=t(wt("desce")),
         dIn=t(wt("O")) - 0.2, dia=t(wt("dia")), sem=t(wt("semana,")), esc2=t(wt("escrito")), eIn=t(wt("Proteger")) - 0.2)
SP = W[-1][2] + 0.15
END = SP + S.TAIL
rng = np.random.default_rng(43)

def bed():
    n = int(SR * END); tt = np.arange(n) / SR; sig = np.zeros(n)
    for kk, f in enumerate([55.0, 82.41, 110.0, 164.81]):
        for det in (-0.6, 0.6):
            p0 = rng.uniform(0, 2 * np.pi)
            sig += np.sin(2 * np.pi * (f + det) * tt + p0) * (0.5 if kk < 2 else 0.25) + 0.18 * np.sin(4 * np.pi * (f + det) * tt + p0)
    air = X.lp(rng.normal(0, 1, n), 0.02)
    sig = sig / np.abs(sig).max() + air / np.abs(air).max() * 0.25
    swell = 1 + 0.5 * np.exp(-((tt - M['l4']) / 1.4) ** 2) + 0.5 * np.exp(-((tt - M['des']) / 1.4) ** 2) + 0.3 * np.exp(-((tt - M['esc2']) / 1.4) ** 2)
    out = sig * (0.85 + 0.15 * np.sin(2 * np.pi * 0.12 * tt)) * swell * np.clip(tt / 1.2, 0, 1) * np.clip((END - tt) / 2.2, 0, 1)
    out = out / np.abs(out).max() * 0.5
    return np.stack([out, out * 0.98], 1).astype(np.float32)

def place(track, clip, at, gain=1.0):
    i = int(at * SR)
    if i < 0: clip = clip[-i:]; i = 0
    j = min(track.shape[0], i + clip.shape[0]); track[i:j] += clip[: j - i] * gain

def main(raw, out):
    fx = np.zeros((int(SR * END), 2), np.float32)
    WH, IM = X.whoosh(), X.impact()
    place(fx, X.pop(1500), 0.05, 0.5); place(fx, X.pop(2300, 0.12, 0.2), 0.3, 0.4)
    for i, k in enumerate(["l1", "l2", "l3", "l4"]): place(fx, IM, M[k], 0.35 + 0.15 * i)
    for i, k in enumerate(["g1", "g2", "g3", "g4"]): place(fx, X.pop(1600 + 200 * i), M[k], 0.45)
    for k in ("bIn", "cIn", "dIn", "eIn"): place(fx, WH, M[k] - 0.3, 0.7)
    R = X.riser(); place(fx, R, M["lad"] + 0.4 - R.shape[0] / SR, 0.35)
    place(fx, X.pop(900, 0.15, 0.3), M["dob"], 0.6); place(fx, IM, M["des"], 1.0)
    place(fx, X.pop(1800), M["dia"], 0.45); place(fx, X.pop(2000), M["sem"], 0.45); place(fx, IM, M["esc2"], 0.5)
    place(fx, IM, SP + 0.05, 0.4); place(fx, X.chime(), SP + 0.6, 0.18)
    b = bed()
    def wav(p, a):
        a = np.clip(a, -1, 1); w = wave.open(p, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()
    wav(os.path.join(HERE, "fx.wav"), fx * 0.8); wav(os.path.join(HERE, "bed.wav"), b)
    fc = ("[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v][vsc];"
          "[2:a]volume=0.16[bd];[bd][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[bdd];[1:a]volume=0.55[fxx];"
          "[v][bdd][fxx]amix=inputs=3:normalize=0:duration=longest,apad,atrim=0:%.2f,loudnorm=I=-14:TP=-1.5:LRA=11[a]" % END)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", os.path.join(HERE, "narr.mp3"), "-i", os.path.join(HERE, "fx.wav"), "-i", os.path.join(HERE, "bed.wav"),
                    "-filter_complex", fc, "-map", "[a]", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", raw, "-i", os.path.join(HERE, "mix.wav"),
                    "-vf", "tmix=frames=2:weights='1 1',select='not(mod(n\\,2))',setpts=N/30/TB,format=yuv420p", "-r", "30", "-map", "0:v", "-map", "1:a", "-t", "%.2f" % END,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("ok", out, END)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
