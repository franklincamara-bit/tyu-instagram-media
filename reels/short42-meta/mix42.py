# Mix do Short "Bateu a meta às 10h. E depois?" (VID-42): narração Rafael Valente + lápis + whooshes + pops + pad sintetizado.
import json, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from sfx import *
D = 36.8; N = int(D * SR); buf = np.zeros((N, 2), np.float32)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, '..', 'narr.mp3'), '-ac', '1', '-ar', str(SR), os.path.join(HERE, '..', 'narr.wav')], check=True)
narr = read_wav_mono(os.path.join(HERE, '..', 'narr.wav')); narr /= np.abs(narr).max()
place(buf, st(narr), 0.0, db(-3))
for t0, t1, kind in json.load(open(os.path.join(HERE, '..', 'pen.json'))):
    d = t1 - t0
    if d > 0.02: place(buf, pencil(d), t0, db(-28 if kind == 'path' else -30))
for t in [6.4, 11.1, 14.7, 19.0, 25.0, 33.6]: place(buf, whoosh(0.5), t - 0.1, db(-24))
for t in [3.2, 10.0, 13.75, 17.84]: place(buf, pop(760, 0.12), t, db(-24))
for t in [28.9, 30.3, 31.75]: place(buf, pop(1100, 0.1), t, db(-26))
place(buf, chime(), 33.7, db(-17))
A2, C3, E3, G3, F2, D3, G2, B2 = 110.0, 130.81, 164.81, 196.0, 87.31, 146.83, 98.0, 123.47
bed = pad([[C3, E3, G3, B2 * 2], [A2, C3, E3, G3], [F2, A2, C3, E3], [G2, B2, D3, G3]], 4.0, D)
fade = np.ones(N); fade[:SR] = np.linspace(0, 1, SR); fade[-int(SR * 1.5):] = np.linspace(1, 0, int(SR * 1.5))
buf += bed * fade[:, None] * db(-26)
buf /= np.abs(buf).max() * 1.05
write_wav(os.path.join(HERE, '..', 'mix_raw.wav'), buf)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(HERE, '..', 'mix_raw.wav'), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', os.path.join(HERE, '..', 'mix.wav')], check=True)
print('ok')
