# Capa do Reel Cash Flow (TYU-52) — 1080x1920 (texto dentro do recorte 4:5 do feed).
# Chamadas oferecidas: (1) "O RECIBO QUE NINGUÉM SOMA" [escolhida]  (2) "APROVADO… E JÁ NO VERMELHO"  (3) "SUA MESA COMEÇA EM −875"
import os, asyncio
from playwright.async_api import async_playwright
import cashflow1 as T
HERE = os.path.dirname(os.path.abspath(__file__))
POSE = os.path.join(T.ROOT, "assets", "cansado.png")
HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;color:#0B1533}
#bg{position:absolute;inset:0;background:radial-gradient(1000px 900px at 85% 10%,rgba(37,99,235,.20),transparent 60%),
  radial-gradient(900px 800px at 10% 85%,rgba(229,72,77,.12),transparent 60%),linear-gradient(180deg,#F4F7FD,#E3EAF6)}
#tag{position:absolute;left:0;right:0;top:300px;text-align:center}
#tag b{display:inline-block;font:600 28px 'Inter';letter-spacing:6px;color:#fff;background:#0B1533;padding:14px 26px;border-radius:999px}
.t{position:absolute;left:0;right:0;text-align:center;font-family:'InterD';font-weight:900;line-height:.9;letter-spacing:-5px;white-space:nowrap;text-transform:uppercase;font-size:120px}
#t1{top:390px;color:#0B1533}
#t2{top:510px;color:#E5484D}
#paper{position:absolute;left:110px;top:720px;width:520px;height:760px;background:#FFFEFA;box-shadow:0 30px 60px rgba(11,21,51,.18);transform:rotate(-4deg);padding:40px 38px;
  clip-path:polygon(0 0,100% 0,100% 97%,95% 100%,90% 97%,85% 100%,80% 97%,75% 100%,70% 97%,65% 100%,60% 97%,55% 100%,50% 97%,45% 100%,40% 97%,35% 100%,30% 97%,25% 100%,20% 97%,15% 100%,10% 97%,5% 100%,0 97%)}
#paper .h{font:900 36px 'InterD';letter-spacing:5px;text-align:center;margin-bottom:26px}
.r{display:flex;justify-content:space-between;font:700 30px 'InterD';padding:20px 0;border-bottom:2px dashed rgba(11,21,51,.14)}
.r b{color:#E5484D;font-weight:900}
.tt{display:flex;justify-content:space-between;align-items:baseline;margin-top:26px;border-top:5px dashed #0B1533;padding-top:20px}
.tt span{font:900 34px 'InterD';letter-spacing:4px}.tt b{font:900 70px 'InterD';color:#E5484D;letter-spacing:-2px}
#sel{font:500 18px 'Inter';color:#8A93A6;text-align:center;margin-top:18px}
#pose{position:absolute;left:600px;top:780px;width:470px;filter:drop-shadow(0 26px 30px rgba(11,21,51,.22))}
#q{position:absolute;left:0;right:0;top:1500px;text-align:center}
#q b{display:inline-block;font:900 50px 'InterD';color:#0B1533;background:#FFD43B;padding:12px 26px 16px;border-radius:18px;letter-spacing:-1px}
#logo{position:absolute;left:0;right:0;top:1660px;text-align:center}
#logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(11,21,51,.15)}
#logo img{width:280px;display:block}
</style></head><body>
<div id="bg"></div>
<div id="tag"><b>QUANTO CUSTOU OPERAR</b></div>
<div class="t" id="t1">O recibo que</div>
<div class="t" id="t2">ninguém soma</div>
<div id="paper"><div class="h">RECIBO DA MESA</div>
 <div class="r"><span>3 × avaliação</span><b>US$ 450</b></div>
 <div class="r"><span>2 × reset</span><b>US$ 160</b></div>
 <div class="r"><span>Ativação</span><b>US$ 130</b></div>
 <div class="r"><span>Dados + plataforma</span><b>US$ 135</b></div>
 <div class="tt"><span>TOTAL</span><b>US$ 875</b></div>
 <div id="sel">Exemplo ilustrativo · valores fictícios</div></div>
<img id="pose" src="file://__POSE__">
<div id="q"><b>Antes do 1º saque.</b></div>
<div id="logo"><span><img src="file://__LOGO__"></span></div>
</body></html>"""

async def main():
    h = HTML.replace("__INTER__", T.INTER).replace("__LOGO__", T.LOGO).replace("__POSE__", POSE)
    hp = os.path.join(HERE, "capa_cashflow1.html"); open(hp, "w").write(h)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(HERE, "cashflow1-capa.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
