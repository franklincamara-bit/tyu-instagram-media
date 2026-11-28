# Capas do tutorial VID-1 "Primeiros passos: as 3 listas antes do primeiro trade" (3 opções, 1280x720) no padrão "capa ousada" (04/11/2026).
# Uso: python3 capa1.py -> vid1-capa-1.jpg, -2.jpg, -3.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("explicando", "bracos-cruzados", "joinha")}
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
"""
C1 = """<div class="bg" style="background:radial-gradient(900px 700px at 40% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="left:56px;top:56px;font-size:104px">3 LISTAS</div>
<div class="t y" style="left:56px;top:164px;font-size:104px">ANTES DO</div>
<div class="t y" style="left:56px;top:272px;font-size:104px">1º TRADE</div>
<div class="card" style="left:100px;top:392px;width:600px;height:200px;transform:rotate(-2deg)">
 <div style="position:absolute;left:30px;top:20px;font:900 38px 'InterD';color:#2563EB">1 · Setups</div>
 <div style="position:absolute;left:30px;top:76px;font:900 38px 'InterD';color:#C8262D">2 · Erros</div>
 <div style="position:absolute;left:30px;top:132px;font:900 38px 'InterD';color:#7C3AED">3 · Falhas de disciplina</div></div>
<img class="av" src="file://__AV1__" style="right:20px;top:40px;height:700px">
"""
C2 = """<div class="bg" style="background:linear-gradient(110deg,#B3121C 0%,#E5303A 48%,#15803D 52%,#0B5A2A 100%)"></div><div class="rays"></div>
<div class="t w" style="left:44px;top:70px;font-size:92px">SEM</div>
<div class="t w" style="left:44px;top:160px;font-size:92px">LISTAS</div>
<div class="band" style="left:40px;top:290px"><b style="background:#0A1640;font-size:34px">DIÁRIO SEM PADRÃO</b></div>
<div class="t w" style="right:44px;top:70px;font-size:92px;text-align:right">COM AS</div>
<div class="t y" style="right:44px;top:160px;font-size:92px;text-align:right">3 LISTAS</div>
<div class="band" style="right:40px;top:290px"><b style="background:#0A1640;font-size:34px;transform:rotate(3deg)">SEUS PADRÕES À VISTA</b></div>
<img class="av" src="file://__AV2__" style="left:510px;top:120px;height:620px">
"""
C3 = """<div class="bg" style="background:radial-gradient(900px 700px at 70% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="left:56px;top:56px;font-size:100px">PRIMEIROS</div>
<div class="t y" style="left:56px;top:156px;font-size:100px">PASSOS</div>
<div class="band" style="left:60px;top:290px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">COMECE AQUI</b></div>
<div class="card" style="left:470px;top:380px;width:720px;height:290px;transform:rotate(-2deg)">
 <div class="lbl" style="position:absolute;left:34px;top:24px">CONFIGURAÇÕES</div>
 <div style="position:absolute;left:34px;top:62px;font:900 46px 'InterD';color:#2563EB">› Gerenciar Setups</div>
 <div style="position:absolute;left:34px;top:130px;font:900 46px 'InterD';color:#C8262D">› Gerenciar Erros</div>
 <div style="position:absolute;left:34px;top:198px;font:900 46px 'InterD';color:#7C3AED">› Falhas de Disciplina</div></div>
<img class="av" src="file://__AV3__" style="left:860px;top:20px;height:380px">
"""
def page(body):
    b = body.replace("__AV1__", AV["explicando"]).replace("__AV2__", AV["bracos-cruzados"]).replace("__AV3__", AV["joinha"])
    return f"<html><head><style>{CSS.replace('__INTER__', INTER)}</style></head><body>{b}<div class='logo'><img src='file://{LOGO}'></div></body></html>"
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": 1280, "height": 720})
        for i, c in enumerate([C1, C2, C3], 1):
            f = os.path.join(HERE, f"_c{i}.html"); open(f, "w").write(page(c))
            await pg.goto("file://" + f); await pg.wait_for_timeout(600)
            await pg.screenshot(path=os.path.join(HERE, f"vid1-capa-{i}.jpg"), type="jpeg", quality=92)
            os.remove(f)
        await br.close()
asyncio.run(main())
