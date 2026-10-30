# Trilha do Tribunal do Trade #1: efeitos sintetizados + cama + narração (−14 LUFS); gera o MP4 final a 30 fps.
# Uso: python3 mix_tribunal1.py raw.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tribunal1 as T

NARR = os.path.join(HERE, "narracao.mp3")
SR = 48000
ph = lambda i: T.PHRASES[i][2]
SP = ph(len(T.PHRASES) - 1)[1] + 0.2
END = SP + T.TAIL
M = dict(slam1=0.30, reuIn=ph(1)[0] + 0.05, bIn=ph(3)[0] - 0.15, m1=ph(5)[0] + 0.25, m2=ph(7)[0] + 0.05, m3=ph(9)[0] + 0.05,
         c945=ph(3)[0], c950=ph(6)[0], c1000=ph(8)[0], back=ph(10)[0], zero=ph(11)[0], ghost=ph(12)[0], dIn=ph(13)[0] - 0.12,
         slam2=ph(13)[0], mesmo=ph(14)[0], rule=ph(15)[0], eIn=ph(16)[0] - 0.1, com=ph(17)[0])
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
    for k in np.arange(M['bIn'], M['back'], 0.5):
        i = int(k * SR); m = min(n, i + 2400); puls[i:m] += np.sin(2 * np.pi * 70 * np.arange(m - i) / SR) * np.exp(-np.arange(m - i) / SR * 30)
    swell = 1 + 0.5 * np.exp(-((t - M['slam2']) / 1.2) ** 2)
    out = (sig + puls * 0.8) * swell * np.clip(t / 1.0, 0, 1) * np.clip((END - t) / 2.2, 0, 1)
    out = out / np.abs(out).max() * 0.5
    return np.stack([out, out * 0.98], 1).astype(np.float32)

def place(track, clip, at, gain=1.0):
    i = int(at * SR)
    if i < 0: clip = clip[-i:]; i = 0
    j = min(track.shape[0], i + clip.shape[0]); track[i:j] += clip[: j - i] * gain

def main(raw, out):
    fx = np.zeros((int(SR * END), 2), np.float32)
    WH, IM, K = whoosh(), impact(), knock()
    # abertura: martelo (três batidas) + impacto
    place(fx, K, M['slam1'] - 0.02, 0.9); place(fx, IM, M['slam1'], 0.35)
    # réu cai do alto
    place(fx, WH[: int(SR * .35)], M['reuIn'], 0.35); place(fx, pop(700, 0.12, 0.5), M['reuIn'] + 0.45, 0.6)
    for key in ('bIn', 'dIn', 'eIn'): place(fx, WH, M[key] - 0.3, 0.6)
    for key in ('c945', 'c950', 'c1000'): place(fx, tick(), M[key], 0.45)
    for key in ('m1', 'm2', 'm3'): place(fx, boop_down(), M[key], 0.5)
    place(fx, pop(1500), M['back'], 0.45); place(fx, pop(1900), M['zero'], 0.45); place(fx, pop(1200), M['ghost'], 0.45)
    R = riser(); place(fx, R, M['slam2'] - R.shape[0] / SR, 0.35)
    place(fx, K, M['slam2'] - 0.02, 1.0); place(fx, IM, M['slam2'], 0.8)
    place(fx, pop(1600), M['mesmo'], 0.35); place(fx, pop(1700), M['rule'], 0.4)
    place(fx, pop(2000), M['com'], 0.4)
    place(fx, IM, SP + 0.05, 0.35); place(fx, chime(), SP + 0.6, 0.18)
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
