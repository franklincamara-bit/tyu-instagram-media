"""Opera em várias contas? (TYU-12, carrossel, publica sex 27/11/2026) — função Copiar trades (trade copier).
Capa colorida (preferência do Franklin: menos branco). Slides 2 e 3 no padrão E.
A tela do slide 2 é RECRIADA em HTML a partir do componente real do app (src/components/trade/ManageCopiesSection.jsx
e textos de src/locales/pt-BR.json, conferidos em 18/11/2026), com contas fictícias e resultados ocultos.
A seção "Cópias (trade copier)" só aparece no formulário do trade quando o usuário tem mais de uma conta (TradeForm.jsx).
Uso: python copiar_12.py [pasta_saida]   (precisa de Archivo.ttf, cansado.png e joinha.png nesta pasta)
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else D)
OUT.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(D / "Archivo.ttf")
LOGO = b64(D.parent.parent / "assets" / "logo.png")
CANS = b64(D / "cansado.png")
JOIA = b64(D / "joinha.png")

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
.blur {{ display:inline-block; width:86px; height:22px; border-radius:6px; background:linear-gradient(90deg,#CBD5E1,#E2E8F0,#CBD5E1); filter:blur(2px); vertical-align:middle; }}
"""

def form(conta, rot, top, left, z):
    return f"""
<div style="position:absolute;left:{left}px;top:{top}px;width:520px;transform:rotate({rot}deg);z-index:{z};background:#fff;border-radius:26px;box-shadow:0 26px 50px rgba(0,0,0,.35);padding:26px 30px 28px">
  <div style="display:flex;justify-content:space-between;align-items:center"><span style="font:800 26px Inter;color:#0B1533">Novo trade</span>
   <span style="font:700 20px Inter;color:#2563EB;background:#EEF4FF;border-radius:999px;padding:6px 16px">{conta}</span></div>
  <div style="margin-top:18px;font:600 17px Inter;letter-spacing:3px;color:#94A3B8">SETUP</div>
  <div style="margin-top:6px;height:46px;border-radius:12px;background:#F3F5FA;border:2px solid #E2E8F0;font:600 22px/42px Inter;color:#475569;padding-left:16px">Rompimento da abertura</div>
  <div style="margin-top:14px;font:600 17px Inter;letter-spacing:3px;color:#94A3B8">DEBRIEF</div>
  <div style="margin-top:6px;height:92px;border-radius:12px;background:#F3F5FA;border:2px solid #E2E8F0;font:500 21px/1.35 Inter;color:#475569;padding:10px 16px">Entrei antes da confirmação. Mesmo erro de ontem…</div>
</div>"""

S1 = f"""
<div style="position:absolute;inset:0;background:radial-gradient(760px 640px at 95% 4%,rgba(255,212,59,.30),transparent 60%),radial-gradient(900px 800px at 0% 100%,rgba(22,163,74,.30),transparent 60%),linear-gradient(160deg,#2563EB 0%,#1D4ED8 48%,#0B1533 100%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:90px 90px"></div>
<div class="logochip"><img src="data:image/png;base64,{LOGO}"></div>
<div class="pillseries" style="left:72px;top:170px;background:#0B1533;color:#FFD43B;box-shadow:0 10px 26px rgba(0,0,0,.3)">VÁRIAS CONTAS, UM DIÁRIO</div>
<div class="h" style="position:absolute;left:72px;top:262px;font-size:122px;width:980px;color:#fff;text-shadow:0 8px 0 rgba(11,21,51,.35)">
  OPERA EM<br><span style="color:#FFD43B">VÁRIAS CONTAS?</span>
</div>
<div style="position:absolute;left:72px;top:566px;width:600px;font:500 33px/1.36 Inter;color:#E0E9FF">
  E lança o <b style="color:#fff">mesmo trade</b> três vezes no diário, com o <b style="color:#fff">mesmo debrief</b>?
</div>
{form("Conta 03", -9, 770, 40, 1)}
{form("Conta 02", -4, 800, 120, 2)}
{form("Conta 01", 2, 840, 200, 3)}
<img src="data:image/png;base64,{CANS}" style="position:absolute;right:-90px;top:600px;width:520px;z-index:4;filter:drop-shadow(0 30px 40px rgba(0,0,0,.40))">
<div class="stamp" style="left:330px;top:1130px;font-size:52px;z-index:5">3× O MESMO TRABALHO</div>
<div class="foot" style="color:#BFD3FF">tradeyouup.net &nbsp;·&nbsp; 1/3</div><div class="swipe" style="color:#FFD43B">deslize →</div>
"""

def cand(conta, info, top):
    return f"""
  <div style="display:flex;align-items:flex-start;gap:18px;padding:14px 12px;border-radius:14px">
    <div style="width:30px;height:30px;border-radius:7px;background:#0F172A;flex:none;margin-top:3px;display:flex;align-items:center;justify-content:center">
      <svg viewBox="0 0 24 24" width="22" height="22"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
    <div><div style="font:700 25px Inter;color:#0F172A">{conta} <span style="font:700 15px Inter;background:#E2E8F0;color:#334155;border-radius:6px;padding:2px 8px;vertical-align:middle">NT8</span></div>
      <div style="font:500 21px Inter;color:#64748B;margin-top:4px">{info} · <span class="blur"></span></div></div>
  </div>"""

S2 = f"""
<div class="circ" style="width:820px;height:820px;left:-400px;top:-420px;background:#EFF5FF"></div>
<div class="circ" style="width:760px;height:760px;right:-430px;bottom:-360px;background:#FFF6D6"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">NA PLATAFORMA</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:96px;width:940px">
  Registre uma vez.<br><span style="color:#2563EB">Copie para as outras.</span>
</div>
<div style="position:absolute;left:72px;top:432px;width:936px;font:500 27px/1.4 Inter;color:#475569">
  No próprio trade, em <b style="color:#0B1533">Cópias (trade copier)</b>, toque em <b style="color:#0B1533">Copiar trade</b> e escolha para onde vai a cópia.
</div>
<div class="card" style="position:absolute;left:72px;top:560px;width:936px;padding:30px 34px 28px;border-radius:24px;box-shadow:0 30px 70px rgba(15,23,42,.16)">
  <div style="font:800 32px Inter;color:#0F172A">Copiar trade</div>
  <div style="font:500 22px Inter;color:#64748B;margin-top:6px">Para onde vai a cópia deste trade?</div>
  <div style="display:flex;gap:16px;margin-top:20px">
    <div style="flex:1;border:3px solid #F59E0B;background:#FFFBEB;border-radius:16px;padding:16px 18px">
      <div style="font:800 23px Inter;color:#1E293B">🔗 Trades já registrados</div>
      <div style="font:500 18px/1.38 Inter;color:#64748B;margin-top:6px">Vieram do NinjaTrader ou você já lançou. Os valores ficam como estão; vão o debrief e as imagens.</div></div>
    <div style="flex:1;border:2px solid #E2E8F0;border-radius:16px;padding:16px 18px">
      <div style="font:800 23px Inter;color:#1E293B">＋ Criar trades novos</div>
      <div style="font:500 18px/1.38 Inter;color:#64748B;margin-top:6px">Cria um trade em cada conta com os mesmos dados deste, inclusive o resultado.</div></div>
  </div>
  <div style="font:500 19px Inter;color:#64748B;margin-top:20px">Trades de outras contas no mesmo dia. Os que parecem o mesmo trade já vêm marcados.</div>
  {cand("Conta 02", "10:42 · Compra · 2x", 0)}
  {cand("Conta 03", "10:42 · Compra · 1x", 0)}
  <div style="display:flex;justify-content:flex-end;gap:14px;margin-top:10px">
    <span style="font:700 22px Inter;color:#0F172A;border:2px solid #E2E8F0;border-radius:12px;padding:12px 24px">Cancelar</span>
    <span style="font:700 22px Inter;color:#fff;background:#0F172A;border-radius:12px;padding:12px 24px">Confirmar</span></div>
</div>
<div class="selo" style="left:72px;top:1208px">Exemplo ilustrativo · conta demo · tela recriada, resultados ocultos</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 2/3</div><div class="swipe">deslize →</div>
"""

def item(n, q, a, top, cor):
    return f"""
<div class="card" style="position:absolute;left:72px;top:{top}px;width:936px;padding:30px 34px;display:flex;gap:28px;align-items:flex-start">
  <div style="font:900 84px Archivo;font-stretch:80%;color:{cor};line-height:.9;width:70px">{n}</div>
  <div><div style="font:800 34px Inter;color:#0B1533">{q}</div><div style="font:500 26px/1.42 Inter;color:#475569;margin-top:8px">{a}</div></div>
</div>"""

S3 = f"""
<div class="circ" style="width:820px;height:820px;right:-420px;top:-420px;background:#EEFBF3"></div>
<div class="circ" style="width:700px;height:700px;left:-380px;bottom:-330px;background:#EFF5FF"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">COMO ESCOLHER</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:92px;width:940px">
  O debrief vai junto.<br><span style="color:#16A34A">O resultado de cada<br>conta continua dela.</span>
</div>
{item("1", "Veio do NinjaTrader?", "Vincule. Os valores de cada conta ficam como estão; o debrief e as imagens são copiados.", 560, "#2563EB")}
{item("2", "Lançou em uma conta só?", "Crie as cópias: um trade em cada conta com os mesmos dados, inclusive o resultado.", 790, "#F59E0B")}
<div style="position:absolute;left:72px;top:1040px;width:620px;font:800 40px/1.2 Inter;color:#0B1533">A decisão foi uma só.<br><span style="color:#2563EB">A revisão também pode ser.</span></div>
<div style="position:absolute;left:72px;top:1170px;font:600 26px Inter;color:#64748B">Quantas contas você opera hoje?</div>
<img src="data:image/png;base64,{JOIA}" style="position:absolute;right:30px;top:990px;width:250px;filter:drop-shadow(0 24px 30px rgba(15,23,42,.25))">
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 3/3 &nbsp;·&nbsp; Conteúdo educativo</div>
"""

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"copiar-trades-12-0{i}.png"))
    b.close()
print("ok")
