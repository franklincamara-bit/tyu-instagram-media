# Capa do Tribunal do Trade #1 — 1080x1920. Chamada escolhida: "O STOP QUE ANDOU SOZINHO" + carimbo CULPADO.
# Alternativas oferecidas: "CULPADO. MESMO QUANDO DÁ CERTO." / "VOCÊ MOVE O STOP?"
import os, asyncio
from playwright.async_api import async_playwright
import tribunal1 as T
HERE = os.path.dirname(os.path.abspath(__file__))

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'Inter';src:url('file://__INTER__/Inter-SemiBold.otf');font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;color:#0B1533}
#bg{position:absolute;inset:0;background:radial-gradient(1000px 900px at 85% 10%,rgba(37,99,235,.22),transparent 60%),
  radial-gradient(900px 800px at 10% 80%,rgba(229,72,77,.12),transparent 60%),linear-gradient(180deg,#F4F7FD,#E3EAF6)}
#tag{position:absolute;left:0;right:0;top:250px;text-align:center}
#tag b{display:inline-block;font:600 28px 'Inter';letter-spacing:6px;color:#fff;background:#0B1533;padding:14px 26px;border-radius:999px}
.t{position:absolute;left:0;right:0;text-align:center;font-family:'InterD';font-weight:900;line-height:.9;letter-spacing:-6px;white-space:nowrap;text-transform:uppercase}
#t1{top:360px;font-size:126px;color:#0B1533}
#t2{top:492px;font-size:126px;color:#E5484D}
#judge{position:absolute;left:330px;top:820px;width:520px;height:440px;overflow:hidden}
#judge img{position:absolute;left:0;top:0;width:520px;filter:drop-shadow(0 26px 30px rgba(11,21,51,.22))}
#bench{position:absolute;left:110px;top:1250px;width:860px;height:230px;border-radius:26px 26px 10px 10px;background:linear-gradient(180deg,#16224A,#0B1533 60%,#081029);box-shadow:0 40px 80px rgba(11,21,51,.35)}
#bench .ln{position:absolute;left:40px;right:40px;top:44px;height:3px;background:#2563EB}
#bench .pl{position:absolute;left:50%;top:80px;transform:translateX(-50%);font:600 24px 'Inter';letter-spacing:8px;color:rgba(255,255,255,.75);border:2px solid rgba(255,255,255,.22);border-radius:12px;padding:10px 22px;white-space:nowrap}
.reu{position:absolute;left:70px;top:1050px;width:360px;height:168px;transform:rotate(-8deg)}
.reu .body{position:absolute;inset:0;border-radius:84px;background:linear-gradient(180deg,#F05A5F,#D93A40);box-shadow:0 26px 44px rgba(217,58,64,.35)}
.reu .txt{position:absolute;left:0;right:0;bottom:20px;text-align:center;font:900 48px 'InterD';letter-spacing:4px;color:#fff}
.reu .eye{position:absolute;top:30px;width:52px;height:52px;border-radius:50%;background:#fff}
.reu .eye i{position:absolute;left:10px;top:20px;width:22px;height:22px;border-radius:50%;background:#0B1533}
.reu .brow{position:absolute;top:16px;width:54px;height:10px;border-radius:6px;background:#7A1D21}
.reu .sweat{position:absolute;right:34px;top:4px;width:26px;height:36px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:#9CC3FF}
.reu .leg{position:absolute;bottom:-40px;width:14px;height:46px;border-radius:7px;background:#0B1533}
#stamp{position:absolute;left:0;right:0;top:680px;text-align:center}
#stamp b{display:inline-block;font:900 110px 'InterD';letter-spacing:4px;color:#E5484D;border:11px solid #E5484D;border-radius:26px;padding:0 34px 8px;background:rgba(255,255,255,.8);transform:rotate(-6deg)}
#logo{position:absolute;left:0;right:0;top:1560px;text-align:center}
#logo span{display:inline-block;background:#fff;border-radius:999px;padding:22px 44px;box-shadow:0 20px 50px rgba(11,21,51,.15)}
#logo img{width:300px;display:block}
</style></head><body>
<div id="bg"></div>
<div id="tag"><b>TRIBUNAL DO TRADE · Nº 1</b></div>
<div class="t" id="t1">O stop que</div>
<div class="t" id="t2">andou sozinho</div>
<div id="judge"><img src="file://__JUIZ__"></div>
<div id="bench"><div class="ln"></div><div class="pl">EXCELENTÍSSIMO JUIZ</div></div>
<div class="reu"><div class="body"></div><div class="leg" style="left:120px"></div><div class="leg" style="left:226px"></div>
 <div class="eye" style="left:108px"><i></i></div><div class="eye" style="left:198px"><i></i></div>
 <div class="brow" style="left:104px;transform:rotate(-12deg)"></div><div class="brow" style="left:198px;transform:rotate(12deg)"></div><div class="sweat"></div><div class="txt">STOP</div></div>
<div id="stamp"><b>CULPADO</b></div>
<div id="logo"><span><img src="file://__LOGO__"></span></div>
</body></html>"""

async def main():
    h = HTML.replace("__INTER__", T.INTER).replace("__LOGO__", T.LOGO).replace("__JUIZ__", T.JUIZ)
    hp = os.path.join(HERE, "capa_tribunal1.html"); open(hp, "w").write(h)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(HERE, "tribunal1-capa.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
