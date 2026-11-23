# Capas do Short VID-44 (3 opções, 1080x1920) no padrão "capa ousada" (04/11/2026): fundo saturado, título 3D branco + amarelo,
# faixa inclinada, personagem oficial com luz de recorte, logo no selo branco, faixa de baixo calma. Base: reels/stop40/capa40.py.
# Uso: python3 capa44.py  -> short43-capa-1.jpg, -2.jpg, -3.jpg
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



# 1 · "NO LUCRO E REPROVADO?" — tela dividida verde x vermelho, +1.000 à esquerda, carimbo ENCERRADA à direita, personagem no meio
C1 = """<div class="bg" style="background:linear-gradient(115deg,#07612F 0%,#0F9A52 47%,#E5303A 53%,#B3121C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:190px;font-size:150px">NO LUCRO E</div>
<div class="t y" style="top:345px;font-size:150px">REPROVADO?</div>
<div class="band" style="top:575px"><b style="background:#0A1640;border-color:#FFD43B;color:#FFD43B">CONTA DE MESA</b></div>
<div style="position:absolute;left:40px;top:720px;font:900 130px 'InterD';color:#16A34A;letter-spacing:-6px;-webkit-text-stroke:10px #fff;paint-order:stroke fill;transform:rotate(-4deg);filter:drop-shadow(0 24px 30px rgba(0,0,0,.35))">+1.000</div>
<div style="position:absolute;right:30px;top:745px;font:900 72px 'InterD';color:#fff;background:#E5303A;border:8px solid #fff;padding:6px 26px 12px;border-radius:22px;transform:rotate(6deg);box-shadow:0 24px 50px rgba(0,0,0,.4);letter-spacing:-2px">ENCERRADA</div>
<img class="av" src="file://__AV1__" style="left:200px;top:930px;width:640px">
"""

# 2 · "O LIMITE SOBE. NÃO DESCE." — azul royal -> marinho, linha tracejada amarela em escada atrás do personagem, que olha para cima
C2 = """<div class="bg" style="background:radial-gradient(900px 900px at 50% 40%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:190px;font-size:150px">O LIMITE SOBE.</div>
<div class="t y" style="top:345px;font-size:170px">NÃO DESCE.</div>
<div class="band" style="top:590px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">E ENCERRA A CONTA</b></div>
<svg style="position:absolute;left:0;top:740px;filter:drop-shadow(0 20px 30px rgba(0,0,0,.4))" width="1080" height="800" viewBox="0 0 1080 800">
 <path d="M40,760 L40,640 L240,640 L240,500 L440,500 L440,360 L640,360 L640,220 L840,220 L840,80 L1050,80" fill="none" stroke="#FFD43B" stroke-width="16" stroke-dasharray="40 24" stroke-linecap="round" stroke-linejoin="round"/>
 <path d="M1050,80 l-60,-34 l0,68 z" fill="#FFD43B"/></svg>
<div style="position:absolute;right:50px;top:740px;font:900 44px 'InterD';color:#0A1640;background:#FFD43B;padding:6px 20px 10px;border-radius:14px;transform:rotate(-3deg)">LIMITE</div>
<img class="av" src="file://__AV2__" style="left:120px;top:860px;width:330px">
"""

# 3 · "A LINHA QUE TE PERSEGUE" — gráfico do saldo com a linha do limite colada embaixo, personagem apontando
C3 = """<div class="bg" style="background:radial-gradient(900px 1000px at 30% 45%,#2F6BFF,#0B3BC4 45%,#071A5C 100%)"></div><div class="rays"></div>
<div class="t w" style="top:180px;font-size:160px">A LINHA QUE</div>
<div class="t y" style="top:345px;font-size:160px">TE PERSEGUE</div>
<div class="band" style="top:580px"><b style="background:linear-gradient(180deg,#F04C52,#C8262D)">CONTA DE MESA</b></div>
<div style="position:absolute;left:330px;top:770px;width:700px;height:640px;background:#fff;border-radius:44px;box-shadow:0 40px 80px rgba(0,0,0,.45);transform:rotate(3deg);overflow:hidden">
 <div style="position:absolute;left:36px;top:30px;font:700 26px 'InterD';letter-spacing:4px;color:#7A8499">SALDO × LIMITE</div>
 <svg style="position:absolute;left:0;top:80px" width="700" height="560" viewBox="0 0 700 560">
  <path d="M30,470 L110,420 L160,445 L240,350 L290,375 L380,270 L430,295 L520,170 L570,200 L640,120" fill="none" stroke="#2563EB" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M30,540 L110,540 L110,490 L240,490 L240,420 L380,420 L380,340 L520,340 L520,240 L640,240" fill="none" stroke="#E5484D" stroke-width="10" stroke-dasharray="26 16" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="640" cy="120" r="16" fill="#2563EB" stroke="#fff" stroke-width="5"/></svg>
</div>
<img class="av" src="file://__AV3__" style="left:-20px;top:860px;width:460px">
"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for i, body in enumerate([C1, C2, C3], 1):
            h = ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS + "</style></head><body>" + body +
                 "<div class='calm'></div><div class='logo'><span><img src='file://__LOGO__'></span></div></body></html>")
            for k, v in {"__INTER__": INTER, "__LOGO__": LOGO, "__AV1__": AV["cansado"], "__AV2__": AV["pensativo"], "__AV3__": AV["explicando"]}.items():
                h = h.replace(k, v)
            hp = os.path.join(HERE, "capa44_%d.html" % i); open(hp, "w").write(h)
            await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(HERE, "short44-capa-%d.jpg" % i), type="jpeg", quality=92)
            os.remove(hp)
        await b.close()

asyncio.run(main())
