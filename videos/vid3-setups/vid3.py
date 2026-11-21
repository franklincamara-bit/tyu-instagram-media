"""VID-3 — Biblioteca de Setups: como cadastrar seus setups (produção 21/11/2026).
Motor: render.py (tutorial-narrado-v2, cópia do VID-6) + avatar-guia em miniatura (poses oficiais) caminhando pela tela.
Prints 800x600 da conta de teste em src/ (nomes de traders reais trocados no DOM só para o print; nada salvo).
Narração: narr-elevenlabs.mp3 (Rafael Valente, eleven_v4) cortada em audio/s1..s8.wav.
Uso: python3 vid3.py [cena ...] | end | all
"""
import os, sys, subprocess, glob, math
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R

R.UP = os.path.join(HERE, "up"); R.AUD = os.path.join(HERE, "audio"); R.OUT = os.path.join(HERE, "out")
os.makedirs(R.OUT, exist_ok=True)
R.LOGO = os.path.join(HERE, "logo.png")
R.NEXT_TITLE = "Como cadastrar seus erros"
AVDIR = os.path.join(HERE, "avatar")

def load(name):
    src = glob.glob(os.path.join(HERE, "src", name + ".*"))[0]
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))

NAMES = ["lista", "biblio", "biblio2", "form-topo", "form-regras", "form-fim", "lista-novo", "nt-topo", "nt-lista", "nt-mais", "lista-atalho"]
def shots():
    return R.Lazy({n: (lambda n=n: dict(img=load(n), dark=False, chrome="browser")) for n in NAMES})

def c(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

LISTA = (238, 133, 762, 507); BADGE = (250, 284, 382, 302); IMPORT = (504, 66, 666, 95); NOVO = (673, 66, 782, 95)
BMODAL = (225, 88, 575, 512); BITEM = (245, 162, 540, 214)
NOME = (220, 128, 566, 157); DESC = (220, 194, 566, 240); SESS = (220, 278, 566, 390)
CRIT = (220, 192, 566, 256); REGRAS = (220, 290, 566, 370)
LINKS = (220, 272, 566, 330); OBS = (220, 370, 566, 416); UPLOAD = (220, 453, 566, 484); SALVAR = (510, 494, 566, 524)
NOVOCARD = (238, 505, 750, 577)
SETUPF = (505, 357, 716, 401); PLUS = (722, 355, 750, 384); NTLIST = (505, 404, 716, 588); SEMSETUP = (508, 441, 712, 466)
QMODAL = (235, 178, 566, 420); QNOME = (253, 248, 547, 277); QDESC = (253, 314, 547, 360); CRIAR = (253, 374, 547, 402)
ATCARD = (238, 505, 750, 557); PENCIL = (686, 513, 716, 543)

def scenes():
    return [
        dict(where="Novo Trade", title="Sem setup é quebra", audio="s1.wav", av=dict(side="left", bub=[(4.6, "Sem setup = quebra")]), beats=[
            dict(t=0.0, shot="nt-topo", hl=[SETUPF], focus=(420, 300, 780, 440), cap="A partir do 6º trade no registro manual, o setup é obrigatório."),
            dict(t=4.4, shot="nt-lista", hl=[SEMSETUP], focus=(420, 340, 780, 600), cap="E “Sem Setup” conta como quebra de disciplina."),
            dict(t=7.9, shot="nt-lista", hl=[NTLIST], focus=(420, 340, 780, 600), cap="Vamos montar os seus."),
        ]),
        dict(where="Configurações", title="Gerenciar Setups", audio="s2.wav", av=dict(side="right", bub=[(4.4, "Sua biblioteca")]), beats=[
            dict(t=0.0, shot="lista", hl=[LISTA], focus=(200, 50, 790, 520), cap="Seus setups ficam em Configurações › Gerenciar Setups."),
            dict(t=4.2, shot="lista", hl=[BADGE], focus=(230, 220, 560, 330), zmax=2.2, cap="Cada um mostra quantos trades você fez com ele e a sua taxa de acerto."),
        ]),
        dict(where="Gerenciar Setups", title="Biblioteca de Setups", audio="s3.wav", av=dict(side="right", bub=[(2.0, "Importa e ajusta")]), beats=[
            dict(t=0.0, shot="lista", hl=[IMPORT], click=c(IMPORT), focus=(380, 40, 790, 230), cap="Não quer começar do zero?"),
            dict(t=1.7, shot="biblio", hl=[BMODAL], focus=(200, 80, 600, 520), cap="Em Importar da Biblioteca, você marca um modelo e traz para a sua lista."),
            dict(t=3.6, shot="biblio2", hl=[BITEM], click=(260, 180), focus=(200, 80, 600, 520), cap="Em Importar da Biblioteca, você marca um modelo e traz para a sua lista."),
            dict(t=6.2, shot="biblio2", hl=[BITEM], focus=(200, 80, 600, 520), cap="Depois, ajuste as regras ao seu jeito de operar. Modelo é ponto de partida, não sinal de entrada."),
        ]),
        dict(where="Gerenciar Setups", title="Novo Setup", audio="s4.wav", av=dict(side="right", bub=[]), beats=[
            dict(t=0.0, shot="lista", hl=[NOVO], click=c(NOVO), focus=(430, 40, 790, 230), cap="Para criar o seu, clique em Novo Setup."),
            dict(t=2.9, shot="form-topo", hl=[NOME], focus=(200, 60, 600, 400), cap="Um nome que você reconheça na hora,"),
            dict(t=4.8, shot="form-topo", hl=[DESC, SESS], focus=(200, 160, 600, 400), cap="uma descrição curta e as sessões em que ele vale."),
        ]),
        dict(where="Novo Setup", title="Critérios e regras", audio="s5.wav", av=dict(side="right", pose="bracos", bub=[(11.2, "Se não dá para escrever…")]), beats=[
            dict(t=0.0, shot="form-regras", hl=[CRIT, REGRAS], focus=(200, 160, 600, 390), cap="É aqui que o setup ganha valor."),
            dict(t=2.1, shot="form-regras", hl=[CRIT], focus=(200, 160, 600, 280), cap="Em Critérios de Formação: o que precisa aparecer no gráfico."),
            dict(t=6.1, shot="form-regras", hl=[REGRAS], focus=(200, 260, 600, 390), cap="Em Regras de Entrada/Saída: onde entra, onde fica o stop, onde sai."),
            dict(t=11.1, shot="form-regras", hl=[CRIT, REGRAS], focus=(200, 160, 600, 390), cap="Se não dá para escrever, ainda não é um setup."),
        ]),
        dict(where="Novo Setup", title="Extras e salvar", audio="s6.wav", av=dict(side="left", bub=[]), beats=[
            dict(t=0.0, shot="form-fim", hl=[LINKS, OBS, UPLOAD], focus=(200, 250, 600, 500), cap="Se quiser: links de estudo, observações e um print de exemplo."),
            dict(t=4.8, shot="form-fim", hl=[SALVAR], click=c(SALVAR), focus=(330, 380, 600, 540), cap="Salve,"),
            dict(t=5.66, shot="lista-novo", hl=[NOVOCARD], focus=(220, 330, 780, 590), cap="e ele já aparece na lista."),
        ]),
        dict(where="Novo Trade", title="Atalho: o “+”", audio="s7.wav", av=dict(side="left", bub=[(5.4, "Atalho: +")]), beats=[
            dict(t=0.0, shot="nt-lista", hl=[NTLIST], focus=(420, 340, 780, 600), cap="No Novo Trade, escolha o setup na lista."),
            dict(t=2.9, shot="nt-topo", hl=[PLUS], click=c(PLUS), focus=(470, 320, 790, 430), zmax=2.2, cap="Surgiu um setup novo no meio do registro?"),
            dict(t=5.3, shot="nt-mais", hl=[QNOME, CRIAR], focus=(220, 170, 590, 430), cap="Clique no “+”, dê um nome e crie ali mesmo."),
        ]),
        dict(where="Gerenciar Setups", title="Depois, complete", audio="s8.wav", av=dict(side="right", bub=[(3.4, "Depois, complete!")]), beats=[
            dict(t=0.0, shot="nt-mais", hl=[QNOME, QDESC], focus=(220, 170, 590, 430), cap="Só que o atalho guarda só o nome e a descrição."),
            dict(t=3.2, shot="lista-atalho", hl=[ATCARD], click=c(PENCIL), focus=(220, 380, 780, 590), cap="Depois, complete os critérios e as regras em Gerenciar Setups."),
            dict(t=7.3, shot="form-regras", hl=[CRIT, REGRAS], focus=(200, 160, 600, 390), cap="Senão, é só um rótulo."),
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
N = 8

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
                    "-movflags", "+faststart", os.path.join(R.OUT, "vid3-final.mp4")], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "end":
        assemble(); sys.exit()
    only = [int(x) for x in a] if a and a[0] != "all" else list(range(1, N + 1))
    R.main(only)
    if not a or a[0] == "all":
        assemble()
