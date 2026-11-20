# Capas v4 do tutorial VID-7 (3 opções, 1280x720), pedido do Franklin em 18/11/2026:
# título "Antes do primeiro trade, faça isso" + abaixo "Aprenda como utilizar o menu Iniciar Dia".
# Uso: python3 capa7v4.py -> vid7-capa-v4-1.jpg, -2.jpg, -3.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("explicando", "pensativo", "joinha")}
CSS = """
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1280px;height:720px;overflow:hidden;font-family:'InterD'}
.bg{position:absolute;inset:0}
.rays{position:absolute;left:-400px;top:-700px;width:2000px;height:2000px;background:repeating-conic-gradient(from 0deg at 50% 50%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg);-webkit-mask-image:radial-gradient(circle at 50% 50%,#000 10%,transparent 60%)}
.t{position:absolute;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-2px;-webkit-text-stroke:8px #0A1640;paint-order:stroke fill;text-shadow:0 5px 0 #0A1640,0 10px 0 #0A1640,0 15px 0 rgba(10,22,64,.85),0 24px 30px rgba(0,0,0,.45)}
.w{color:#fff}.y{color:#FFD43B}
.band{position:absolute}
.band b{display:inline-block;font:900 46px 'InterD';color:#fff;padding:10px 32px 14px;border-radius:18px;transform:rotate(-3deg);border:5px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.4)}
.av{position:absolute;filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 22px rgba(120,190,255,.8)) drop-shadow(0 30px 40px rgba(0,0,0,.45))}
.logo{position:absolute;left:40px;bottom:30px;background:#fff;border-radius:999px;padding:12px 26px;box-shadow:0 14px 34px rgba(0,0,0,.3)}
.logo img{width:190px;display:block}
.card{position:absolute;background:#fff;border-radius:30px;box-shadow:0 30px 60px rgba(0,0,0,.45);overflow:hidden}
.lbl{font:700 20px 'InterD';letter-spacing:3px;color:#7A8499}
.sub{position:absolute;background:#fff;border-radius:22px;padding:16px 30px 18px;box-shadow:0 20px 44px rgba(0,0,0,.4);font:900 46px 'InterD';color:#0B1533;line-height:1.05}
.sub em{font-style:normal;color:#1D4ED8}
.menu{position:absolute;background:#fff;border-radius:22px;box-shadow:0 26px 50px rgba(0,0,0,.45);padding:14px;width:300px}
.mi{font:700 26px 'InterD';color:#64748B;padding:12px 16px;border-radius:14px}
.mi.on{background:#FFD43B;color:#0B1533;font-weight:900}
"""
C1 = """<div class="bg" style="background:radial-gradient(900px 700px at 40% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="left:52px;top:52px;font-size:92px">ANTES DO</div>
<div class="t w" style="left:52px;top:144px;font-size:92px">PRIMEIRO TRADE,</div>
<div class="t y" style="left:52px;top:236px;font-size:110px">FAÇA ISSO</div>
<div class="sub" style="left:56px;top:400px;transform:rotate(-1.5deg)">Aprenda como utilizar<br>o menu <em>Iniciar Dia</em></div>
<img class="av" src="file://__AV1__" style="right:0px;top:60px;height:680px">
"""
C2 = """<div class="bg" style="background:linear-gradient(115deg,#0E8A43 0%,#16A34A 46%,#0E2A8A 54%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="left:48px;top:56px;font-size:84px">ANTES DO PRIMEIRO</div>
<div class="t w" style="left:48px;top:140px;font-size:84px">TRADE, <span class="y">FAÇA ISSO</span></div>
<div class="band" style="left:52px;top:270px"><b style="background:#0A1640;font-size:36px">APRENDA COMO UTILIZAR O MENU INICIAR DIA</b></div>
<div class="menu" style="left:100px;top:400px;width:auto;transform:rotate(-3deg)">
 <div class="mi on" style="font-size:44px;padding:16px 30px">☀ Iniciar Dia</div></div>
<img class="av" src="file://__AV3__" style="right:30px;top:300px;height:440px">
"""
C3 = """<div class="bg" style="background:radial-gradient(900px 700px at 70% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<img class="av" src="file://__AV2__" style="left:-10px;top:70px;height:670px">
<div class="t w" style="left:430px;top:60px;font-size:84px">ANTES DO</div>
<div class="t w" style="left:430px;top:146px;font-size:84px">PRIMEIRO TRADE,</div>
<div class="t y" style="left:430px;top:232px;font-size:110px">FAÇA ISSO</div>
<div class="band" style="left:440px;top:392px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D);font-size:34px">APRENDA COMO UTILIZAR<br>O MENU INICIAR DIA</b></div>
"""
def page(body):
    b = body.replace("__AV1__", AV["explicando"]).replace("__AV2__", AV["pensativo"]).replace("__AV3__", AV["joinha"])
    return f"<html><head><style>{CSS.replace('__INTER__', INTER)}</style></head><body>{b}<div class='logo'><img src='file://{LOGO}'></div></body></html>"
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": 1280, "height": 720})
        for i, c in enumerate([C1, C2, C3], 1):
            f = os.path.join(HERE, f"_c{i}.html"); open(f, "w").write(page(c))
            await pg.goto("file://" + f); await pg.wait_for_timeout(600)
            await pg.screenshot(path=os.path.join(HERE, f"vid7-capa-v4-{i}.jpg"), type="jpeg", quality=92)
            os.remove(f)
        await br.close()
asyncio.run(main())
