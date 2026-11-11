# Compõe as capas 4-6 do TYU-59 (fundos/títulos gerados no ChatGPT, conversa nova de 11/11/2026, em capas-chatgpt/)
# com o personagem oficial (assets/) e o logo no selo branco. Uso: python3 compor_chatgpt.py -> cp-capa-opcao-4..6.jpg
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
LOGO = Image.open(os.path.join(HERE, "tpl", "logo.png")).convert("RGBA")
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 26)
POSES = {1: "celular-contrariado.png", 2: "cansado.png", 3: "celular-contrariado.png"}
for i in (1, 2, 3):
    bg = Image.open(os.path.join(HERE, "capas-chatgpt", f"cp-chatgpt-opcao-{i}.png")).convert("RGBA").resize((1080, 1920), Image.LANCZOS)
    av = Image.open(os.path.join(ROOT, "assets", POSES[i])).convert("RGBA")
    w = 600 if i != 2 else 560; av = av.resize((w, int(av.height * w / av.width)), Image.LANCZOS)
    if av.height > 820: av = av.crop((0, 0, av.width, 820))
    # brilho de recorte
    a = av.split()[3]; glow = Image.new("RGBA", av.size, (140, 200, 255, 0)); glow.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda p: min(255, int(p * 1.3))))
    x, y = -40, 1520 - av.height
    bg.alpha_composite(glow, (x, y)); bg.alpha_composite(av, (x, y))
    # faixa de baixo calma + selo + logo
    calm = Image.new("RGBA", (1080, 380), (0, 0, 0, 0)); dc = ImageDraw.Draw(calm)
    for k in range(380): dc.line([(0, k), (1080, k)], fill=(5, 12, 40, int(230 * min(1, k / 140))))
    bg.alpha_composite(calm, (0, 1540))
    d = ImageDraw.Draw(bg); t = "Exemplo ilustrativo · conta demo"; tw = d.textlength(t, font=F)
    d.text(((1080 - tw) / 2, 1585), t, font=F, fill=(255, 255, 255, 210))
    lw = 290; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    pw, ph = lw + 80, lg.height + 40; px, py = (1080 - pw) // 2, 1650
    d.rounded_rectangle([px, py, px + pw, py + ph], ph // 2, fill="white"); bg.alpha_composite(lg, (px + 40, py + 20))
    bg.convert("RGB").save(os.path.join(HERE, f"cp-capa-opcao-{i + 3}.jpg"), quality=92)
