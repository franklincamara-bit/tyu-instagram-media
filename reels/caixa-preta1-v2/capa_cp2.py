# Capa v2.1 do Trial Reel "Caixa-Preta do Trader #1" (TYU-59), roteiro v2.1, 1080x1920, padrão "capa ousada" (04/11/2026):
# fundo azul royal -> marinho, título 3D branco + amarelo, faixa inclinada, personagem oficial com luz de recorte, logo no selo branco.
# Uso: python3 capa_cp2.py  -> caixa-preta1-v2-capa.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(HERE, "tpl", "logo.png")
AV = os.path.join(ROOT, "assets", "celular-contrariado.png")

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:'InterD'}
.bg{position:absolute;inset:0;background:radial-gradient(900px 900px at 50% 38%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)}
.rays{position:absolute;left:-600px;top:-300px;width:2400px;height:2400px;background:repeating-conic-gradient(from 0deg at 50% 50%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg);
  -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 10%,transparent 60%)}
.t{position:absolute;left:0;right:0;text-align:center;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-3px;
  -webkit-text-stroke:10px #0A1640;paint-order:stroke fill;text-shadow:0 6px 0 #0A1640,0 12px 0 #0A1640,0 18px 0 rgba(10,22,64,.85),0 30px 40px rgba(0,0,0,.45)}
.w{color:#fff}.y{color:#FFD43B}
.band{position:absolute;left:0;right:0;text-align:center}
.band b{display:inline-block;font:900 62px 'InterD';color:#fff;padding:14px 40px 20px;border-radius:22px;letter-spacing:-1px;transform:rotate(-3deg);
  border:6px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.4);background:linear-gradient(180deg,#FF8A3D,#E2600E)}
.av{position:absolute;filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 26px rgba(120,190,255,.8)) drop-shadow(0 40px 50px rgba(0,0,0,.45))}
.card{position:absolute;right:46px;top:790px;width:500px;height:650px;background:#fff;border-radius:44px;box-shadow:0 40px 80px rgba(0,0,0,.45);transform:rotate(3deg);overflow:hidden}
.hd{position:absolute;left:36px;top:30px;font:700 26px 'InterD';letter-spacing:4px;color:#7A8499}
.rail{position:absolute;left:150px;top:100px;width:10px;height:500px;border-radius:5px;background:linear-gradient(180deg,#7A8499,#F59E0B 50%,#E5484D)}
.ev{position:absolute;left:24px;width:460px;height:80px}
.ev .tm{position:absolute;left:0;top:18px;width:100px;text-align:right;font:900 36px 'InterD';letter-spacing:-1px}
.ev .d{position:absolute;left:114px;top:16px;width:46px;height:46px;border-radius:50%;background:#fff;border:9px solid}
.ev .x{position:absolute;left:186px;top:14px;font:900 38px 'InterD';letter-spacing:-1px;color:#0B1533}
.mz{position:absolute;left:12px;top:92px;width:478px;height:100px;border-radius:24px;border:7px solid #FFD43B;box-shadow:0 0 0 10px rgba(255,212,59,.3)}
.logo{position:absolute;left:0;right:0;top:1590px;text-align:center}
.logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(0,0,0,.3)}
.logo img{width:290px;display:block}
.calm{position:absolute;left:0;right:0;top:1540px;bottom:0;background:linear-gradient(180deg,transparent,rgba(5,12,40,.55))}
</style></head><body>
<div class="bg"></div><div class="rays"></div>
<div class="t w" style="top:210px;font-size:100px;letter-spacing:-2px">O ERRO COMEÇOU</div>
<div class="t y" style="top:325px;font-size:156px">12 MIN ANTES</div>
<div class="band" style="top:570px"><b>CAIXA-PRETA DO TRADER</b></div>
<img class="av" src="file://__AV__" style="left:-30px;top:760px;width:560px">
<div class="card"><div class="hd">MINUTO A MINUTO</div><div class="rail"></div>
 <div class="mz"></div>
 <div class="ev" style="top:102px"><div class="tm" style="color:#D97706">9h38</div><div class="d" style="border-color:#F59E0B"></div><div class="x">“só 1R”</div></div>
 <div class="ev" style="top:222px"><div class="tm" style="color:#0B1533">9h40</div><div class="d" style="border-color:#7A8499"></div><div class="x">stop −1R</div></div>
 <div class="ev" style="top:342px"><div class="tm" style="color:#D97706">9h46</div><div class="d" style="border-color:#F59E0B"></div><div class="x">mão 2×</div></div>
 <div class="ev" style="top:462px"><div class="tm" style="color:#E5484D">9h50</div><div class="d" style="border-color:#E5484D"></div><div class="x" style="color:#E5484D">DIA −3R</div></div>
</div>
<div class="calm"></div><div class="logo"><span><img src="file://__LOGO__"></span></div>
</body></html>"""


async def main():
    h = HTML
    for k, v in {"__INTER__": INTER, "__LOGO__": LOGO, "__AV__": AV}.items(): h = h.replace(k, v)
    p = os.path.join(HERE, "capa.html"); open(p, "w").write(h)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + p); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(HERE, "caixa-preta1-v2-capa.jpg"), type="jpeg", quality=92); await b.close()

asyncio.run(main())
