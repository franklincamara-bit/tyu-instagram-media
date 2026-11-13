"""VID-27 v2 — Como conectar o NinjaTrader 8.
Câmera que segue o destaque, cursor animado com clique, holofote, legendas por frase, trilha de progresso.
Uso: python3 render.py [cena ...]   (sem argumentos: tudo + montagem final)
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cards

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.join(HERE, "up")
AUD = os.path.join(HERE, "audio")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
LOGO = os.path.join(HERE, "logo.png")

W, H, FPS = 1920, 1080, 30
SS = 2                       # palco interno em 2x
VIO = (124, 58, 237)
VIO_D = (91, 33, 182)
AMBER = (245, 158, 11)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
FI = "/usr/share/fonts/opentype/inter/"
def font(w, s):
    return ImageFont.truetype(FI + {"r": "Inter-Regular.otf", "m": "Inter-Medium.otf", "s": "Inter-SemiBold.otf",
                                    "b": "Inter-Bold.otf", "d": "InterDisplay-SemiBold.otf"}[w], s)
F_CAP = font("d", 44)
F_TITLE = font("b", 34)
F_WHERE = font("b", 22)
F_CALL = font("s", 30)
F_CALL_B = font("b", 32)
F_MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26) if os.path.exists(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf") else font("m", 26)

def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

# ---------------------------------------------------------------- quadros-fonte
def blur_boxes(im, boxes, k=2, radius=9):
    """Borra caixas dadas em coordenadas do print original (800 px) — a imagem está em k×."""
    for b in boxes:
        bb = tuple(int(v * k) for v in b)
        bb = (max(0, bb[0]), max(0, bb[1]), min(im.width, bb[2]), min(im.height, bb[3]))
        if bb[2] <= bb[0] or bb[3] <= bb[1]:
            continue
        reg = im.crop(bb)
        small = reg.resize((max(1, reg.width // 6), max(1, reg.height // 6)), Image.BILINEAR)
        reg = small.resize(reg.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(radius))
        im.paste(reg, bb[:2])
    return im

def up(name):
    f = os.path.join(UP, name + ".png")
    if os.path.exists(f):
        return Image.open(f).convert("RGB")
    import glob
    src = glob.glob(os.path.join(HERE, "src", name + ".*"))[0]
    print("  (prévia sem EDSR:", name, ")", flush=True)
    im = Image.open(src).convert("RGB")
    return im.resize((im.width * 2, im.height * 2), Image.LANCZOS)

def S(b, k=2):
    return tuple(v * k for v in b)

# linhas da lista de vínculo (prints 800x494): y do topo do ID, x final do ID
ROWS = [(212, 308), (258, 256), (304, 256), (349, 297), (395, 286), (441, 308), (487, 308)]
ID_BOXES = [(204, y - 2, e + 2, y + 14) for y, e in ROWS]
NICK_BOXES = [(578, y + 2, 700, y + 18) for y, _ in ROWS]

class Lazy(dict):
    def __init__(self, f): super().__init__(); self.f = f
    def __missing__(self, k):
        v = self.f[k](); v.setdefault("k", 2); v.setdefault("off", (0, 0)); self[k] = v; return v

def shots():
    def br(name, crop=None, blur=None, off=(0, 0)):
        def f():
            im = up(name)
            if blur: im = blur_boxes(im, blur)
            if crop: im = im.crop(crop)
            return dict(img=im, dark=False, chrome="browser", off=off)
        return f
    def nt(name):
        return lambda: dict(img=up(name), dark=True, chrome="nt8")
    def card(fn):
        def f():
            im, ex = fn(); return dict(img=im, dark=False, chrome="card", extra=ex, k=1)
        return f
    vc = (190, 112, 742, 478)
    tb = [(165, 128, 264, 143)] + [(636, y - 9, 692, y + 9) for y in (180, 252, 325, 396, 467)] + \
         [(219, 164, 258, 180), (219, 237, 255, 253), (219, 310, 258, 326), (219, 381, 258, 397), (219, 452, 268, 468)]
    tc = (150, 98, 780, 494)
    return Lazy({
        "menu": br("3p1qzn", (0, 0, 1600, 1040)),
        "hero0": br("xg367g", (0, 0, 1600, 1040)),
        "tok0": br("e0nvc0", (0, 0, 1580, 1020)),
        "tok1": br("2yjis0", (0, 0, 1580, 1040), [(68, 170, 612, 202), (242, 304, 288, 324)]),
        "dl0": br("zrjz8u", (0, 0, 1580, 1040)),
        "dlcard": card(cards.download_card),
        "imp": nt("nt8-importar"),
        "pick": card(cards.pick_card),
        "novo": nt("nt8-novo"),
        "sync": nt("nt8-tyu-sync"),
        "hero1": br("4og5hq"),
        "vinc": br("3ewwc8", S(vc), ID_BOXES + NICK_BOXES, vc[:2]),
        "lista": br("159tb0", S(vc), ID_BOXES + NICK_BOXES[1:] + [(578, 214, 700, 230), (578, 254, 700, 430)], vc[:2]),
        "trades": br("1preqg", S(tc), tb, tc[:2]),
    })

# ---------------------------------------------------------------- palco
STAGE_TOP, STAGE_BOT = 132, 1080 - 70     # área útil (topo: título; base: trilha)
def bg():
    g = np.zeros((H * SS, W * SS, 3), np.float32)
    y = np.linspace(0, 1, H * SS)[:, None]
    x = np.linspace(0, 1, W * SS)[None, :]
    top = np.array([244, 245, 250], np.float32); bot = np.array([229, 233, 242], np.float32)
    g[:] = (top * (1 - y[..., None]) + bot * y[..., None])
    # brilho violeta suave no canto superior direito
    d = np.sqrt((x - 0.92) ** 2 + (y * 0.56 - 0.0) ** 2)
    glow = np.clip(1 - d / 0.55, 0, 1) ** 2
    g = g * (1 - 0.16 * glow[..., None]) + np.array([167, 139, 250], np.float32) * 0.16 * glow[..., None]
    return Image.fromarray(g.clip(0, 255).astype(np.uint8))
BG = None

def build_stage(sh):
    """Compõe o quadro numa janela (navegador / NinjaTrader / cartão) no palco 2x.
    Devolve (palco, função que mapeia coords do print original -> palco)."""
    img = sh["img"]; k = sh["k"]
    chrome = sh["chrome"]
    bar = {"browser": 64, "nt8": 0, "card": 0}[chrome] * SS // 2 * 2
    aw, ah = 1700 * SS, (STAGE_BOT - STAGE_TOP - 40) * SS
    s = min(aw / img.width, (ah - bar) / img.height)
    s = min(s, 2.3)
    iw, ih = int(img.width * s), int(img.height * s)
    ww, wh = iw, ih + bar
    x0 = (W * SS - ww) // 2
    y0 = STAGE_TOP * SS + ((STAGE_BOT - STAGE_TOP) * SS - wh) // 2
    st = BG.copy()
    # sombra
    pad = 80
    shd = Image.new("L", (ww + 2 * pad, wh + 2 * pad), 0)
    ImageDraw.Draw(shd).rounded_rectangle([pad, pad + 24, pad + ww, pad + wh + 24], radius=36, fill=95)
    shd = shd.filter(ImageFilter.GaussianBlur(38))
    st.paste(Image.new("RGB", shd.size, (30, 27, 75)), (x0 - pad, y0 - pad), shd)
    win = Image.new("RGB", (ww, wh), (255, 255, 255))
    wd = ImageDraw.Draw(win)
    if chrome == "browser":
        wd.rectangle([0, 0, ww, bar], fill=(248, 249, 252))
        wd.line([0, bar - 1, ww, bar - 1], fill=(226, 232, 240), width=2)
        for i, c in enumerate([(248, 113, 113), (251, 191, 36), (74, 222, 128)]):
            cx = 40 + i * 36
            wd.ellipse([cx - 11, bar // 2 - 11, cx + 11, bar // 2 + 11], fill=c)
        ux0, ux1 = 170, min(ww - 170, 170 + 900)
        wd.rounded_rectangle([ux0, bar // 2 - 22, ux1, bar // 2 + 22], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        wd.text((ux0 + 26, bar // 2), "tradeyouup.net", font=font("m", 26), fill=(71, 85, 105), anchor="lm")
    win.paste(img.resize((iw, ih), Image.LANCZOS), (0, bar))
    mask = Image.new("L", (ww, wh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, ww - 1, wh - 1], radius=26, fill=255)
    st.paste(win, (x0, y0), mask)
    ox, oy = sh["off"]
    def m(px, py):
        return (x0 + (px - ox) * k * s, y0 + bar + (py - oy) * k * s)
    full = (x0, y0, x0 + ww, y0 + wh)
    return st, m, full

# ---------------------------------------------------------------- câmera
def cam_for(box_stage, full, zmax, tight=False):
    """Retângulo de câmera (palco 2x, 16:9) que enquadra a caixa com folga e a mantém acima da legenda."""
    fw, fh = W * SS, H * SS
    if box_stage is None:
        return (0, 0, fw, fh)
    x0, y0, x1, y1 = box_stage
    if tight:
        bw, bh = (x1 - x0) * 1.12 + 120, (y1 - y0) * 1.3 + 120
    else:
        bw, bh = (x1 - x0) * 1.9 + 160, (y1 - y0) * 2.1 + 160
    cw = min(max(bw, bh * 16 / 9, fw / zmax), fw)
    for _ in range(12):
        ch = cw * 9 / 16
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + ch * 0.06
        cx = min(max(cx, cw / 2), fw - cw / 2)
        cy = min(max(cy, ch / 2), fh - ch / 2)
        top = cy - ch / 2
        # base da caixa em fração da altura da tela; legenda ocupa ~ os 20% de baixo
        if (y1 - top) / ch <= 0.78 or cw <= fw / 3.2 or (y1 - y0) > 0.5 * ch:
            break
        cw *= 0.9
    return (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)

def lerp_rect(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(4))

# ---------------------------------------------------------------- desenho em tela
CURSOR = None
def make_cursor():
    s = 3
    pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24)]
    im = Image.new("RGBA", (40 * s, 48 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = [(4 * s + x * s, 4 * s + y * s) for x, y in pts]
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 3 * s, y + 4 * s) for x, y in P], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(3 * s))
    im = Image.alpha_composite(im, sh)
    d = ImageDraw.Draw(im)
    d.polygon(P, fill=(17, 17, 17))
    inner = [(4 * s + x * s, 4 * s + y * s) for x, y in [(2.2, 5), (2.2, 29.5), (9.4, 23), (15.6, 36.6), (18.6, 35.2), (12.6, 22), (22, 22)]]
    d.polygon(inner, fill=(255, 255, 255))
    return im.resize((40, 48), Image.LANCZOS)

def rr_mask_hole(size, box, r):
    m = Image.new("L", size, 255)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=r, fill=0)
    return m

def wrap_caption(text, maxw):
    words, lines, cur = text.split(), [], ""
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=F_CAP) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    if len(lines) == 2 and len(lines[1]) < 12:          # evita viúva
        ws = text.split(); h = len(ws) // 2
        lines = [" ".join(ws[:h + 1]), " ".join(ws[h + 1:])]
    return lines

def draw_callout(frame, anchor, lines, a, side="right", accent=VIO):
    """Balão com seta apontando para 'anchor' (coords de tela). lines: [(texto, fonte, cor)]"""
    if a <= 0:
        return frame
    d0 = ImageDraw.Draw(frame)
    pw = max(d0.textlength(t, font=f) for t, f, c in lines) + 56
    lh = [f.getmetrics()[0] + f.getmetrics()[1] + 10 for t, f, c in lines]
    ph = sum(lh) + 36
    ax, ay = anchor
    if side == "right":
        bx, by = ax + 34, ay - ph / 2
    elif side == "left":
        bx, by = ax - 34 - pw, ay - ph / 2
    elif side == "below":
        bx, by = ax - pw / 2, ay + 30
    else:
        bx, by = ax - pw / 2, ay - 30 - ph
    bx = min(max(bx, 30), W - 30 - pw)
    by = min(max(by, STAGE_TOP + 10), H - 230 - ph)
    off = (1 - ease_out(a)) * 14
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    al = int(255 * min(1, a * 1.4))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([bx, by + off + 8, bx + pw, by + off + ph + 8], radius=22, fill=(30, 27, 75, int(70 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    ov = Image.alpha_composite(ov, sh); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([bx, by + off, bx + pw, by + off + ph], radius=22, fill=(255, 255, 255, al), outline=accent + (al,), width=3)
    od.rounded_rectangle([bx, by + off, bx + 10, by + off + ph], radius=5, fill=accent + (al,))
    y = by + off + 18
    for (t, f, c), h_ in zip(lines, lh):
        od.text((bx + 34, y), t, font=f, fill=c + (al,))
        y += h_
    return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

# ---------------------------------------------------------------- cena
def adur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

def render_scene(n, sc, SH, total_scenes, t_offset, t_total):
    audio = os.path.join(AUD, sc["audio"])
    lead, tail = 0.45, 0.75
    dur = lead + adur(audio) + tail
    nfr = int(round(dur * FPS))
    beats = sc["beats"]
    starts = [lead + b["t"] for b in beats]
    stages = {}
    def stage(key):
        if key not in stages:
            stages[key] = build_stage(SH[key])
        return stages[key]
    # pré-calcula câmeras e posições do cursor (em coords do palco)
    plan = []
    for i, b in enumerate(beats):
        st, m, full = stage(b["shot"])
        k = b.get("hl") or []
        hl = [(*m(x0, y0), *m(x1, y1)) for x0, y0, x1, y1 in k]
        focus = b.get("focus")
        if focus == "full" or (not hl and focus is None):
            fbox = None
        elif focus:
            fbox = (*m(focus[0], focus[1]), *m(focus[2], focus[3]))
        else:
            fbox = (min(h[0] for h in hl), min(h[1] for h in hl), max(h[2] for h in hl), max(h[3] for h in hl))
        zmax = b.get("zmax", 1.9 if not SH[b["shot"]]["dark"] else 1.55)
        cam = cam_for(fbox, full, zmax, tight=bool(focus) and focus != "full")
        click = b.get("click")
        cpos = m(*click) if click else None
        plan.append(dict(st=st, m=m, hl=hl, cam=cam, click=cpos, b=b, start=starts[i],
                         end=starts[i + 1] if i + 1 < len(beats) else dur))
    caps = []
    for p in plan:
        if caps and caps[-1][2] == p["b"]["cap"]:
            caps[-1] = (caps[-1][0], p["end"], caps[-1][2])
        else:
            caps.append((p["start"], p["end"], p["b"]["cap"]))
    tmp = os.path.join(OUT, f"c{n}.mp4")
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", "-i", audio, "-filter_complex",
                             f"[1:a]adelay={int(lead*1000)}|{int(lead*1000)},apad=whole_dur={dur},aresample=48000[a]",
                             "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
                             "-preset", "medium", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-t", f"{dur}", tmp],
                            stdin=subprocess.PIPE)
    cursor_prev = None
    for fi in range(nfr):
        t = fi / FPS
        bi = max(i for i, p in enumerate(plan) if p["start"] <= t or i == 0)
        p = plan[bi]
        prev = plan[bi - 1] if bi > 0 else None
        lt = t - p["start"] if bi > 0 or t >= p["start"] else 0
        same_shot = prev is not None and prev["b"]["shot"] == p["b"]["shot"]
        # câmera
        if prev is not None and same_shot:
            cam = lerp_rect(prev["cam"], p["cam"], ease(lt / 0.9))
        else:
            # entra no quadro: começa um pouco mais aberto e aproxima
            wide = lerp_rect(p["cam"], (0, 0, W * SS, H * SS), 0.35)
            cam = lerp_rect(wide, p["cam"], ease(lt / 1.2))
        # leve deriva contínua (respiração)
        drift = 1 + 0.012 * ease((t - p["start"]) / max(0.5, p["end"] - p["start"]))
        cx, cy = (cam[0] + cam[2]) / 2, (cam[1] + cam[3]) / 2
        cw, ch = (cam[2] - cam[0]) / drift, (cam[3] - cam[1]) / drift
        cam = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        def render_cam(stg, cm):
            return stg.resize((W, H), Image.BICUBIC, box=tuple(cm), reducing_gap=2.0)
        frame = render_cam(p["st"], cam)
        # transição entre quadros diferentes
        if prev is not None and not same_shot and lt < 0.45:
            pc = prev["cam"]
            old = render_cam(prev["st"], lerp_rect(pc, (pc[0] + (pc[2]-pc[0])*0.03, pc[1] + (pc[3]-pc[1])*0.03,
                                                         pc[2] - (pc[2]-pc[0])*0.03, pc[3] - (pc[3]-pc[1])*0.03), ease(lt / 0.45)))
            frame = Image.blend(old, frame, ease(lt / 0.45))
        scale = W / (cam[2] - cam[0])
        def to_screen(pt):
            return ((pt[0] - cam[0]) * scale, (pt[1] - cam[1]) * scale)
        # holofote + destaque
        ha = ease((lt - 0.25) / 0.45) if p["hl"] else 0
        if ha > 0 and not p["b"].get("no_spot"):
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            hole = Image.new("L", (W, H), int(72 * ha))
            hd = ImageDraw.Draw(hole)
            for h_ in p["hl"]:
                a_ = to_screen(h_[:2]); b_ = to_screen(h_[2:])
                hd.rounded_rectangle([a_[0] - 12, a_[1] - 12, b_[0] + 12, b_[1] + 12], radius=18, fill=0)
            hole = hole.filter(ImageFilter.GaussianBlur(3))
            frame.paste(Image.new("RGB", (W, H), (15, 12, 40)), (0, 0), hole)
        if ha > 0:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            col = AMBER if SH[p["b"]["shot"]]["dark"] else VIO
            for h_ in p["hl"]:
                a_ = to_screen(h_[:2]); b_ = to_screen(h_[2:])
                g = 6 * (1 - ha)
                od.rounded_rectangle([a_[0] - 12 - g, a_[1] - 12 - g, b_[0] + 12 + g, b_[1] + 12 + g], radius=18,
                                     outline=col + (int(90 * ha),), width=12)
                od.rounded_rectangle([a_[0] - 12 - g, a_[1] - 12 - g, b_[0] + 12 + g, b_[1] + 12 + g], radius=18,
                                     outline=col + (int(255 * ha),), width=5)
            frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
        # sobreposições específicas
        for fx in p["b"].get("fx", []):
            frame = fx(frame, lt, to_screen, p["m"])
        # cursor
        if p["click"] is not None:
            target = p["click"]
            if cursor_prev is None:
                cursor_prev = (target[0] + 260, target[1] + 220)
            mv = ease((lt - 0.15) / 0.85)
            # arco suave
            sx, sy = cursor_prev
            mx, my = (sx + target[0]) / 2, min(sy, target[1]) - 60
            u = mv
            pos = ((1 - u) ** 2 * sx + 2 * (1 - u) * u * mx + u * u * target[0],
                   (1 - u) ** 2 * sy + 2 * (1 - u) * u * my + u * u * target[1])
            sp = to_screen(pos)
            tc = lt - 1.05
            press = 0.86 if 0 <= tc < 0.14 else 1.0
            if 0 <= tc < 0.7:
                r = 14 + 60 * ease_out(tc / 0.7)
                al = int(170 * (1 - tc / 0.7))
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(ov).ellipse([sp[0] - r, sp[1] - r, sp[0] + r, sp[1] + r], outline=VIO + (al,), width=6)
                ImageDraw.Draw(ov).ellipse([sp[0] - r * 0.45, sp[1] - r * 0.45, sp[0] + r * 0.45, sp[1] + r * 0.45], fill=VIO + (al // 3,))
                frame = Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
            cur = CURSOR if press == 1.0 else CURSOR.resize((int(40 * press), int(48 * press)), Image.LANCZOS)
            frame.paste(cur, (int(sp[0]) - 2, int(sp[1]) - 2), cur)
            if fi + 1 < nfr:
                nxt = plan[bi + 1] if bi + 1 < len(plan) else None
                if nxt is not None and (fi + 1) / FPS >= nxt["start"]:
                    cursor_prev = pos if nxt["b"]["shot"] == p["b"]["shot"] else None
        else:
            if bi + 1 < len(plan) and (fi + 1) / FPS >= plan[bi + 1]["start"]:
                cursor_prev = None
        frame = chrome_ui(frame, sc, p["b"], n, total_scenes, t, caps, (t_offset + t) / t_total)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close(); proc.wait()
    return tmp, dur

TOPFADE = None
SELO = "Exemplo ilustrativo · conta demo"
def chrome_ui(frame, sc, b, n, total, t, caps, prog):
    global TOPFADE
    if TOPFADE is None:
        a = np.zeros((H, W, 4), np.uint8)
        a[..., :3] = (240, 242, 248)
        ys = np.arange(150)
        a[:150, :, 3] = (np.clip(1 - ys / 150, 0, 1) ** 1.6 * 235)[:, None].astype(np.uint8)
        TOPFADE = Image.fromarray(a, "RGBA")
    frame = Image.alpha_composite(frame.convert("RGBA"), TOPFADE).convert("RGB")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    # faixa superior
    where = b.get("where", sc["where"])
    nt = where.startswith("Ninja")
    x = 60
    wtxt = where.upper()
    ww = od.textlength(wtxt, font=F_WHERE) + 40
    tw = od.textlength(sc["title"], font=F_TITLE)
    od.rounded_rectangle([x - 12, 32, x + ww + 20 + tw + 28, 98], radius=33, fill=(255, 255, 255, 236))
    dw = total * 30 + 26
    od.rounded_rectangle([W - 60 - (total - 1) * 30 - 26, 40, W - 34, 90], radius=25, fill=(255, 255, 255, 236))
    od.rounded_rectangle([x, 44, x + ww, 86], radius=21, fill=(30, 41, 59, 255) if nt else VIO + (255,))
    od.text((x + 20, 65), wtxt, font=F_WHERE, fill=(255, 255, 255, 255), anchor="lm")
    x += ww + 20
    od.text((x, 65), sc["title"], font=F_TITLE, fill=INK + (255,), anchor="lm")
    # pontos de progresso (direita)
    for i in range(total):
        cx = W - 60 - (total - 1 - i) * 30
        if i + 1 < n:
            od.ellipse([cx - 7, 58, cx + 7, 72], fill=VIO + (255,))
        elif i + 1 == n:
            od.rounded_rectangle([cx - 7, 58, cx + 7, 72], radius=7, fill=VIO + (255,))
            od.ellipse([cx - 12, 53, cx + 12, 77], outline=VIO + (120,), width=3)
        else:
            od.ellipse([cx - 6, 59, cx + 6, 71], fill=(203, 213, 225, 255))
    if SELO:
        od.text((W - 40, 118), SELO, font=font("m", 22), fill=MUTED + (235,), anchor="ra")
    # trilha de progresso na base
    od.rectangle([0, H - 8, W, H], fill=(226, 232, 240, 255))
    od.rectangle([0, H - 8, int(W * prog), H], fill=VIO + (255,))
    frame = Image.alpha_composite(frame.convert("RGBA"), ov)
    # legenda
    for c0, c1, txt in caps:
        if c0 - 0.05 <= t < c1:
            a = min(1, ease((t - c0 + 0.05) / 0.25), ease((c1 - t) / 0.2) if c1 - t < 0.2 else 1)
            lines = wrap_caption(txt, 1500)
            lh = 60
            widths = [ImageDraw.Draw(frame).textlength(l, font=F_CAP) for l in lines]
            bw = max(widths) + 80
            bh = lh * len(lines) + 40
            bx0 = (W - bw) / 2
            by0 = H - 46 - bh + (1 - a) * 10
            cov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            cd = ImageDraw.Draw(cov)
            cd.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=26, fill=(15, 23, 42, int(222 * a)))
            for k_, l in enumerate(lines):
                cd.text(((W - widths[k_]) / 2, by0 + 20 + k_ * lh), l, font=F_CAP, fill=(255, 255, 255, int(255 * a)))
            frame = Image.alpha_composite(frame, cov)
            break
    return frame.convert("RGB")

# ---------------------------------------------------------------- efeitos
def fx_typed_token(box, start=0.6, dur=0.9):
    """Digita uma máscara do token dentro do campo (coords do print)."""
    def f(frame, lt, ts, m):
        if lt < start:
            return frame
        n = int(min(1, (lt - start) / dur) * 30)
        a_ = ts(m(box[0], box[1])); b_ = ts(m(box[2], box[3]))
        d = ImageDraw.Draw(frame)
        fs = max(16, int((b_[1] - a_[1]) * 0.5))
        fnt = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Medium.otf", fs)
        txt = ("tyu_nt8_" + "•" * 22)[:n]
        d.text((a_[0] + 14, (a_[1] + b_[1]) / 2), txt, font=fnt, fill=(235, 235, 235), anchor="lm")
        return frame
    return f

def fx_callout(anchor_pt, lines, side="right", start=0.5, accent=VIO):
    def f(frame, lt, ts, m):
        a = ease((lt - start) / 0.4)
        return draw_callout(frame, ts(m(*anchor_pt)), lines, a, side, accent)
    return f

def fx_badge(center, text, start=0.4, col=(22, 163, 74), bgc=(220, 252, 231)):
    def f(frame, lt, ts, m):
        a = ease_out((lt - start) / 0.45)
        if a <= 0:
            return frame
        c = ts(m(*center))
        fnt = font("b", 40)
        d0 = ImageDraw.Draw(frame)
        tw = d0.textlength(text, font=fnt)
        w_, h_ = tw + 140, 92
        sc_ = 0.85 + 0.15 * a
        w_, h_ = w_ * sc_, h_ * sc_
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        al = int(255 * a)
        od.rounded_rectangle([c[0] - w_ / 2, c[1] - h_ / 2, c[0] + w_ / 2, c[1] + h_ / 2], radius=h_ / 2, fill=bgc + (al,), outline=col + (al,), width=3)
        ix = c[0] - w_ / 2 + 50 * sc_
        od.line([ix - 14, c[1], ix - 3, c[1] + 11, ix + 16, c[1] - 11], fill=col + (al,), width=7, joint="curve")
        od.text((ix + 36 * sc_, c[1]), text, font=font("b", int(40 * sc_)), fill=(21, 128, 61, al), anchor="lm")
        return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
    return f

def fx_lower_chip(label, value, start=0.2, accent=AMBER):
    """Faixa destacada acima da legenda (ex.: endereço do servidor)."""
    def f(frame, lt, ts, m):
        a = ease_out((lt - start) / 0.45)
        if a <= 0:
            return frame
        fl, fv = font("s", 34), font("b", 44)
        d0 = ImageDraw.Draw(frame)
        w1, w2 = d0.textlength(label, font=fl), d0.textlength(value, font=fv)
        bw, bh = w1 + w2 + 130, 100
        bx, by = (W - bw) / 2, 128 + (1 - a) * 16
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([bx, by + 10, bx + bw, by + bh + 10], radius=50, fill=(0, 0, 0, int(80 * a)))
        ov = Image.alpha_composite(ov, sh.filter(ImageFilter.GaussianBlur(16)))
        od = ImageDraw.Draw(ov)
        al = int(255 * a)
        od.rounded_rectangle([bx, by, bx + bw, by + bh], radius=50, fill=(255, 255, 255, al), outline=accent + (al,), width=4)
        od.text((bx + 50, by + bh / 2), label, font=fl, fill=MUTED + (al,), anchor="lm")
        od.text((bx + 80 + w1, by + bh / 2), value, font=fv, fill=INK + (al,), anchor="lm")
        return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")
    return f

# ---------------------------------------------------------------- roteiro
def scenes():
    dl_extra = cards.download_card()[1]
    pk_extra = cards.pick_card()[1]
    url_lines = [("Se estiver vazio, digite:", F_CALL, MUTED), ("https://tradeyouup.net/functions/", F_CALL_B, INK)]
    return [
        dict(where="Plataforma", title="Abra a integração", audio="s1.mp3", beats=[
            dict(t=0.0, shot="menu", focus=(0, 0, 220, 520), zmax=1.3, cap="Vamos conectar o NinjaTrader 8 à plataforma."),
            dict(t=3.15, shot="menu", hl=[(22, 57, 190, 84)], click=(120, 70), cap="No menu lateral, abra Configurações."),
            dict(t=5.95, shot="menu", hl=[(31, 377, 170, 423)], click=(100, 400), cap="Depois, clique em Integração NinjaTrader 8."),
            dict(t=9.65, shot="hero0", hl=[(548, 92, 748, 183)], cap="Repare no status: por enquanto, Não conectado."),
        ]),
        dict(where="Plataforma", title="Passo 1 · Gere o token", audio="s2.mp3", beats=[
            dict(t=0.0, shot="tok0", hl=[(57, 156, 251, 211)], click=(150, 184), cap="No passo um, clique em Gerar token."),
            dict(t=3.1, shot="tok1", hl=[(62, 166, 616, 204)], cap="O token aparece uma única vez."),
            dict(t=5.4, shot="tok1", hl=[(625, 168, 729, 203)], click=(680, 186), focus=(50, 110, 760, 270),
                 cap="Clique em Copiar e guarde até colar no NinjaTrader."),
        ]),
        dict(where="Plataforma", title="Passo 2 · Baixe o add-on", audio="s3.mp3", beats=[
            dict(t=0.0, shot="dl0", hl=[(391, 259, 704, 307)], click=(560, 284), focus=(40, 90, 750, 420),
                 cap="No passo dois, comece baixando o add-on: clique no botão Baixar."),
            dict(t=4.7, shot="dlcard", hl=[dl_extra["row"], dl_extra["path"]], focus="full",
                 cap="Salve o arquivo no seu computador, por exemplo na pasta Downloads."),
            dict(t=8.86, shot="dlcard", focus="full", fx=[fx_badge(dl_extra["badge_anchor"], "Não precisa descompactar")],
                 cap="Não precisa descompactar. O NinjaTrader importa o zip direto."),
        ]),
        dict(where="NinjaTrader 8", title="Importe o add-on", audio="s4.mp3", beats=[
            dict(t=0.0, shot="imp", hl=[(242, 5, 361, 27)], click=(300, 16), cap="Agora, no NinjaTrader, abra o menu Ferramentas."),
            dict(t=3.6, shot="imp", hl=[(7, 230, 268, 250)], click=(120, 240), focus=(0, 0, 500, 372),
                 cap="Na lista, passe o mouse em Importar."),
            dict(t=6.35, shot="imp", hl=[(271, 286, 494, 306)], click=(380, 296), focus=(0, 0, 500, 372),
                 cap="E clique em Complemento de NinjaScript."),
            dict(t=9.15, shot="pick", hl=[pk_extra["row"]], click=((pk_extra["abrir"][0] + pk_extra["abrir"][2]) / 2,
                                                               (pk_extra["abrir"][1] + pk_extra["abrir"][3]) / 2),
                 focus="full", where="Windows", cap="Escolha o arquivo zip que você salvou e clique em Abrir."),
        ]),
        dict(where="NinjaTrader 8", title="Abra o add-on", audio="s5.wav", beats=[
            dict(t=0.0, shot="novo", hl=[(156, 5, 226, 27)], click=(190, 16), cap="Em seguida, abra o menu Novo."),
            dict(t=2.65, shot="novo", hl=[(7, 556, 218, 579)], click=(80, 567), focus=(0, 470, 235, 610),
                 cap="No fim da lista, clique em TYU Sync."),
        ]),
        dict(where="NinjaTrader 8", title="Cole o token e salve", audio="s6.mp3", beats=[
            dict(t=0.0, shot="sync", hl=[(22, 187, 442, 209)], click=(200, 198), fx=[fx_typed_token((22, 187, 442, 209), 1.3)],
                 cap="Cole o token no campo Token de sincronização."),
            dict(t=3.25, shot="sync", hl=[(22, 233, 442, 255)], fx=[fx_typed_token((22, 187, 442, 209), -5)],
                 focus=(0, 150, 475, 323), cap="O campo Servidor já vem preenchido."),
            dict(t=5.7, shot="sync", hl=[(22, 233, 442, 255)], fx=[fx_typed_token((22, 187, 442, 209), -5),
                 fx_lower_chip("Se estiver vazio, digite:", "https://tradeyouup.net/functions/")],
                 focus=(0, 150, 475, 323), cap="Se estiver vazio, digite este endereço."),
            dict(t=8.7, shot="sync", hl=[(22, 293, 121, 322)], click=(70, 307), fx=[fx_typed_token((22, 187, 442, 209), -5)],
                 focus=(0, 150, 475, 323), cap="Clique em Salvar."),
            dict(t=10.15, shot="hero1", hl=[(548, 52, 748, 142)], where="Plataforma", focus=(250, 20, 800, 175), zmax=2.4,
                 cap="Em poucos segundos, o status na plataforma muda para Conectado."),
        ]),
        dict(where="Plataforma", title="Passo 3 · Vincule as contas", audio="s7.mp3", beats=[
            dict(t=0.0, shot="vinc", hl=[(198, 202, 732, 470)], focus=(190, 112, 742, 478), no_spot=True,
                 cap="No passo três, cada conta do NinjaTrader aparece nesta lista."),
            dict(t=4.4, shot="lista", hl=[(574, 234, 726, 442)], click=(650, 222), focus=(190, 112, 742, 478),
                 cap="Para cada uma, escolha em qual conta da plataforma os trades vão entrar."),
            dict(t=8.95, shot="lista", hl=[(574, 234, 726, 442)], focus=(190, 112, 742, 478),
                 fx=[fx_callout((574, 420), [("No fim da lista:", F_CALL, MUTED), ("+ Criar nova conta", F_CALL_B, VIO)],
                                side="left", start=0.3)],
                 cap="Se a conta ainda não existe, use Criar nova conta, no fim da lista."),
        ]),
        dict(where="Plataforma", title="Visualizar Trades · Pronto", audio="s8.mp3", beats=[
            dict(t=0.0, shot="trades", hl=[(259, 310, 330, 327), (288, 381, 330, 398)], focus=(150, 290, 780, 420),
                 cap="Pronto. Quando você zera a posição, o trade entra sozinho, marcado A revisar."),
            dict(t=5.9, shot="trades", focus="full", cap="Agora é só fazer o seu debrief."),
        ]),
    ]

def main(only):
    global BG, CURSOR
    BG = bg(); CURSOR = make_cursor()
    SH = shots()
    SC = scenes()
    durs = [0.45 + adur(os.path.join(AUD, s["audio"])) + 0.75 for s in SC]
    t_total = sum(durs)
    offs = [sum(durs[:i]) for i in range(len(SC))]
    for i in only:
        f, d = render_scene(i, SC[i - 1], SH, len(SC), offs[i - 1], t_total)
        print("cena", i, round(d, 2), flush=True)
    return SC

NEXT_TITLE = ""
def end_card(path, audio_en, secs=4.2):
    c = Image.new("RGB", (W, H), (255, 255, 255))
    logo = Image.open(LOGO).convert("RGBA")
    lw = 640
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    nfr = int(secs * FPS)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", "-i", audio_en, "-filter_complex",
                             f"[1:a]adelay=500|500,apad=whole_dur={secs},aresample=48000[a]",
                             "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
                             "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-t", f"{secs}", path], stdin=subprocess.PIPE)
    f1, f2 = font("m", 36), font("b", 46)
    for i in range(nfr):
        t = i / FPS
        fr = c.copy()
        a = ease_out(t / 0.8)
        s = 0.94 + 0.06 * a
        lg = logo.resize((int(logo.width * s), int(logo.height * s)), Image.LANCZOS)
        al = lg.split()[3].point(lambda v: int(v * a))
        lg.putalpha(al)
        fr.paste(lg, ((W - lg.width) // 2, 250 + int((1 - a) * 20)), lg)
        b = ease((t - 0.9) / 0.6)
        if b > 0:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            t1 = "Próximo vídeo"; t2 = NEXT_TITLE
            od.text((W / 2, 690), t1, font=f1, fill=MUTED + (int(255 * b),), anchor="mm")
            od.text((W / 2, 752), t2, font=f2, fill=INK + (int(255 * b),), anchor="mm")
            fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if args and args[0] == "end":
        BG = bg()
        end_card(os.path.join(OUT, "end.mp4"), os.path.join(AUD, "en_end.wav"))
        sys.exit()
    only = [int(a) for a in args] or list(range(1, 9))
    SC = main(only)
    if not args:
        end_card(os.path.join(OUT, "end.mp4"), os.path.join(AUD, "en_end.wav"))
        lst = os.path.join(OUT, "list.txt")
        with open(lst, "w") as fh:
            for i in range(1, 9):
                fh.write(f"file 'c{i}.mp4'\n")
            fh.write("file 'end.mp4'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                        os.path.join(OUT, "VID-27-v2.mp4")], check=True)
        print("ok")

