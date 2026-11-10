# Trilha do Trial Reel TYU-59 v2.1 (Caixa-Preta #1): efeitos sintetizados + cama + narração, -14 LUFS. Funções de som de ../stop40/mix40.py.
# Uso: python3 mix_cp2.py raw.mp4 saida.mp4
import os, sys, subprocess, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "stop40"))
import cp2 as S
import mix40 as X
NARR = os.path.join(HERE, "narr.mp3")
SR = X.SR
M = S.M
SP = S.END_NARR + 0.25
END = SP + S.TAIL
X.END = END
X.M = {"g57": M["ev"][3], "v2": M["stamp"], "sr": M["dia"]}


def tick():
    t = np.arange(int(SR * 0.04)) / SR
    return X.st(np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 120))


def main(raw, out):
    fx = np.zeros((int(SR * END), 2), np.float32)
    WH, IM = X.whoosh(), X.impact()
    X.place(fx, X.pop(1500), 0.08, 0.5)
    X.place(fx, WH[: int(SR * .4)], M["op"] - 0.1, 0.4); X.place(fx, X.pop(1900), M["op"] + 0.1, 0.4)
    R = X.riser(); X.place(fx, R[: int(SR * 0.9)], M["er"] - 0.6, 0.3); X.place(fx, IM, M["er"], 0.8)
    X.place(fx, WH, M["bIn"] - 0.2, 0.7); X.place(fx, IM, M["open"], 0.5); X.place(fx, X.chime(), M["open"] + 0.05, 0.15)
    X.place(fx, WH, M["cIn"] - 0.3, 0.7)
    t = M["cIn"]
    while t < M["rIn"] - 0.3:
        X.place(fx, tick(), t, 0.05); t += 1.0
    for i, a in enumerate(M["ev"]): X.place(fx, X.pop(1500 + i * 120), a, 0.45 + 0.05 * i)
    X.place(fx, X.pop(1300), M["bub"], 0.35); X.place(fx, X.chime(), M["seal"], 0.12); X.place(fx, IM, M["crack"], 0.45)
    X.place(fx, IM, M["ev"][1], 0.6)
    X.place(fx, WH, M["rIn"] - 0.3, 0.7)
    X.place(fx, R[: int(SR * 0.7)], M["stopT"] - 0.6, 0.25); X.place(fx, IM, M["stopT"] + 0.2, 0.5)
    X.place(fx, X.pop(1200), M["zerar"], 0.6); X.place(fx, IM, M["stamp"], 1.0)
    X.place(fx, R[: int(SR * 1.2)], M["vira"] - 0.2, 0.25); X.place(fx, X.chime(), M["alvo"], 0.16); X.place(fx, X.pop(1700), M["sem"], 0.4)
    X.place(fx, WH, M["xIn"] - 0.3, 0.7); X.place(fx, IM, M["dia"], 0.9)
    X.place(fx, WH, M["qIn"] - 0.3, 0.6); X.place(fx, IM, M["q2"], 0.6)
    X.place(fx, IM, SP + 0.05, 0.4); X.place(fx, X.chime(), SP + 0.6, 0.18)
    b = X.bed()
    def wav(p, a):
        a = np.clip(a, -1, 1); w = wave.open(p, "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((a * 32767).astype(np.int16).tobytes()); w.close()
    wav(os.path.join(HERE, "fx.wav"), fx * 0.8); wav(os.path.join(HERE, "bed.wav"), b)
    fc = ("[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit=2[v][vsc];"
          "[2:a]volume=0.16[bd];[bd][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[bdd];[1:a]volume=0.55[fxx];"
          "[v][bdd][fxx]amix=inputs=3:normalize=0:duration=longest,apad,atrim=0:%.2f,loudnorm=I=-14:TP=-1.5:LRA=11[a]" % END)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", NARR, "-i", os.path.join(HERE, "fx.wav"), "-i", os.path.join(HERE, "bed.wav"),
                    "-filter_complex", fc, "-map", "[a]", "-ar", "48000", os.path.join(HERE, "mix.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", raw, "-i", os.path.join(HERE, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-t", "%.2f" % END, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("ok", out, END)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
