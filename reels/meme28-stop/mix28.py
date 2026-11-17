# Mix do Meme #1 (TYU-28): sem narração. Fase A lo-fi calma, scratch + batida seca no STOP, fase B batida acelerada com pops nas figurinhas, fim com acorde e chime. -14 LUFS.
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from sfx import *
D = 10.6; N = int(D * SR); buf = np.zeros((N, 2), np.float32); music = np.zeros(N)
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def addm(x, t, g=1.0):
    i = int(t * SR)
    if i >= N: return
    m = min(len(x), N - i); music[i:i + m] += x[:m] * g
def kick():
    t = np.arange(int(SR * 0.3)) / SR
    return np.sin(2 * np.pi * (55 + 80 * np.exp(-t * 30)) * t) * np.exp(-t * 10)
def hat():
    n = int(SR * 0.05); t = np.arange(n) / SR
    nz = fft_band(rng.normal(0, 1, n), 6000, 12000); nz /= np.abs(nz).max(); return nz * np.exp(-t * 80) * 0.35
def snare():
    n = int(SR * 0.2); t = np.arange(n) / SR
    nz = fft_band(rng.normal(0, 1, n), 1500, 7000); nz /= np.abs(nz).max(); return nz * np.exp(-t * 22) * 0.6
K, H, S = kick(), hat(), snare()
# fase A: Cmaj9 / Am9 tranquilos, 84 bpm
B = 60 / 84; t = 0.0; k = 0
for ch in [[48, 55, 59, 62, 64], [45, 52, 55, 59, 64]]:
    for j, m in enumerate(ch): addm(note_epiano(f(m), B * 3.8, 0.55 if j else 0.8), t + j * 0.015)
    for b in range(4):
        tb = t + b * B
        if tb < 2.5:
            if b in (0, 2): addm(K, tb, 0.8)
            if b in (1, 3): addm(S, tb, 0.5)
            addm(H, tb, 0.8); addm(H, tb + B / 2, 0.5)
    t += 4 * B
music[int(2.5 * SR):] = 0
# fase B: 140 bpm tenso (Dm / Bb / A)
B2 = 60 / 140; t = 3.05; beat = 0
CH = [[50, 53, 57, 62], [46, 50, 53, 58], [45, 49, 52, 57], [45, 49, 52, 57]]
while t < 8.0:
    if beat % 4 == 0:
        for j, m in enumerate(CH[(beat // 4) % 4]): addm(note_epiano(f(m), B2 * 3.6, 0.6), t + j * 0.01, 0.9)
        addm(note_epiano(f(CH[(beat // 4) % 4][0] - 12), B2 * 3.8, 0.9), t, 0.9)
    addm(K, t, 1.0)
    if beat % 2 == 1: addm(S, t, 0.7)
    addm(H, t + B2 / 2, 0.7)
    t += B2; beat += 1
# fim: acorde resolvido
for j, m in enumerate([41, 48, 52, 55, 60, 64]): addm(note_epiano(f(m), 2.4, 0.6), 8.1 + j * 0.03)
music = onepole_lp(music / np.abs(music).max(), 6000)
fade = np.ones(N); e0 = int(9.9 * SR); fade[e0:] = np.linspace(1, 0, N - e0) ** 1.5
buf += st(music * fade) * db(-12)
# scratch (varredura descendente) e batida seca no STOP
n = int(SR * 0.35); tt = np.arange(n) / SR
scr = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-tt * 9) + 80) / SR) * np.exp(-tt * 4) * 0.6
nz = fft_band(rng.normal(0, 1, n), 800, 5000); scr += nz / np.abs(nz).max() * np.exp(-tt * 10) * 0.3
place(buf, st(scr), 2.38, db(-14))
tt = np.arange(int(SR * 0.45)) / SR
thud = np.sin(2 * np.pi * (45 + 100 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 9)
place(buf, st(thud), 2.55, db(-6)); place(buf, pop(380, 0.2), 2.57, db(-16))
place(buf, whoosh(0.4), 2.95, db(-20)); place(buf, whoosh(0.5), 7.95, db(-20))
for tp in [3.45, 4.55, 5.75, 6.9]: place(buf, pop(820, 0.12), tp, db(-18))
for tp in [5.15, 7.35]: place(buf, pop(300, 0.18), tp, db(-16))
place(buf, chime(), 8.3, db(-18))
buf /= np.abs(buf).max() * 1.05
write_wav(os.path.join(HERE, 'mix_raw.wav'), buf)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', os.path.join(HERE, 'mix.wav')], check=True)
print('ok')
