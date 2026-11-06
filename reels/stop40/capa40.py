# Capas do Short VID-40 (3 opções, 1080x1920) no padrão "capa ousada" (04/11/2026): fundo saturado, título 3D branco + amarelo,
# faixa inclinada, personagem oficial com luz de recorte, logo no selo branco, faixa de baixo calma.
# Uso: python3 capa40.py  -> stop40-capa-1.jpg, -2.jpg, -3.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(HERE, "tpl", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("explicando", "celular-contrariado", "cansado")}

CSS = """
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:'InterD'}
.bg{position:absolute;inset:0}
.rays{position:absolute;left:-600px;top:-300px;width:2400px;height:2400px;background:repeating-conic-gradient(from 0deg at 50% 50%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg);
  -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 10%,transparent 60%)}
.t{position:absolute;left:0;right:0;text-align:center;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-3px;
  -webkit-text-stroke:10px #0A1640;paint-order:stroke fill;text-shadow:0 6px 0 #0A1640,0 12px 0 #0A1640,0 18px 0 rgba(10,22,64,.85),0 30px 40px rgba(0,0,0,.45)}
.w{color:#fff}.y{color:#FFD43B}
.band{position:absolute;left:0;right:0;text-align:center}
.band b{display:inline-block;font:900 70px 'InterD';color:#fff;padding:14px 46px 20px;border-radius:22px;letter-spacing:-1px;transform:rotate(-3deg);
  border:6px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.4)}
.av{position:absolute;filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 26px rgba(120,190,255,.8)) drop-shadow(0 40px 50px rgba(0,0,0,.45))}
.logo{position:absolute;left:0;right:0;top:1590px;text-align:center}
.logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(0,0,0,.3)}
.logo img{width:290px;display:block}
.calm{position:absolute;left:0;right:0;top:1540px;bottom:0;background:linear-gradient(180deg,transparent,rgba(5,12,40,.55))}
"""

C1 = """<div class="bg" style="background:radial-gradient(900px 900px at 50% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:200px;font-size:150px">SÓ UM</div>
<div class="t y" style="top:350px;font-size:150px">POUQUINHO?</div>
<div class="band" style="top:560px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">MOVER O STOP</b></div>
<img class="av" src="file://__AV1__" style="left:-20px;top:760px;width:560px">
<div style="position:absolute;right:50px;top:800px;width:470px;height:640px;background:#fff;border-radius:44px;box-shadow:0 40px 80px rgba(0,0,0,.45);transform:rotate(3deg);overflow:hidden">
 <div style="position:absolute;left:36px;top:30px;font:700 26px 'InterD';letter-spacing:4px;color:#7A8499">ACERTO MÍNIMO</div>
 <div style="position:absolute;left:0;right:0;top:80px;text-align:center;font:900 120px 'InterD';color:#2563EB;letter-spacing:-5px">40%</div>
 <div style="position:absolute;left:0;right:0;top:215px;text-align:center;font:900 80px 'InterD';color:#0B1533">↓</div>
 <div style="position:absolute;left:0;right:0;top:300px;text-align:center;font:900 170px 'InterD';color:#E5484D;letter-spacing:-8px">57%</div>
 <div style="position:absolute;left:30px;right:30px;top:520px;height:12px;background:#E5484D;border-radius:6px"></div>
 <div style="position:absolute;left:30px;right:30px;top:490px;height:6px;background:repeating-linear-gradient(90deg,#E5484D 0 16px,transparent 16px 28px);opacity:.6"></div>
 <div style="position:absolute;left:36px;top:556px;font:900 40px 'InterD';color:#E5484D">STOP 20 → 40</div>
</div>
"""

C2 = """<div class="bg" style="background:linear-gradient(115deg,#B3121C 0%,#E5303A 46%,#0E2A8A 54%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:190px;font-size:128px">QUANTO CUSTA</div>
<div class="t y" style="top:330px;font-size:128px">MOVER O STOP?</div>
<img class="av" src="file://__AV2__" style="left:-10px;top:690px;width:520px">
<div style="position:absolute;left:470px;right:-40px;top:1020px;height:18px;background:#fff;box-shadow:0 0 30px rgba(255,80,80,.9)"></div>
<div style="position:absolute;left:470px;right:-40px;top:1022px;height:14px;background:#E5484D"></div>
<div style="position:absolute;left:640px;top:1036px;width:6px;height:90px;background:#fff"></div>
<div style="position:absolute;left:440px;top:1110px;width:575px;transform:rotate(-5deg);transform-origin:180px 0">
 <div style="background:#FFD43B;border:8px solid #0A1640;border-radius:30px 30px 30px 30px;padding:26px 30px 30px;box-shadow:0 30px 60px rgba(0,0,0,.45);text-align:center">
  <div style="font:900 32px 'InterD';letter-spacing:3px;color:#0A1640">ACERTO EXIGIDO</div>
  <div style="font:900 98px 'InterD';color:#0A1640;letter-spacing:-4px;line-height:1.05">40%<span style="color:#C8262D">→</span>57%</div>
 </div>
</div>
<div style="position:absolute;left:520px;top:950px;font:900 44px 'InterD';color:#fff;-webkit-text-stroke:6px #0A1640;paint-order:stroke fill">STOP</div>
"""

C3 = """<div class="bg" style="background:radial-gradient(900px 1000px at 70% 45%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:210px;font-size:160px">ARRASTOU</div>
<div class="t y" style="top:370px;font-size:160px">O STOP?</div>
<div class="band" style="top:590px"><b style="background:#0A1640;border-color:#FFD43B;color:#FFD43B">O PREÇO DA DECISÃO</b></div>
<img class="av" src="file://__AV3__" style="left:-60px;top:800px;width:600px">
<div style="position:absolute;left:560px;top:860px;width:460px;height:460px">
 <div style="position:absolute;inset:0;opacity:.18;transform:translateX(-120px)"><svg viewBox="0 0 100 100" width="460" height="460"><polygon points="30,2 70,2 98,30 98,70 70,98 30,98 2,70 2,30" fill="#fff"/></svg></div>
 <div style="position:absolute;inset:0;opacity:.35;transform:translateX(-60px)"><svg viewBox="0 0 100 100" width="460" height="460"><polygon points="30,2 70,2 98,30 98,70 70,98 30,98 2,70 2,30" fill="#fff"/></svg></div>
 <svg viewBox="0 0 100 100" width="460" height="460" style="position:absolute;inset:0;transform:rotate(12deg);filter:drop-shadow(0 30px 40px rgba(0,0,0,.5))">
  <polygon points="30,2 70,2 98,30 98,70 70,98 30,98 2,70 2,30" fill="#fff"/><polygon points="31.5,6 68.5,6 94,31.5 94,68.5 68.5,94 31.5,94 6,68.5 6,31.5" fill="#E5303A"/>
  <text x="50" y="61" text-anchor="middle" font-family="InterD" font-weight="900" font-size="30" fill="#fff" letter-spacing="-1">STOP</text></svg>
</div>
<div style="position:absolute;left:600px;top:1360px;font:900 54px 'InterD';color:#fff;-webkit-text-stroke:8px #0A1640;paint-order:stroke fill">−20 → <span style="color:#FF6B70">−40</span></div>
"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for i, body in enumerate([C1, C2, C3], 1):
            h = ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>" + body +
                 "<div class='calm'></div><div class='logo'><span><img src='file://__LOGO__'></span></div></body></html>")
            for k, v in {"__INTER__": INTER, "__LOGO__": LOGO, "__AV1__": AV["explicando"], "__AV2__": AV["celular-contrariado"], "__AV3__": AV["explicando"]}.items():
                h = h.replace(k, v)
            hp = os.path.join(HERE, "capa40_%d.html" % i); open(hp, "w").write(h)
            await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(HERE, "stop40-capa-%d.jpg" % i), type="jpeg", quality=92)
            os.remove(hp)
        await b.close()

asyncio.run(main())
