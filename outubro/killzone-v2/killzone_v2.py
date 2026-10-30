"""Killzone v2 (retorno 30/10/2026): killzone = janela para operar; dentro dela, espera-se o setup."""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else D / "kz_new")
OUT.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(D / "Archivo.ttf")
LOGO = b64("/home/claude/tyu-instagram-media/assets/logo.png")
AVATAR = b64(D / "avatar_lupa.png")

CSS = f"""
@font-face {{ font-family: Archivo; src: url(data:font/ttf;base64,{FONT}); font-weight: 100 900; font-stretch: 62% 125%; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:#fff; font-family: Archivo, Inter, sans-serif; color:#0B1533; position:relative; overflow:hidden; }}
.circ {{ position:absolute; border-radius:50%; }}
.logo {{ position:absolute; left:72px; top:58px; width:156px; }}
.label {{ position:absolute; left:72px; top:168px; font-weight:800; letter-spacing:5px; font-size:24px; color:#2563EB; }}
.h {{ font-weight:900; font-stretch:72%; line-height:0.98; letter-spacing:-1px; }}
.pill {{ display:inline-block; color:#fff; padding:0 22px 8px; border-radius:22px; }}
.foot {{ position:absolute; left:72px; bottom:44px; font-size:21px; color:#94A3B8; font-family: Inter; }}
.swipe {{ position:absolute; right:72px; bottom:42px; font-size:22px; color:#2563EB; font-weight:800; font-family: Inter; }}
.card {{ background:#fff; border:2px solid #E2E8F0; border-radius:28px; box-shadow:0 18px 40px rgba(15,23,42,.08); }}
.tl {{ position:absolute; left:72px; width:936px; height:236px; padding:40px 20px 0; }}
.track {{ position:relative; height:64px; background:#EEF2F6; border-radius:14px; margin-top:44px; }}
.blk {{ position:absolute; top:0; height:64px; border-radius:12px; }}
.blk span {{ position:absolute; top:-42px; left:50%; transform:translateX(-50%); font:700 22px Inter; white-space:nowrap; color:#0B1533; }}
.ticks {{ display:flex; justify-content:space-between; margin:16px -20px 0; font:600 19px Inter; color:#94A3B8; }}
.badge {{ display:inline-block; font:800 17px Inter; letter-spacing:2px; padding:8px 14px; border-radius:10px; }}
"""

def timeline(top):
    # régua 24h, horário de NY (definição clássica): Londres 2h-5h, NY 7h-10h, Ásia 20h-24h
    w = 896
    pos = lambda h: h / 24 * w
    blk = lambda a, b, name, col: f'<div class="blk" style="left:{pos(a)}px;width:{pos(b)-pos(a)}px;background:{col}"><span>{name}</span></div>'
    ticks = "".join(f"<span>{h:02d}h</span>" for h in range(0, 25, 3)).replace("24h", "00h")
    return f'''<div class="card tl" style="top:{top}px"><div class="track">
      {blk(2,5,"Londres","#2563EB")}{blk(7,10,"Nova York","#2563EB")}{blk(20,24,"Ásia","#CBD5E1")}
    </div><div class="ticks">{ticks}</div></div>'''

S1 = f"""
<div class="circ" style="width:560px;height:560px;right:-280px;top:-340px;background:#2563EB"></div>
<div class="circ" style="width:900px;height:900px;left:-420px;top:910px;background:#EFF5FF"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">ICT SEM MITO</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:112px;width:720px">
  Killzone é a sua janela para<br><span class="pill" style="background:#16A34A;margin-top:12px">operar.</span>
</div>
<div class="h" style="position:absolute;left:72px;top:600px;font-size:62px;color:#2563EB;width:660px">
  Mas janela aberta não é sinal de entrada.
</div>
<div style="position:absolute;left:72px;top:770px;width:640px;font:500 30px/1.35 Inter;color:#334155">
  Dentro dela, você <b style="color:#0B1533">espera o seu setup aparecer</b>.
</div>
<img src="data:image/png;base64,{AVATAR}" style="position:absolute;right:20px;top:330px;width:290px">
{timeline(1000)}
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 1/3</div><div class="swipe">deslize →</div>
"""

def li(ok, txt):
    sym = '<span style="color:#16A34A">✓</span>' if ok else '<span style="color:#E5484D">✕</span>'
    return f'<div style="display:flex;gap:16px;margin-top:22px;font:700 31px/1.25 Inter">{sym}<div>{txt}</div></div>'

S2 = f"""
<div class="circ" style="width:820px;height:820px;left:-380px;top:-380px;background:#EFF5FF"></div>
<div class="circ" style="width:760px;height:760px;right:-420px;bottom:-330px;background:#2563EB"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">O QUE É, DE VERDADE</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:92px;width:940px">
  A hora certa de operar.<br>Esperando o setup certo.
</div>
<div style="position:absolute;left:72px;top:420px;width:930px;font:400 31px/1.5 Inter;color:#475569">
  No ICT, killzone é o período em que a liquidez das grandes sessões entra no mercado. É ali que deslocamentos e capturas de liquidez costumam aparecer. Por isso é a janela para operar.
</div>
<div class="card" style="position:absolute;left:72px;top:640px;width:454px;padding:38px 32px 44px">
  <div class="badge" style="background:#DCFCE7;color:#15803D">NA KILLZONE, VOCÊ</div>
  {li(True,"Fica atento ao mercado")}{li(True,"Espera o seu setup se formar")}{li(True,"Executa quando ele aparece")}
</div>
<div class="card" style="position:absolute;left:554px;top:640px;width:454px;padding:38px 32px 44px">
  <div class="badge" style="background:#FEE2E2;color:#C53030">NA KILLZONE, VOCÊ NÃO</div>
  {li(False,"Entra só porque o horário abriu")}{li(False,"Força um trade sem setup")}{li(False,"Trata o relógio como gatilho")}
</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 2/3</div>
"""

S3 = f"""
<div class="circ" style="width:560px;height:560px;right:-280px;top:-340px;background:#2563EB"></div>
<div class="circ" style="width:900px;height:900px;left:-420px;top:910px;background:#EFF5FF"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">NA PRÁTICA</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:84px;width:940px">
  Killzone + setup<br>= <span style="color:#16A34A">trade.</span>
</div>
<div class="h" style="position:absolute;left:72px;top:400px;font-size:84px;width:940px">
  Killzone sem setup<br>= <span style="color:#2563EB">espera.</span>
</div>
<div style="position:absolute;left:72px;top:610px;width:936px;background:#0B1533;border-radius:28px;padding:34px 36px">
  <div style="font:800 34px Inter;color:#fff">A janela fechou e o setup não veio?</div>
  <div style="font:400 29px Inter;color:#C7D2FE;margin-top:8px">Dia sem trade. Isso também é disciplina.</div>
</div>
{timeline(800)}
<div style="position:absolute;left:72px;top:1052px;width:936px;font:400 20px/1.35 Inter;color:#94A3B8">
  Definição clássica do ICT, horário de Nova York (há variações entre autores). Conteúdo educativo, não é recomendação de operação.
</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 3/3</div>
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f"killzone-v2-0{i}.png"))
    b.close()
print("ok", OUT)
