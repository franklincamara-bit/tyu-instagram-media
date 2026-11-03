# Capa do Reel Duas Realidades #1 (TYU-57) — 1080x1920, colorida, texto dentro do recorte 4:5 do feed (y 285–1635).
import os, asyncio
from playwright.async_api import async_playwright
import duas1 as T
HERE = os.path.dirname(os.path.abspath(__file__))
HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-Medium.otf');font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;color:#fff;font-family:'InterD'}
.half{position:absolute;top:0;bottom:0;width:540px}
#L{left:0;background:radial-gradient(700px 700px at 20% 30%,rgba(147,180,248,.45),transparent 60%),linear-gradient(170deg,#2563EB 0%,#1D4ED8 55%,#0B1533 100%)}
#R{right:0;background:radial-gradient(700px 700px at 80% 30%,rgba(255,212,59,.35),transparent 60%),linear-gradient(190deg,#F05A5F 0%,#E5484D 50%,#7F1D1D 100%)}
.half:after{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.07) 2px,transparent 2px);background-size:90px 90px}
#cut{position:absolute;left:532px;top:0;bottom:0;width:16px;background:#FFD43B;box-shadow:0 0 40px rgba(0,0,0,.35);z-index:2}
#tag{position:absolute;left:0;right:0;top:310px;text-align:center;z-index:3}
#tag b{display:inline-block;font:600 28px 'Inter';letter-spacing:6px;color:#0B1533;background:#FFD43B;padding:14px 26px;border-radius:999px}
.t{position:absolute;left:0;right:0;text-align:center;font-weight:900;line-height:.92;letter-spacing:-5px;white-space:nowrap;text-transform:uppercase;font-size:118px;z-index:3;text-shadow:0 10px 34px rgba(11,21,51,.45)}
#t1{top:400px}#t2{top:515px;color:#FFD43B}
.card{position:absolute;top:720px;width:430px;height:530px;background:#fff;border-radius:40px;box-shadow:0 40px 80px rgba(0,0,0,.35);color:#0B1533;padding:34px 30px;z-index:3}
#cA{left:55px;transform:rotate(-3deg)}#cB{left:595px;transform:rotate(3deg)}
.card .h{font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
.card .n{font:900 40px 'InterD';letter-spacing:-1px;margin-top:8px;white-space:nowrap}
.card svg{display:block;margin-top:18px}
.card .v{font:900 120px 'InterD';letter-spacing:-4px;line-height:1;margin-top:10px}
#cA .v{color:#2563EB}#cB .v{color:#E5484D}
#q{position:absolute;left:0;right:0;top:1390px;text-align:center;z-index:3}
#q b{display:inline-block;font:900 50px 'InterD';color:#0B1533;background:#fff;padding:12px 28px 16px;border-radius:18px;letter-spacing:-1px}
#sel{position:absolute;left:0;right:0;top:1490px;text-align:center;font:500 24px 'Inter';color:rgba(255,255,255,.85);z-index:3}
#logo{position:absolute;left:0;right:0;top:1660px;text-align:center;z-index:3}
#logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(0,0,0,.30)}
#logo img{width:280px;display:block}
</style></head><body>
<div class="half" id="L"></div><div class="half" id="R"></div><div id="cut"></div>
<div id="tag"><b>DUAS REALIDADES #1</b></div>
<div class="t" id="t1">Mesmo trade.</div>
<div class="t" id="t2">Mesmo stop.</div>
<div class="card" id="cA"><div class="h">REALIDADE A</div><div class="n">Respeitou o stop</div>
 <svg width="370" height="220"><line x1="10" x2="360" y1="60" y2="60" stroke="#0B1533" stroke-width="4"/><line x1="10" x2="360" y1="130" y2="130" stroke="#2563EB" stroke-width="5" stroke-dasharray="14 10"/>
 <path d="M10 60 L60 40 L110 62 L160 35 L210 75 L260 58 L310 100 L345 130" fill="none" stroke="#0B1533" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="345" cy="130" r="10" fill="#2563EB"/></svg>
 <div class="v">−1R</div></div>
<div class="card" id="cB"><div class="h">REALIDADE B</div><div class="n">"Só mais um espaço"</div>
 <svg width="370" height="220"><line x1="10" x2="360" y1="60" y2="60" stroke="#0B1533" stroke-width="4"/><line x1="10" x2="360" y1="205" y2="205" stroke="#F59E0B" stroke-width="5" stroke-dasharray="14 10"/>
 <path d="M10 60 L60 40 L110 62 L160 35 L210 75 L250 110 L290 150 L330 185 L355 205" fill="none" stroke="#0B1533" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="355" cy="205" r="10" fill="#E5484D"/></svg>
 <div class="v">−3R</div></div>
<div id="q"><b>Qual das duas é você?</b></div>
<div id="sel">Exemplo ilustrativo · conta demo</div>
<div id="logo"><span><img src="file://__LOGO__"></span></div>
</body></html>"""

async def main():
    h = HTML.replace("__INTER__", T.INTER).replace("__LOGO__", T.LOGO)
    hp = os.path.join(HERE, "capa_duas1.html"); open(hp, "w").write(h)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(HERE, "duas-realidades1-capa.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
