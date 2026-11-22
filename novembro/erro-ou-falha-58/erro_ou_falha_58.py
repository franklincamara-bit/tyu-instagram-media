"""Erro técnico ou falha de disciplina? 3 casos (TYU-58, carrossel, publica qua 02/12/2026).
Capa colorida (preferência do Franklin). Slides 2 e 3 no padrão E (fundo branco). Sem ativo, sem preço, resultados em R.
Uso: python erro_ou_falha_58.py [pasta_saida]   (precisa de Archivo.ttf, pensativo.png e explicando.png nesta pasta)
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
.pillseries {{ position:absolute; font:800 24px Inter; letter-spacing:6px; padding:14px 30px; border-radius:999px; }}
.selo {{ position:absolute; font:700 19px Inter; letter-spacing:1px; color:#64748B; background:#F1F5F9; border:2px solid #E2E8F0; border-radius:999px; padding:8px 18px; }}
.tag {{ display:inline-block; font:900 26px Archivo; font-stretch:85%; letter-spacing:2px; color:#fff; padding:8px 18px 9px; border-radius:12px; }}
"""

def qcard(letra, rot, x, y, r="−1R"):
    return f"""<div style="position:absolute;left:{x}px;top:{y}px;width:200px;height:250px;background:#fff;border-radius:26px;
      box-shadow:0 26px 50px rgba(0,0,0,.35);transform:rotate({rot}deg);display:flex;flex-direction:column;align-items:center;justify-content:center">
      <div style="font:800 30px Inter;color:#64748B;letter-spacing:4px">TRADE {letra}</div>
      <div style="font:900 150px Archivo;font-stretch:80%;color:#2563EB;line-height:1">?</div>
      <div style="font:800 26px Inter;color:#E5484D">{r}</div></div>"""

S1 = f"""
<div style="position:absolute;inset:0;background:radial-gradient(760px 640px at 95% 4%,rgba(255,212,59,.30),transparent 60%),radial-gradient(900px 800px at 0% 100%,rgba(229,72,77,.30),transparent 60%),linear-gradient(160deg,#2563EB 0%,#1D4ED8 48%,#0B1533 100%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:90px 90px"></div>
<div class="logochip"><img src="data:image/png;base64,{LOGO}"></div>
<div class="pillseries" style="left:72px;top:170px;background:#0B1533;color:#FFD43B;box-shadow:0 10px 26px rgba(0,0,0,.3)">QUIZ DO DEBRIEF</div>
<div class="h" style="position:absolute;left:72px;top:262px;font-size:132px;width:980px;color:#fff;text-shadow:0 8px 0 rgba(11,21,51,.35)">
  3 TRADES RUINS.<br><span style="color:#FFD43B">3 CAUSAS<br>DIFERENTES.</span>
</div>
<div style="position:absolute;left:72px;top:672px;width:600px;font:500 33px/1.36 Inter;color:#E0E9FF">
  Erro técnico ou falha de disciplina? <b style="color:#fff">Classifica antes de arrastar.</b>
</div>
{qcard("A", -6, 64, 880)}
{qcard("B", 2, 290, 860)}
{qcard("C", -3, 516, 885, "−2R")}
<img src="data:image/png;base64,{PENS}" style="position:absolute;right:0px;top:560px;width:300px;z-index:4;filter:drop-shadow(0 30px 40px rgba(0,0,0,.40))">
<div class="selo" style="left:72px;top:1196px;background:rgba(255,255,255,.92);border-color:rgba(255,255,255,.6);color:#334155">Exemplo ilustrativo · conta demo</div>
<div class="foot" style="color:#BFD3FF">tradeyouup.net &nbsp;·&nbsp; 1/3</div><div class="swipe" style="color:#FFD43B;z-index:6;background:#0B1533;padding:8px 18px;border-radius:999px;right:56px;bottom:34px">deslize →</div>
"""

def caso(letra, texto, tag, cor, porque, top):
    return f"""<div class="card" style="position:absolute;left:72px;top:{top}px;width:936px;padding:26px 30px 28px 132px;min-height:200px">
  <div style="position:absolute;left:30px;top:28px;width:76px;height:76px;border-radius:20px;background:#0B1533;color:#FFD43B;
    display:flex;align-items:center;justify-content:center;font:900 46px Archivo;font-stretch:80%">{letra}</div>
  <div style="font:600 29px/1.34 Inter;color:#0B1533">“{texto}”</div>
  <div style="margin-top:16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap">
    <span class="tag" style="background:{cor}">{tag}</span>
    <span style="font:500 23px/1.3 Inter;color:#64748B">{porque}</span></div>
</div>"""

AZ, VM = "#2563EB", "#E5484D"
S2 = f"""
<div class="circ" style="width:820px;height:820px;left:-400px;top:-420px;background:#EFF5FF"></div>
<div class="circ" style="width:760px;height:760px;right:-430px;bottom:-360px;background:#FFF1F1"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">AS RESPOSTAS</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:84px;width:940px">
  Mesmo vermelho.<br><span style="color:{AZ}">Causas diferentes.</span>
</div>
{caso("A", "Setup certo, regra seguida. Mas o rompimento era falso.", "ERRO TÉCNICO", AZ, "o plano foi cumprido; a leitura falhou", 430)}
{caso("B", "Viu o setup se formando e entrou antes da confirmação pra não perder o movimento.", "FALHA DE DISCIPLINA", VM, "o plano mandava esperar", 685)}
{caso("C", "Calculou a mão errado e arriscou 2R achando que era 1R.", "ERRO TÉCNICO", AZ, "de execução", 940)}
<div class="selo" style="left:72px;top:1200px">Resultados em R · sem ativo · exemplo ilustrativo</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 2/3</div><div class="swipe">deslize →</div>
"""

def col(titulo, cor, verbo, itens, x):
    return f"""<div class="card" style="position:absolute;left:{x}px;top:420px;width:300px;min-height:350px;padding:26px 26px 28px;border-top:10px solid {cor}">
  <div style="font:800 22px Inter;letter-spacing:3px;color:{cor}">{titulo}</div>
  <div style="font:600 24px Inter;color:#64748B;margin-top:18px">se corrige com</div>
  <div style="font:900 50px/1 Archivo;font-stretch:78%;color:#0B1533;margin-top:6px">{verbo}</div>
  <div style="font:500 22px/1.4 Inter;color:#475569;margin-top:16px">{itens}</div></div>"""

S3 = f"""
<div class="circ" style="width:820px;height:820px;right:-420px;top:-420px;background:#EFF5FF"></div>
<div class="circ" style="width:700px;height:700px;left:-380px;bottom:-330px;background:#FFF1F1"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">POR QUE SEPARAR?</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:84px;width:960px">
  Cada causa tem<br><span style="color:{AZ}">um conserto diferente.</span>
</div>
{col("ERRO TÉCNICO", AZ, "ESTUDO", "leitura, execução,<br>cálculo da mão", 72)}
{col("FALHA DE DISCIPLINA", VM, "REGRA E<br>ROTINA", "o que você faz quando<br>o plano manda esperar", 400)}
<img src="data:image/png;base64,{EXPL}" style="position:absolute;right:0px;top:385px;width:262px;filter:drop-shadow(0 24px 30px rgba(15,23,42,.25))">
<div style="position:absolute;left:72px;top:975px;width:936px;padding:30px 34px;border-radius:28px;background:#0B1533">
  <div style="font:900 56px/1.04 Archivo;font-stretch:76%;color:#fff">Estudar mais o setup<br><span style="color:#FFD43B">não conserta o clique antecipado.</span></div></div>
<div style="position:absolute;left:72px;top:1196px;font:700 30px Inter;color:#0B1533">No debrief, registre cada um no seu lugar.</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 3/3 &nbsp;·&nbsp; Conteúdo educativo</div>
"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"erro-ou-falha-58-0{i}.png"))
    b.close()
print("ok")
