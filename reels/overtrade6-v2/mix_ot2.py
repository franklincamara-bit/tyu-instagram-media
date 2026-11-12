# Mix do Reel "Overtrade: a curva das decisões" v2 (TYU-62): narração Rafael Valente + lápis + trilha lo-fi sintetizada (nova, diferente da cama de pad dos outros vídeos).
import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from sfx import *
D = 39.0; N = int(D * SR); buf = np.zeros((N, 2), np.float32)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, 'narr.mp3'), '-ac', '1', '-ar', str(SR), os.path.join(HERE, 'narr.wav')], check=True)
narr = read_wav_mono(os.path.join(HERE, 'narr.wav')); narr /= np.abs(narr).max()
place(buf, st(narr), 0.0, db(-3))
for t0, t1, kind in json.load(open(os.path.join(HERE, 'pen.json'))):
    d = t1 - t0
    if d > 0.02: place(buf, pencil(d), t0, db(-30 if kind == 'path' else -32))
for t in [8.35, 18.65, 23.3, 29.55, 35.8]: place(buf, whoosh(0.5), t - 0.1, db(-25))
for t in [1.57, 8.47, 11.31, 13.8, 16.65, 18.74]: place(buf, pop(700, 0.12), t, db(-25))
place(buf, chime(), 35.9, db(-18))

# ---- trilha lo-fi 80 bpm ----
BPM = 80; B = 60 / BPM; music = np.zeros(N)
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
CH = [[50, 53, 57, 60, 64], [43, 53, 57, 59, 64], [48, 52, 55, 59, 62], [45, 52, 55, 60, 64]]  # Dm9 G13 Cmaj9 Am7(add9)
TENSE = (18.65, 23.3); CALM = 29.55
t = 0.0; beat = 0
while t < 35.6:
    bar = beat // 4; pos = beat % 4
    tense = TENSE[0] <= t < TENSE[1]; calm = t >= CALM
    swing = 0.06 * B
    if not tense:
        if pos == 0:
            ch = CH[bar % 4]
            for k, m in enumerate(ch):
                addm(note_epiano(f(m), B * 3.6, 0.55 if k else 0.8), t + k * 0.012, 1.0)
            addm(note_epiano(f(ch[0] - 12), B * 3.8, 0.9), t, 0.9)
        if pos == 2 and not calm:
            addm(note_epiano(f(CH[bar % 4][-1] + 12), B * 0.9, 0.35), t + swing, 1.0)
        if not calm and t > 1.5:
            if pos in (0, 2): addm(K, t, 0.9)
            if pos in (1, 3): addm(S, t, 0.7)
            addm(H, t, 1.0); addm(H, t + B / 2 + swing, 0.6)
    else:
        addm(K, t, 1.0)  # pulso de coração
        addm(K, t + 0.22, 0.55)
    t += B; beat += 1
for k, m in enumerate([48, 52, 55, 59, 62, 67]): addm(note_epiano(f(m), 3.0, 0.6), 35.8 + k * 0.03, 1.0)
addm(note_epiano(f(36), 3.0, 0.9), 35.8, 1.0)
# tensão: drone grave + riser no trade 6
n0, n1 = int(TENSE[0] * SR), int(TENSE[1] * SR); tt = np.arange(n1 - n0) / SR
drone = (np.sin(2 * np.pi * f(38) * tt) + 0.5 * np.sin(2 * np.pi * f(38) * 1.5 * tt)) * np.minimum(1, tt / 0.8) * np.minimum(1, (tt[-1] - tt) / 0.4)
music[n0:n1] += drone * 0.5
rs = fft_band(rng.normal(0, 1, n1 - n0), 800, 6000); rs /= np.abs(rs).max()
music[n0:n1] += rs * (tt / tt[-1]) ** 3 * 0.25
music = onepole_lp(music / np.abs(music).max(), 5200)
fade = np.ones(N); fade[:int(SR * 0.6)] = np.linspace(0, 1, int(SR * 0.6)); e0 = int(37.2 * SR); fade[e0:] = np.linspace(1, 0, N - e0) ** 1.5
buf += st(music * fade) * db(-15)
buf /= np.abs(buf).max() * 1.05
write_wav(os.path.join(HERE, 'mix_raw.wav'), buf)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', os.path.join(HERE, 'mix.wav')], check=True)
print('ok')
