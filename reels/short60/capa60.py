# Capa do Short 60% (chamada 1: "ACERTA MAIS. GANHA MENOS?") — 1080x1920, personagem oficial (pose pensativo).
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
INTER = "/usr/share/fonts/opentype/inter"
FONT = os.path.join(HERE, "tpl", "Archivo.ttf")
LOGO = os.path.join(HERE, "tpl", "logo.png")
AV = os.path.join(HERE, "tpl", "pensativo.png")

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Archivo';src:url('file://__FONT__') format('truetype');font-weight:100 900;font-stretch:62% 125%}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;color:#0B1533}
#bg{position:absolute;inset:0;background:radial-gradient(1000px 900px at 85% 10%,rgba(37,99,235,.22),transparent 60%),
  radial-gradient(900px 800px at 10% 80%,rgba(229,72,77,.12),transparent 60%),linear-gradient(180deg,#F4F7FD,#E3EAF6)}
#floor{position:absolute;left:-1200px;width:3480px;top:1250px;height:2400px;transform-origin:50% 0;transform:perspective(900px) rotateX(74deg);
  background-image:linear-gradient(rgba(11,21,51,.08) 2px,transparent 2px),linear-gradient(90deg,rgba(11,21,51,.08) 2px,transparent 2px);background-size:120px 120px;
  -webkit-mask-image:linear-gradient(180deg,transparent,#000 15%,#000 50%,transparent)}
.t{position:absolute;left:0;right:0;text-align:center;font-family:'InterD';font-weight:900;line-height:.9;letter-spacing:-6px;white-space:nowrap;text-transform:uppercase}
#t1{top:215px;font-size:132px;color:#0B1533}
#t2{top:365px;font-size:132px;color:#2563EB}
#chip{position:absolute;left:0;right:0;top:555px;text-align:center}
#chip b{display:inline-block;font:900 64px 'InterD';color:#fff;background:linear-gradient(180deg,#F04C52,#D93A40);padding:12px 40px 18px;border-radius:30px;letter-spacing:-1px;
  box-shadow:0 22px 50px rgba(217,58,64,.35);transform:rotate(-2deg)}
#av{position:absolute;left:-40px;top:780px;width:760px;height:1140px;overflow:hidden}
#av img{position:absolute;left:0;top:0;width:760px;filter:drop-shadow(0 30px 40px rgba(11,21,51,.25))}
#score{position:absolute;right:56px;top:860px;width:450px;background:#fff;border-radius:40px;padding:30px 34px 34px;box-shadow:0 40px 90px rgba(11,21,51,.20);transform:rotate(3deg)}
#score .k{font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
#score .n{display:flex;align-items:center;gap:18px;margin-top:6px}
#score .n span{font:900 168px 'InterD';letter-spacing:-9px;line-height:.95}
#score .n span small{font-size:92px;letter-spacing:-3px}
#score .c{width:96px;height:96px;border-radius:50%;background:linear-gradient(160deg,#34C77B,#169A55);display:flex;align-items:center;justify-content:center;box-shadow:0 16px 30px rgba(22,154,85,.35)}
#bal{position:absolute;right:56px;top:1250px;width:450px;background:#fff;border-radius:40px;padding:28px 34px 20px;box-shadow:0 40px 90px rgba(11,21,51,.20);transform:rotate(-2deg)}
#bal .k{font:600 22px 'Inter';letter-spacing:4px;color:#7A8499}
#bal .v{font:900 96px 'InterD';color:#E5484D;letter-spacing:-4px;margin-top:2px}
#logo{position:absolute;left:0;right:0;top:1640px;text-align:center}
#logo span{display:inline-block;background:#fff;border-radius:999px;padding:22px 44px;box-shadow:0 20px 50px rgba(11,21,51,.15)}
#logo img{width:300px;display:block}
</style></head><body>
<div id="bg"></div><div id="floor"></div>
<div class="t" id="t1">Acerta mais.</div>
<div class="t" id="t2">Ganha menos?</div>
<div id="chip"><b>FAZ A CONTA</b></div>
<div id="av"><img src="file://__AV__"></div>
<div id="score"><div class="k">TAXA DE ACERTO</div><div class="n"><span>60<small>%</small></span>
 <div class="c"><svg width="58" height="58" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div></div>
<div id="bal"><div class="k">SALDO DA CONTA</div><div class="v">−200</div>
 <svg width="380" height="120" viewBox="0 0 380 120"><path d="M6 18 L40 10 L70 40 L104 30 L134 62 L168 52 L200 80 L236 68 L266 96 L300 86 L338 112" fill="none" stroke="#E5484D" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>
 <path d="M318 86 L352 116 L312 118 Z" fill="#E5484D"/></svg></div>
<div id="logo"><span><img src="file://__LOGO__"></span></div>
</body></html>"""

async def main():
    h = HTML.replace("__FONT__", FONT).replace("__INTER__", INTER).replace("__LOGO__", LOGO).replace("__AV__", AV)
    hp = os.path.join(HERE, "capa60.html"); open(hp, "w").write(h)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(HERE, "short60-capa.png"))
        await pg.screenshot(path=os.path.join(HERE, "short60-capa.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
