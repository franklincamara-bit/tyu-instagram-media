"""Tribunal do Trade #2: o alvo que nunca existiu (TYU-61, carrossel, publica qua 18/11/2026).
Série Tribunal do Trade (o #1 foi o Trial Reel do stop móvel). Réu: um trade sem alvo definido.
Capa colorida (preferência do Franklin: menos branco). Slides 2 e 3 no padrão E, com variação.
Números = R e taxa de acerto de empate (cálculo próprio, antes de custos): 1/(1+0,5) = 66,7% ; 1/(1+2) = 33,3%.
Uso: python tribunal_02.py [pasta_saida]   (precisa de Archivo.ttf e das poses nesta pasta)
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else D)
OUT.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(D / "Archivo.ttf")
LOGO = b64(D.parent.parent / "assets" / "logo.png")
JUIZ = b64(D / "explicando.png")
CRUZ = b64(D / "bracos-cruzados.png")

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
"""

# ---------------- SLIDE 1 — capa colorida ----------------
S1 = f"""
<div style="position:absolute;inset:0;background:radial-gradient(760px 640px at 95% 4%,rgba(255,212,59,.28),transparent 60%),radial-gradient(900px 800px at 0% 100%,rgba(229,72,77,.32),transparent 60%),linear-gradient(160deg,#2563EB 0%,#1D4ED8 48%,#0B1533 100%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:90px 90px"></div>
<div class="logochip"><img src="data:image/png;base64,{LOGO}"></div>
<div class="pillseries" style="left:72px;top:170px;background:#0B1533;color:#FFD43B;box-shadow:0 10px 26px rgba(0,0,0,.3)">TRIBUNAL DO TRADE · Nº 2</div>
<div class="h" style="position:absolute;left:72px;top:262px;font-size:136px;width:960px;color:#fff;text-shadow:0 8px 0 rgba(11,21,51,.35)">
  O ALVO QUE<br><span style="color:#FFD43B">NUNCA EXISTIU</span>
</div>
<div style="position:absolute;left:72px;top:556px;width:560px;font:500 31px/1.38 Inter;color:#E0E9FF">
  <b style="color:#fff">Réu:</b> um trade que entrou com stop e sem saída escrita.
</div>
<div style="position:absolute;left:72px;top:700px;width:540px;background:rgba(11,21,51,.72);border:2px solid rgba(255,255,255,.18);border-radius:26px;padding:26px 30px">
  <div style="font:800 20px Inter;letter-spacing:4px;color:#93B4FF">DEPOIMENTO DO RÉU</div>
  <div style="font:700 34px/1.3 Inter;color:#fff;margin-top:12px">“Chegou a +1,2R.<br>Saí no +0,3R.<br><span style="color:#FFD43B">Protegi o lucro</span>, Excelência.”</div>
</div>
<img src="data:image/png;base64,{JUIZ}" style="position:absolute;right:-40px;top:560px;width:520px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.40))">
<div style="position:absolute;left:570px;top:1100px;width:490px;height:260px;background:linear-gradient(180deg,#16224A,#0B1533);border-radius:18px;box-shadow:0 20px 40px rgba(0,0,0,.45)">
  <div style="margin:18px 26px 0;height:3px;background:#2563EB"></div>
  <div style="margin:20px auto 0;width:400px;white-space:nowrap;text-align:center;font:600 18px Inter;letter-spacing:6px;color:#C7D2FE;border:2px solid rgba(199,210,254,.35);border-radius:10px;padding:8px 0">EXCELENTÍSSIMO JUIZ</div>
</div>
<div class="stamp" style="left:84px;top:1010px;font-size:58px">EM JULGAMENTO</div>
<div class="foot" style="color:#BFD3FF">tradeyouup.net &nbsp;·&nbsp; 1/3</div><div class="swipe" style="color:#FFD43B">deslize →</div>
"""

# ---------------- SLIDE 2 — os autos ----------------
def ev(hora, r, txt, fala, cor):
    return f"""
  <div style="display:flex;align-items:center;gap:26px;padding:22px 30px;border-bottom:2px solid #EEF2F6">
    <div style="width:118px;font:800 34px Inter;color:#0B1533">{hora}</div>
    <div style="width:150px;text-align:center;font:900 38px Archivo;font-stretch:80%;color:{cor};background:{cor}14;border-radius:14px;padding:6px 0">{r}</div>
    <div style="flex:1">
      <div style="font:700 27px/1.25 Inter;color:#0B1533">{txt}</div>
      <div style="font:italic 500 24px/1.3 Inter;color:#64748B;margin-top:4px">{fala}</div>
    </div>
  </div>"""

S2 = f"""
<div class="circ" style="width:820px;height:820px;left:-400px;top:-420px;background:#EFF5FF"></div>
<div class="circ" style="width:760px;height:760px;right:-430px;bottom:-360px;background:#FFF6D6"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">OS AUTOS DO PROCESSO</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:92px;width:940px">
  Quem decidiu a saída<br><span style="color:#E5484D">não foi o plano.</span>
</div>
<div class="card" style="position:absolute;left:72px;top:440px;width:936px;overflow:hidden">
  <div style="display:flex;gap:26px;padding:16px 30px;background:#0B1533;font:800 18px Inter;letter-spacing:3px;color:#93B4FF">
    <div style="width:118px">HORA</div><div style="width:150px;text-align:center">RESULTADO</div><div>O QUE ACONTECEU</div>
  </div>
  {ev("9h41", "0R", "Entrada. Stop de 1R. Alvo: nenhum.", "“Vejo na hora até onde vai.”", "#475569")}
  {ev("9h52", "+1,2R", "O preço anda a favor.", "“Pode ir mais. Deixa correr.”", "#16A34A")}
  {ev("10h03", "+0,6R", "Metade do lucro devolvido.", "“Agora eu seguro. Vai voltar.”", "#B7791F")}
  {ev("10h09", "+0,3R", "Saída no susto.", "“Protegi o lucro.”", "#E5484D")}
</div>
<div style="position:absolute;left:72px;top:1052px;width:936px;font:400 29px/1.42 Inter;color:#475569">
  Sem alvo escrito, cada vela vira uma nova decisão. Primeiro decide a <b style="color:#0B1533">ganância</b>, depois decide o <b style="color:#0B1533">medo</b>.
</div>
<div style="position:absolute;left:72px;top:1192px;width:936px;font:600 19px Inter;color:#94A3B8">Exemplo ilustrativo · horários e resultados fictícios, em R</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 2/3</div><div class="swipe">deslize →</div>
"""

# ---------------- SLIDE 3 — o veredito ----------------
def conta(saida, pct, cor, nota):
    return f"""
  <div class="card" style="flex:1;padding:24px 26px 22px;text-align:center">
    <div style="font:700 22px Inter;color:#64748B">Stop 1R · saída média</div>
    <div style="font:900 64px Archivo;font-stretch:80%;color:{cor};margin-top:2px">{saida}</div>
    <div style="height:2px;background:#EEF2F6;margin:12px 0 14px"></div>
    <div style="font:700 22px Inter;color:#64748B">acerto para empatar</div>
    <div style="font:900 84px Archivo;font-stretch:80%;color:#0B1533;line-height:1">{pct}</div>
    <div style="font:500 21px/1.3 Inter;color:#64748B;margin-top:8px">{nota}</div>
  </div>"""

S3 = f"""
<div class="circ" style="width:560px;height:560px;right:-300px;top:-330px;background:#E5484D"></div>
<div class="circ" style="width:900px;height:900px;left:-440px;top:1000px;background:#EFF5FF"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label" style="color:#E5484D">O VEREDITO</div>
<div class="stamp" style="right:96px;top:150px;font-size:64px">CULPADO</div>
<div class="h" style="position:absolute;left:72px;top:266px;font-size:80px;width:960px">
  Sem alvo, você nem sabe<br><span style="color:#2563EB">quanto precisa acertar.</span>
</div>
<div style="position:absolute;left:72px;top:450px;width:936px;display:flex;gap:28px">
  {conta("+0,5R", "67%", "#E5484D", "2 de cada 3 trades<br>precisam dar certo")}
  {conta("+2R", "33%", "#16A34A", "1 de cada 3 trades<br>já empata")}
</div>
<div style="position:absolute;left:72px;top:868px;width:936px;font:500 19px Inter;color:#94A3B8">Cálculo próprio, antes de custos: acerto de empate = perda ÷ (ganho + perda).</div>
<div style="position:absolute;left:72px;top:922px;width:700px;background:#0B1533;border-radius:28px;padding:28px 34px;box-shadow:0 20px 40px rgba(11,21,51,.18)">
  <div style="font:800 20px Inter;letter-spacing:4px;color:#FFD43B">A SENTENÇA</div>
  <div style="font:800 32px/1.25 Inter;color:#fff;margin-top:10px">Antes de clicar, escreva a saída.</div>
  <div style="font:400 25px/1.42 Inter;color:#C7D2FE;margin-top:8px">Alvo em R, ou a regra que move o stop. Mudou no meio do trade? Anote o porquê no diário.</div>
</div>
<img src="data:image/png;base64,{CRUZ}" style="position:absolute;right:20px;top:880px;width:270px;filter:drop-shadow(0 20px 30px rgba(15,23,42,.25))">
<div style="position:absolute;left:72px;top:1190px;width:700px;font:700 27px/1.3 Inter;color:#0B1533">Próximo réu? Comenta aí qual erro<br>vai a julgamento.</div>
<div style="position:absolute;left:72px;top:1268px;width:700px;font:400 18px Inter;color:#94A3B8">Conteúdo educativo. Não é recomendação de investimento.</div>
<div class="foot" style="bottom:22px">tradeyouup.net &nbsp;·&nbsp; 3/3</div>
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"tribunal-02-0{i}.png"))
    b.close()
print("ok", OUT)
