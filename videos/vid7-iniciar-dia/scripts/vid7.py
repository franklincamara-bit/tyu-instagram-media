"""VID-7 — Como preencher o Iniciar Dia (motor tutorial-narrado-v2)."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw
import render as R
from render import font, VIO, INK, MUTED
HERE = os.path.dirname(os.path.abspath(__file__))
R.UP = os.path.join(HERE, "up"); R.AUD = os.path.join(HERE, "audio"); R.OUT = os.path.join(HERE, "out")
os.makedirs(R.OUT, exist_ok=True)
R.NEXT_TITLE = "Como registrar um trade manualmente"
RED = (229, 72, 77); GREEN = (22, 163, 74)

def hook_card():
    w, h = 1500, 820
    im = Image.new("RGB", (w, h), (255, 255, 255)); d = ImageDraw.Draw(im)
    # painel esquerdo: a opção
    d.rounded_rectangle([60, 120, 700, 700], 36, fill=(246, 247, 251), outline=(226, 232, 240), width=3)
    d.text((100, 170), "CONFIGURAÇÃO DE DISCIPLINA", font=font("b", 28), fill=MUTED)
    d.rounded_rectangle([100, 250, 660, 370], 22, fill=(237, 233, 254), outline=VIO, width=4)
    d.text((140, 285), "Sim, considerar como", font=font("s", 34), fill=INK)
    d.text((140, 325), "quebra de disciplina", font=font("s", 34), fill=INK)
    d.rounded_rectangle([100, 400, 660, 490], 22, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
    d.text((140, 445), "Trade sem Iniciar Dia", font=font("m", 32), fill=MUTED, anchor="lm")
    d.text((380, 600), "↓  item “não seguiu”", font=font("b", 34), fill=RED, anchor="mm")
    # seta
    d.polygon([(745, 390), (800, 410), (745, 430)], fill=VIO); d.line([(720, 410), (760, 410)], fill=VIO, width=8)
    # painel direito: Daily Score
    d.rounded_rectangle([840, 120, 1440, 700], 36, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
    d.text((880, 170), "DAILY SCORE · DISCIPLINA", font=font("b", 28), fill=MUTED)
    d.text((880, 230), "pesa 30% da nota do dia", font=font("m", 28), fill=MUTED)
    d.text((880, 300), "100", font=font("b", 96), fill=(148, 163, 184))
    d.line([(875, 360), (1075, 360)], fill=(148, 163, 184), width=6)
    d.text((1110, 345), "→", font=font("b", 72), fill=INK, anchor="lm")
    d.text((1200, 300), "50", font=font("b", 110), fill=RED)
    d.rounded_rectangle([880, 470, 1400, 500], 15, fill=(241, 245, 249))
    d.rounded_rectangle([880, 470, 1140, 500], 15, fill=RED)
    d.text((880, 540), "1 trade “seguiu totalmente” + dia sem leitura", font=font("m", 25), fill=MUTED)
    d.text((880, 580), "= Disciplina 50 (−15 no Daily Score)", font=font("s", 27), fill=INK)
    d.text((w / 2, 770), "Exemplo ilustrativo · conta demo", font=font("m", 26), fill=MUTED, anchor="mm")
    return im

B = json.load(open(os.path.join(HERE, "boxes.json")))
def pad(b, p=8):
    return (b[0] - p, b[1] - p, b[2] + p, b[3] + p)
def ctr(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
APT = (395, 140, 1141, 378)
APT7 = (395, 140, 1141, 552)

def shots():
    def br(name):
        return lambda: dict(img=Image.open(os.path.join(R.UP, name + ".png")).convert("RGB"), dark=False, chrome="browser")
    names = ["menu","apt0","apt1","apt2","apt3","apt4","apt5","apt6","apt7","apt8","cfg","form","biasopen","opt","opt2","saved","novo"]
    d = {n: br(n) for n in names}
    d["hook"] = lambda: dict(img=hook_card(), dark=False, chrome="card", k=1)
    return R.Lazy(d)

def scenes():
    cfg, menu = B["cfg"], B["menu"]
    sim, nao = cfg["sim"], cfg["nao"]
    opts = (min(sim[0], nao[0]) - 6, min(sim[1], nao[1]) - 14, 1127, max(sim[3], nao[3]) + 14)
    form = B["form"]; bias_field = (409, form["bias"][1] - 10, 1127, form["bias"][3] + 10)
    bo = B["biasopen"]; bias_opts = (410, bo["alt"][1] - 8, 1127, bo["neu"][3] + 8)
    o = B["opt"]
    f1 = (409, o["a1"][1] - 4, 1127, o["a1"][3] + 95); f2 = (409, o["a2"][1] - 4, 1127, o["a2"][3] + 95); f3 = (409, o["a3"][1] - 4, 1127, o["a3"][3] + 95)
    o2 = B["opt2"]; sv = B["saved"]; nv = B["novo"]
    a7 = B["apt7"]; a8 = B["apt8"]
    res_box = (a8["num"][0] - 60, a8["num"][1] - 30, a8["score"][2] + 60, a8["score"][3] + 12)
    return [
        dict(where="Plataforma", title="Trade sem leitura do dia", audio="s1.wav", beats=[
            dict(t=0.0, shot="cfg", hl=[pad(sim, 10)], focus=(400, 180, 1140, 520),
                 cap="Se você ligar esta opção, trade sem Iniciar Dia conta como quebra de disciplina."),
            dict(t=6.2, shot="hook", focus="full", cap="E isso derruba a sua nota de Disciplina no Daily Score."),
        ]),
        dict(where="Plataforma", title="Onde fica", audio="s2.wav", beats=[
            dict(t=0.0, shot="menu", focus=(0, 0, 330, 700), zmax=1.5, cap="No menu lateral, clique em Iniciar Dia."),
            dict(t=1.4, shot="menu", hl=[(18, menu["iniciar"][1] - 10, 236, menu["iniciar"][3] + 10)],
                 click=ctr(menu["iniciar"]), focus=(0, 200, 520, 560), cap="No menu lateral, clique em Iniciar Dia."),
            dict(t=3.0, shot="menu", hl=[(300, 60, 760, 160)], focus=(250, 20, 1250, 420), cap="Faça isso antes do primeiro trade."),
        ]),
        dict(where="Iniciar Dia", title="Aptidão para Operar", audio="s3.wav", beats=[
            dict(t=0.0, shot="apt0", hl=[APT], focus=(395, 70, 1141, 400), cap="No topo, responda a Aptidão para Operar."),
            dict(t=3.5, shot="apt1", hl=[APT], focus=(395, 70, 1141, 400), cap="Sono, energia, clareza, ansiedade, irritação e autocontrole."),
            dict(t=4.95, shot="apt2", hl=[APT], focus=(395, 70, 1141, 400), cap="Sono, energia, clareza, ansiedade, irritação e autocontrole."),
            dict(t=5.75, shot="apt3", hl=[APT], focus=(395, 70, 1141, 400), cap="Sono, energia, clareza, ansiedade, irritação e autocontrole."),
            dict(t=6.7, shot="apt4", hl=[APT], focus=(395, 70, 1141, 400), cap="Sono, energia, clareza, ansiedade, irritação e autocontrole."),
            dict(t=7.6, shot="apt5", hl=[APT], focus=(395, 70, 1141, 400), cap="Sono, energia, clareza, ansiedade, irritação e autocontrole."),
            dict(t=8.9, shot="apt7", hl=[pad(a7["calmo"], 40)], focus=APT7, cap="Diga como se sente e clique em Gerar Score."),
            dict(t=10.2, shot="apt7", hl=[pad(a7["gerar"], 6)], click=ctr(a7["gerar"]), focus=APT7, cap="Diga como se sente e clique em Gerar Score."),
            dict(t=11.6, shot="apt8", hl=[res_box], focus=(395, 140, 1141, 470), cap="Escala de 1 a 5 em cada pergunta."),
        ]),
        dict(where="Iniciar Dia", title="Configuração de Disciplina", audio="s4.wav", beats=[
            dict(t=0.0, shot="cfg", hl=[opts], focus=(400, 180, 1140, 530),
                 cap="Escolha se trade sem leitura conta como quebra de disciplina."),
            dict(t=4.9, shot="cfg", hl=[pad(cfg["nota"], 6)], focus=(400, 180, 1140, 530),
                 cap="A escolha vale a partir de hoje. Dias anteriores mantêm a regra da época."),
        ]),
        dict(where="Iniciar Dia", title="Bias do Dia", audio="s5.wav", beats=[
            dict(t=0.0, shot="form", hl=[pad(form["data"], 6)], focus=(400, 100, 1140, 330), cap="Agora, a leitura do dia. Confira a data."),
            dict(t=2.7, shot="biasopen", hl=[bias_opts], focus=(400, 180, 1140, 420),
                 cap="Só o Bias do Dia é obrigatório: altista, baixista ou neutro."),
            dict(t=6.2, shot="form", hl=[bias_field], click=ctr(form["bias"]), focus=(400, 100, 1140, 330),
                 cap="Só o Bias do Dia é obrigatório: altista, baixista ou neutro."),
        ]),
        dict(where="Iniciar Dia", title="Campos opcionais", audio="s6.wav", beats=[
            dict(t=0.0, shot="opt", hl=[f1], focus=(400, 100, 1140, 560), cap="Se quiser, anote a análise geral do dia,"),
            dict(t=2.35, shot="opt", hl=[f2], focus=(400, 100, 1140, 560), cap="os pontos relevantes do gráfico e os setups planejados."),
            dict(t=4.0, shot="opt", hl=[f3], focus=(400, 100, 1140, 560), cap="os pontos relevantes do gráfico e os setups planejados."),
            dict(t=5.55, shot="opt2", hl=[pad(o2["print"], 6)], focus=(400, 300, 1140, 560), cap="Dá para anexar um print do gráfico."),
        ]),
        dict(where="Iniciar Dia", title="Salvar", audio="s7.wav", beats=[
            dict(t=0.0, shot="opt2", hl=[pad(o2["salvar"], 6)], click=ctr(o2["salvar"]), focus=(400, 520, 1140, 780),
                 cap="Clique em Salvar Leitura do Dia."),
            dict(t=1.85, shot="saved", hl=[pad(sv["bias"], 6)], focus=(400, 180, 1140, 720), cap="Leitura salva."),
            dict(t=2.4, shot="novo", hl=[pad(nv["badge"], 8)], where="Novo Trade", focus=(400, 240, 1140, 400), zmax=2.3,
                 cap="O bias aparece como referência quando você registra um trade."),
        ]),
    ]

R.shots = shots
R.scenes = scenes

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "card":
        hook_card().save(os.path.join(R.OUT, "hook.png")); sys.exit()
    if args and args[0] == "end":
        R.BG = R.bg()
        sil = os.path.join(R.AUD, "silence.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "1", sil], check=True)
        R.end_card(os.path.join(R.OUT, "end.mp4"), sil, secs=4.5); sys.exit()
    only = [int(a) for a in args] or list(range(1, 8))
    R.main(only)
