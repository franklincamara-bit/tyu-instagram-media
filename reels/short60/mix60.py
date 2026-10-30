# Trilha do Short 60%: efeitos sintetizados + cama sonora + narração; gera o MP4 final a 30 fps.
# Uso: python3 mix60.py raw60.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import short60 as S

HERE = os.path.dirname(os.path.abspath(__file__))
NARR = os.path.join(HERE, "narr.mp3")
SR = 48000
PH = S.load_phrases()
W, _ = S.words_and_groups(PH)
PW = []; k = 0
for c, _x in S.PHRASES: PW.append(k); k += len(c.split())
wa = lambda p, j: W[PW[p] + j][1]
ph = lambda i: PH[i]
SP = PH[-1][1] + 0.1
END = SP + S.TAIL
M = dict(cai=wa(0, 10), faz=ph(1)[0], bIn=ph(1)[1] + 0.15, gIn=ph(2)[0] + 0.1, rIn=ph(3)[0] + 0.05, cnt=ph(4)[0], tot=ph(5)[0],
         cIn=ph(6)[0] - 0.1, cgIn=ph(7)[0] + 0.15, crIn=wa(7, 7), ccnt=ph(8)[0], ctot=ph(9)[0], cmp=ph(9)[1] + 0.1,
         dIn=ph(10)[0] + 1.1, n67=wa(10, 8), eIn=ph(11)[0] - 0.15)
rng = np.random.default_rng(5)


def env_exp(n, rate): return np.exp(-np.arange(n) / SR * rate)
def st(x): return np.stack([x, x], 1).astype(np.float32)

def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i in range(x.size): acc += a * (x[i] - acc); y[i] = acc
    return y

def pop(freq=1800, dur=0.09, noise=0.35):
    t = np.arange(int(SR * dur)) / SR
    s = (np.sin(2 * np.pi * freq * t * (1 - 0.35 * t / dur)) * 0.7 + rng.normal(0, 1, t.size) * np.exp(-t * 160) * noise) * np.exp(-t * 55)
    return st(s)

def whoosh(dur=0.6):
    n = int(SR * dur); t = np.arange(n) / SR
    nz = rng.normal(0, 1, n)
    sw = np.concatenate([lp(nz[: n // 2], 0.04), lp(nz[n // 2:], 0.12)])
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return st(sw / np.abs(sw).max() * e)

def impact(dur=0.9):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 90 * np.exp(-t * 4) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)
    hit = lp(rng.normal(0, 1, n), 0.25) * np.exp(-t * 30)
    s = body * 0.9 + hit / np.abs(hit).max() * 0.6
    return st(s / np.abs(s).max())

def riser(dur=1.6):
    n = int(SR * dur); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / dur) ** 2) / SR) * 0.4 + lp(rng.normal(0, 1, n), 0.05) * 3
    s *= (t / dur) ** 2
    return st(s / np.abs(s).max())

def chime():
    t = np.arange(int(SR * 1.4)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in [(1318.5, .5), (1975.5, .3), (2637, .15)]) * np.exp(-t * 3.5)
    return st(s / np.abs(s).max())

def bed():
    n = int(SR * END); t = np.arange(n) / SR
    sig = np.zeros(n)
    for kk, f in enumerate([55.0, 82.41, 110.0, 164.81]):
        for det in (-0.6, 0.6):
            p0 = rng.uniform(0, 2 * np.pi)
            sig += np.sin(2 * np.pi * (f + det) * t + p0) * (0.5 if kk < 2 else 0.25) + 0.18 * np.sin(4 * np.pi * (f + det) * t + p0)
    air = lp(rng.normal(0, 1, n), 0.02)
    sig = sig / np.abs(sig).max() + air / np.abs(air).max() * 0.25
    swell = 1 + 0.5 * np.exp(-((t - M['tot']) / 1.4) ** 2) + 0.5 * np.exp(-((t - M['ctot']) / 1.4) ** 2) + 0.4 * np.exp(-((t - M['n67']) / 1.4) ** 2)
    out = sig * (0.85 + 0.15 * np.sin(2 * np.pi * 0.12 * t)) * swell * np.clip(t / 1.2, 0, 1) * np.clip((END - t) / 2.2, 0, 1)
    out = out / np.abs(out).max() * 0.5
    return np.stack([out, out * 0.98], 1).astype(np.float32)

def place(track, clip, at, gain=1.0):
    i = int(at * SR)
    if i < 0: clip = clip[-i:]; i = 0
    j = min(track.shape[0], i + clip.shape[0]); track[i:j] += clip[: j - i] * gain

def tiles(fx, gs, n, dur, f0):
    for i in range(0, n, 3):
        place(fx, pop(f0 + (i % 9) * 40, 0.05, 0.6), gs + dur * i / n + 0.32, 0.22)

def main(raw, out):
    fx = np.zeros((int(SR * END), 2), np.float32)
    WH, IM = whoosh(), impact()
    place(fx, pop(1500), 0.12, 0.5); place(fx, pop(2300, 0.12, 0.2), 0.6, 0.5); place(fx, WH[: int(SR * .4)], 0.8, 0.35)
    place(fx, IM, M['cai'], 0.45)
    place(fx, IM, M['faz'], 0.8)
    for key in ('bIn', 'cIn', 'cmp', 'dIn', 'eIn'): place(fx, WH, M[key] - 0.3, 0.7)
    # peças caindo (mesma regra de duração do HTML)
    gdA = max(0.9, min(1.8, M['rIn'] - M['gIn'] - 0.25)); rdA = max(0.9, min(1.8, M['cnt'] + 0.3 - M['rIn']))
    tiles(fx, M['gIn'], 60, gdA, 1700); tiles(fx, M['rIn'], 40, rdA, 900)
    gdB = max(0.9, min(1.8, M['crIn'] - M['cgIn'] - 0.25)); rdB = max(0.9, min(1.8, M['ccnt'] + 0.3 - M['crIn']))
    tiles(fx, M['cgIn'], 40, gdB, 1700); tiles(fx, M['crIn'], 60, rdB, 900)
    place(fx, IM, M['tot'], 1.0); place(fx, IM, M['ctot'], 1.0)
    R = riser(); place(fx, R, M['n67'] - R.shape[0] / SR, 0.45); place(fx, IM, M['n67'] + 0.2, 0.7)
    pa = (M['eIn'] + 0.15) + (SP - M['eIn'] - 0.15) * 0.45
    for i, a in enumerate([pa + .3, pa + .65, pa + 1.0]): place(fx, pop(1700 + i * 150), a, 0.4)
    place(fx, IM, SP + 0.05, 0.4); place(fx, chime(), SP + 0.6, 0.18)
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
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-profile:v", "high", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    print("ok", out, END, M)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
