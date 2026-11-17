"""Ilustrações próprias (não imitam o Windows/Chrome): cartão de download e cartão de seleção do arquivo.
Geradas em 2x (para combinar com os prints ampliados)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/usr/share/fonts/opentype/inter/"
def font(w, s):
    return ImageFont.truetype(F + {"r": "Inter-Regular.otf", "m": "Inter-Medium.otf", "s": "Inter-SemiBold.otf",
                                   "b": "Inter-Bold.otf"}[w], s)

VIO = (124, 58, 237)
VIO_L = (237, 233, 254)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
LINE = (226, 232, 240)
GREEN = (22, 163, 74)


def zip_icon(d, x, y, s=1.0, col=VIO):
    w, h = int(64 * s), int(80 * s)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(10 * s), fill=(245, 243, 255), outline=col, width=max(2, int(4 * s)))
    # zíper
    for k in range(5):
        yy = y + int((12 + k * 10) * s)
        d.rectangle([x + w // 2 - int(6 * s), yy, x + w // 2, yy + int(5 * s)], fill=col)
        d.rectangle([x + w // 2, yy + int(5 * s), x + w // 2 + int(6 * s), yy + int(10 * s)], fill=col)
    d.rounded_rectangle([x + w // 2 - int(9 * s), y + int(62 * s), x + w // 2 + int(9 * s), y + int(72 * s)], radius=int(3 * s), fill=col)
    d.text((x + w / 2, y + h + int(14 * s)), "ZIP", font=font("b", int(18 * s)), fill=col, anchor="mm")


def folder_icon(d, x, y, s=1.0, col=(245, 158, 11)):
    d.rounded_rectangle([x, y + int(8 * s), x + int(40 * s), y + int(34 * s)], radius=int(5 * s), fill=col)
    d.rounded_rectangle([x, y, x + int(18 * s), y + int(14 * s)], radius=int(4 * s), fill=col)


def download_icon(d, cx, cy, s, col):
    d.line([cx, cy - 16 * s, cx, cy + 6 * s], fill=col, width=int(5 * s))
    d.line([cx - 11 * s, cy - 4 * s, cx, cy + 7 * s, cx + 11 * s, cy - 4 * s], fill=col, width=int(5 * s), joint="curve")
    d.line([cx - 16 * s, cy + 16 * s, cx + 16 * s, cy + 16 * s], fill=col, width=int(5 * s))


def card_base(w, h):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    return im, ImageDraw.Draw(im)


def download_card():
    """1600x1000: painel 'Download concluído' + caminho da pasta. Devolve (img, caixas)."""
    W, H = 1600, 1000
    im, d = card_base(W, H)
    d.rectangle([0, 0, W, 110], fill=(248, 250, 252))
    d.line([0, 110, W, 110], fill=LINE, width=3)
    download_icon(d, 80, 52, 1.6, VIO)
    d.text((130, 55), "Downloads", font=font("s", 40), fill=INK, anchor="lm")
    d.text((W - 70, 55), "Concluído", font=font("m", 32), fill=GREEN, anchor="rm")
    # linha do arquivo
    row = (70, 170, W - 70, 400)
    d.rounded_rectangle(row, radius=28, fill=(250, 250, 255), outline=(221, 214, 254), width=3)
    zip_icon(d, 120, 205, 1.75)
    d.text((290, 245), "TYUSync.zip", font=font("b", 64), fill=INK, anchor="lm")
    d.text((290, 320), "cerca de 10 KB  ·  download concluído", font=font("r", 36), fill=MUTED, anchor="lm")
    # check
    cx, cy = W - 170, 285
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(220, 252, 231))
    d.line([cx - 20, cy, cx - 5, cy + 16, cx + 22, cy - 15], fill=GREEN, width=9, joint="curve")
    # caminho
    d.text((70, 490), "Salvo em", font=font("m", 34), fill=MUTED, anchor="lm")
    path = (70, 530, W - 70, 680)
    d.rounded_rectangle(path, radius=24, fill=(248, 250, 252), outline=LINE, width=3)
    folder_icon(d, 115, 585, 1.6)
    x = 200
    for i, part in enumerate(["Este computador", "Downloads", "TYUSync.zip"]):
        fnt = font("b" if i == 2 else "m", 42)
        d.text((x, 607), part, font=fnt, fill=INK if i == 2 else (51, 65, 85), anchor="lm")
        x += d.textlength(part, font=fnt)
        if i < 2:
            d.text((x + 28, 607), "›", font=font("m", 46), fill=MUTED, anchor="mm")
            x += 58
    # selo (aparece depois, desenhado pelo renderizador como sobreposição)
    boxes = {"row": row, "path": path, "badge_anchor": (W // 2, 840)}
    return im, boxes


def pick_card():
    """1600x1000: janela genérica 'Escolher arquivo' com a pasta Downloads aberta."""
    W, H = 1600, 1000
    im, d = card_base(W, H)
    d.rectangle([0, 0, W, 100], fill=(30, 41, 59))
    d.text((60, 50), "Escolha o arquivo para importar", font=font("s", 38), fill=(255, 255, 255), anchor="lm")
    # barra lateral
    d.rectangle([0, 100, 400, H], fill=(248, 250, 252))
    d.line([400, 100, 400, H], fill=LINE, width=3)
    items = ["Área de trabalho", "Documentos", "Downloads", "Imagens"]
    for i, it in enumerate(items):
        y = 170 + i * 90
        if it == "Downloads":
            d.rounded_rectangle([24, y - 36, 376, y + 36], radius=18, fill=VIO_L)
        folder_icon(d, 50, y - 17, 1.0, (245, 158, 11) if it == "Downloads" else (148, 163, 184))
        d.text((110, y), it, font=font("s" if it == "Downloads" else "m", 34), fill=INK, anchor="lm")
    # caminho
    d.text((450, 160), "Downloads", font=font("b", 44), fill=INK, anchor="lm")
    d.line([450, 215, W - 50, 215], fill=LINE, width=3)
    # arquivo
    row = (440, 245, W - 50, 395)
    d.rounded_rectangle(row, radius=22, fill=(245, 243, 255), outline=(196, 181, 253), width=3)
    zip_icon(d, 480, 268, 1.05)
    d.text((600, 300), "TYUSync.zip", font=font("b", 48), fill=INK, anchor="lm")
    d.text((600, 352), "Pasta compactada  ·  10 KB", font=font("r", 32), fill=MUTED, anchor="lm")
    # outros arquivos (genéricos, apagados)
    for i in range(2):
        y = 450 + i * 110
        d.rounded_rectangle([480, y, 540, y + 70], radius=10, fill=(241, 245, 249))
        d.rounded_rectangle([600, y + 16, 600 + 380 - i * 90, y + 40], radius=10, fill=(241, 245, 249))
    # botões
    abrir = (W - 330, H - 150, W - 60, H - 60)
    cancelar = (W - 620, H - 150, W - 360, H - 60)
    d.rounded_rectangle(cancelar, radius=20, fill=(241, 245, 249), outline=LINE, width=3)
    d.text(((cancelar[0] + cancelar[2]) / 2, (cancelar[1] + cancelar[3]) / 2), "Cancelar", font=font("s", 36), fill=(51, 65, 85), anchor="mm")
    d.rounded_rectangle(abrir, radius=20, fill=VIO)
    d.text(((abrir[0] + abrir[2]) / 2, (abrir[1] + abrir[3]) / 2), "Abrir", font=font("b", 38), fill=(255, 255, 255), anchor="mm")
    return im, {"row": row, "abrir": abrir}


if __name__ == "__main__":
    a, _ = download_card(); a.save("/tmp/claude-0/-home-claude/6989be45-5e2d-582c-8cbc-9d4d373d165a/scratchpad/v2/card_dl.png")
    b, _ = pick_card(); b.save("/tmp/claude-0/-home-claude/6989be45-5e2d-582c-8cbc-9d4d373d165a/scratchpad/v2/card_pick.png")
