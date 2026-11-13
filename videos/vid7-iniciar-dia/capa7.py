# Capas do tutorial VID-7 "Como preencher o Iniciar Dia" (3 opções, 1280x720) no padrão "capa ousada" (04/11/2026).
# Uso: python3 capa7.py -> vid7-capa-1.jpg, -2.jpg, -3.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("explicando", "celular-contrariado", "joinha")}
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
<div class="t w" style="left:56px;top:70px;font-size:104px">ANTES DO</div>
<div class="t y" style="left:56px;top:178px;font-size:104px">1º TRADE</div>
<div class="band" style="left:60px;top:322px"><b style="background:linear-gradient(180deg,#22B45A,#15803D)">FAÇA O INICIAR DIA</b></div>
<div class="card" style="left:90px;top:440px;width:470px;height:150px;transform:rotate(-2deg)">
 <div class="lbl" style="position:absolute;left:28px;top:22px">BIAS DO DIA *</div>
 <div style="position:absolute;left:28px;top:62px;font:900 56px 'InterD';color:#0B1533">🟢 Altista</div></div>
<img class="av" src="file://__AV1__" style="right:20px;top:40px;height:700px">
"""
C2 = """<div class="bg" style="background:linear-gradient(110deg,#B3121C 0%,#E5303A 48%,#0E2A8A 52%,#071A5C 100%)"></div><div class="rays"></div>
<img class="av" src="file://__AV2__" style="left:590px;top:150px;height:590px">
<div class="t w" style="left:50px;top:60px;font-size:92px">TRADE SEM</div>
<div class="t y" style="left:50px;top:158px;font-size:92px">LEITURA?</div>
<div class="band" style="left:50px;top:290px"><b style="background:#0A1640">= QUEBRA DE DISCIPLINA</b></div>
<div class="card" style="right:50px;top:150px;width:390px;height:400px;transform:rotate(3deg)">
 <div class="lbl" style="position:absolute;left:30px;top:26px">DISCIPLINA</div>
 <div style="position:absolute;left:30px;top:70px;font:900 80px 'InterD';color:#94A3B8;text-decoration:line-through;text-decoration-thickness:7px">100</div>
 <div style="position:absolute;left:0;right:0;top:160px;text-align:center;font:900 56px 'InterD';color:#0B1533">↓</div>
 <div style="position:absolute;left:0;right:0;top:220px;text-align:center;font:900 130px 'InterD';color:#E5484D;letter-spacing:-6px">50</div>
 <div style="position:absolute;left:30px;bottom:24px;font:700 18px 'InterD';color:#7A8499">Exemplo ilustrativo · conta demo</div></div>
"""
C3 = """<div class="bg" style="background:radial-gradient(900px 700px at 70% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<img class="av" src="file://__AV3__" style="left:10px;top:50px;height:680px">
<div class="t w" style="left:470px;top:70px;font-size:96px">SÓ 1 CAMPO</div>
<div class="t y" style="left:470px;top:170px;font-size:96px">É OBRIGATÓRIO</div>
<div class="band" style="left:480px;top:300px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">INICIAR DIA EM 1 MINUTO</b></div>
<div class="card" style="left:520px;top:420px;width:640px;height:170px;transform:rotate(-2deg)">
 <div class="lbl" style="position:absolute;left:30px;top:24px">BIAS DO DIA *</div>
 <div style="position:absolute;left:30px;top:66px;font:900 52px 'InterD';color:#0B1533">🟢 Altista · 🔴 · ⚪</div></div>
"""
def page(body):
    b = body.replace("__AV1__", AV["explicando"]).replace("__AV2__", AV["celular-contrariado"]).replace("__AV3__", AV["joinha"])
    return f"<html><head><style>{CSS.replace('__INTER__', INTER)}</style></head><body>{b}<div class='logo'><img src='file://{LOGO}'></div></body></html>"
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={"width": 1280, "height": 720})
        for i, c in enumerate([C1, C2, C3], 1):
            f = os.path.join(HERE, f"_c{i}.html"); open(f, "w").write(page(c))
            await pg.goto("file://" + f); await pg.wait_for_timeout(600)
            await pg.screenshot(path=os.path.join(HERE, f"vid7-capa-{i}.jpg"), type="jpeg", quality=92)
            os.remove(f)
        await br.close()
asyncio.run(main())
