"""TYU-55 Conversas que o Trader Esconde #2 (imagem única 1080x1350, chat Trader x Stop).
Uso: python3 conversas_02.py [saida.png]
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
REPO = D.parent.parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else D / "conversas-02.png"
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
LOGO = b64(REPO / "assets/logo.png")
AV = b64(REPO / "assets/celular-contrariado.png")

MSGS = [
    ("in",  "Fui atingido. −1R, como combinado.", "10:31"),
    ("out", "Peraí. Me dá outra chance.", "10:31"),
    ("out", "Se eu tivesse colocado 5 pontos mais longe, tinha virado gain.", "10:32"),
    ("in",  "Sempre tem 5 pontos que teriam dado certo. Você só descobre depois.", "10:32"),
    ("out", "Então deixa eu entrar de novo agora, só pra recuperar.", "10:33"),
    ("in",  "Isso não é setup. É vingança com outro nome.", "10:33"),
    ("out", "Você é muito rígido.", "10:34"),
    ("in",  "Eu sou a única parte do seu plano que fez exatamente o que você pediu. 🙂", "10:34"),
]
bubbles = "\n".join(
    f'<div class="row {d}"><div class="b {d}">{t}<span class="t">{h}</span></div></div>' for d, t, h in MSGS)

HTML = f"""<html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; overflow:hidden; position:relative; background:#EAF0F8;
  font-family:Inter, 'Noto Color Emoji', sans-serif; color:#0B1533; }}
.head {{ position:absolute; left:0; right:0; top:0; height:150px; background:#0B1533; display:flex; align-items:center; padding:0 56px; gap:26px; }}
.ic {{ width:84px; height:84px; border-radius:50%; background:#E5484D; display:flex; align-items:center; justify-content:center; font-size:44px; }}
.nm {{ font:800 46px Inter; color:#fff; }}
.on {{ font:500 26px Inter; color:#7FB0FF; margin-top:2px; }}
.serie {{ margin-left:auto; font:800 18px Inter; letter-spacing:3px; color:#0B1533; background:#FFD43B; padding:10px 14px; border-radius:8px; }}
.chat {{ position:absolute; left:48px; right:48px; top:170px; display:flex; flex-direction:column; gap:12px; }}
.row {{ display:flex; }}
.row.out {{ justify-content:flex-end; }}
.b {{ max-width:800px; padding:16px 24px 14px; border-radius:26px; font:600 30px/1.27 Inter, 'Noto Color Emoji'; position:relative; box-shadow:0 3px 0 rgba(11,21,51,.07); }}
.b.in {{ background:#fff; color:#0B1533; border-bottom-left-radius:8px; }}
.b.out {{ background:#2563EB; color:#fff; border-bottom-right-radius:8px; }}
.t {{ display:inline-block; font:500 18px Inter; margin-left:14px; opacity:.6; vertical-align:-2px; white-space:nowrap; }}
.typing {{ align-self:flex-end; background:#2563EB; border-radius:26px; border-bottom-right-radius:8px; padding:18px 26px; display:flex; gap:10px; align-items:center; }}
.typing i {{ width:13px; height:13px; border-radius:50%; background:#fff; opacity:.85; display:block; }}
.typing i:nth-child(2) {{ opacity:.6; }} .typing i:nth-child(3) {{ opacity:.35; }}
.typing span {{ font:500 20px Inter; color:#DCE7FF; margin-left:8px; }}
.band {{ position:absolute; left:0; right:0; bottom:110px; height:150px; background:#0B1533; display:flex; align-items:center; padding:0 56px; }}
.band p {{ font:800 38px/1.25 Inter; color:#fff; }}
.band p b {{ color:#FFD43B; }}
.foot {{ position:absolute; left:0; right:0; bottom:0; height:110px; background:#fff; display:flex; align-items:center; padding:0 56px; gap:22px; }}
.av {{ width:78px; height:78px; border-radius:50%; border:4px solid #2563EB; overflow:hidden; background:#DCE7FF; }}
.av img {{ width:100%; height:auto; margin-top:2px; }}
.fs {{ font:600 26px Inter; color:#475569; }}
.logo {{ margin-left:auto; width:150px; }}
</style></head><body>
<div class="head"><div class="ic">🛑</div><div><div class="nm">Stop</div><div class="on">online</div></div><div class="serie">CONVERSAS #2</div></div>
<div class="chat">
{bubbles}
<div class="typing"><i></i><i></i><i></i><span>digitando…</span></div>
</div>
<div class="band"><p>Stop atingido é o plano funcionando.<br><b>O erro é renegociar com ele.</b></p></div>
<div class="foot"><div class="av"><img src="data:image/png;base64,{AV}"></div><div class="fs">Conversas que o Trader Esconde · #2</div><img class="logo" src="data:image/png;base64,{LOGO}"></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(HTML)
    pg.wait_for_timeout(500)
    h = pg.evaluate("document.querySelector('.chat').getBoundingClientRect().bottom")
    print("chat bottom:", h)
    pg.screenshot(path=str(OUT))
    b.close()
print(OUT)
