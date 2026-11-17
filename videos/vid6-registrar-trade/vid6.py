"""VID-6 — Como registrar um trade manualmente (produção 17/11/2026).
Motor: render.py (tutorial-narrado-v2, cópia do VID-7). Prints 800x600 da conta de teste (Novo Trade, nada salvo) em src/.
Narração: audio/narr-a.mp3 (Rafael Valente, eleven_v4) cortada em s1..s8.wav.
Uso: python3 vid6.py [cena ...] | end | all
"""
import os, sys, subprocess, glob
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R

R.UP = os.path.join(HERE, "up"); R.AUD = os.path.join(HERE, "audio"); R.OUT = os.path.join(HERE, "out")
os.makedirs(R.OUT, exist_ok=True)
R.LOGO = os.path.join(HERE, "logo.png")
R.NEXT_TITLE = "Como cadastrar seus setups"

FOOT = (12, 515, 196, 566)  # nome e e-mail do rodapé do menu

def load(name):
    src = glob.glob(os.path.join(HERE, "src", name + ".*"))[0]
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    return R.blur_boxes(im, [FOOT], k=2, radius=14)

NAMES = ["top", "ativo", "setupopen", "filled1", "sessao", "emoopen", "discopen", "naoseguiu", "faldif", "behav", "erroopen", "bottom"]
def shots():
    return R.Lazy({n: (lambda n=n: dict(img=load(n), dark=False, chrome="browser")) for n in NAMES})

def c(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

MENU_NT = (18, 320, 169, 344); MANUAL = (240, 157, 493, 181); CSV = (495, 157, 748, 181)
DATA = (238, 240, 484, 296); CONTA = (505, 240, 750, 312); ATIVO_DD = (238, 357, 451, 470)
SETUP_LIST = (505, 357, 716, 585); SEM_SETUP = (508, 441, 712, 466)
TIPO_ROW = (238, 440, 750, 509); RESULT = (588, 440, 750, 509)
DET = (250, 148, 750, 190); SESSAO = (238, 216, 750, 287); EMO_LIST = (238, 405, 487, 570)
DISC_LIST = (505, 190, 752, 324); FALHAS = (238, 312, 750, 492); LINK = (505, 264, 750, 290); MODAL = (197, 123, 603, 477)
BIAS = (238, 310, 750, 370); DISC_F = (505, 190, 750, 257); ERRO_LIST = (253, 310, 705, 452)
COMENT = (238, 180, 750, 285); PRINTS = (238, 305, 750, 505); SALVAR = (238, 523, 750, 563)

def scenes():
    return [
        dict(where="Plataforma", title="Resultado é só metade", audio="s1.wav", beats=[
            dict(t=0.0, shot="filled1", hl=[RESULT], focus=(220, 380, 770, 560), cap="Registrar só o resultado é guardar metade do trade."),
            dict(t=3.45, shot="behav", hl=[DISC_F, BIAS], focus=(220, 180, 770, 520), cap="A outra metade é como você decidiu."),
        ]),
        dict(where="Plataforma", title="Onde fica", audio="s2.wav", beats=[
            dict(t=0.0, shot="top", focus=(0, 150, 520, 470), zmax=1.8, cap="No menu, clique em Novo Trade."),
            dict(t=0.6, shot="top", hl=[MENU_NT], click=c(MENU_NT), focus=(0, 150, 520, 470), zmax=1.8, cap="No menu, clique em Novo Trade."),
            dict(t=2.2, shot="top", hl=[CSV], focus=(220, 60, 770, 300), cap="Dá para importar por CSV,"),
            dict(t=4.1, shot="top", hl=[MANUAL], focus=(220, 60, 770, 300), cap="mas aqui vamos registrar no modo Manual."),
        ]),
        dict(where="Novo Trade", title="Dados da operação", audio="s3.wav", beats=[
            dict(t=0.0, shot="top", hl=[DATA, CONTA], focus=(220, 190, 770, 420), cap="Confira a data e a conta."),
            dict(t=1.9, shot="ativo", hl=[ATIVO_DD], click=(344, 453), focus=(220, 300, 770, 520), cap="Escolha o ativo e o setup."),
            dict(t=3.0, shot="setupopen", hl=[SETUP_LIST], focus=(220, 300, 770, 600), cap="Escolha o ativo e o setup."),
            dict(t=4.0, shot="setupopen", hl=[SEM_SETUP], focus=(300, 330, 770, 600), cap="Se operou fora de qualquer setup, existe a opção Sem Setup,"),
            dict(t=7.4, shot="setupopen", hl=[SEM_SETUP], focus=(300, 330, 770, 600), cap="que conta como quebra de disciplina."),
        ]),
        dict(where="Novo Trade", title="Tipo, quantidade e resultado", audio="s4.wav", beats=[
            dict(t=0.0, shot="filled1", hl=[TIPO_ROW], focus=(220, 300, 770, 560), cap="Depois, marque se foi compra ou venda, a quantidade de contratos e o resultado."),
            dict(t=3.0, shot="filled1", hl=[RESULT], focus=(220, 300, 770, 560), cap="Depois, marque se foi compra ou venda, a quantidade de contratos e o resultado."),
        ]),
        dict(where="Novo Trade", title="Detalhes do trade", audio="s5.wav", beats=[
            dict(t=0.0, shot="sessao", hl=[DET], focus=(220, 100, 770, 320), cap="Agora, os detalhes do trade."),
            dict(t=2.1, shot="sessao", hl=[DET], focus=(220, 100, 770, 320), cap="São eles que alimentam as suas análises de comportamento."),
            dict(t=5.2, shot="sessao", hl=[SESSAO], focus=(220, 180, 770, 330), cap="Marque a sessão"),
            dict(t=6.3, shot="emoopen", hl=[EMO_LIST], focus=(220, 380, 770, 590), cap="e como você se sentiu."),
        ]),
        dict(where="Novo Trade", title="Seguiu o plano?", audio="s6.wav", beats=[
            dict(t=0.0, shot="discopen", hl=[DISC_LIST], focus=(400, 170, 770, 340), cap="Seguiu o plano?"),
            dict(t=1.2, shot="naoseguiu", hl=[FALHAS], focus=(220, 180, 770, 500), cap="Se não seguiu, aparece o campo de falhas de disciplina."),
            dict(t=4.5, shot="naoseguiu", hl=[LINK], click=c(LINK), focus=(400, 180, 770, 330), cap="Na dúvida entre falha e erro,"),
            dict(t=5.9, shot="faldif", hl=[MODAL], focus=(180, 110, 620, 490), cap="este link explica a diferença."),
        ]),
        dict(where="Novo Trade", title="Bias e erros", audio="s7.wav", beats=[
            dict(t=0.0, shot="behav", hl=[BIAS], focus=(220, 280, 770, 400), cap="Marque a direção em relação ao seu bias"),
            dict(t=2.3, shot="erroopen", hl=[ERRO_LIST], focus=(220, 280, 770, 520), cap="e, se houve, os erros do trade."),
            dict(t=4.5, shot="behav", hl=[DISC_F], focus=(220, 170, 770, 400), cap="Um trade pode terminar no stop e mesmo assim ter seguido o plano."),
        ]),
        dict(where="Novo Trade", title="Comentário, prints e salvar", audio="s8.wav", beats=[
            dict(t=0.0, shot="bottom", hl=[COMENT], focus=(220, 150, 770, 320), cap="Por fim, escreva um comentário,"),
            dict(t=1.8, shot="bottom", hl=[PRINTS], focus=(220, 280, 770, 520), cap="anexe até dois prints do gráfico"),
            dict(t=4.0, shot="bottom", hl=[SALVAR], click=c(SALVAR), focus=(220, 420, 770, 590), cap="e clique em Salvar Trade."),
        ]),
    ]

R.shots = shots
R.scenes = scenes
N = 8

def assemble():
    sil = os.path.join(R.AUD, "silence.wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "1", sil], check=True)
    R.BG = R.bg()
    R.end_card(os.path.join(R.OUT, "end.mp4"), sil, secs=4.5)
    lst = os.path.join(R.OUT, "list.txt")
    with open(lst, "w") as fh:
        for i in range(1, N + 1):
            fh.write(f"file 'c{i}.mp4'\n")
        fh.write("file 'end.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", os.path.join(R.OUT, "vid6-final.mp4")], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "end":
        assemble(); sys.exit()
    only = [int(x) for x in a] if a and a[0] != "all" else list(range(1, N + 1))
    R.main(only)
    if not a or a[0] == "all":
        assemble()
