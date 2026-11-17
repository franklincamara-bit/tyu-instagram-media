# Efeitos e trilhas sintetizados (sem material de terceiros).
import numpy as np
import subprocess, wave

SR = 48000
rng = np.random.default_rng(7)


def st(x):
    return np.stack([x, x], 1).astype(np.float32)


def onepole_lp(x, fc):
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(x.size):
        acc += a * (x[i] - acc); y[i] = acc
    return y


def fft_band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(x.size, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, x.size)


def place(buf, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf): return
    n = min(len(clip), len(buf) - i)
    buf[i:i + n] += clip[:n] * gain


def pencil(dur):
    n = max(1, int(dur * SR)); t = np.arange(n) / SR
    nz = fft_band(rng.normal(0, 1, n), 1800, 7500)
    nz /= np.abs(nz).max() + 1e-9
    # traço: grão de ~14 Hz com variação
    grain = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (11 + 6 * rng.random()) * t + rng.random() * 6))
    env = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.03).clip(0, 1)
    return st(nz * grain * env)


def whoosh(dur=0.5):
    n = int(SR * dur); t = np.arange(n) / SR
    nz = fft_band(rng.normal(0, 1, n), 300, 4000)
    nz /= np.abs(nz).max()
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return st(nz * e)


def pop(freq=900, dur=0.12):
    t = np.arange(int(SR * dur)) / SR
    s = np.sin(2 * np.pi * freq * t * (1 + 0.6 * t / dur)) * np.exp(-t * 38)
    return st(s)


def chime(freqs=(1046.5, 1318.5, 1568.0), dur=1.8):
    t = np.arange(int(SR * dur)) / SR
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2.5 + k)) for k, f in enumerate(freqs))
    s += 0.3 * sum(np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6) for f in freqs)
    return st(s / np.abs(s).max())


def note_epiano(f, dur, vel=1.0):
    n = int(SR * dur); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3) + 0.12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 6))
    env = np.minimum(1, t / 0.008) * np.exp(-t * 1.4)
    rel = np.minimum(1, (dur - t) / 0.08).clip(0, 1)
    return s * env * rel * vel


def pad(chords, beat_len, total, gain=1.0):
    """chords: lista de listas de freqs, cada acorde dura beat_len segundos; repete até total."""
    n = int(total * SR); out = np.zeros(n)
    t = 0.0; k = 0
    while t < total:
        ch = chords[k % len(chords)]
        seg = int(beat_len * SR); tt = np.arange(seg) / SR
        s = np.zeros(seg)
        for f in ch:
            det = 1.003
            s += np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * det * tt + 1) + 0.18 * np.sin(2 * np.pi * 2 * f * tt)
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (beat_len - tt) / 0.6).clip(0, 1)
        s *= env
        i = int(t * SR); m = min(seg, n - i)
        out[i:i + m] += s[:m]
        t += beat_len; k += 1
    out = onepole_lp(out / (np.abs(out).max() + 1e-9), 1400)
    return st(out / np.abs(out).max() * gain)


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def read_wav_mono(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def db(x): return 10 ** (x / 20)
