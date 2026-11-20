"""Matemática cruel: acerta 60% e perde (TYU-51, carrossel, publica seg 30/11/2026).
Capa colorida (preferência do Franklin). Slides 2 e 3 no padrão E. Valores em R (múltiplos do risco), antes de custos.
Conta: 6 acertos × +0,5R = +3R; 4 erros × −1R = −4R; resultado −1R com 60% de acerto.
Acerto mínimo para empatar = perda ÷ (ganho + perda) = 1 ÷ (1 + ganho/perda):
  0,5 → 66,7% (67%) · 1 → 50% · 1,5 → 40% · 2 → 33,3% (33%).
Uso: python acerta60_51.py [pasta_saida]   (precisa de Archivo.ttf, pensativo.png e explicando.png nesta pasta)
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else D)
OUT.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(D / "Archivo.ttf")
LOGO = b64(D.parent.parent / "assets" / "logo.png")
PENS = b64(D / "pensativo.png")
EXPL = b64(D / "explicando.png")

CSS = f"""
@font-face {{ font-family: Archivo; src: url(data:font/ttf;base64,{FONT}); font-weight: 100 900; font-stretch: 62% 125%; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:#fff; font-family: Archivo, Inter, sans-serif; color:#0B1533; position:relative; overflow:hidden; }}
.circ {{ position:absolute; border-radius:50%; }}
.logo {{ position:absolute; left:72px; top:58px; width:156px; }}
.logochip {{ position:absolute; left:56px; top:44px; background:#fff; border-radius:999px; padding:14px 22px; box-shadow:0 12px 30px rgba(0,0,0,.25); }}
.logochip img {{ width:150px; display:block; }}
.label {{ position:absolute; left:72px; top:168px; font-weight:800; letter-spacing:5px; font-size:24px; color:#2563EB; }}
.h {{ font-weight:900; font-stretch:72%; line-height:0.98; letter-spacing:-1px; }}
.foot {{ position:absolute; left:72px; bottom:44px; font-size:21px; color:#94A3B8; font-family: Inter; }}
.swipe {{ position:absolute; right:72px; bottom:42px; font-size:22px; color:#2563EB; font-weight:800; font-family: Inter; }}
.card {{ background:#fff; border:2px solid #E2E8F0; border-radius:28px; box-shadow:0 18px 40px rgba(15,23,42,.08); }}
.stamp {{ position:absolute; font-weight:900; font-stretch:90%; letter-spacing:2px; color:#E5484D; border:8px solid #E5484D; border-radius:20px; background:rgba(255,255,255,.96); padding:6px 30px 10px; transform:rotate(-6deg); box-shadow:0 18px 40px rgba(0,0,0,.25); }}
.pillseries {{ position:absolute; font:800 24px Inter; letter-spacing:6px; padding:14px 30px; border-radius:999px; }}
.selo {{ position:absolute; font:700 19px Inter; letter-spacing:1px; color:#64748B; background:#F1F5F9; border:2px solid #E2E8F0; border-radius:999px; padding:8px 18px; }}
"""

CHECK = '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
XMARK = '<svg viewBox="0 0 24 24" width="36" height="36"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/></svg>'

def dots():
    seq = "VVXVVXVXVX"  # 6 acertos, 4 erros
    out = []
    for c in seq:
        bg = "#16A34A" if c == "V" else "#E5484D"
        out.append(f'<div style="width:66px;height:66px;border-radius:18px;background:{bg};display:flex;align-items:center;justify-content:center;box-shadow:0 8px 16px rgba(0,0,0,.18)">{CHECK if c=="V" else XMARK}</div>')
    return "".join(out)

S1 = f"""
<div style="position:absolute;inset:0;background:radial-gradient(760px 640px at 95% 4%,rgba(255,212,59,.30),transparent 60%),radial-gradient(900px 800px at 0% 100%,rgba(229,72,77,.32),transparent 60%),linear-gradient(160deg,#2563EB 0%,#1D4ED8 48%,#0B1533 100%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:90px 90px"></div>
<div class="logochip"><img src="data:image/png;base64,{LOGO}"></div>
<div class="pillseries" style="left:72px;top:170px;background:#0B1533;color:#FFD43B;box-shadow:0 10px 26px rgba(0,0,0,.3)">MATEMÁTICA CRUEL</div>
<div class="h" style="position:absolute;left:72px;top:262px;font-size:136px;width:980px;color:#fff;text-shadow:0 8px 0 rgba(11,21,51,.35)">
  ACERTA 60%.<br><span style="color:#FFD43B">E AINDA PERDE.</span>
</div>
<div style="position:absolute;left:72px;top:566px;width:560px;font:500 33px/1.36 Inter;color:#E0E9FF">
  Taxa de acerto alta <b style="color:#fff">não paga a conta sozinha</b>. A outra metade da história é o tamanho de cada trade.
</div>
<div style="position:absolute;left:56px;top:830px;width:700px;background:#fff;border-radius:28px;padding:28px 30px 30px;box-shadow:0 30px 60px rgba(0,0,0,.35);transform:rotate(-2deg)">
  <div style="display:flex;justify-content:space-between;align-items:baseline">
    <span style="font:800 26px Inter;color:#0B1533">Últimos 10 trades</span>
    <span style="font:800 26px Inter;color:#16A34A">6 de 10 certos</span></div>
  <div style="display:grid;grid-template-columns:repeat(5,66px);gap:16px 40px;margin-top:22px;justify-content:center">{dots()}</div>
  <div style="margin-top:22px;height:2px;background:#E2E8F0"></div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:16px">
    <span style="font:600 24px Inter;color:#64748B">Resultado</span>
    <span style="font:900 54px Archivo;font-stretch:80%;color:#E5484D">−1R</span></div>
</div>
<img src="data:image/png;base64,{PENS}" style="position:absolute;right:-10px;top:560px;width:330px;z-index:4;filter:drop-shadow(0 30px 40px rgba(0,0,0,.40))">
<div class="stamp" style="left:520px;top:1150px;font-size:46px;z-index:5">CERTO NA MAIORIA</div>
<div class="foot" style="color:#BFD3FF">tradeyouup.net &nbsp;·&nbsp; 1/3</div><div class="swipe" style="color:#FFD43B;z-index:6;background:#0B1533;padding:8px 18px;border-radius:999px;right:56px;bottom:34px">deslize →</div>
"""

def bar(v, i):
    win = v > 0
    h = 75 if win else 150
    cor = "#16A34A" if win else "#E5484D"
    txt = "+0,5R" if win else "−1R"
    pos = f"bottom:220px;height:{h}px" if win else f"top:200px;height:{h}px"
    lab = f"bottom:{220+h+10}px" if win else f"top:{200+h+10}px"
    x = 40 + i * 86
    return (f'<div style="position:absolute;left:{x}px;{pos};width:58px;border-radius:10px;background:{cor}"></div>'
            f'<div style="position:absolute;left:{x-14}px;{lab};width:86px;text-align:center;font:800 19px Inter;color:{cor}">{txt}</div>')

BARS = "".join(bar(v, i) for i, v in enumerate([1,1,-1,1,1,-1,1,-1,1,-1]))

S2 = f"""
<div class="circ" style="width:820px;height:820px;left:-400px;top:-420px;background:#EFF5FF"></div>
<div class="circ" style="width:760px;height:760px;right:-430px;bottom:-360px;background:#FFF1F1"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">A CONTA</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:96px;width:940px">
  6 acertos pequenos.<br><span style="color:#E5484D">4 erros grandes.</span>
</div>
<div style="position:absolute;left:72px;top:432px;width:936px;font:500 27px/1.4 Inter;color:#475569">
  Cada acerto rende <b style="color:#16A34A">meio risco</b>. Cada erro leva <b style="color:#E5484D">o risco inteiro</b>.
<br><span style="color:#94A3B8;font-size:23px">R = quanto você arrisca por trade.</span>
</div>
<div class="card" style="position:absolute;left:72px;top:560px;width:936px;height:420px;overflow:hidden">
  <div style="position:absolute;left:24px;right:24px;top:199px;height:2px;background:#CBD5E1"></div>
  {BARS}
</div>
<div style="position:absolute;left:72px;top:1010px;width:936px;display:flex;gap:18px">
  <div class="card" style="flex:1;padding:20px 22px;border-radius:22px"><div style="font:600 21px Inter;color:#64748B">6 × +0,5R</div><div style="font:900 56px Archivo;font-stretch:80%;color:#16A34A">+3R</div></div>
  <div class="card" style="flex:1;padding:20px 22px;border-radius:22px"><div style="font:600 21px Inter;color:#64748B">4 × −1R</div><div style="font:900 56px Archivo;font-stretch:80%;color:#E5484D">−4R</div></div>
  <div style="flex:1.1;padding:20px 22px;border-radius:22px;background:#0B1533"><div style="font:600 21px Inter;color:#94A3B8">Resultado</div><div style="font:900 56px Archivo;font-stretch:80%;color:#FFD43B">−1R</div></div>
</div>
<div class="selo" style="left:72px;top:1190px">Exemplo ilustrativo · conta demo · antes de custos</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 2/3</div><div class="swipe">deslize →</div>
"""

def row(ratio, minimo, cor, destaque=False):
    bg = "background:#FFF7D6;" if destaque else ""
    return f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:16px 28px;border-top:2px solid #EEF2F7;{bg}">
  <span style="font:700 30px Inter;color:#0B1533">{ratio}</span>
  <span style="font:900 46px Archivo;font-stretch:80%;color:{cor}">{minimo}</span></div>"""

S3 = f"""
<div class="circ" style="width:820px;height:820px;right:-420px;top:-420px;background:#EEFBF3"></div>
<div class="circ" style="width:700px;height:700px;left:-380px;bottom:-330px;background:#EFF5FF"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">SEU ACERTO MÍNIMO</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:84px;width:960px">
  Quanto você precisa acertar?<br><span style="color:#16A34A">Depende do ganho e da perda.</span>
</div>
<div class="card" style="position:absolute;left:72px;top:420px;width:640px;overflow:hidden;padding-top:6px">
  <div style="display:flex;justify-content:space-between;padding:16px 28px 14px;font:700 20px Inter;letter-spacing:2px;color:#64748B">
    <span>GANHO MÉDIO ÷ PERDA MÉDIA</span><span>PARA EMPATAR</span></div>
  {row("0,5", "67%", "#E5484D", True)}
  {row("1", "50%", "#F59E0B")}
  {row("1,5", "40%", "#2563EB")}
  {row("2", "33%", "#16A34A")}
</div>
<div style="position:absolute;left:72px;top:900px;width:640px;font:600 23px/1.4 Inter;color:#64748B">
  Acerto mínimo = perda ÷ (ganho + perda). Antes de custos.
</div>
<img src="data:image/png;base64,{EXPL}" style="position:absolute;right:10px;top:440px;width:330px;filter:drop-shadow(0 24px 30px rgba(15,23,42,.25))">
<div style="position:absolute;left:72px;top:1000px;width:936px;font:800 40px/1.2 Inter;color:#0B1533">Antes de mirar no acerto,<br><span style="color:#2563EB">olhe quanto você ganha e quanto perde.</span></div>
<div style="position:absolute;left:72px;top:1140px;font:600 26px Inter;color:#64748B">Você sabe o seu ganho médio e a sua perda média?</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 3/3 &nbsp;·&nbsp; Conteúdo educativo</div>
"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"acerta60-51-0{i}.png"))
    b.close()
print("ok")
