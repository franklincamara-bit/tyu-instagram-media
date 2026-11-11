# Capa do Trial Reel "Tribunal do Trade #1 — corte de 15 s" (TYU-69), padrão capa ousada. Uso: python3 capa_corte15.py
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"; LOGO = os.path.join(ROOT, "assets", "logo.png")
A = lambda n: os.path.join(ROOT, "assets", n)
BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;font-family:'InterD'}
.bg{position:absolute;inset:0}
.rays{position:absolute;left:-600px;top:-300px;width:2400px;height:2400px;background:repeating-conic-gradient(from 0deg at 50% 50%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg);-webkit-mask-image:radial-gradient(circle at 50% 50%,#000 10%,transparent 60%)}
.t{position:absolute;left:0;right:0;text-align:center;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-3px;-webkit-text-stroke:10px #0A1640;paint-order:stroke fill;text-shadow:0 6px 0 #0A1640,0 12px 0 #0A1640,0 18px 0 rgba(10,22,64,.85),0 30px 40px rgba(0,0,0,.45)}
.w{color:#fff}.y{color:#FFD43B}.r{color:#FF4D55}
.band{position:absolute;left:0;right:0;text-align:center}
.band b{display:inline-block;font:900 58px 'InterD';color:#fff;padding:14px 40px 20px;border-radius:22px;letter-spacing:-1px;transform:rotate(-3deg);border:6px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.4);background:linear-gradient(180deg,#FF8A3D,#E2600E)}
.av{position:absolute;filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 26px rgba(120,190,255,.8)) drop-shadow(0 40px 50px rgba(0,0,0,.45))}
.card{position:absolute;background:#fff;border-radius:40px;box-shadow:0 40px 80px rgba(0,0,0,.45);overflow:hidden}
.logo{position:absolute;left:0;right:0;top:1600px;text-align:center}
.logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(0,0,0,.3)}.logo img{width:290px;display:block}
.calm{position:absolute;left:0;right:0;top:1540px;bottom:0;background:linear-gradient(180deg,transparent,rgba(5,12,40,.55))}
.seal{position:absolute;left:0;right:0;top:1520px;text-align:center;font:700 26px 'InterD';color:rgba(255,255,255,.8);letter-spacing:1px}
</style></head><body>__BODY__<div class="calm"></div><div class="seal">Exemplo ilustrativo · conta demo</div><div class="logo"><span><img src="file://__LOGO__"></span></div></body></html>"""
BLUE = '<div class="bg" style="background:radial-gradient(900px 900px at 50% 38%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>'
OPS = {1: BLUE + """
<div class="t w" style="top:200px;font-size:128px">O STOP ANDOU</div>
<div class="t y" style="top:330px;font-size:190px">3 VEZES</div>
<div class="band" style="top:590px"><b>TRIBUNAL DO TRADE</b></div>
<img class="av" src="file://__AV1__" style="left:250px;top:760px;width:600px">
<div style="position:absolute;left:60px;top:1130px;transform:rotate(-10deg);border:12px solid #fff;border-radius:26px;padding:6px 34px 14px;background:#E5484D;font:900 120px 'InterD';color:#fff;letter-spacing:-3px;box-shadow:0 30px 60px rgba(0,0,0,.45)">CULPADO</div>
<div class="card" style="right:40px;top:800px;width:330px;height:250px;transform:rotate(4deg)">
 <div style="position:absolute;left:0;right:0;top:30px;text-align:center;font:700 26px 'InterD';letter-spacing:3px;color:#7A8499">RISCO DO TRADE</div>
 <div style="position:absolute;left:0;right:0;top:70px;text-align:center;font:900 64px 'InterD';color:#0B1533;white-space:nowrap">1R <span style="color:#F59E0B">→</span></div>
 <div style="position:absolute;left:0;right:0;top:140px;text-align:center;font:900 92px 'InterD';color:#E5484D;letter-spacing:-3px">2,8R</div></div>"""}
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for n, body in OPS.items():
            h = BASE.replace("__BODY__", body)
            for k, v in {"__INTER__": INTER, "__LOGO__": LOGO, "__AV1__": A("explicando.png"), "__AV2__": A("cansado.png")}.items(): h = h.replace(k, v)
            p = os.path.join(HERE, "capa.html"); open(p, "w").write(h)
            await pg.goto("file://" + p); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(HERE, "tribunal1-corte15-capa.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
