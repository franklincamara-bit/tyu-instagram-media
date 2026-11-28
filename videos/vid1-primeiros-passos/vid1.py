"""VID-1 — Primeiros passos: as 3 listas antes do primeiro trade (produção 28/11/2026).
Motor: render.py (tutorial-narrado-v2) + avatar-guia (cópia do vid3.py).
Prints 800x600 da conta de teste em src/ (rodapé e nomes de setups trocados no DOM só para o print; nada salvo).
Narração: narr-elevenlabs.mp3 (Rafael Valente, elevenlabs.io) cortada em audio/s1..s5.wav.
Uso: python3 vid1.py [cena ...] | end | all
"""
import os, sys, subprocess, glob, math
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R

R.UP = os.path.join(HERE, "up"); R.AUD = os.path.join(HERE, "audio"); R.OUT = os.path.join(HERE, "out")
os.makedirs(R.OUT, exist_ok=True)
R.LOGO = os.path.join(HERE, "logo.png")
R.NEXT_TITLE = "Como cadastrar seus setups"
AVDIR = os.path.join(HERE, "avatar")

def load(name):
    src = glob.glob(os.path.join(HERE, "src", name + ".*"))[0]
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))

NAMES = ["dash", "menu", "setups", "erros", "falhas", "nt-topo", "nt-detalhes"]
def shots():
    return R.Lazy({n: (lambda n=n: dict(img=load(n), dark=False, chrome="browser")) for n in NAMES})

def c(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

CARDS = (238, 203, 750, 297)
MENU = (19, 140, 170, 495); CONFIG = (19, 143, 169, 168); M_SET = (27, 209, 151, 238); M_ERR = (27, 293, 151, 322)
M_FAL = (27, 329, 151, 371); M_NT8 = (27, 449, 151, 492)
S_LIST = (238, 133, 762, 507); S_IMP = (504, 66, 666, 95); S_NOVO = (673, 66, 782, 95)
E_LIST = (238, 133, 750, 597); E_NOVO = (670, 66, 770, 95); E_TOP = (238, 133, 750, 314)
F_LIST = (238, 133, 750, 597); F_NOVO = (665, 66, 770, 95); F_TOP = (238, 133, 750, 314)
SETUPF = (504, 357, 716, 401); DISC = (505, 265, 750, 335); ERRO = (251, 505, 740, 578)
FM = (0, 135, 470, 505)

def scenes():
    return [
        dict(where="Dashboard", title="3 listas antes do 1º trade", audio="s1.wav", av=dict(side="right", bub=[(1.7, "3 listas!")]), beats=[
            dict(t=0.0, shot="dash", hl=[], focus=(200, 50, 790, 320), cap="Conta criada?"),
            dict(t=1.4, shot="dash", hl=[], focus=(220, 180, 770, 320), cap="Antes do primeiro trade, monte três listas."),
            dict(t=4.4, shot="menu", hl=[M_SET, M_ERR, M_FAL], focus=FM, cap="São elas que fazem a plataforma entender o seu jeito de operar."),
        ]),
        dict(where="Configurações", title="1 · Setups", audio="s2.wav", av=dict(side="right", bub=[(4.8, "1 · Setups")]), beats=[
            dict(t=0.0, shot="menu", hl=[CONFIG], focus=FM, cap="Todas ficam em Configurações, no fim do menu."),
            dict(t=3.2, shot="menu", hl=[M_SET], click=c(M_SET), focus=FM, cap="Primeiro, os seus setups: as entradas que você aceita fazer."),
            dict(t=4.6, shot="setups", hl=[S_LIST], focus=(200, 50, 790, 520), cap="Primeiro, os seus setups: as entradas que você aceita fazer."),
            dict(t=7.27, shot="setups", hl=[S_NOVO, S_IMP], click=c(S_NOVO), focus=(430, 40, 790, 230), cap="Crie os seus em Novo Setup, ou importe um modelo da biblioteca."),
        ]),
        dict(where="Configurações", title="2 · Erros", audio="s3.wav", av=dict(side="right", bub=[(1.8, "2 · Erros")]), beats=[
            dict(t=0.0, shot="menu", hl=[M_ERR], click=c(M_ERR), focus=FM, cap="Depois, os erros de execução que você mais comete."),
            dict(t=1.5, shot="erros", hl=[E_LIST], focus=(200, 50, 790, 600), cap="Depois, os erros de execução que você mais comete."),
            dict(t=3.56, shot="erros", hl=[E_TOP], focus=(200, 110, 790, 340), cap="É com eles que a plataforma mostra os seus padrões."),
        ]),
        dict(where="Configurações", title="3 · Falhas de disciplina", audio="s4.wav", av=dict(side="right", pose="bracos", bub=[(2.0, "3 · Falhas")]), beats=[
            dict(t=0.0, shot="menu", hl=[M_FAL], click=c(M_FAL), focus=FM, cap="E as falhas de disciplina:"),
            dict(t=1.6, shot="falhas", hl=[F_LIST], focus=(200, 50, 790, 600), cap="quando você sabia que não devia e fez assim mesmo."),
            dict(t=4.85, shot="falhas", hl=[F_TOP], focus=(200, 110, 790, 340), cap="Elas aparecem na análise de disciplina do seu painel."),
        ]),
        dict(where="Novo Trade", title="Pronto: registre", audio="s5.wav", av=dict(side="right", bub=[(6.7, "NT8? Conecte!")]), beats=[
            dict(t=0.0, shot="nt-topo", hl=[SETUPF], focus=(420, 300, 780, 440), cap="Pronto. Agora, cada trade que você registrar já tem setup,"),
            dict(t=3.3, shot="nt-detalhes", hl=[DISC, ERRO], focus=(230, 250, 770, 600), cap="erro e falha para escolher na lista."),
            dict(t=6.5, shot="menu", hl=[M_NT8], click=c(M_NT8), focus=FM, cap="Usa NinjaTrader 8? Conecte a integração e os trades entram sozinhos."),
        ]),
    ]

# ---------------------------------------------------------------- avatar-guia
AVH = 300; FEET = 912
_POSE = {}
def pose(name, flip):
    k = (name, flip)
    if k not in _POSE:
        fn = {"aponta": "tyu-avatar-oficial.png", "bracos": "tyu-avatar-bracos-cruzados.png",
              "joinha": "tyu-avatar-joinha.png", "dedo": "tyu-avatar-dedo-cima-v2.png"}[name]
        im = Image.open(os.path.join(AVDIR, fn)).convert("RGBA")
        im = im.crop(im.getbbox())
        im = im.resize((int(im.width * AVH / im.height), AVH), Image.LANCZOS)
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        # sombra suave no chão
        _POSE[k] = im
    return _POSE[k]

def draw_bubble(frame, x, ytop, text, a, side):
    ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = R.font("b", 30)
    tw = d.textlength(text, font=f)
    bw, bh = tw + 44, 62
    bx = x - bw / 2
    bx = max(30, min(R.W - 30 - bw, bx))
    by = ytop - bh - 26 + (1 - a) * 12
    al = int(255 * a)
    d.rounded_rectangle([bx + 4, by + 6, bx + bw + 4, by + bh + 6], radius=24, fill=(15, 23, 42, int(50 * a)))
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=24, fill=(255, 255, 255, al), outline=R.VIO + (al,), width=4)
    tx = min(max(x, bx + 30), bx + bw - 30)
    d.polygon([(tx - 14, by + bh - 2), (tx + 14, by + bh - 2), (tx, by + bh + 20)], fill=(255, 255, 255, al))
    d.line([(tx - 14, by + bh), (tx, by + bh + 20), (tx + 14, by + bh)], fill=R.VIO + (al,), width=4)
    d.text((bx + bw / 2, by + bh / 2), text, font=f, fill=R.INK + (al,), anchor="mm")
    return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

def draw_avatar(frame, sc, t):
    av = sc.get("av")
    if not av:
        return frame
    side = av["side"]
    flip = side == "left"
    tx = 250 if side == "left" else R.W - 250
    sx = -200 if side == "left" else R.W + 200
    walk = 1.4
    u = R.ease(t / walk)
    x = sx + (tx - sx) * u
    walking = t < walk
    if walking:
        ph = t * 2 * math.pi * 2.6
        bob = abs(math.sin(ph)) * 14
        rot = math.sin(ph) * 4
        im = pose("aponta", flip).rotate(rot, resample=Image.BICUBIC, expand=True)
    else:
        bob = math.sin((t - walk) * 2.2) * 3
        nm = av.get("pose", "aponta")
        im = pose(nm, flip)
    # sombra
    ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    sw = 120 - bob * 2
    ImageDraw.Draw(ov).ellipse([x - sw / 2, FEET - 10, x + sw / 2, FEET + 10], fill=(15, 23, 42, 60))
    ov = ov.filter(ImageFilter.GaussianBlur(5))
    fr = Image.alpha_composite(frame.convert("RGBA"), ov)
    fr.alpha_composite(im, (int(x - im.width / 2), int(FEET - im.height - bob)))
    frame = fr.convert("RGB")
    for bt, txt in av.get("bub", []):
        if t >= bt:
            a = R.ease((t - bt) / 0.3)
            frame = draw_bubble(frame, x, FEET - AVH - bob, txt, a, side)
    return frame

_chrome = R.chrome_ui
def chrome_with_avatar(frame, sc, b, n, total, t, caps, prog):
    frame = draw_avatar(frame, sc, t)
    return _chrome(frame, sc, b, n, total, t, caps, prog)
R.chrome_ui = chrome_with_avatar

R.shots = shots
R.scenes = scenes
N = 5

def end_card(path, audio, secs=4.5):
    """Tela final do motor + avatar acenando (joinha) e saindo pela esquerda."""
    tmp = path.replace(".mp4", "-base.mp4")
    R.end_card(tmp, audio, secs=secs)
    frames = os.path.join(R.OUT, "endfr"); os.makedirs(frames, exist_ok=True)
    for f in glob.glob(os.path.join(frames, "*.png")):
        os.remove(f)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, os.path.join(frames, "%04d.png")], check=True)
    im = pose("joinha", False)
    fs = sorted(glob.glob(os.path.join(frames, "*.png")))
    for i, f in enumerate(fs):
        t = i / R.FPS
        fr = Image.open(f).convert("RGBA")
        x = R.W - 330
        if t > 3.2:
            x = (R.W - 330) + (-300 - (R.W - 330)) * R.ease((t - 3.2) / 1.2)
        bob = math.sin(t * 3) * 4
        fr.alpha_composite(im, (int(x - im.width / 2), int(980 - im.height - bob)))
        fr.convert("RGB").save(f)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(R.FPS), "-i", os.path.join(frames, "%04d.png"), "-i", tmp,
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-c:a", "copy", "-shortest", path], check=True)

def assemble():
    sil = os.path.join(R.AUD, "silence.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "1", sil], check=True)
    R.BG = R.bg()
    end_card(os.path.join(R.OUT, "end.mp4"), sil, secs=4.5)
    lst = os.path.join(R.OUT, "list.txt")
    with open(lst, "w") as fh:
        for i in range(1, N + 1):
            fh.write(f"file 'c{i}.mp4'\n")
        fh.write("file 'end.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", os.path.join(R.OUT, "vid1-final.mp4")], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "end":
        assemble(); sys.exit()
    only = [int(x) for x in a] if a and a[0] != "all" else list(range(1, N + 1))
    R.main(only)
    if not a or a[0] == "all":
        assemble()
