# Capas do Short VID-43 (3 opções, 1080x1920) no padrão "capa ousada" (04/11/2026): fundo saturado, título 3D branco + amarelo,
# faixa inclinada, personagem oficial com luz de recorte, logo no selo branco, faixa de baixo calma. Base: reels/stop40/capa40.py.
# Uso: python3 capa43.py  -> short43-capa-1.jpg, -2.jpg, -3.jpg
import os, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INTER = "/usr/share/fonts/opentype/inter"
LOGO = os.path.join(ROOT, "assets", "logo.png")
AV = {k: os.path.join(ROOT, "assets", k + ".png") for k in ("explicando", "pensativo", "cansado")}

CSS = """
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Black.otf');font-weight:900}
@font-face{font-family:'InterD';src:url('file://__INTER__/InterDisplay-Bold.otf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:'InterD'}
.bg{position:absolute;inset:0}
.rays{position:absolute;left:-600px;top:-300px;width:2400px;height:2400px;background:repeating-conic-gradient(from 0deg at 50% 50%,rgba(255,255,255,.07) 0 6deg,transparent 6deg 14deg);
  -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 10%,transparent 60%)}
.t{position:absolute;left:0;right:0;text-align:center;font-weight:900;text-transform:uppercase;line-height:.92;letter-spacing:-3px;
  -webkit-text-stroke:10px #0A1640;paint-order:stroke fill;text-shadow:0 6px 0 #0A1640,0 12px 0 #0A1640,0 18px 0 rgba(10,22,64,.85),0 30px 40px rgba(0,0,0,.45)}
.w{color:#fff}.y{color:#FFD43B}
.band{position:absolute;left:0;right:0;text-align:center}
.band b{display:inline-block;font:900 70px 'InterD';color:#fff;padding:14px 46px 20px;border-radius:22px;letter-spacing:-1px;transform:rotate(-3deg);
  border:6px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.4)}
.av{position:absolute;filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 26px rgba(120,190,255,.8)) drop-shadow(0 40px 50px rgba(0,0,0,.45))}
.logo{position:absolute;left:0;right:0;top:1590px;text-align:center}
.logo span{display:inline-block;background:#fff;border-radius:999px;padding:20px 40px;box-shadow:0 20px 50px rgba(0,0,0,.3)}
.logo img{width:290px;display:block}
.calm{position:absolute;left:0;right:0;top:1540px;bottom:0;background:linear-gradient(180deg,transparent,rgba(5,12,40,.55))}
"""


# 1 · "PERDEU 20%? PRECISA DE 25%" — tela dividida vermelho x verde, degrau caindo x seta subindo, personagem surpreso no meio
C1 = """<div class="bg" style="background:linear-gradient(115deg,#B3121C 0%,#E5303A 47%,#0F9A52 53%,#07612F 100%)"></div><div class="rays"></div>
<div class="t w" style="top:190px;font-size:140px">PERDEU 20%?</div>
<div class="t y" style="top:340px;font-size:128px">PRECISA DE 25%</div>
<div class="band" style="top:560px"><b style="background:#0A1640;border-color:#FFD43B;color:#FFD43B">A CONTA QUE NINGUÉM FAZ</b></div>
<svg style="position:absolute;left:30px;top:760px" width="360" height="620" viewBox="0 0 360 620">
 <path d="M10,60 L120,60 L120,220 L230,220 L230,400 L340,400 L340,600 L10,600 Z" fill="#fff" opacity=".95"/>
 <path d="M10,60 L120,60 L120,220 L230,220 L230,400 L340,400" fill="none" stroke="#0A1640" stroke-width="10" stroke-linejoin="round"/></svg>
<div style="position:absolute;left:60px;top:1240px;font:900 120px 'InterD';color:#E5303A;letter-spacing:-5px;-webkit-text-stroke:8px #fff;paint-order:stroke fill">−20%</div>
<svg style="position:absolute;right:30px;top:740px;filter:drop-shadow(0 26px 30px rgba(0,0,0,.35))" width="330" height="520" viewBox="0 0 330 520">
 <path d="M165,10 L320,190 L220,190 L220,510 L110,510 L110,190 L10,190 Z" fill="#fff"/><path d="M165,34 L292,176 L206,176 L206,496 L124,496 L124,176 L38,176 Z" fill="#16A34A"/></svg>
<div style="position:absolute;right:40px;top:1240px;font:900 120px 'InterD';color:#16A34A;letter-spacing:-5px;-webkit-text-stroke:8px #fff;paint-order:stroke fill">+25%</div>
<img class="av" src="file://__AV1__" style="left:330px;top:770px;width:420px">
"""

# 2 · "A VOLTA É MAIS LONGA" — azul royal -> marinho, escada descendo e ladeira subindo, personagem olhando a ladeira
C2 = """<div class="bg" style="background:radial-gradient(900px 900px at 50% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:200px;font-size:150px">A VOLTA É</div>
<div class="t y" style="top:350px;font-size:150px">MAIS LONGA</div>
<div class="band" style="top:570px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">−50% PEDE +100%</b></div>
<svg style="position:absolute;left:0;top:760px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.4))" width="1080" height="760" viewBox="0 0 1080 760">
 <path d="M40,80 L150,80 L150,230 L260,230 L260,400 L370,400 L370,620 L480,620 L480,740 L40,740 Z" fill="#F04C52"/>
 <path d="M40,80 L150,80 L150,230 L260,230 L260,400 L370,400 L370,620 L480,620" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>
 <path d="M480,620 C700,600 860,420 1050,40 L1050,740 L480,740 Z" fill="#22C26A"/>
 <path d="M480,620 C700,600 860,420 1050,40" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/></svg>
<img class="av" src="file://__AV2__" style="left:400px;top:880px;width:230px">
"""

# 3 · "−50% = +100%" — número gigante 3D, faixa inclinada, personagem apontando
C3 = """<div class="bg" style="background:radial-gradient(900px 1000px at 30% 45%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:230px;font-size:230px;letter-spacing:-10px">−50%</div>
<div class="t y" style="top:470px;font-size:230px;letter-spacing:-10px">= +100%</div>
<div class="band" style="top:770px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">A CONTA QUE NINGUÉM FAZ</b></div>
<img class="av" src="file://__AV3__" style="left:-30px;top:900px;width:520px">
<div style="position:absolute;left:520px;top:960px;width:500px;background:#fff;border-radius:40px;box-shadow:0 40px 80px rgba(0,0,0,.45);transform:rotate(3deg);padding:30px 36px 34px">
 <div style="font:700 26px 'InterD';letter-spacing:4px;color:#7A8499">PERDEU → PARA VOLTAR</div>
 <div style="display:flex;justify-content:space-between;font:900 60px 'InterD';margin-top:14px"><span style="color:#E5484D">−10%</span><span style="color:#16A34A">+11%</span></div>
 <div style="display:flex;justify-content:space-between;font:900 60px 'InterD';margin-top:6px"><span style="color:#E5484D">−20%</span><span style="color:#16A34A">+25%</span></div>
 <div style="display:flex;justify-content:space-between;font:900 60px 'InterD';margin-top:6px"><span style="color:#E5484D">−30%</span><span style="color:#16A34A">+43%</span></div>
 <div style="display:flex;justify-content:space-between;font:900 62px 'InterD';margin-top:6px;background:#FFF4C2;border-radius:18px;padding:0 12px"><span style="color:#E5484D">−50%</span><span style="color:#16A34A">+100%</span></div>
</div>
"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for i, body in enumerate([C1, C2, C3], 1):
            h = ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>" + body +
                 "<div class='calm'></div><div class='logo'><span><img src='file://__LOGO__'></span></div></body></html>")
            for k, v in {"__INTER__": INTER, "__LOGO__": LOGO, "__AV1__": AV["explicando"], "__AV2__": AV["pensativo"], "__AV3__": AV["explicando"]}.items():
                h = h.replace(k, v)
            hp = os.path.join(HERE, "capa43_%d.html" % i); open(hp, "w").write(h)
            await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(HERE, "short43-capa-%d.jpg" % i), type="jpeg", quality=92)
            os.remove(hp)
        await b.close()

asyncio.run(main())
