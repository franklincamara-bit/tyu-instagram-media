# Capa do Reel TYU-19 "Mesmo stop, três traders" (1080x1920) no padrão "capa ousada" (04/11/2026):
# fundo azul royal -> marinho, título 3D branco + amarelo, faixa inclinada, três poses oficiais com luz de recorte, logo no selo branco.
# Uso: python3 capa19.py -> tres-traders19-capa.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "reels", "stop40", "tpl", "logo.png")
A = lambda k: "file://" + os.path.join(ROOT, "assets", k + ".png")
CSS = """
@font-face{font-family:'InterD';src:url('file://%s/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://%s/InterDisplay-Bold.otf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:'InterD'}
.bg{position:absolute;inset:0;background:radial-gradient(1000px 900px at 50%% 42%%,#2F6BFF,#0B3BC4 45%%,#071A5C 100%%)}
.rays{position:absolute;left:-600px;top:-300px;width:2400px;height:2400px;background:repeating-conic-gradient(from 0deg at 50%% 50%%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg);-webkit-mask-image:radial-gradient(circle at 50%% 50%%,#000 10%%,transparent 60%%)}
.t{position:absolute;left:0;right:0;text-align:center;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-3px;-webkit-text-stroke:10px #0A1640;paint-order:stroke fill;text-shadow:0 6px 0 #0A1640,0 12px 0 #0A1640,0 18px 0 rgba(10,22,64,.85),0 30px 40px rgba(0,0,0,.45)}
.w{color:#fff}.y{color:#FFD43B}
.band{position:absolute;left:0;right:0;text-align:center}
.band b{display:inline-block;font:900 66px 'InterD';color:#fff;padding:14px 46px 20px;border-radius:22px;letter-spacing:-1px;transform:rotate(-3deg);border:6px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.4);background:linear-gradient(180deg,#F04C52,#C8262D)}
.col{position:absolute;top:760px;width:330px;height:760px}
.av{position:absolute;left:50%%;bottom:110px;height:600px;transform:translateX(-50%%);filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 22px rgba(120,190,255,.8)) drop-shadow(0 30px 40px rgba(0,0,0,.45))}
.tag{position:absolute;left:4px;right:4px;bottom:20px;white-space:nowrap;text-align:center;font:900 37px 'InterD';color:#0A1640;border:6px solid #0A1640;border-radius:20px;padding:10px 4px 14px;box-shadow:0 18px 30px rgba(0,0,0,.4)}
.num{position:absolute;left:14px;top:0;font:900 110px 'InterD';color:#fff;-webkit-text-stroke:8px #0A1640;paint-order:stroke fill;opacity:.95}
.logo{position:absolute;left:0;right:0;top:1600px;text-align:center}
.logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(0,0,0,.3)}
.logo img{width:290px;display:block}
.calm{position:absolute;left:0;right:0;top:1560px;bottom:0;background:linear-gradient(180deg,transparent,rgba(5,12,40,.55))}
""" % (INTER, INTER)
BODY = """<div class="bg"></div><div class="rays"></div>
<div class="t w" style="top:190px;font-size:150px">MESMO STOP.</div>
<div class="t y" style="top:345px;font-size:150px">3 TRADERS.</div>
<div class="band" style="top:560px"><b>QUAL É VOCÊ?</b></div>
<div class="col" style="left:30px"><div class="num">1</div><img class="av" src="%s" style="transform:translateX(-50%%) rotate(-2deg)"><div class="tag" style="background:#9BE89F">VOLTA AMANHÃ</div></div>
<div class="col" style="left:375px"><div class="num">2</div><img class="av" src="%s"><div class="tag" style="background:#FF8A8F">MÃO 2×</div></div>
<div class="col" style="left:720px"><div class="num">3</div><img class="av" src="%s" style="transform:translateX(-50%%) rotate(2deg)"><div class="tag" style="background:#FFD43B">SEM STOP</div></div>
<div class="calm"></div><div class="logo"><span><img src="file://%s"></span></div>""" % (A("caderno"), A("celular-contrariado"), A("pensativo"), LOGO)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        hp = os.path.join(HERE, "_capa19.html"); open(hp, "w").write("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>" + BODY + "</body></html>")
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(HERE, "tres-traders19-capa.jpg"), type="jpeg", quality=92); os.remove(hp); await b.close()
asyncio.run(main())
