# Trilha do Reel TYU-62 (overtrade, sem narração): efeitos sintetizados + cama de ../stop40/mix40.py, -14 LUFS.
# Uso: python3 mix_ot.py raw.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "stop40"))
import ot as S
import mix40 as X
SR = X.SR; M = S.M; END = S.END
X.END = END
X.M = {"g57": M["ev"][5], "v2": M["dIn"] + 1.4, "sr": M["eIn"]}

def main(raw, out):
    fx = np.zeros((int(SR * END), 2), np.float32)
    WH, IM, R = X.whoosh(), X.impact(), X.riser()
    X.place(fx, IM, M["slam"], 1.0); X.place(fx, X.pop(1400), M["t1"], 0.5)
    for a in (.45, .75, 1.05): X.place(fx, X.pop(1700), a, 0.4)
    X.place(fx, X.pop(1900), M["t2"], 0.4)
    rv = R[::-1].copy(); X.place(fx, rv[: int(SR * 1.0)], M["rew"], 0.35); X.place(fx, WH, M["cIn"] - 0.3, 0.7)
    for i, a in enumerate(M["ev"]): X.place(fx, X.pop(1300 + i * 140), a, 0.45 + 0.06 * i)
    X.place(fx, IM, M["ev"][5], 0.7); X.place(fx, X.chime(), M["curve"], 0.14)
    X.place(fx, WH, M["dIn"] - 0.3, 0.6); X.place(fx, IM, M["d2"], 0.7)
    X.place(fx, WH, M["eIn"] - 0.3, 0.6)
    for i in range(6): X.place(fx, X.pop(1500 + i * 120), M["e2"] + i * .18, 0.35)
    X.place(fx, IM, M["fIn"] + 0.05, 0.4); X.place(fx, X.chime(), M["fIn"] + 0.6, 0.18)
    b = X.bed()
    def wav(p, a):
        a = np.clip(a, -1, 1); w = wave.open(p, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()
    wav(os.path.join(HERE, "fx.wav"), fx * 0.8); wav(os.path.join(HERE, "bed.wav"), b)
    fc = "[1:a]volume=0.5[bd];[0:a]volume=0.7[fxx];[bd][fxx]amix=inputs=2:normalize=0,atrim=0:%.2f,loudnorm=I=-14:TP=-1.5:LRA=11[a]" % END
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", os.path.join(HERE, "fx.wav"), "-i", os.path.join(HERE, "bed.wav"),
                    "-filter_complex", fc, "-map", "[a]", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", raw, "-i", os.path.join(HERE, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-t", "%.2f" % END, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("ok", out, END)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
