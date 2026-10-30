"""TYU-48 Sábado de revisão: fechamento de outubro (carrossel 3 slides, visual caderno de investigação)."""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else D / "sab_out")
OUT.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(D / "Archivo.ttf")
LOGO = b64("/home/claude/tyu-instagram-media/assets/logo.png")
AV = b64("/home/claude/tyu-instagram-media/assets/mesa-notebook.png")

CSS = f"""
@font-face {{ font-family: Archivo; src: url(data:font/ttf;base64,{FONT}); font-weight:100 900; font-stretch:62% 125%; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; overflow:hidden; position:relative; font-family:Archivo, Inter, sans-serif; color:#0B1533;
  background:#fff repeating-linear-gradient(to bottom, transparent 0 63px, #DCE6F5 63px 65px); background-position:0 30px; }}
.margin {{ position:absolute; left:140px; top:0; bottom:0; width:3px; background:#F2A7A7; }}
.holes span {{ position:absolute; left:50px; width:34px; height:34px; border-radius:50%; background:#EEF2F7; box-shadow:inset 0 3px 6px rgba(15,23,42,.15); }}
.logo {{ position:absolute; right:64px; top:56px; width:150px; }}
.tag {{ position:absolute; left:180px; top:72px; font:800 22px Inter; letter-spacing:4px; color:#fff; background:#2563EB; padding:10px 16px; border-radius:8px; }}
.h {{ font-weight:900; font-stretch:72%; line-height:.98; letter-spacing:-1px; }}
.hand {{ font-family: 'Comic Neue', 'Segoe Print', cursive; }}
.foot {{ position:absolute; left:180px; bottom:40px; font:400 21px Inter; color:#94A3B8; background:#fff; padding:2px 6px; }}
.swipe {{ position:absolute; right:64px; bottom:38px; font:800 22px Inter; color:#2563EB; background:#fff; padding:2px 6px; }}
.note {{ position:absolute; background:#FFF7CC; box-shadow:0 14px 30px rgba(15,23,42,.12); padding:30px 32px; }}
.q {{ display:flex; gap:26px; align-items:flex-start; margin-bottom:70px; }}
.n {{ flex:none; width:74px; height:74px; border-radius:50%; border:4px solid #2563EB; color:#2563EB; font:900 40px Archivo; display:flex; align-items:center; justify-content:center; background:#fff; }}
.qt {{ font:800 44px/1.15 Inter; }}
.qs {{ font:400 30px/1.35 Inter; color:#475569; margin-top:6px; }}
.circle {{ border:5px solid #E5484D; border-radius:50%; padding:2px 14px; }}
"""
HOLES = '<div class="holes">' + "".join(f'<span style="top:{y}px"></span>' for y in (180, 470, 760, 1050)) + "</div>"

S1 = f"""<div class="margin"></div>{HOLES}
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="tag">SÁBADO DE REVISÃO</div>
<div class="h" style="position:absolute;left:180px;top:180px;font-size:118px;width:840px;background:rgba(255,255,255,.0)">
 Outubro<br>acabou.
</div>
<div class="h" style="position:absolute;left:180px;top:440px;font-size:76px;width:820px;color:#2563EB">
 Qual <span class="circle" style="color:#E5484D">erro</span> você<br>leva para novembro?
</div>
<div class="note" style="left:180px;top:720px;width:430px;transform:rotate(-2deg)">
 <div style="font:800 24px Inter;letter-spacing:2px;color:#A16207">CASO: OUTUBRO</div>
 <div style="font:500 29px/1.4 Inter;margin-top:10px">Suspeito: o mesmo erro de sempre.<br>Prova: o seu diário.<br>Tempo: 15 minutos.</div>
</div>
<img src="data:image/png;base64,{AV}" style="position:absolute;right:30px;bottom:110px;width:470px">
<div class="foot">tradeyouup.net · 1/3</div><div class="swipe">deslize →</div>"""

S2 = f"""<div class="margin"></div>{HOLES}
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="tag">A INVESTIGAÇÃO</div>
<div class="h" style="position:absolute;left:180px;top:170px;font-size:84px;width:840px">3 perguntas para<br>fechar o mês</div>
<div style="position:absolute;left:180px;top:430px;width:840px">
 <div class="q"><div class="n">1</div><div><div class="qt">Qual erro apareceu mais vezes?</div><div class="qs">Conte no diário. Não confie na memória: ela guarda o trade mais doído, não o mais frequente.</div></div></div>
 <div class="q"><div class="n">2</div><div><div class="qt">Quanto ele custou, em R?</div><div class="qs">Some o resultado dos trades com esse erro. Ex.: 9 vezes, −6R no mês.</div></div></div>
 <div class="q"><div class="n">3</div><div><div class="qt">Em que situação ele aparece?</div><div class="qs">Horário, depois de um stop, fora do setup, com a meta do dia batida…</div></div></div>
</div>
<div style="position:absolute;left:180px;top:1150px;font:600 19px Inter;color:#64748B;background:#fff;padding:4px 10px;border:1.5px solid #CBD5E1;border-radius:8px">Exemplo ilustrativo</div>
<div class="foot">tradeyouup.net · 2/3</div>"""

S3 = f"""<div class="margin"></div>{HOLES}
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="tag">O VEREDITO</div>
<div class="h" style="position:absolute;left:180px;top:170px;font-size:96px;width:840px">Escolha <span style="color:#2563EB">um</span> erro.<br>Só um.</div>
<div style="position:absolute;left:180px;top:400px;width:820px;font:400 31px/1.45 Inter;color:#334155">
 E escreva a regra que impede ele de acontecer em novembro. Uma regra que dá para cumprir sem pensar na hora.
</div>
<div class="note" style="left:180px;top:600px;width:800px;transform:rotate(-1.2deg)">
 <div style="font:800 24px Inter;letter-spacing:2px;color:#A16207">EXEMPLOS DE REGRA</div>
 <div style="font:600 32px/1.55 Inter;margin-top:12px">• Depois de 2 stops seguidos, encerro o dia.<br>• Sem o meu setup, não tem entrada.<br>• Meta batida, plataforma fechada.</div>
</div>
<div style="position:absolute;left:180px;top:1000px;width:840px;background:#0B1533;color:#fff;border-radius:24px;padding:30px 34px">
 <div style="font:800 34px Inter">Um erro corrigido por mês.</div>
 <div style="font:400 28px Inter;color:#C7D2FE;margin-top:6px">É assim que a revisão vira evolução.</div>
</div>
<div class="foot">tradeyouup.net · 3/3</div>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f"sabado-revisao-outubro-0{i}.png"))
    b.close()
print("ok", OUT)
