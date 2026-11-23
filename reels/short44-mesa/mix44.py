# Trilha do Short VID-44: efeitos sintetizados (geradores do mix60.py) + cama sonora + narração, −14 LUFS, MP4 final 30 fps.
# Uso: python3 mix44.py raw44.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "short60"))
import mix60 as X            # pop, whoosh, impact, riser, chime, lp, st
sys.path.insert(0, HERE)
import short44 as S

SR = X.SR
W = S.load_words()
def wt(txt, start=0):
    for i in range(start, len(W)):
        if W[i][0] == txt: return i
    raise KeyError(txt)
t = lambda i: W[i][1]
M = dict(m53=t(wt("53")), m2=t(wt("2")), sob=t(wt("sobe")), m51=t(wt("51")), dev=t(wt("devolução")), vol=t(wt("volta.")) + 0.15,
         enc=t(wt("encerrada.")), luc=t(wt("lucro.")), des=t(wt("desce")), aIn=t(wt("Só")) - 0.2, bIn=t(wt("Aí")) - 0.2,
         dIn=t(wt("Antes")) - 0.2, pico=t(wt("Pico")), lim=t(wt("limite.")), esp=t(wt("espaço")), eIn=t(wt("E", 80)) - 0.2)
SP = W[-1][2] + 0.15
END = SP + S.TAIL
rng = np.random.default_rng(44)

def bed():
    n = int(SR * END); tt = np.arange(n) / SR; sig = np.zeros(n)
    for kk, f in enumerate([55.0, 82.41, 110.0, 164.81]):
        for det in (-0.6, 0.6):
            p0 = rng.uniform(0, 2 * np.pi)
            sig += np.sin(2 * np.pi * (f + det) * tt + p0) * (0.5 if kk < 2 else 0.25) + 0.18 * np.sin(4 * np.pi * (f + det) * tt + p0)
    air = X.lp(rng.normal(0, 1, n), 0.02)
    sig = sig / np.abs(sig).max() + air / np.abs(air).max() * 0.25
    swell = 1 + 0.5 * np.exp(-((tt - M['vol']) / 1.4) ** 2) + 0.4 * np.exp(-((tt - M['enc']) / 1.4) ** 2) + 0.3 * np.exp(-((tt - M['esp']) / 1.4) ** 2)
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
    place(fx, X.pop(1500), 0.02, 0.5); place(fx, IM, 0.25, 0.6); place(fx, X.pop(2300, 0.12, 0.2), 0.5, 0.45)
    place(fx, WH, 1.15, 0.8)
    place(fx, X.pop(1700), M["m2"], 0.4); place(fx, X.pop(2100), M["m53"], 0.5)
    place(fx, X.pop(1900), M["sob"], 0.45); place(fx, X.pop(1500), M["m51"], 0.45)
    R = X.riser(); place(fx, R, M["vol"] - R.shape[0] / SR, 0.35)
    place(fx, WH, M["dev"] - 0.3, 0.5); place(fx, IM, M["vol"], 1.0); place(fx, IM, M["enc"], 0.7); place(fx, X.pop(1600), M["luc"], 0.45)
    place(fx, X.pop(900, 0.15, 0.3), M["des"], 0.5)
    for k in ("dIn", "eIn"): place(fx, WH, M[k] - 0.3, 0.7)
    place(fx, X.pop(1800), M["pico"], 0.45); place(fx, X.pop(2000), M["lim"], 0.45); place(fx, IM, M["esp"], 0.5)
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
