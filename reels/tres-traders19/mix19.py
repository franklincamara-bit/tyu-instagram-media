# Mix do Reel "Mesmo stop, três traders" (TYU-19): narração Rafael Valente (início em 0,3 s) + lápis + efeitos + trilha lo-fi sintetizada.
import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from sfx import *
D = 23.8; N = int(D * SR); buf = np.zeros((N, 2), np.float32)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, 'narr.mp3'), '-ac', '1', '-ar', str(SR), os.path.join(HERE, 'narr.wav')], check=True)
narr = read_wav_mono(os.path.join(HERE, 'narr.wav')); narr /= np.abs(narr).max()
place(buf, st(narr), 0.3, db(-3))
for t0, t1, kind in json.load(open(os.path.join(HERE, 'pen.json'))):
    d = t1 - t0
    if d > 0.02: place(buf, pencil(d), t0, db(-30 if kind == 'path' else -32))
for t in [3.5, 6.15, 10.0, 13.55, 17.4, 20.45]: place(buf, whoosh(0.5), t - 0.1, db(-25))
for t in [4.85, 5.03, 5.21, 7.45, 8.2, 9.3]: place(buf, pop(760, 0.12), t, db(-25))
# batida seca do stop
tt = np.arange(int(SR * 0.4)) / SR
thud = np.sin(2 * np.pi * (48 + 90 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 10)
place(buf, st(thud), 1.92, db(-10)); place(buf, pop(420, 0.18), 2.33, db(-20))
place(buf, chime(), 20.55, db(-18))
BPM = 84; B = 60 / BPM; music = np.zeros(N)
def kick():
    t = np.arange(int(SR * 0.35)) / SR
    return np.sin(2 * np.pi * (55 + 70 * np.exp(-t * 30)) * t) * np.exp(-t * 9)
def snare():
    n = int(SR * 0.22); t = np.arange(n) / SR
    nz = fft_band(rng.normal(0, 1, n), 1500, 7000); nz /= np.abs(nz).max()
    return nz * np.exp(-t * 22) * 0.6
def hat():
    n = int(SR * 0.05); t = np.arange(n) / SR
    nz = fft_band(rng.normal(0, 1, n), 6000, 12000); nz /= np.abs(nz).max()
    return nz * np.exp(-t * 80) * 0.35
def addm(x, t, g=1.0):
    i = int(t * SR)
    if i >= N: return
    m = min(len(x), N - i); music[i:i + m] += x[:m] * g
K, S, H = kick(), snare(), hat()
f = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [[45, 52, 55, 60, 64], [41, 52, 57, 60, 64], [48, 52, 55, 59, 62], [43, 50, 55, 59, 62]]  # Am9 Fmaj7 Cmaj9 G6
TENSE = (10.0, 17.35)
t = 2.3; beat = 0
while t < 20.3:
    bar = beat // 4; pos = beat % 4; tense = TENSE[0] <= t < TENSE[1]; swing = 0.06 * B
    if pos == 0:
        ch = CH[bar % 4]
        for k, m in enumerate(ch): addm(note_epiano(f(m), B * 3.6, 0.5 if k else 0.75), t + k * 0.012, 0.8 if tense else 1.0)
        addm(note_epiano(f(ch[0] - 12), B * 3.8, 0.9), t, 0.9)
    if tense:
        addm(K, t, 1.0); addm(K, t + 0.22, 0.55)
    else:
        if pos in (0, 2): addm(K, t, 0.9)
        if pos in (1, 3): addm(S, t, 0.7)
        addm(H, t, 1.0); addm(H, t + B / 2 + swing, 0.6)
    t += B; beat += 1
for k, m in enumerate([45, 52, 57, 60, 64, 69]): addm(note_epiano(f(m), 3.0, 0.6), 20.45 + k * 0.03, 1.0)
addm(note_epiano(f(33), 3.0, 0.9), 20.45, 1.0)
music = onepole_lp(music / np.abs(music).max(), 5200)
fade = np.ones(N); i0 = int(SR * 2.3); fade[:i0] = 0; fade[i0:i0 + int(SR * 0.6)] = np.linspace(0, 1, int(SR * 0.6)); e0 = int(22.6 * SR); fade[e0:] = np.linspace(1, 0, N - e0) ** 1.5
buf += st(music * fade) * db(-15)
buf /= np.abs(buf).max() * 1.05
write_wav(os.path.join(HERE, 'mix_raw.wav'), buf)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', os.path.join(HERE, 'mix.wav')], check=True)
print('ok')
