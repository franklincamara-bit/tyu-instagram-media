# Capas v3 (opções 1-3, "isca") do Trial Reel "Caixa-Preta do Trader #1" (TYU-59), pedido do Franklin em 10/11/2026:
# "a capa precisa ser uma isca". Padrão capa ousada (fonte única 04/11). Uso: python3 capas_v3.py -> cp-capa-opcao-1..3.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"; LOGO = os.path.join(HERE, "tpl", "logo.png")
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
OPS = {
# 1 — curiosidade numérica: "ERA SÓ 1R… / VIROU −3R"
1: BLUE + """
<div class="t w" style="top:200px;font-size:150px">ERA SÓ 1R…</div>
<div class="t y" style="top:380px;font-size:190px">VIROU −3R</div>
<div class="band" style="top:640px"><b>CAIXA-PRETA DO TRADER #1</b></div>
<img class="av" src="file://__AV1__" style="left:-40px;top:800px;width:580px">
<div class="card" style="right:50px;top:860px;width:480px;height:560px;transform:rotate(3deg)">
 <div style="position:absolute;left:0;right:0;top:40px;text-align:center;font:700 28px 'InterD';letter-spacing:4px;color:#7A8499">RESULTADO DO DIA</div>
 <div style="position:absolute;left:0;right:0;top:110px;text-align:center;font:900 130px 'InterD';color:#0B1533;letter-spacing:-4px">−1R</div>
 <div style="position:absolute;left:0;right:0;top:250px;text-align:center;font:900 90px 'InterD';color:#F59E0B">↓</div>
 <div style="position:absolute;left:0;right:0;top:350px;text-align:center;font:900 150px 'InterD';color:#E5484D;letter-spacing:-5px">−3R</div>
 <div style="position:absolute;left:0;right:0;top:505px;text-align:center;font:700 28px 'InterD';color:#7A8499">em 12 minutos</div>
</div>""",
# 2 — tela dividida verde × vermelho: "O ERRO QUE PARECE SEGURO"
2: """<div class="bg" style="background:linear-gradient(100deg,#0E9F6E 0 49.6%,#fff 49.6% 50.4%,#D92D3A 50.4%)"></div>
<div class="bg" style="background:radial-gradient(1100px 900px at 50% 45%,transparent 40%,rgba(0,0,0,.45))"></div>
<div class="t w" style="top:190px;font-size:118px">O ERRO QUE</div>
<div class="t y" style="top:310px;font-size:132px;letter-spacing:-5px;white-space:nowrap">PARECE SEGURO</div>
<div style="position:absolute;left:40px;top:600px;width:480px;text-align:center;font:900 64px 'InterD';color:#fff;line-height:1;text-shadow:0 6px 20px rgba(0,0,0,.4)">“É SÓ 1R”<div style="font:700 34px 'InterD';margin-top:14px;opacity:.95">9h38 · dentro do plano ✓</div></div>
<div style="position:absolute;right:40px;top:600px;width:480px;text-align:center;font:900 64px 'InterD';color:#fff;line-height:1;text-shadow:0 6px 20px rgba(0,0,0,.4)">DIA −3R<div style="font:700 34px 'InterD';margin-top:14px;opacity:.95">9h50 · fora de tudo ✗</div></div>
<img class="av" src="file://__AV2__" style="left:240px;top:820px;width:600px">
<div class="band" style="top:1400px"><b>CAIXA-PRETA DO TRADER #1</b></div>""",
# 3 — identificação: "VOCÊ JÁ FEZ ISSO / (E CHAMOU DE GESTÃO)"
3: BLUE + """
<div class="t w" style="top:190px;font-size:130px">VOCÊ JÁ FEZ</div>
<div class="t w" style="top:315px;font-size:130px">ISSO HOJE?</div>
<div class="t y" style="top:465px;font-size:70px;letter-spacing:-2px;line-height:1">E CHAMOU DE<br>GESTÃO DE RISCO</div>
<img class="av" src="file://__AV1__" style="left:-30px;top:760px;width:560px">
<div class="card" style="right:46px;top:830px;width:500px;height:300px;transform:rotate(-3deg);border-radius:60px 60px 60px 10px">
 <div style="position:absolute;left:40px;right:40px;top:50px;font:900 76px 'InterD';color:#0B1533;line-height:1;letter-spacing:-2px">“se der errado, é só 1R”</div></div>
<div class="card" style="right:70px;top:1150px;width:440px;height:230px;transform:rotate(4deg);background:#E5484D">
 <div style="position:absolute;left:0;right:0;top:34px;text-align:center;font:700 30px 'InterD';color:#fff;letter-spacing:3px">12 MINUTOS DEPOIS</div>
 <div style="position:absolute;left:0;right:0;top:86px;text-align:center;font:900 104px 'InterD';color:#fff;letter-spacing:-4px;white-space:nowrap">DIA −3R</div></div>
<div class="band" style="top:1405px"><b>CAIXA-PRETA DO TRADER #1</b></div>""",
}
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for n, body in OPS.items():
            h = BASE.replace("__BODY__", body)
            for k, v in {"__INTER__": INTER, "__LOGO__": LOGO, "__AV1__": A("celular-contrariado.png"), "__AV2__": A("cansado.png")}.items(): h = h.replace(k, v)
            p = os.path.join(HERE, f"capa{n}.html"); open(p, "w").write(h)
            await pg.goto("file://" + p); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(HERE, f"cp-capa-opcao-{n}.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
