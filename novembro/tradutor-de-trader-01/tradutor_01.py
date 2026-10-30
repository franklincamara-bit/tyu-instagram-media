"""TYU-50 Tradutor de Trader #1 (imagem única 1080x1350, visual legenda de filme).
Uso: python3 tradutor_01.py <Archivo.ttf> [saida.png]
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
REPO = D.parent.parent
FONT_PATH = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else D / "tradutor-de-trader-01.png"
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(FONT_PATH)
LOGO = b64(REPO / "assets/logo.png")
AV = b64(REPO / "assets/explicando.png")

HTML = f"""<html><head><style>
@font-face {{ font-family: Archivo; src: url(data:font/ttf;base64,{FONT}); font-weight:100 900; font-stretch:62% 125%; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; overflow:hidden; position:relative; background:#fff; font-family:Inter, sans-serif; color:#0B1533; }}
.top {{ position:absolute; left:56px; right:56px; top:44px; display:flex; justify-content:space-between; align-items:center; }}
.tag {{ font:800 22px Inter; letter-spacing:4px; color:#fff; background:#2563EB; padding:10px 16px; border-radius:8px; }}
.logo {{ width:150px; }}
.frame {{ position:absolute; left:56px; right:56px; top:120px; height:700px; border-radius:22px; overflow:hidden;
  background: radial-gradient(ellipse 60% 70% at 62% 45%, #3B4A6B 0%, #1B2540 55%, #0B1124 100%); }}
.bar {{ position:absolute; left:0; right:0; height:62px; background:#05080F; }}
.grain {{ position:absolute; inset:0; background:repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 2px, transparent 2px 4px); }}
.av {{ position:absolute; left:60%; transform:translateX(-50%); top:84px; height:1150px; filter: drop-shadow(0 20px 40px rgba(0,0,0,.45)) brightness(.93); }}
.sub {{ position:absolute; left:40px; right:40px; bottom:100px; text-align:center; font:600 52px/1.25 Inter; color:#FFF8D6;
  text-shadow: 0 0 6px #000, 0 3px 0 #000, 0 -2px 0 #000, 2px 0 0 #000, -2px 0 0 #000; }}
.shade {{ position:absolute; left:0; right:0; bottom:0; height:300px; background:linear-gradient(to bottom, transparent, rgba(5,8,15,.85)); }}
.rec {{ position:absolute; left:28px; top:84px; font:600 18px Inter; letter-spacing:3px; color:#CBD5E1; opacity:.8; }}
.rec b {{ display:inline-block; width:12px; height:12px; border-radius:50%; background:#E5484D; margin-right:10px; vertical-align:1px; }}
.tr {{ position:absolute; left:56px; right:56px; top:868px; }}
.lbl {{ font:800 24px Inter; letter-spacing:5px; color:#2563EB; display:flex; align-items:center; gap:16px; }}
.lbl:after {{ content:""; flex:1; height:3px; background:#2563EB; opacity:.25; }}
.big {{ font-family:Archivo; font-weight:900; font-stretch:72%; font-size:132px; line-height:.95; letter-spacing:-1px; margin-top:18px; }}
.big span {{ color:#2563EB; }}
.note {{ font:400 30px/1.4 Inter; color:#475569; margin-top:22px; }}
.foot {{ position:absolute; left:0; right:0; bottom:0; height:96px; border-top:2px solid #E2E8F0; display:flex; align-items:center; justify-content:space-between; padding:0 56px; }}
.foot .s {{ font:600 26px Inter; color:#475569; }}
.foot .u {{ font:400 22px Inter; color:#94A3B8; }}
</style></head><body>
<div class="top"><div class="tag">TRADUTOR DE TRADER</div><img class="logo" src="data:image/png;base64,{LOGO}"></div>
<div class="frame">
  <div class="grain"></div>
  <img class="av" src="data:image/png;base64,{AV}">
  <div class="shade"></div><div class="bar" style="top:0"></div><div class="bar" style="bottom:0"></div>
  <div class="rec"><b></b>CENA 1 · DEPOIS DO STOP</div>
  <div class="sub">— Foi só uma entrada de teste.</div>
</div>
<div class="tr">
  <div class="lbl">TRADUÇÃO</div>
  <div class="big">Entrei <span>sem gatilho.</span></div>
  <div class="note">Trade de teste também é trade: arrisca dinheiro de verdade, entra no diário e conta no risco do dia.</div>
</div>
<div class="foot"><div class="s">Tradutor de Trader · #1</div><div class="u">tradeyouup.net</div></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(HTML)
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(OUT))
    b.close()
print(OUT)
