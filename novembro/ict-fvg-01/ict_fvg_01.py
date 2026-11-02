"""ICT sem mito #2 — FVG (TYU-56, publica qua 11/11/2026).
Gancho: "Nem todo FVG será preenchido. E agora?" — probabilidade, nunca regra.
Capa colorida (preferência do Franklin, 01/11: menos branco). Slides 2 e 3 no padrão E.
Uso: python ict_fvg_01.py [pasta_saida]   (precisa de Archivo.ttf e das poses nesta pasta)
"""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else D)
OUT.mkdir(exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONT = b64(D / "Archivo.ttf")
LOGO = b64(D.parent.parent / "assets" / "logo.png")
PENS = b64(D / "pensativo.png")
EXPL = b64(D / "explicando.png")

CSS = f"""
@font-face {{ font-family: Archivo; src: url(data:font/ttf;base64,{FONT}); font-weight: 100 900; font-stretch: 62% 125%; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:#fff; font-family: Archivo, Inter, sans-serif; color:#0B1533; position:relative; overflow:hidden; }}
.circ {{ position:absolute; border-radius:50%; }}
.logo {{ position:absolute; left:72px; top:58px; width:156px; }}
.logochip {{ position:absolute; left:56px; top:44px; background:#fff; border-radius:999px; padding:14px 22px; box-shadow:0 12px 30px rgba(0,0,0,.25); }}
.logochip img {{ width:150px; display:block; }}
.label {{ position:absolute; left:72px; top:168px; font-weight:800; letter-spacing:5px; font-size:24px; color:#2563EB; }}
.h {{ font-weight:900; font-stretch:72%; line-height:0.98; letter-spacing:-1px; }}
.pill {{ display:inline-block; padding:0 22px 8px; border-radius:22px; }}
.foot {{ position:absolute; left:72px; bottom:44px; font-size:21px; color:#94A3B8; font-family: Inter; }}
.swipe {{ position:absolute; right:72px; bottom:42px; font-size:22px; color:#2563EB; font-weight:800; font-family: Inter; }}
.card {{ background:#fff; border:2px solid #E2E8F0; border-radius:28px; box-shadow:0 18px 40px rgba(15,23,42,.08); }}
.badge {{ display:inline-block; font:800 17px Inter; letter-spacing:2px; padding:8px 14px; border-radius:10px; }}
.seal {{ font:600 18px Inter; color:#94A3B8; text-align:center; margin-top:10px; }}
"""

# ---- diagrama de velas (ilustrativo, sem ativo nem preço) ----
def candle(x, o, c, hi, lo, w=34, up=True):
    col = "#16A34A" if up else "#E5484D"
    top, bot = min(o, c), max(o, c)
    return (f'<line x1="{x}" y1="{hi}" x2="{x}" y2="{lo}" stroke="{col}" stroke-width="4" stroke-linecap="round"/>'
            f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{max(bot-top,4)}" rx="5" fill="{col}"/>')

def diagram(kind, W=420, H=360, dark=False):
    """kind: 'fvg' (só o gap), 'filled' (preço volta), 'run' (preço segue)."""
    grid = "rgba(255,255,255,.10)" if dark else "#EEF2F6"
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 420 360" xmlns="http://www.w3.org/2000/svg">']
    for y in (60, 120, 180, 240, 300):
        s.append(f'<line x1="0" y1="{y}" x2="420" y2="{y}" stroke="{grid}" stroke-width="2"/>')
    # 3 velas do FVG de alta: máxima da vela 1 (y=230) < mínima da vela 3 (y=160) => gap entre 160 e 230
    s.append('<rect x="20" y="160" width="390" height="70" rx="8" fill="rgba(255,212,59,.45)" stroke="#E0A800" stroke-width="2" stroke-dasharray="8 6"/>')
    s.append('<text x="392" y="203" text-anchor="end" font-family="Inter" font-weight="800" font-size="22" fill="#8A6A00">FVG</text>')
    s.append(candle(50, 290, 250, 230, 305))           # vela 1 (máxima em 230)
    s.append(candle(100, 260, 120, 105, 268, w=40))     # vela 2: deslocamento forte
    s.append(candle(150, 140, 100, 85, 160))            # vela 3 (mínima em 160)
    if kind == "filled":
        s.append(candle(200, 105, 150, 95, 158, up=False))
        s.append(candle(245, 150, 200, 140, 212, up=False))   # entra no gap
        s.append(candle(290, 200, 150, 140, 214))
        s.append(candle(335, 150, 95, 80, 160))
    elif kind == "run":
        s.append(candle(200, 100, 70, 58, 112))
        s.append(candle(245, 75, 50, 38, 88))
        s.append(candle(290, 55, 30, 20, 66))
        s.append(candle(335, 35, 22, 12, 46))
        s.append('<path d="M190 250 L370 250" stroke="#94A3B8" stroke-width="3" stroke-dasharray="6 8"/>')
        s.append('<text x="370" y="280" text-anchor="end" font-family="Inter" font-weight="700" font-size="19" fill="#64748B">nunca voltou</text>')
    s.append('</svg>')
    return "".join(s)

# ---------------- SLIDE 1 — capa colorida ----------------
S1 = f"""
<div style="position:absolute;inset:0;background:radial-gradient(800px 700px at 92% 6%,rgba(255,212,59,.30),transparent 60%),radial-gradient(900px 800px at 0% 100%,rgba(22,163,74,.30),transparent 60%),linear-gradient(155deg,#2563EB 0%,#1D4ED8 50%,#0B1533 100%)"></div>
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:90px 90px"></div>
<div class="logochip"><img src="data:image/png;base64,{LOGO}"></div>
<div class="label" style="color:#FFD43B;top:172px">ICT SEM MITO</div>
<div class="h" style="position:absolute;left:72px;top:214px;font-size:118px;width:900px;color:#fff">
  Nem todo FVG<br>é <span class="pill" style="background:#FFD43B;color:#0B1533;margin-top:10px">preenchido.</span>
</div>
<div class="h" style="position:absolute;left:72px;top:500px;font-size:66px;width:620px;color:#BFD3FF">
  E agora?
</div>
<div style="position:absolute;left:72px;top:600px;width:560px;font:500 30px/1.38 Inter;color:#E0E9FF">
  Se você trata o gap como <b style="color:#fff">promessa</b>, cada FVG que não volta vira frustração.
</div>
<div class="card" style="position:absolute;left:72px;top:800px;width:520px;padding:24px 40px 18px;border:none;box-shadow:0 30px 60px rgba(0,0,0,.35)">
  {diagram("run", W=440, H=330)}
  <div class="seal">Exemplo ilustrativo · sem ativo nem preço</div>
</div>
<img src="data:image/png;base64,{PENS}" style="position:absolute;right:10px;top:520px;width:430px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.40))">
<div class="foot" style="color:#BFD3FF">tradeyouup.net &nbsp;·&nbsp; 1/3</div><div class="swipe" style="color:#FFD43B">deslize →</div>
"""

# ---------------- SLIDE 2 — o que é ----------------
S2 = f"""
<div class="circ" style="width:820px;height:820px;left:-380px;top:-380px;background:#EFF5FF"></div>
<div class="circ" style="width:760px;height:760px;right:-420px;bottom:-330px;background:#FFF6D6"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">O QUE É, DE VERDADE</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:92px;width:940px">
  Um desequilíbrio.<br><span style="color:#2563EB">Não uma promessa.</span>
</div>
<div style="position:absolute;left:72px;top:420px;width:936px;font:400 30px/1.48 Inter;color:#475569">
  FVG (fair value gap) é o espaço que sobra quando o preço anda tão rápido que as sombras da 1ª e da 3ª vela não se encostam. O preço <b style="color:#0B1533">pode</b> voltar para rebalancear. Pode também seguir direto.
</div>
<div class="card" style="position:absolute;left:72px;top:660px;width:454px;padding:26px 16px 22px;text-align:center">
  <div class="badge" style="background:#DCFCE7;color:#15803D">ÀS VEZES VOLTA</div>
  <div style="margin-top:10px">{diagram("filled", W=410, H=330)}</div>
</div>
<div class="card" style="position:absolute;left:554px;top:660px;width:454px;padding:26px 16px 22px;text-align:center">
  <div class="badge" style="background:#FEE2E2;color:#C53030">ÀS VEZES NÃO</div>
  <div style="margin-top:10px">{diagram("run", W=410, H=330)}</div>
</div>
<div style="position:absolute;left:72px;top:1150px;width:936px;font:600 19px Inter;color:#94A3B8;text-align:center">Exemplo ilustrativo · sem ativo nem preço</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 2/3</div><div class="swipe">deslize →</div>
"""

def li(ok, txt):
    sym = '<span style="color:#16A34A">✓</span>' if ok else '<span style="color:#E5484D">✕</span>'
    return f'<div style="display:flex;gap:16px;margin-top:18px;font:700 28px/1.25 Inter">{sym}<div>{txt}</div></div>'

# ---------------- SLIDE 3 — na prática ----------------
S3 = f"""
<div class="circ" style="width:560px;height:560px;right:-280px;top:-340px;background:#2563EB"></div>
<div class="circ" style="width:900px;height:900px;left:-420px;top:930px;background:#EFF5FF"></div>
<img class="logo" src="data:image/png;base64,{LOGO}">
<div class="label">NA PRÁTICA</div>
<div class="h" style="position:absolute;left:72px;top:212px;font-size:78px;width:960px">
  FVG é região de interesse.<br><span style="color:#2563EB">Não é ordem pendurada.</span>
</div>
<div class="card" style="position:absolute;left:72px;top:420px;width:640px;padding:30px 36px 38px">
  {li(True,"Use junto do seu setup, como contexto")}
  {li(True,"Defina antes onde a ideia está errada")}
  {li(False,"Entrar só porque “o gap tem que fechar”")}
  {li(False,"Mover o stop esperando o preenchimento")}
</div>
<img src="data:image/png;base64,{EXPL}" style="position:absolute;right:10px;top:400px;width:300px">
<div style="position:absolute;left:72px;top:880px;width:936px;background:#0B1533;border-radius:28px;padding:34px 36px;box-shadow:0 20px 40px rgba(11,21,51,.18)">
  <div style="font:800 34px/1.25 Inter;color:#fff">Quantos dos FVGs que você marcou foram preenchidos?</div>
  <div style="font:400 28px/1.4 Inter;color:#C7D2FE;margin-top:10px">Anote no diário. O seu histórico responde melhor que qualquer regra.</div>
</div>
<div style="position:absolute;left:72px;top:1160px;width:936px;font:400 20px/1.35 Inter;color:#94A3B8">
  Conceito do ICT (há variações entre autores). Conteúdo educativo, não é recomendação de operação.
</div>
<div class="foot">tradeyouup.net &nbsp;·&nbsp; 3/3</div>
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, body in enumerate([S1, S2, S3], 1):
        pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"ict-fvg-0{i}.png"))
    b.close()
print("ok", OUT)
