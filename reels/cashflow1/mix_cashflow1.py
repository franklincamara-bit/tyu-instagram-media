# Trilha do Reel Cash Flow (TYU-52): efeitos sintetizados + cama + narração (−14 LUFS); gera o MP4 final a 30 fps.
# Uso: python3 mix_cashflow1.py raw.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cashflow1 as T

NARR = os.path.join(HERE, "narracao.mp3")
SR = 48000
ph = lambda i: T.PHRASES[i][2]
W, G, PW = T.words_and_groups()
wa = lambda p, j: W[PW[p] + j][1]
SP = ph(16)[0] - 0.15
END = ph(16)[1] + T.TAIL
M = dict(ok=0.55, conf=ph(1)[0], prIn=ph(2)[0] + 0.6, bIn=ph(2)[1] - 0.35, l0=ph(3)[0], v0=ph(4)[0], l1=ph(5)[0], v1=ph(6)[0],
         l2=ph(7)[0], v2=wa(7, 3), l3=ph(8)[0], v3=wa(8, 6), sep=ph(9)[0], tot=ph(10)[0], st=ph(11)[0], cIn=ph(12)[0] - 0.2,
         slide=ph(12)[0] + 0.2, nz=ph(13)[0], dIn=ph(14)[0] - 0.2, rec=wa(14, 9), cf=wa(15, 3))
rng = np.random.default_rng(7)


def st(x): return np.stack([x, x], 1).astype(np.float32)

def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i in range(x.size): acc += a * (x[i] - acc); y[i] = acc
    return y

def pop(freq=1800, dur=0.09, noise=0.35):
    t = np.arange(int(SR * dur)) / SR
    s = (np.sin(2 * np.pi * freq * t * (1 - 0.35 * t / dur)) * 0.7 + rng.normal(0, 1, t.size) * np.exp(-t * 160) * noise) * np.exp(-t * 55)
    return st(s)

def boop_down(f0=520, dur=0.32):
    t = np.arange(int(SR * dur)) / SR
    f = f0 * np.exp(-t * 3.2)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return st(s / np.abs(s).max())

def whoosh(dur=0.6):
    n = int(SR * dur); t = np.arange(n) / SR
    nz = rng.normal(0, 1, n)
    sw = np.concatenate([lp(nz[: n // 2], 0.04), lp(nz[n // 2:], 0.12)])
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return st(sw / np.abs(sw).max() * e)

def knock(dur=0.45):
    # martelo de juiz: batida de madeira (corpo grave + estalo)
    n = int(SR * dur); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 150 * t) * np.exp(-t * 28) + 0.6 * np.sin(2 * np.pi * 310 * t) * np.exp(-t * 40)
    click = lp(rng.normal(0, 1, n), 0.5) * np.exp(-t * 180)
    s = body + click / np.abs(click).max() * 0.8
    return st(s / np.abs(s).max())

def impact(dur=0.9):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 90 * np.exp(-t * 4) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    hit = lp(rng.normal(0, 1, n), 0.25) * np.exp(-t * 30)
    s = body * 0.9 + hit / np.abs(hit).max() * 0.6
    return st(s / np.abs(s).max())

def riser(dur=1.2):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / dur) ** 2) / SR) * 0.4 + lp(rng.normal(0, 1, n), 0.05) * 3
    s *= (t / dur) ** 2
    return st(s / np.abs(s).max())

def chime():
    t = np.arange(int(SR * 1.4)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1318.5, .5), (1975.5, .3), (2637, .15)]) * np.exp(-t * 3.5)
    return st(s / np.abs(s).max())

def tick():
    t = np.arange(int(SR * 0.05)) / SR
    return st(np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 120))

def bed():
    n = int(SR * END); t = np.arange(n) / SR
    sig = np.zeros(n)
    for kk, f in enumerate([55.0, 65.41, 82.41, 130.81]):  # lá menor com tensão (tribunal)
        for det in (-0.5, 0.5):
            p0 = rng.uniform(0, 2 * np.pi)
            sig += np.sin(2 * np.pi * (f + det) * t + p0) * (0.5 if kk < 2 else 0.22) + 0.15 * np.sin(4 * np.pi * (f + det) * t + p0)
    air = lp(rng.normal(0, 1, n), 0.02)
    sig = sig / np.abs(sig).max() + air / np.abs(air).max() * 0.25
    # pulso discreto tipo relógio durante a acusação
    puls = np.zeros(n)
    for k in np.arange(M['bIn'], M['cIn'], 0.5):
        i = int(k * SR); m = min(n, i + 2400); puls[i:m] += np.sin(2 * np.pi * 70 * np.arange(m - i) / SR) * np.exp(-np.arange(m - i) / SR * 30)
    swell = 1 + 0.5 * np.exp(-((t - M['st']) / 1.2) ** 2)
    out = (sig + puls * 0.8) * swell * np.clip(t / 1.0, 0, 1) * np.clip((END - t) / 2.2, 0, 1)
    out = out / np.abs(out).max() * 0.5
    return np.stack([out, out * 0.98], 1).astype(np.float32)

def place(track, clip, at, gain=1.0):
    i = int(at * SR)
    if i < 0: clip = clip[-i:]; i = 0
    j = min(track.shape[0], i + clip.shape[0]); track[i:j] += clip[: j - i] * gain

def printer(dur=0.5):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.zeros(n)
    for k in np.arange(0, dur, 0.035):
        i = int(k * SR); m = min(n, i + 700); s[i:m] += lp(rng.normal(0, 1, m - i), 0.5) * np.exp(-np.arange(m - i) / SR * 260)
    s += np.sin(2 * np.pi * 95 * t) * 0.25
    s *= np.clip(t / 0.03, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
    return st(s / np.abs(s).max())

def ding():
    t = np.arange(int(SR * 1.2)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1046.5, .6), (1568, .3), (2093, .12)]) * np.exp(-t * 4)
    return st(s / np.abs(s).max())

def main(raw, out):
    fx = np.zeros((int(SR * END), 2), np.float32)
    WH, IM, K = whoosh(), impact(), knock()
    place(fx, K, M['ok'] - 0.02, 0.8); place(fx, IM, M['ok'], 0.3)
    for i in range(6): place(fx, pop(1500 + i * 180, 0.07, 0.6), M['conf'] + i * 0.05, 0.22)
    place(fx, WH, M['prIn'] - 0.2, 0.45); place(fx, WH, M['bIn'] - 0.2, 0.5)
    place(fx, printer(0.5), M['bIn'], 0.4)
    for a, b in [('l0', 'v0'), ('l1', 'v1'), ('l2', 'v2'), ('l3', 'v3')]:
        place(fx, printer(0.55), M[a], 0.45); place(fx, pop(1700), M[b], 0.45)
    place(fx, printer(0.5), M['sep'], 0.4)
    for k in np.arange(M['tot'], M['tot'] + 1.3, 0.07): place(fx, tick(), k, 0.25)
    place(fx, ding(), M['tot'] + 1.3, 0.3)
    R = riser(); place(fx, R, M['st'] - R.shape[0] / SR, 0.3)
    place(fx, K, M['st'] - 0.02, 1.0); place(fx, IM, M['st'], 0.7)
    place(fx, WH, M['cIn'] - 0.2, 0.55); place(fx, boop_down(420, 0.9), M['slide'], 0.35); place(fx, pop(900, 0.12, 0.5), M['nz'], 0.5)
    place(fx, WH, M['dIn'] - 0.2, 0.55)
    for i in range(5): place(fx, pop(1400 + i * 120), M['dIn'] + 0.5 + i * 0.45, 0.3)
    place(fx, pop(2000), M['rec'], 0.35); place(fx, pop(2100), M['cf'], 0.4)
    place(fx, WH, SP - 0.3, 0.45); place(fx, IM, SP + 0.05, 0.3); place(fx, chime(), SP + 0.9, 0.18)
    b = bed()
    def wav(p, a):
        a = np.clip(a, -1, 1); w = wave.open(p, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()
    wav(os.path.join(HERE, "fx.wav"), fx * 0.8); wav(os.path.join(HERE, "bed.wav"), b)
    fc = ("[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v][vsc];"
          "[2:a]volume=0.16[bd];[bd][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[bdd];[1:a]volume=0.55[fxx];"
          "[v][bdd][fxx]amix=inputs=3:normalize=0:duration=longest,apad,atrim=0:%.2f,loudnorm=I=-14:TP=-1.5:LRA=11[a]" % END)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", NARR, "-i", os.path.join(HERE, "fx.wav"), "-i", os.path.join(HERE, "bed.wav"),
                    "-filter_complex", fc, "-map", "[a]", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", raw, "-i", os.path.join(HERE, "mix.wav"),
                    "-vf", "tmix=frames=2:weights='1 1',select='not(mod(n\\,2))',setpts=N/30/TB,format=yuv420p", "-r", "30", "-map", "0:v", "-map", "1:a", "-t", "%.2f" % END,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("ok", out, END)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
