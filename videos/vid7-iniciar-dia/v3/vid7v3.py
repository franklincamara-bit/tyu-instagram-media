"""VID-7 v3 — Como preencher o Iniciar Dia (refeito pelo comentário do Franklin de 14/11/2026).
Motor: ../scripts/render.py (tutorial-narrado-v2). Prints 800x560 da conta de teste em src/.
Uso: python3 vid7v3.py [cena ...] | end | all
"""
import os, sys, subprocess
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import render as R

R.UP = os.path.join(HERE, "up"); R.AUD = os.path.join(HERE, "audio"); R.OUT = os.path.join(HERE, "out")
os.makedirs(R.OUT, exist_ok=True)
R.LOGO = os.path.join(HERE, "..", "scripts", "logo.png")
R.NEXT_TITLE = "Como registrar um trade manualmente"

BLUR = {
    "menu": [(14, 452, 242, 512)],                      # nome e e-mail do rodapé
    "rep_leit": [(88, 362, 690, 548)],                  # print do gráfico (ativo e preços)
    "rep_trade": [(120, 244, 330, 284), (585, 228, 692, 296)],  # ativo/conta e resultado
}

def load(name):
    import glob
    src = glob.glob(os.path.join(HERE, "src", name + ".*"))[0]
    im = Image.open(src).convert("RGB")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if name in BLUR:
        im = R.blur_boxes(im, BLUR[name], k=2, radius=14)
    return im

def shots():
    names = ["menu", "top", "apt1", "apt3", "apt4", "apt5", "apt7", "rep_apt", "cfg0", "cfg1", "cfg2",
             "form", "biasopen", "fill1", "fill2", "salvar", "rep_leit", "rep_trade"]
    d = {n: (lambda n=n: dict(img=load(n), dark=False, chrome="browser")) for n in names}
    return R.Lazy(d)

def c(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

APT_CARD = (24, 318, 776, 556)
OPTS = (45, 414, 755, 485)
APT_F = (20, 250, 780, 560)

def scenes():
    return [
        dict(where="Plataforma", title="Iniciar Dia", audio="s1.wav", beats=[
            dict(t=0.0, shot="top", hl=[(88, 85, 318, 149)], focus=(0, 60, 800, 300),
                 cap="Neste vídeo, você vai aprender a usar o Iniciar Dia:"),
            dict(t=3.5, shot="top", focus="full", cap="a preparação que você faz antes do primeiro trade."),
        ]),
        dict(where="Plataforma", title="Onde fica", audio="s2.wav", beats=[
            dict(t=0.0, shot="menu", focus=(0, 180, 520, 470), zmax=1.8, cap="No menu lateral, clique em Iniciar Dia."),
            dict(t=0.9, shot="menu", hl=[(24, 365, 216, 397)], click=c((24, 365, 216, 397)), focus=(0, 180, 520, 470),
                 cap="No menu lateral, clique em Iniciar Dia."),
            dict(t=3.1, shot="top", hl=[(24, 261, 288, 293)], focus=(0, 230, 800, 560), cap="A página reúne a Aptidão para Operar,"),
            dict(t=5.4, shot="cfg0", hl=[(24, 12, 776, 226)], focus=(0, 0, 800, 240), cap="a Configuração de Disciplina"),
            dict(t=7.1, shot="form", hl=[(30, 12, 770, 352)], focus="full", cap="e a leitura do dia."),
        ]),
        dict(where="Iniciar Dia", title="Aptidão para Operar: o que é", audio="s3.wav", beats=[
            dict(t=0.0, shot="apt1", hl=[(24, 261, 288, 293), APT_CARD], focus=(0, 250, 800, 560),
                 cap="A Aptidão para Operar avalia como você chega ao mercado."),
            dict(t=3.7, shot="apt4", hl=[(45, 370, 400, 402)], focus=APT_F, cap="Cansaço, ansiedade e irritação pesam nas decisões,"),
            dict(t=5.6, shot="apt5", hl=[(45, 370, 400, 402)], focus=APT_F, cap="Cansaço, ansiedade e irritação pesam nas decisões,"),
            dict(t=7.2, shot="apt5", hl=[APT_CARD], focus=APT_F, cap="e é melhor saber disso antes do primeiro trade."),
        ]),
        dict(where="Iniciar Dia", title="Aptidão para Operar: passo a passo", audio="s4.wav", beats=[
            dict(t=0.0, shot="apt1", hl=[OPTS], focus=APT_F, cap="Responda de 1 a 5:"),
            dict(t=1.4, shot="apt1", hl=[(45, 370, 400, 402)], click=c((476, 414, 610, 485)), focus=APT_F,
                 cap="sono, energia, clareza mental,"),
            dict(t=3.5, shot="apt3", hl=[(45, 370, 400, 402)], focus=APT_F, cap="sono, energia, clareza mental,"),
            dict(t=4.6, shot="apt4", hl=[(45, 370, 400, 402)], focus=APT_F, cap="ansiedade, irritação e autocontrole."),
            dict(t=5.6, shot="apt5", hl=[(45, 370, 400, 402)], focus=APT_F, cap="ansiedade, irritação e autocontrole."),
            dict(t=7.7, shot="apt7", hl=[(40, 163, 282, 242)], click=c((40, 163, 282, 242)), focus=(0, 60, 800, 500),
                 cap="Diga como se sente e clique em Gerar Score."),
            dict(t=9.0, shot="apt7", hl=[(601, 426, 755, 466)], click=c((601, 426, 755, 466)), focus=(0, 60, 800, 500),
                 cap="Diga como se sente e clique em Gerar Score."),
            dict(t=10.8, shot="rep_apt", where="Resultado", hl=[(66, 170, 704, 312)], focus=(20, 90, 780, 500),
                 cap="O resultado mostra o seu nível de aptidão e uma orientação para o dia."),
        ]),
        dict(where="Iniciar Dia", title="Configuração de Disciplina", audio="s5.wav", beats=[
            dict(t=0.0, shot="cfg0", hl=[(24, 12, 776, 226)], focus=(0, 0, 800, 240),
                 cap="Em Configuração de Disciplina está uma ferramenta importante:"),
            dict(t=3.6, shot="cfg0", hl=[(93, 30, 759, 91)], focus=(0, 0, 800, 240),
                 cap="ela garante que você nunca comece a operar sem ter feito e registrado a análise do dia."),
            dict(t=8.6, shot="cfg0", hl=[(612, 120, 747, 148)], click=c((612, 120, 747, 148)), focus=(0, 0, 800, 240),
                 cap="Clique em Alterar configuração e escolha Sim."),
            dict(t=10.2, shot="cfg1", hl=[(54, 189, 746, 233)], click=c((54, 189, 400, 233)), focus=(0, 100, 800, 350),
                 cap="Clique em Alterar configuração e escolha Sim."),
            dict(t=11.4, shot="cfg2", hl=[(54, 189, 746, 233)], focus=(0, 100, 800, 350),
                 cap="A partir daí, fazer trade antes de salvar a leitura do dia conta como quebra de disciplina no seu Daily Score."),
        ]),
        dict(where="Iniciar Dia", title="Leitura do dia: Bias", audio="s6.wav", beats=[
            dict(t=0.0, shot="form", hl=[(30, 12, 770, 200)], focus=(0, 0, 800, 360), cap="Agora, a leitura do dia."),
            dict(t=2.1, shot="form", hl=[(49, 69, 751, 105)], focus=(0, 0, 800, 360), cap="Confira a data"),
            dict(t=3.2, shot="biasopen", hl=[(51, 204, 751, 305)], click=c((49, 162, 751, 196)), focus=(0, 100, 800, 360),
                 cap="e escolha o Bias do Dia: altista, baixista ou neutro."),
            dict(t=7.1, shot="fill1", hl=[(49, 135, 751, 196)], focus=(0, 0, 800, 360), cap="É o único campo obrigatório."),
        ]),
        dict(where="Iniciar Dia", title="Análise Geral para o Dia", audio="s7.wav", beats=[
            dict(t=0.0, shot="fill1", hl=[(49, 226, 751, 351)], focus=(0, 150, 800, 420),
                 cap="Em Análise Geral para o Dia, descreva o seu entendimento do mercado hoje,"),
            dict(t=4.2, shot="fill1", hl=[(49, 226, 751, 351), (49, 162, 751, 196)], focus=(0, 120, 800, 420),
                 cap="inclusive o que justifica o seu bias."),
        ]),
        dict(where="Iniciar Dia", title="Pontos Relevantes no Gráfico", audio="s8.wav", beats=[
            dict(t=0.0, shot="fill1", hl=[(49, 380, 751, 505)], focus=(0, 300, 800, 560),
                 cap="Pontos Relevantes no Gráfico talvez seja a parte mais importante."),
            dict(t=4.0, shot="fill1", hl=[(49, 410, 751, 470)], focus=(0, 330, 800, 540), cap="Aqui você anota os níveis do seu plano:"),
            dict(t=5.9, shot="fill1", hl=[(49, 410, 751, 470)], focus=(0, 330, 800, 540),
                 cap="os alvos do dia e as regiões onde vai esperar o preço reagir para entrar,"),
            dict(t=10.0, shot="fill1", hl=[(49, 410, 751, 470)], focus=(0, 330, 800, 540), cap="se o seu setup aparecer."),
        ]),
        dict(where="Iniciar Dia", title="Setups Planejados", audio="s9.wav", beats=[
            dict(t=0.0, shot="fill2", hl=[(49, 32, 751, 156)], focus=(0, 0, 800, 260),
                 cap="Em Setups Planejados, anote quais setups você pretende usar"),
            dict(t=3.6, shot="fill2", hl=[(49, 32, 751, 156)], focus=(0, 0, 800, 260), cap="quando o preço chegar a esses pontos."),
        ]),
        dict(where="Iniciar Dia", title="Prints e Observações", audio="s10.wav", beats=[
            dict(t=0.0, shot="fill2", hl=[(49, 340, 213, 407), (49, 436, 213, 503)], focus=(0, 300, 800, 540),
                 cap="Você pode anexar até dois prints do gráfico."),
            dict(t=3.0, shot="fill2", hl=[(49, 186, 751, 310)], focus=(0, 150, 800, 400),
                 cap="E, em Observações, fica qualquer outra anotação do dia."),
        ]),
        dict(where="Iniciar Dia", title="Salvar e relatório do dia", audio="s11.wav", beats=[
            dict(t=0.0, shot="salvar", hl=[(49, 400, 751, 436)], click=c((49, 400, 751, 436)), focus=(0, 240, 800, 480),
                 cap="Clique em Salvar Leitura do Dia."),
            dict(t=2.3, shot="rep_leit", where="Relatório do dia", hl=[(66, 90, 704, 335)], focus=(20, 80, 780, 345),
                 cap="Tudo o que você preencheu aparece no relatório de encerramento do dia,"),
            dict(t=5.5, shot="rep_trade", where="Relatório do dia", hl=[(66, 212, 704, 468)], focus=(20, 80, 780, 520),
                 cap="junto com os trades realizados."),
        ]),
    ]

R.shots = shots
R.scenes = scenes
N = 11

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
                    os.path.join(R.OUT, "vid7-v3-final.mp4")], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "end":
        assemble(); sys.exit()
    only = [int(x) for x in a] if a and a[0] != "all" else list(range(1, N + 1))
    R.main(only)
    if not a or a[0] == "all":
        assemble()
